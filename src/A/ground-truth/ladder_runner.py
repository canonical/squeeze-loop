#!/usr/bin/env python3
"""Run the metric-subtlety LADDER for Use Case A (level-up-A.md).

For each rung: compute the INTENDED value (the handbook's pinned reading) and each
FORK value (a plausible wrong reading that still runs) against the real warehouse.
A fork is CAUGHT when its value diverges from the intended value -- the
coherent-and-wrong an independent exerciser detects.

Verdict per rung:
  PASS     every fork diverges from intended (all coherent-and-wrong readings caught)
  PARTIAL  some fork equals intended ON THIS DATA -- the dataset does not exercise
           that interpretation fork. Reported honestly (not hidden); it is a
           coverage observation about the data's richness, not a defect, so the run
           still exits 0. (level-up-A: the experiment needs both a rich upper bound
           AND data rich enough to separate the forks.)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))            # for metrics.py
sys.path.insert(0, str(HERE / "ladder"))  # for ladder.py
import metrics
import ladder as L

DB = HERE / "shared" / "base_warehouse.db"


def ensure_db():
    if not DB.exists():
        import build_ground_truth  # noqa: F401  (its import builds nothing; call main)
        build_ground_truth.main() if hasattr(build_ground_truth, "main") else None
    if not DB.exists():
        # build via the script's top-level entry
        import subprocess
        subprocess.run([sys.executable, str(HERE / "build_ground_truth.py")], cwd=HERE, check=True)


def scalar(conn, sql):
    return metrics._scalar(conn, sql, ())


def main():
    ensure_db()
    conn = metrics.connect_ro(str(DB))
    print("=== Use Case A metric-subtlety ladder (level-up-A) ===")
    rows, ok = [], True
    for r in L.RUNGS:
        intended = scalar(conn, r["intended"])
        forks = []
        for f in r["forks"]:
            val = scalar(conn, f["sql"])
            caught = val != intended
            forks.append({"name": f["name"], "value": val, "caught": caught, "why": f["why"]})
        all_caught = all(f["caught"] for f in forks)
        verdict = "PASS" if all_caught else "PARTIAL"
        rows.append({"id": r["id"], "tier": r["tier"], "name": r["name"],
                     "intended": intended, "verdict": verdict, "forks": forks})
        nf = len(forks); nc = sum(f["caught"] for f in forks)
        mark = "[PASS]   " if verdict == "PASS" else "[PARTIAL]"
        print(f"{mark} {r['tier']:<10} {r['name']:<30} intended={intended:<12} "
              f"forks caught {nc}/{nf}")
        for f in forks:
            if not f["caught"]:
                print(f"          NOT EXERCISED by data: {f['name']} (= intended) -- {f['why']}")

    n_pass = sum(1 for r in rows if r["verdict"] == "PASS")
    print(f"\nladder: {n_pass}/{len(rows)} rungs with every fork caught; "
          f"{len(rows) - n_pass} PARTIAL (a fork the current data does not separate)")

    out = {
        "instance": "A-ladder",
        "rungs": len(rows),
        "rungs_all_forks_caught": n_pass,
        "per_rung": [{"tier": r["tier"], "name": r["name"], "intended": r["intended"],
                      "verdict": r["verdict"],
                      "forks_caught": sum(f["caught"] for f in r["forks"]),
                      "forks_total": len(r["forks"])} for r in rows],
    }
    ev = HERE.parents[0] / "evidence" / "ladder_results.json"
    ev.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(f"results -> {ev}")
    sys.exit(0)  # PARTIAL is an honest coverage observation, not a failure


if __name__ == "__main__":
    main()
