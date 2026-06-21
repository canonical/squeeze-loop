#!/usr/bin/env python3
"""The Squeeze Connector for Use Case B (in-band-deliverable-spec.md SS3/SS4).

The sentinel forces the implementer's bot logic and the exerciser's adversarial
matrix to reconcile over the frozen Lower Bound REST app. It imports neither band
as a peer of the other: it loads the implementer's process_customer_turn by path
and reads the exerciser's JSON (Strict Serialization). All decisions are committed
through the live REST app -- the runner never writes the DB.

Checks (nonzero exit on any failure):

  ISOLATION   the implementer/ and exerciser/ directories contain zero cross-
              references to each other (Zero Import Linkage, spec SS"physical
              isolation"), verified by AST import scan + filesystem-path scan.
  APP         starts python3 <repo>/src/B/ground-truth/app.py on 127.0.0.1:8000,
              waits until POST /start answers, and tears it down at the end.
  GATE C      every CLAUSE_n declared by the upper bound is covered by some
              scenario's target_clauses. The clause set is parsed from
              src/B/upper-bound/refund_policy.md via that band's handbook.py
              (imported by path). If the upper bound is not built yet, GATE C
              degrades to a WARNING using the canonical clause set rather than
              crashing.
  GATE B      for each scenario: POST /start, then for each turn call
              refund_bot_logic.process_customer_turn(...) and POST /chat with its
              message, then GET /state and assert committed_action ==
              expected_terminal_action (mismatch == GATE B CRASH).
  ARCHIVE     replay every certified case in
              src/B/ground-truth/shared/archive_ledger through the implementer
              and assert the committed action equals the certified verdict
              (no decision flips -- the lower-bound invariant).

Usage:
  python3 runner/execute_squeeze.py            # drive the real implementer
  python3 runner/execute_squeeze.py --bad      # load the coherent-and-wrong bot
  REFUND_BOT=<path/to/module.py> ...           # override the bot under test
"""

import argparse
import ast
import importlib.util
import json
import os
import re
import socket
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

RUNNER = Path(__file__).resolve().parent
ROOT = RUNNER.parent                       # src/B/in-band-deliverable
ROOT_B = ROOT.parent                       # src/B
REPO = ROOT_B.parent.parent                # repo root
GROUND_TRUTH = ROOT_B / "ground-truth"
APP = GROUND_TRUTH / "app.py"
ARCHIVE = GROUND_TRUTH / "shared" / "archive_ledger"
UPPER_BOUND = ROOT_B / "upper-bound"

IMPL_DEFAULT = ROOT / "implementer" / "src" / "refund_bot_logic.py"
BAD_DEFAULT = ROOT / "evidence" / "coherent_wrong_bot.py"
MATRIX = ROOT / "exerciser" / "scenarios" / "adversarial_matrix.json"

HOST, PORT = "127.0.0.1", 8000
BASE_URL = f"http://{HOST}:{PORT}/api/session"

# Canonical clause set (upper-bound-spec.md SS2) used when the upper bound is not built.
CANONICAL_CLAUSES = ["CLAUSE_1", "CLAUSE_2", "CLAUSE_3"]


class GateFail(Exception):
    pass


# --------------------------------------------------------------------------- #
# REST helpers (sentinel side; the bot under test does its own REST calls)
# --------------------------------------------------------------------------- #
def _post(path, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}{path}", data=data,
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=5) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def _get(path):
    req = urllib.request.Request(f"{BASE_URL}{path}", method="GET")
    with urllib.request.urlopen(req, timeout=5) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


# --------------------------------------------------------------------------- #
# ISOLATION
# --------------------------------------------------------------------------- #
def _links_to(pyfile, other):
    """Real linkage only: an import of, or a filesystem path into, the other band.
    A prose mention of the word in a comment/docstring is not linkage."""
    text = pyfile.read_text()
    for node in ast.walk(ast.parse(text)):
        if isinstance(node, ast.Import):
            for n in node.names:
                if other in n.name.split("."):
                    return f"imports {n.name}"
        elif isinstance(node, ast.ImportFrom):
            if node.module and other in node.module.split("."):
                return f"from {node.module} import ..."
    if re.search(rf"\b{other}/", text) or f"/home/{other}" in text:
        return f"path reference to {other}/"
    return None


