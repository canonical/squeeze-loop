#!/usr/bin/env python3
"""Evidence harness (paper-bench-agent) for Use Case A.

Runs the full src/A squeeze end-to-end and emits re-runnable measurements:
  - evidence/results.json   the machine-readable record
  - tex/macros/results.tex  generated LaTeX macros (\\Res...), so every number in
                            the paper is produced here, never hand-typed

Deterministic: same warehouse + same code -> same numbers. This is the executable
lower bound for the paper's claims about Use Case A.
"""

import hashlib
import json
import subprocess
import sqlite3
import sys
from pathlib import Path

EV = Path(__file__).resolve().parent
A = EV.parent
REPO = A.parents[1]                       # A=src/A -> parents[0]=src, [1]=repo
GT = A / "ground-truth"
UB = A / "upper-bound"
IB = A / "in-band-deliverable"
DB = GT / "shared" / "base_warehouse.db"
LEDGER = GT / "shared" / "history_ledger.json"
SIG = GT / "shared" / "history_ledger.sig"
TESTS = IB / "exerciser" / "tests"
MACROS = REPO / "tex" / "macros" / "results.tex"


def run(*cmd, env=None):
    return subprocess.run([str(c) for c in cmd], capture_output=True, text=True, env=env)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    R = {}

    # --- layer self-checks --------------------------------------------------
    R["ground_truth_verify_ok"] = run("python3", GT / "verify_ground_truth.py").returncode == 0
    R["upper_bound_validate_ok"] = run("python3", UB / "validate_handbook.py").returncode == 0

    # --- counts from the artifacts -----------------------------------------
    sys.path.insert(0, str(UB))
    import handbook  # noqa: E402
    metrics = handbook.parse(UB / "metric_handbook.md")
    R["metrics"] = len(metrics)
    R["clauses"] = sum(len(m.clauses) for m in metrics)

    R["certified_ledger_metrics"] = len(json.loads(LEDGER.read_text()))
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    R["warehouse_users"] = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    R["warehouse_events"] = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    conn.close()

    # --- regenerate the exerciser matrices, count test cases ----------------
    run("python3", IB / "exerciser" / "build_validation_matrix.py")
    positives = negatives = 0
    for mx in sorted(TESTS.glob("validation_matrix.METRIC_*.json")):
        m = json.loads(mx.read_text())
        positives += len(m.get("positives", []))
        negatives += len(m.get("negatives", []))
    R["positive_cells"] = positives
    R["seeded_defects"] = negatives          # the named clause-violating mutations

    # --- run the squeeze with the real (correct) implementer ----------------
    sq = run("python3", IB / "runner" / "execute_squeeze.py")
    R["squeeze_ok"] = sq.returncode == 0
    R["isolation_ok"] = "[PASS] ISOLATION" in sq.stdout
    R["positives_passed"] = sq.stdout.count("[PASS] POSITIVE")
    R["defects_caught"] = sq.stdout.count("[PASS] NEGATIVE")
    R["three_way_agreements"] = sq.stdout.count("== ledger")   # impl==exerciser==ledger

    # --- negative control: a coherent-and-wrong implementer must be caught ---
    import os
    env = dict(os.environ, COMPUTE_METRIC=str(EV / "coherent_wrong_fixture.py"))
    nc = run("python3", IB / "runner" / "execute_squeeze.py", env=env)
    R["coherent_wrong_caught"] = nc.returncode == 1 and "GATE B CRASH" in nc.stdout

    # --- total additivity: ledger+sig byte-stable across a rebuild ----------
    before = (sha(LEDGER), sha(SIG))
    run("python3", GT / "build_ground_truth.py")
    after = (sha(LEDGER), sha(SIG))
    R["additivity_stable"] = before == after
    R["ledger_sha256"] = after[0]

    # --- ablation: the physical barrier (C3) on vs off (H2) -----------------
    # For each seeded coherent-and-wrong implementer (a clause-violating mutation),
    # does the exerciser catch it? It depends on where the exerciser's ORACLE
    # comes from:
    #   barrier ON  -> the handbook (upper bound): expected = the correct value.
    #   barrier OFF -> the exerciser has seen the implementation and anchors to
    #                  it: expected = the (wrong) implementation's own output.
    sys.path.insert(0, str(IB / "runner"))
    import mutations  # noqa: E402

    def _impl(metric, s, e):
        return json.loads(run("python3", IB / "implementer" / "src" / "compute_metric.py",
                              "--metric", metric, "--start", s, "--end", e).stdout)["value"]

    aconn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    on = off = seeded = 0
    for mx in sorted(TESTS.glob("validation_matrix.METRIC_*.json")):
        mm = json.loads(mx.read_text())
        mid = mm["metric_id"]
        for neg in mm.get("negatives", []):
            w = neg["window"]
            correct = _impl(mid, w["start"], w["end"])
            wrong = mutations.apply(neg["mutation"], aconn, w["start"], w["end"])
            seeded += 1
            on += (wrong != correct)            # oracle = handbook
            off += (wrong != wrong)             # oracle = the implementation itself -> 0
    aconn.close()
    R["ablation_seeded"] = seeded
    R["ablation_barrier_on_caught"] = on
    R["ablation_barrier_off_caught"] = off

    R["detection_rate_pct"] = round(100 * R["defects_caught"] / max(R["seeded_defects"], 1))

    # --- emit results.json --------------------------------------------------
    (EV / "results.json").write_text(json.dumps(R, indent=2, sort_keys=True) + "\n")

    # --- emit generated LaTeX macros ----------------------------------------
    macro = {
        "ResWorkedMetrics": R["metrics"],
        "ResWorkedClauses": R["clauses"],
        "ResWorkedPositiveCells": R["positive_cells"],
        "ResWorkedThreeWayAgree": R["three_way_agreements"],
        "ResWorkedSeededDefects": R["seeded_defects"],
        "ResWorkedDefectsCaught": R["defects_caught"],
        "ResWorkedDetectionPct": f'{R["detection_rate_pct"]}\\%',
        "ResWorkedWarehouseUsers": R["warehouse_users"],
        "ResWorkedWarehouseEvents": R["warehouse_events"],
        "ResWorkedCertifiedMetrics": R["certified_ledger_metrics"],
        "ResAblationSeeded": R["ablation_seeded"],
        "ResAblationBarrierOn": R["ablation_barrier_on_caught"],
        "ResAblationBarrierOff": R["ablation_barrier_off_caught"],
    }
    MACROS.parent.mkdir(parents=True, exist_ok=True)
    lines = ["% GENERATED by src/A/evidence/measure_squeeze.py -- do not hand-edit.",
             "% Re-run that script to regenerate. Every Use-Case-A number traces here."]
    for k in sorted(macro):
        lines.append(f"\\newcommand{{\\{k}}}{{{macro[k]}}}")
    MACROS.write_text("\n".join(lines) + "\n")

    gate_keys = ["ground_truth_verify_ok", "upper_bound_validate_ok", "squeeze_ok",
                 "isolation_ok", "coherent_wrong_caught", "additivity_stable"]
    ok = all(R[k] for k in gate_keys)
    print(json.dumps(R, indent=2, sort_keys=True))
    print("\nmacros ->", MACROS)
    print("MEASURE OK" if ok else "MEASURE: some checks FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
