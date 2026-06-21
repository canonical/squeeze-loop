#!/usr/bin/env python3
"""Skill-accumulation loop for Use Case C (docs/skill-accumulation-design.md).

The deciding agent (the server) starts blending every subtle clause. Each time the
independent exerciser's conformance check catches a blend, it records the catch;
after consolidating (learning rate K) it writes a skill ("honor this clause") and
stops blending that plane. So the skill ENRICHES over the blended clause families
and the caught-blend rate FALLS across cycles.

Rule 1: only the deciding agent learns; the conformance suite (the answer key)
stays fixed. Reset: start from scratch. Deterministic. Programmatic learner, not a
live LLM (the honest gap).
"""
import json
import os
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0] / "diversity"))
import run_diversity as DV          # build_pool, req, TOKEN, TOTAL, _body

TOKEN, TOTAL = DV.TOKEN, DV.TOTAL
CYCLES = int(os.environ.get("DIV_CYCLES", "100"))
SAMPLE = int(os.environ.get("DIV_SAMPLE", "5"))
SEED = int(os.environ.get("DIV_SEED", "6000"))
CONSOLIDATE_K = int(os.environ.get("DIV_K", "3"))

BLEND_FAMILIES = ("no_id_leak", "clean_error", "state_machine", "idempotency", "pagination")


def server(skill, s, q):
    """Correct on basics; honors a subtle clause only once its family is learned."""
    p, h, b = q["path"], q["headers"], q["body"]
    if p == "/ping":
        return 200, {"status": "ok"}
    if p == "/echo":
        return 200, {"status": "ok", "val": b}
    if p == "/profile/update":
        if h.get("X-API-Key") != TOKEN:
            return 401, {"error": "unauthorized"}
        if b == "MALFORMED":
            if "clean_error" in skill:
                return 400, {"error": "bad_request", "message": "invalid body"}
            return 500, {"error": "Traceback (most recent call last): main.py line 42"}
        s["name"] = b
        return 200, {"status": "ok"}
    if p == "/profile":
        body = {"user_uuid": "u-1", "display_name": s.get("name", "Alice")}
        if "no_id_leak" not in skill:
            body["id"] = 42
        return 200, body
    if p == "/order/create":
        if "idempotency" in skill:
            idem = s.setdefault("idem", {}); k = h.get("Idempotency-Key")
            if k in idem:
                return 200, {"uuid": idem[k]}
            u = f"ord-{len(idem) + 1}"; idem[k] = u; return 201, {"uuid": u}
        s["n"] = s.get("n", 0) + 1
        return 201, {"uuid": f"ord-{s['n']}"}
    if p == "/order/approve":
        if "state_machine" in skill and s.get("status") == "cancelled":
            return 409, {"error": "illegal_transition"}
        s["status"] = "approved"; return 200, {"status": "approved"}
    if p == "/order/cancel":
        s["status"] = "cancelled"; return 200, {"status": "cancelled"}
    if p == "/list":
        if "pagination" in skill:
            return 200, {"items_returned": (b or {}).get("limit")}
        return 200, {"items_returned": TOTAL}
    return 404, {"error": "not_found"}


def passes(skill, case):
    s, resps = {}, []
    for q in case["steps"]:
        resps.append(server(skill, s, q))
    try:
        return bool(case["ok"](resps))
    except Exception:
        return False


def run(cycles=CYCLES, sample=SAMPLE, seed=SEED, k=CONSOLIDATE_K):
    pool = DV.build_pool()
    rng = random.Random(seed)
    skill, catches = {}, {}
    per_cycle, learned = [], []
    for i in range(1, cycles + 1):
        caught = 0
        for case in (rng.choice(pool) for _ in range(sample)):
            if not passes(skill, case):                 # exerciser catches a blend
                caught += 1
                fam = case["family"]
                catches[fam] = catches.get(fam, 0) + 1
                if fam not in skill and catches[fam] >= k:
                    skill[fam] = {"lesson": f"honor the '{fam}' clause; stop blending the planes",
                                  "learned_cycle": i}
                    learned.append({"cycle": i, "family": fam})
        per_cycle.append({"cycle": i, "blends_caught": caught,
                          "caught_pct": round(100 * caught / sample),
                          "skill_size": len(skill)})
    return per_cycle, skill, learned


def main():
    per, skill, learned = run()
    w = max(1, len(per) // 10)
    early = round(sum(c["blends_caught"] for c in per[:w]) / w, 2)
    late = round(sum(c["blends_caught"] for c in per[-w:]) / w, 2)
    print(f"=== C skill loop: {len(per)} cycles from scratch "
          f"(sample {SAMPLE}, K={CONSOLIDATE_K}, seed {SEED}) ===")
    for c in per:
        if c["cycle"] <= 6 or c["cycle"] % 10 == 0 or c in per[-2:]:
            print(f"  cycle {c['cycle']:>3}: blends caught {c['blends_caught']:>2}/{SAMPLE}  skill_size {c['skill_size']}")
    print(f"\nskill enriched 0 -> {len(skill)} ({', '.join(sorted(skill))}); learned at "
          f"{[e['cycle'] for e in learned]}; blends caught first {w} {early} -> last {w} {late}")
    out = {"instance": "C-skill", "cycles": len(per), "sample": SAMPLE, "seed": SEED,
           "consolidate_k": CONSOLIDATE_K, "final_skill_size": len(skill),
           "skills": sorted(skill), "learned_events": learned,
           "blends_first_window_mean": early, "blends_last_window_mean": late,
           "per_cycle": per}
    (HERE / "skill_enrichment_results.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    (HERE / "skill_store.json").write_text(json.dumps(skill, indent=2, sort_keys=True) + "\n")
    print(f"results -> {HERE / 'skill_enrichment_results.json'}")


if __name__ == "__main__":
    main()
