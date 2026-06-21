#!/usr/bin/env python3
"""Lower bound (build): regenerate the manuscript's executable substrate.

The paper's hard truth is that every reported number is produced by a harness,
not typed by hand. This runs all generators, so tex/macros/*.tex is rebuilt from
the committed artifacts (warehouses, eval runs, the reflexive measures). It is the
reflexive analogue of src/A/ground-truth/build_ground_truth.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import _paperlib as L


def main():
    print(f"regenerating {len(L.GENERATORS)} macro generators under {L.REPO}")
    failures = []
    for cwd, script in L.GENERATORS:
        d = L.REPO / cwd
        r = L.run(["python3", script], cwd=d)
        if r.returncode == 0:
            print(f"  [ok] {cwd}/{script}")
        else:
            failures.append(f"{cwd}/{script}")
            print(f"  [FAIL] {cwd}/{script}\n{r.stderr.strip()[:400]}")
    if failures:
        print(f"BUILD FAILED: {len(failures)} generator(s) errored")
        sys.exit(1)
    print("BUILD OK: all macro files regenerated from their artifacts")


if __name__ == "__main__":
    main()
