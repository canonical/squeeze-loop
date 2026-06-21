#!/usr/bin/env python3
"""D diversity test: sample math exercises randomly and observe a real, varying
success rate against a FIXED weak auto-prover (`intros; lia`).

This breaks the level-up ladder's perfect determinism on purpose: each cycle draws
a random sample from the 100-exercise pool and attempts each with the real Rocq
kernel. "found" = the proof closes (exit 0); "not found" = the kernel rejects the
weak tactic. Across cycles the found/not-found counts VARY -- an actual trial.

Randomness is seeded per cycle (base_seed + cycle) so the experiment is reproducible
while the cycles differ from one another; the seed is recorded.
"""
import json
import random
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pool as P

STDLIB = HERE.parents[0] / "ground-truth" / "shared" / "rocq_stdlib"
SAMPLE = 20
CYCLES = int(__import__("os").environ.get("DIV_CYCLES", "10"))
BASE_SEED = int(__import__("os").environ.get("DIV_SEED", "7000"))

PROVER = "intros; lia"  # the fixed weak implementer


def have_kernel():
    import shutil
    return shutil.which("coqc") or shutil.which("rocq")


def attempt(ex):
    """Return True iff `intros; lia` closes the goal (the weak prover finds it)."""
    src = (f"Require Import Lia.\nTheorem {ex['id'].lower()} : {ex['stmt']}.\n"
           f"Proof. {PROVER}. Qed.\n")
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "ex.v"
        f.write_text(src)
        if shutil_which("coqc"):
            cmd = ["coqc", "-R", str(STDLIB), "Top", str(f)]
        else:
            cmd = ["rocq", "compile", "-R", str(STDLIB), "Top", str(f)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        return r.returncode == 0


def shutil_which(b):
    import shutil
    return shutil.which(b)


def main():
    if not have_kernel():
        print("DEPENDENCY UNMET: Rocq (coqc/rocq) absent -- diversity test SKIPPED (not faked).")
        sys.exit(3)

    print(f"=== D diversity: {CYCLES} cycles, sample {SAMPLE}/{len(P.POOL)} per cycle "
          f"(fixed prover: `{PROVER}`) ===")
    verdict = {ex["id"]: attempt(ex) for ex in P.POOL}  # deterministic per exercise: compile once
    per_cycle = []
    for i in range(CYCLES):
        seed = BASE_SEED + i
        rng = random.Random(seed)
        sample = rng.sample(P.POOL, SAMPLE)
        found = sum(verdict[ex["id"]] for ex in sample)
        notfound = SAMPLE - found
        rate = round(100 * found / SAMPLE)
        per_cycle.append({"cycle": i + 1, "seed": seed, "sample": SAMPLE,
                          "found": found, "not_found": notfound, "found_pct": rate})
        print(f"  cycle {i+1:2d} (seed {seed}): found {found}/{SAMPLE} "
              f"({rate}%), not_found {notfound}")

    founds = [c["found"] for c in per_cycle]
    distinct = len(set(founds))
    mean = round(sum(founds) / len(founds), 1)
    print(f"\nfound/cycle: min {min(founds)} max {max(founds)} mean {mean}; "
          f"distinct outcomes across cycles: {distinct}/{CYCLES}")

    # whole-pool baseline (calibration check)
    base_found = sum(verdict.values())
    print(f"whole-pool baseline: found {base_found}/100, not_found {100-base_found} "
          f"(~{100-base_found}% beyond the weak prover)")

    out = {"instance": "D-diversity", "pool": len(P.POOL), "sample": SAMPLE,
           "cycles": CYCLES, "prover": PROVER, "base_seed": BASE_SEED,
           "pool_not_found": 100 - base_found, "found_per_cycle": founds,
           "distinct_outcomes": distinct, "per_cycle": per_cycle}
    (HERE / "diversity_results.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(f"results -> {HERE / 'diversity_results.json'}")


if __name__ == "__main__":
    main()
