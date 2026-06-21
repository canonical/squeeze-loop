#!/usr/bin/env python3
"""C diversity test: sample contract conformance checks randomly and observe a real,
varying blend-detection rate.

The "implementer" is one FIXED weak server: it handles the basic clauses correctly
(ping, auth, echo, read-after-write) but BLENDS the planes on subtler ones (leaks
the internal id, returns a raw traceback, allows an illegal state transition,
ignores idempotency, ignores pagination limits). A check is CAUGHT when a
conformance case fails against the weak server. The pool is 100 checks across 10
families (5 it passes, 5 it blends); sampling randomly per cycle makes the caught
count vary -- an actual trial, not a recomputation.

Seeded per cycle (base + cycle): cycles differ, the experiment reproduces.
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOKEN = "test_secure_token_abc123"
TOTAL = 50
SAMPLE, CYCLES, BASE_SEED = 20, int(__import__("os").environ.get("DIV_CYCLES","10")), int(__import__("os").environ.get("DIV_SEED", "6000"))


def req(method, path, headers=None, body=None):
    return {"method": method, "path": path, "headers": headers or {}, "body": body}


# --- the fixed weak server (correct on basics, blends on subtle clauses) -----
def weak(s, q):
    p, h, b = q["path"], q["headers"], q["body"]
    if p == "/ping":
        return 200, {"status": "ok"}
    if p == "/echo":
        return 200, {"status": "ok", "val": b}
    if p == "/profile/update":
        if h.get("X-API-Key") != TOKEN:
            return 401, {"error": "unauthorized"}
        if b == "MALFORMED":
            return 500, {"error": "Traceback (most recent call last): main.py line 42"}  # BLEND
        s["name"] = b
        return 200, {"status": "ok"}
    if p == "/profile":
        return 200, {"id": 42, "user_uuid": "u-1", "display_name": s.get("name", "Alice")}  # BLEND: id leak
    if p == "/order/create":
        s["n"] = s.get("n", 0) + 1
        s["status"] = "draft"
        return 201, {"uuid": f"ord-{s['n']}"}                # BLEND: ignores Idempotency-Key
    if p == "/order/approve":
        return 200, {"status": "approved"}                   # BLEND: allows illegal transition
    if p == "/order/cancel":
        s["status"] = "cancelled"
        return 200, {"status": "cancelled"}
    if p == "/list":
        return 200, {"items_returned": TOTAL}                # BLEND: ignores limit
    return 404, {"error": "not_found"}


def _body(r, i=-1):
    return r[i][1]


# --- 100 checks: 10 families x 10 parametrised instances ---------------------
def build_pool():
    pool = []

    def add(family, steps, ok):
        pool.append({"family": family, "steps": steps, "ok": ok})

    for i in range(10):
        add("ping", [req("GET", "/ping")], lambda r: r[-1][0] == 200 and "status" in _body(r))
        add("echo", [req("POST", "/echo", body=i)], (lambda i: lambda r: _body(r).get("val") == i)(i))
        add("auth_required", [req("POST", "/profile/update", {}, {"display_name": f"x{i}"})],
            lambda r: r[-1][0] == 401)
        add("auth_ok", [req("POST", "/profile/update", {"X-API-Key": TOKEN}, f"N{i}")],
            lambda r: r[-1][0] == 200)
        add("read_after_write",
            [req("POST", "/profile/update", {"X-API-Key": TOKEN}, f"N{i}"), req("GET", "/profile", {"X-API-Key": TOKEN})],
            (lambda i: lambda r: _body(r).get("display_name") == f"N{i}")(i))
        # --- blended families (the weak server fails these) ---
        add("no_id_leak", [req("GET", "/profile", {"X-API-Key": TOKEN})],
            lambda r: "id" not in _body(r))
        add("clean_error", [req("POST", "/profile/update", {"X-API-Key": TOKEN}, "MALFORMED")],
            lambda r: r[-1][0] == 400 and "traceback" not in str(_body(r)).lower())
        add("state_machine", [req("POST", "/order/create"), req("POST", "/order/cancel"), req("POST", "/order/approve")],
            lambda r: r[-1][0] == 409)
        add("idempotency", [req("POST", "/order/create", {"Idempotency-Key": "K"}), req("POST", "/order/create", {"Idempotency-Key": "K"})],
            lambda r: _body(r, 0).get("uuid") == _body(r, 1).get("uuid"))
        add("pagination", [req("GET", "/list", body={"limit": i + 1})],
            (lambda k: lambda r: _body(r).get("items_returned") == k)(i + 1))
    return pool


def run_case(case):
    s, resps = {}, []
    for q in case["steps"]:
        resps.append(weak(s, q))
    try:
        return bool(case["ok"](resps))
    except Exception:
        return False


def main():
    pool = build_pool()
    print(f"=== C diversity: {CYCLES} cycles, sample {SAMPLE}/{len(pool)} conformance "
          f"checks per cycle (one fixed weak server) ===")
    per_cycle = []
    for i in range(CYCLES):
        seed = BASE_SEED + i
        sample = random.Random(seed).sample(pool, SAMPLE)
        caught = sum(1 for c in sample if not run_case(c))   # weak server fails -> blend caught
        rate = round(100 * caught / SAMPLE)
        per_cycle.append({"cycle": i + 1, "seed": seed, "blends_caught": caught, "caught_pct": rate})
        print(f"  cycle {i+1:2d} (seed {seed}): blends caught {caught}/{SAMPLE} ({rate}%)")

    base = sum(1 for c in pool if not run_case(c))
    cs = [c["blends_caught"] for c in per_cycle]
    distinct = len(set(cs))
    print(f"\nblends caught/cycle: min {min(cs)} max {max(cs)} mean {round(sum(cs)/len(cs),1)}; "
          f"distinct outcomes across cycles: {distinct}/{CYCLES}")
    print(f"whole-pool baseline: {base}/100 checks the weak server fails (blended)")

    out = {"instance": "C-diversity", "pool": len(pool), "sample": SAMPLE, "cycles": CYCLES,
           "base_seed": BASE_SEED, "pool_blended": base, "caught_per_cycle": cs,
           "distinct_outcomes": distinct, "per_cycle": per_cycle}
    (HERE / "diversity_results.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(f"results -> {HERE / 'diversity_results.json'}")


if __name__ == "__main__":
    main()
