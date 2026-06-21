#!/usr/bin/env python3
"""Run the contract-richness LADDER for Use Case C (level-up-C.md).

For each rung: run the conformance cases (derived from the contract) against the
CORRECT server -- they must all pass (no false positive) -- and against each FORK
server (one that passes the happy path but blends a plane). A fork is CAUGHT when
at least one conformance case fails against it: the document plane and the runtime
plane disagree, which the no-blend cross-check detects.

Verdict per rung:
  PASS  correct passes every case AND every fork is caught
  FAIL  the correct server fails a case (a real contract/test defect)
  GAP   a fork passes every case (the suite does not separate it) -- reported
        honestly, never hidden.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "ladder"))
import ladder as L


def run_case(handler, case):
    state, resps = {}, []
    for q in case["steps"]:
        resps.append(handler(state, q))
    try:
        return bool(case["ok"](resps))
    except Exception:
        return False


def main():
    print("=== Use Case C contract-richness ladder (level-up-C) ===")
    rows, ok = [], True
    for r in L.RUNGS:
        correct_pass = all(run_case(r["correct"], c) for c in r["cases"])
        forks = []
        for f in r["forks"]:
            # caught iff at least one conformance case fails against the fork
            caught = any(not run_case(f["handler"], c) for c in r["cases"])
            forks.append({"name": f["name"], "caught": caught, "why": f["why"]})
        all_caught = all(f["caught"] for f in forks)
        if not correct_pass:
            verdict = "FAIL"; ok = False
        elif not all_caught:
            verdict = "GAP"
        else:
            verdict = "PASS"
        rows.append({"id": r["id"], "tier": r["tier"], "clause": r["clause"],
                     "correct_conformant": correct_pass, "verdict": verdict, "forks": forks})
        nc = sum(f["caught"] for f in forks)
        mark = {"PASS": "[PASS]", "GAP": "[GAP ]", "FAIL": "[FAIL]"}[verdict]
        print(f"{mark} {r['tier']:<10} {r['clause']:<55} correct_ok={correct_pass} "
              f"forks caught {nc}/{len(forks)}")
        for f in forks:
            if not f["caught"]:
                print(f"        NOT CAUGHT: {f['name']} (passed every case) -- {f['why']}")

    n_pass = sum(1 for r in rows if r["verdict"] == "PASS")
    print(f"\nladder: {n_pass}/{len(rows)} rungs with correct conformant and every blend caught")

    out = {
        "instance": "C-ladder",
        "rungs": len(rows),
        "rungs_pass": n_pass,
        "per_rung": [{"tier": r["tier"], "clause": r["clause"], "verdict": r["verdict"],
                      "correct_conformant": r["correct_conformant"],
                      "forks_caught": sum(f["caught"] for f in r["forks"]),
                      "forks_total": len(r["forks"])} for r in rows],
    }
    ev = HERE.parents[0] / "evidence" / "ladder_results.json"
    ev.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(f"results -> {ev}")
    sys.exit(0 if ok else 1)   # only a non-conformant CORRECT server is a hard failure


if __name__ == "__main__":
    main()
