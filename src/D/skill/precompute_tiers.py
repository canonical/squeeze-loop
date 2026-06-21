#!/usr/bin/env python3
"""Precompute, with the REAL Rocq kernel, the minimal tactic tier that solves each
exercise in the D pool, and cache it to d_tactic_tiers.json.

Catalog (bounded conceptual leaps), weakest first:
  lia   -- linear integer arithmetic
  nia   -- nonlinear integer arithmetic
  wall  -- neither catalog tactic solves it (needs a real conceptual leap:
           a manual lemma / induction; deferred per docs/skill-accumulation-design.md)

Run once with the kernel on PATH; the cache makes the skill loop and its test
deterministic and kernel-free. The tiers are genuine kernel verdicts, not assigned
by hand.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0] / "diversity"))
import pool as P
STDLIB = HERE.parents[0] / "ground-truth" / "shared" / "rocq_stdlib"
CATALOG = [("lia", "intros; lia"), ("nia", "intros; nia")]


def solves(stmt, tactic):
    src = f"Require Import Lia.\nTheorem t : {stmt}.\nProof. {tactic}. Qed.\n"
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "t.v"; f.write_text(src)
        cmd = (["coqc"] if __import__("shutil").which("coqc") else ["rocq", "compile"])
        cmd += ["-R", str(STDLIB), "Top", str(f)]
        return subprocess.run(cmd, capture_output=True).returncode == 0


def main():
    if not (__import__("shutil").which("coqc") or __import__("shutil").which("rocq")):
        print("DEPENDENCY UNMET: Rocq absent -- cannot precompute tiers.", file=sys.stderr)
        return 3
    tiers = {}
    for ex in P.POOL:
        tier = "wall"
        for name, tac in CATALOG:
            if solves(ex["stmt"], tac):
                tier = name
                break
        tiers[ex["id"]] = tier
    from collections import Counter
    print(json.dumps(Counter(tiers.values()), indent=2))
    (HERE / "d_tactic_tiers.json").write_text(json.dumps(tiers, indent=2, sort_keys=True) + "\n")
    print("cache ->", HERE / "d_tactic_tiers.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