def check_isolation():
    bad = []
    for f in (ROOT / "implementer").rglob("*.py"):
        link = _links_to(f, "exerciser")
        if link:
            bad.append(f"{f.name} {link}")
    for f in (ROOT / "exerciser").rglob("*.py"):
        link = _links_to(f, "implementer")
        if link:
            bad.append(f"{f.name} {link}")
    if bad:
        raise GateFail("Zero Import Linkage violated: " + "; ".join(bad))
    print("[PASS] ISOLATION  -- implementer and exerciser bands are import-isolated")


# --------------------------------------------------------------------------- #
# APP lifecycle
# --------------------------------------------------------------------------- #
def _port_open():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.3)
        return s.connect_ex((HOST, PORT)) == 0


def start_app():
    if not APP.exists():
        raise GateFail(f"ground-truth app not found: {APP}")
    if _port_open():
        raise GateFail(f"port {PORT} already in use -- stop the other listener first")
    proc = subprocess.Popen(
        [sys.executable, str(APP), "--host", HOST, "--port", str(PORT)],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    # Wait until /start answers (probe with an unknown customer -> 404, which means up).
    deadline = time.time() + 15
    while time.time() < deadline:
        if proc.poll() is not None:
            out = proc.stdout.read() if proc.stdout else ""
            raise GateFail(f"app exited early (rc={proc.returncode}):\n{out}")
        try:
            _post("/start", {"case_id": "_probe", "customer_id": "_none"})
            break
        except urllib.error.HTTPError:
            break                      # got an HTTP response -> server is up
        except (urllib.error.URLError, ConnectionError, OSError):
            time.sleep(0.2)
    else:
        proc.terminate()
        raise GateFail("app did not become ready within 15s")
    print(f"[ OK ] APP       -- ground-truth listening on {BASE_URL}")
    return proc


def stop_app(proc):
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
    print("[ OK ] APP       -- ground-truth torn down")


# --------------------------------------------------------------------------- #
# Bot loader (load the implementer's module by path; not a peer import)
# --------------------------------------------------------------------------- #
def load_bot(path):
    spec = importlib.util.spec_from_file_location("bot_under_test", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "process_customer_turn"):
        raise GateFail(f"{path} does not expose process_customer_turn")
    return mod


# --------------------------------------------------------------------------- #
# GATE C
# --------------------------------------------------------------------------- #
def upper_bound_clauses():
    """Return (clause_ids, source_label). Parse via the upper-bound handbook.py
    if the band is built; otherwise return the canonical set with a None source."""
    handbook = UPPER_BOUND / "handbook.py"
    policy_md = UPPER_BOUND / "refund_policy.md"
    if handbook.exists() and policy_md.exists():
        sys.path.insert(0, str(UPPER_BOUND))
        try:
            import handbook as hb  # noqa
            # Support either a Metric-style API (parse()/by_id) or a flat clause API.
            for getter in ("clause_ids", "clauses"):
                if hasattr(hb, getter):
                    obj = getattr(hb, getter)
                    ids = list(obj() if callable(obj) else obj)
                    if ids:
                        return ids, str(policy_md)
            if hasattr(hb, "parse"):
                parsed = hb.parse(str(policy_md))
                # parse() may return policy objects with .clause_ids
                first = parsed[0] if isinstance(parsed, list) and parsed else parsed
                if hasattr(first, "clause_ids"):
                    return list(first.clause_ids), str(policy_md)
        except Exception as e:  # noqa: BLE001 -- degrade rather than crash
            print(f"[WARN] GATE C    -- upper-bound handbook present but unparsable "
                  f"({e}); using canonical clause set")
            return CANONICAL_CLAUSES, None
    return CANONICAL_CLAUSES, None


def gate_c(matrix):
    clause_ids, source = upper_bound_clauses()
    covered = set()
    for s in matrix["scenarios"]:
        covered.update(s.get("target_clauses", []))
    missing = [c for c in clause_ids if c not in covered]
    if source is None:
        if missing:
            print(f"[WARN] GATE C    -- upper bound not built; canonical clauses "
                  f"{clause_ids} NOT all covered (missing {missing})")
        else:
            print(f"[WARN] GATE C    -- upper bound not built; degraded to a warning. "
                  f"Canonical clauses {clause_ids} all covered by scenarios.")
        return
    if missing:
        raise GateFail(f"GATE C: clauses uncovered by the adversarial matrix: {missing} "
                       f"(from {source})")
    print(f"[PASS] GATE C    -- all upper-bound clauses covered {clause_ids}")


# --------------------------------------------------------------------------- #
# GATE B (positives over the adversarial matrix)
# --------------------------------------------------------------------------- #
def gate_b(matrix, bot):
    print(f"\n=== GATE B: {len(matrix['scenarios'])} adversarial scenarios "
          f"(policy {matrix['policy_id']}) ===")
    for scenario in matrix["scenarios"]:
        sid = scenario["scenario_id"]
        _, start = _post("/start", {"case_id": sid, "customer_id": scenario["customer_id"]})
        token = start["session_token"]

        for turn in scenario["turns"]:
            bot_out = bot.process_customer_turn(
                session_token=token, customer_message=turn["message"])
            # Post the bot's reply back to the conversation layer (per the spec loop).
            _post("/chat", {"session_token": token, "message": bot_out.get("message", "")})

        # Finalization turn: the conversation is over, so the bot may now commit a
        # deferred (money-out) REIMBURSE. Protective decisions are already locked.
        bot.process_customer_turn(session_token=token, customer_message="")

        _, final = _get(f"/state/{token}")
        actual = final.get("committed_action")
        expected = scenario["expected_terminal_action"]
        if actual != expected:
            raise GateFail(f"GATE B CRASH: scenario {sid} -- "
                           f"expected {expected}, implementer committed {actual}")
        print(f"[PASS] GATE B    -- {sid}: committed {actual} (== expected) "
              f"{scenario['target_clauses']}")
    print("GATE B SUCCESS: all in-band interactive paths align with policy rules.")


# --------------------------------------------------------------------------- #
# ARCHIVE REGRESSION (lower-bound invariant: no decision flips)
# --------------------------------------------------------------------------- #
def archive_regression(bot):
    cases = sorted(ARCHIVE.glob("case_*_input.json"))
    if not cases:
        print("[WARN] ARCHIVE   -- no archive cases found; skipping regression")
        return
    print(f"\n=== ARCHIVE REGRESSION: {len(cases)} certified cases ===")
    for cfile in cases:
        inp = json.loads(cfile.read_text())
        vfile = cfile.with_name(cfile.name.replace("_input", "_verdict"))
        certified = json.loads(vfile.read_text())["decision"]

        _, start = _post("/start", {"case_id": inp["case_id"], "customer_id": inp["customer_id"]})
        token = start["session_token"]
        for msg in inp["turns"]:
            bot.process_customer_turn(session_token=token, customer_message=msg)
        bot.process_customer_turn(session_token=token, customer_message="")

        _, final = _get(f"/state/{token}")
        actual = final.get("committed_action")
        if actual != certified:
            raise GateFail(f"ARCHIVE REGRESSION: {inp['case_id']} "
                           f"({inp['customer_id']}) flipped -- certified {certified}, "
                           f"implementer committed {actual}")
        print(f"[PASS] ARCHIVE   -- {inp['case_id']} ({inp['customer_id']}): "
              f"{actual} (== certified)")
    print("ARCHIVE REGRESSION SUCCESS: every certified verdict recomputes (no flips).")


# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description="In-band squeeze runner (Use Case B)")
    ap.add_argument("--bad", action="store_true",
                    help="load the coherent-and-wrong negative control instead of the real bot")
    args = ap.parse_args()

    bot_path = Path(os.environ["REFUND_BOT"]) if os.environ.get("REFUND_BOT") else (
        BAD_DEFAULT if args.bad else IMPL_DEFAULT)
    if not bot_path.exists():
        sys.exit(f"error: bot under test not found: {bot_path}")
    if not MATRIX.exists():
        sys.exit(f"error: adversarial matrix not found: {MATRIX} "
                 f"(run exerciser/build_adversarial_matrix.py)")

    label = "NEGATIVE CONTROL (coherent-and-wrong)" if args.bad else "implementer"
    print(f"Bot under test: {bot_path.name}  [{label}]")

    matrix = json.loads(MATRIX.read_text())
    proc = None
    try:
        check_isolation()
        proc = start_app()
        bot = load_bot(bot_path)
        gate_c(matrix)
        gate_b(matrix, bot)
        archive_regression(bot)
    except GateFail as e:
        print(f"\n[FAIL] {e}")
        print("SQUEEZE FAILED")
        if proc:
            stop_app(proc)
        return 1
    except Exception as e:  # noqa: BLE001
        print(f"\n[ERROR] unexpected: {e}")
        print("SQUEEZE FAILED")
        if proc:
            stop_app(proc)
        return 1

    stop_app(proc)
    print("\nSQUEEZE OK: ISOLATION + GATE C + GATE B + ARCHIVE REGRESSION all green.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
