#!/usr/bin/env python3
"""A diversity test: sample metric tasks randomly and observe a real, varying
implementer error rate against the warehouse.

The "implementer" is fixed and weak: it writes the obvious (naive) query. On simple
metrics that is correct; on subtle metrics it is a wrong fork. The error is
naive != intended on the real warehouse -- the coherent-and-wrong the exerciser
catches. Random sampling per cycle makes the error rate vary: an actual trial.

Seeded per cycle (base + cycle): cycles differ, the experiment reproduces.
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[0] / "ground-truth"))
import metrics
import pool as P

DB = HERE.parents[0] / "ground-truth" / "shared" / "base_warehouse.db"
SAMPLE, CYCLES, BASE_SEED = 20, int(__import__("os").environ.get("DIV_CYCLES","10")), int(__import__("os").environ.get("DIV_SEED", "8000"))


def ensure_db():
    if not DB.exists():
        import subprocess
        subprocess.run([sys.executable, "build_ground_truth.py"],
                       cwd=HERE.parents[0] / "ground-truth", check=True)


def main():
    ensure_db()
    conn = metrics.connect_ro(str(DB))
    sc = lambda sql: metrics._scalar(conn, sql, ())
    print(f"=== A diversity: {CYCLES} cycles, sample {SAMPLE}/{len(P.POOL)} metric tasks "
          f"per cycle (weak implementer writes the obvious query) ===")
    per_cycle = []
    for i in range(CYCLES):
        seed = BASE_SEED + i
        sample = random.Random(seed).sample(P.POOL, SAMPLE)
        errors = sum(1 for t in sample if sc(t["naive"]) != sc(t["intended"]))
        rate = round(100 * errors / SAMPLE)
        per_cycle.append({"cycle": i + 1, "seed": seed, "errors_caught": errors, "error_pct": rate})
        print(f"  cycle {i+1:2d} (seed {seed}): implementer errors caught {errors}/{SAMPLE} ({rate}%)")

    # whole-pool baseline
    base = sum(1 for t in P.POOL if sc(t["naive"]) != sc(t["intended"]))
    errs = [c["errors_caught"] for c in per_cycle]
    distinct = len(set(errs))
    print(f"\nerrors/cycle: min {min(errs)} max {max(errs)} mean {round(sum(errs)/len(errs),1)}; "
          f"distinct outcomes across cycles: {distinct}/{CYCLES}")
    print(f"whole-pool baseline: {base}/100 tasks where the obvious query diverges from intent")

    out = {"instance": "A-diversity", "pool": len(P.POOL), "sample": SAMPLE, "cycles": CYCLES,
           "base_seed": BASE_SEED, "pool_diverging": base, "errors_per_cycle": errs,
           "distinct_outcomes": distinct, "per_cycle": per_cycle}
    (HERE / "diversity_results.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(f"results -> {HERE / 'diversity_results.json'}")


if __name__ == "__main__":
    main()
