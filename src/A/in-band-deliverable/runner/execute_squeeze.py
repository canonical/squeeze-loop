#!/usr/bin/env python3
"""The Squeeze Connector (in-band-deliverable-spec §3).

The structural bridge `gate_sentinel.py` runs to force the implementer's code and
the exerciser's tests to reconcile over the read-only warehouse. It imports
neither band; it runs the implementer as a subprocess and reads the exerciser's
JSON (Strict Serialization). It also reads the upper-bound handbook (sentinel-side)
to drive Gate C.

Checks, all of which must pass (nonzero exit otherwise):

  ISOLATION  the implementer and exerciser directories contain zero cross-
             references to each other (Zero Import Linkage, spec Summary 1).
  GATE C     every obligation CLAUSE_x of the metric is named by at least one
             test case's target_clauses (coverage; spec §3 Gate C).
  GATE B+    POSITIVES: the implementer's value matches the exerciser's expected
             value; for quarter windows it also matches the certified ledger
             (Total Additivity, the lower-bound invariant).
             NEGATIVES: the named mutation's value DIVERGES from the implementer's
             correct value -- proving the clause is load-bearing.
"""

import ast
import json
import os
import re
import subprocess
import sqlite3
import sys
from pathlib import Path

import mutations

RUNNER = Path(__file__).resolve().parent
ROOT = RUNNER.parent                       # src/A/in-band-deliverable
ROOT_A = ROOT.parent                       # src/A
EXERCISER_TESTS = ROOT / "exerciser" / "tests"


def _resolve_impl():
    # Deployed location (spec §1) first, then the repo copy; COMPUTE_METRIC overrides.
    env = os.environ.get("COMPUTE_METRIC")
    for p in (Path(env) if env else None,
              Path("/home/implementer/src/compute_metric.py"),
              ROOT / "implementer" / "src" / "compute_metric.py"):
        if p and p.exists():
            return p
    sys.exit("error: compute_metric.py not found")


IMPL = _resolve_impl()

sys.path.insert(0, str(ROOT_A / "upper-bound"))
import handbook as hb                       # noqa: E402  (sentinel reads the ceiling)

QUARTERS = {
    ("2025-01-01T00:00:00Z", "2025-04-01T00:00:00Z"): "2025_Q1",
    ("2025-04-01T00:00:00Z", "2025-07-01T00:00:00Z"): "2025_Q2",
    ("2025-07-01T00:00:00Z", "2025-10-01T00:00:00Z"): "2025_Q3",
    ("2025-10-01T00:00:00Z", "2026-01-01T00:00:00Z"): "2025_Q4",
}


def find(path_opt, *fallbacks):
    for p in (path_opt, *fallbacks):
        if p and Path(p).exists():
            return Path(p)
    return None


DB = find(Path("/opt/squeeze/shared/base_warehouse.db"),
          ROOT_A / "ground-truth" / "shared" / "base_warehouse.db")
LEDGER = find(Path("/opt/squeeze/shared/history_ledger.json"),
              ROOT_A / "ground-truth" / "shared" / "history_ledger.json")


class GateFail(Exception):
    pass


def _eq(a, b, tol=0.005):
    return abs(float(a) - float(b)) <= tol


def run_implementer(metric_id, start, end):
    proc = subprocess.run(
        ["python3", str(IMPL), "--metric", metric_id, "--start", start, "--end", end],
        capture_output=True, text=True)
    if proc.returncode != 0:
        raise GateFail(f"implementer crashed for {metric_id} [{start},{end}): {proc.stderr.strip()}")
    return json.loads(proc.stdout)["value"]


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


def ledger_key(metric_id, quarter):
    return {"METRIC_001": f"{quarter}_revenue_USD",
            "METRIC_002": f"{quarter}_active_users"}[metric_id]


def run_matrix(path, conn, ledger):
    matrix = json.loads(Path(path).read_text())
    mid = matrix["metric_id"]
    metric = hb.by_id(hb.parse(), mid)
    positives = matrix.get("positives", [])
    negatives = matrix.get("negatives", [])
    print(f"\n=== {mid} ({Path(path).name}): {len(positives)} positives, "
          f"{len(negatives)} negatives ===")

    # GATE C: every clause covered by some test case's target_clauses.
    covered = set()
    for tc in positives + negatives:
        covered.update(tc.get("target_clauses", []))
    missing = [c for c in metric.clause_ids if c not in covered]
    if missing:
        raise GateFail(f"GATE C: clauses uncovered by the validation matrix: {missing}")
    print(f"[PASS] GATE C    -- all clauses covered {metric.clause_ids}")

    # GATE B (positives): implementer == exerciser expected; quarters == ledger.
    for tc in positives:
        w = tc["window"]
        got = run_implementer(mid, w["start"], w["end"])
        exp = tc["expected_output"]["value"]
        if not _eq(got, exp):
            raise GateFail(f"GATE B CRASH (coherent-and-wrong): {tc['test_case_id']} "
                           f"implementer={got} exerciser={exp}")
        q = QUARTERS.get((w["start"], w["end"]))
        if q and ledger is not None:
            lv = ledger[ledger_key(mid, q)]
            if not _eq(got, lv):
                raise GateFail(f"INVARIANT BREACH: {tc['test_case_id']} value {got} "
                               f"!= certified ledger {lv}")
        print(f"[PASS] POSITIVE  -- {tc['test_case_id']}: {got} (== expected"
              + (f" == ledger {q}" if q else "") + ")")

    # GATE B (negatives): the named mutation must diverge from the correct value.
    for tc in negatives:
        w = tc["window"]
        correct = run_implementer(mid, w["start"], w["end"])
        mutated = mutations.apply(tc["mutation"], conn, w["start"], w["end"])
        if _eq(mutated, correct):
            raise GateFail(f"VACUOUS NEGATIVE: {tc['test_case_id']} mutation "
                           f"{tc['mutation']} did not diverge (both {correct}) "
                           f"-- clause {tc['target_clauses']} is not load-bearing here")
        print(f"[PASS] NEGATIVE  -- {tc['test_case_id']}: correct={correct} "
              f"vs mutated({tc['mutation']})={mutated} -> "
              f"{tc['expected_fault']['reason']} at {tc['expected_fault']['site']}")


def main():
    if DB is None:
        sys.exit("error: base_warehouse.db not found (build ../ground-truth first)")
    matrices = sorted(EXERCISER_TESTS.glob("validation_matrix.METRIC_*.json"))
    if not matrices:
        sys.exit("error: no validation matrices (run exerciser/build_validation_matrix.py)")
    ledger = json.loads(LEDGER.read_text()) if LEDGER else None

    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    try:
        check_isolation()
        for m in matrices:
            run_matrix(m, conn, ledger)
    except GateFail as e:
        print(f"\n[FAIL] {e}")
        print("SQUEEZE FAILED")
        return 1
    finally:
        conn.close()

    print("\nGATE B SUCCESS: in-band alignment verified across all metrics.")
    print("SQUEEZE OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
