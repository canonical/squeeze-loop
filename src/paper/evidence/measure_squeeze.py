#!/usr/bin/env python3
"""Evidence harness for the reflexive instance: measure the paper-as-squeeze and
emit results.json (mirrors src/A..D/evidence/measure_squeeze.py).

Reports the self-application counts (records, ledger rows, per-circle plans, and
the defects the gates caught in the paper's OWN claims) and the squeeze verdict.
Counts are read from the regenerated reflexive macros + the ledger, so they are
the same numbers the manuscript prints -- no hand-typed figures.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import _paperlib as L

PAPERDIR = Path(__file__).resolve().parents[1]


def main():
    # regenerate the reflexive macros so the counts are current
    L.run(["python3", "reflexive_measures.py"], cwd=L.REPO / "verify")

    runner = PAPERDIR / "in-band-deliverable" / "runner" / "execute_squeeze.py"
    sq = subprocess.run(["python3", str(runner)], capture_output=True, text=True)

    def n(macro):
        v = L.reflex_macro(macro)
        return int(v) if v and v.isdigit() else v

    results = {
        "instance": "paper (reflexive)",
        "squeeze_ok": sq.returncode == 0,
        "cited_sources": len(L.cite_keys()),
        "reading_records": n("ResReflexRecords"),
        "records_read_full": n("ResReflexRecordsFull"),
        "cite_ledger_rows": n("ResReflexCiteRows"),
        "result_ledger_rows": n("ResReflexResultRows"),
        "per_circle_plans": n("ResReflexSpecDocs"),
        "gap_docs": n("ResReflexGapDocs"),
        "self_defects_total": n("ResReflexDefects"),
        "self_defects_literature": n("ResReflexDefectsLit"),
        "self_defects_evidence": n("ResReflexDefectsEvid"),
        "executable_instances": n("ResReflexTerrains"),
    }
    out = PAPERDIR / "evidence" / "results.json"
    out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    print(f"results -> {out}")
    print("MEASURE OK" if results["squeeze_ok"] else "MEASURE: squeeze FAILED")
    sys.exit(0 if results["squeeze_ok"] else 1)


if __name__ == "__main__":
    main()
