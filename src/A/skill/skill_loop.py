#!/usr/bin/env python3
"""Skill-accumulation loop for Use Case A (docs/skill-accumulation-design.md).

The deciding agent (the analyst writing a query) starts with an EMPTY skill store
and writes the OBVIOUS (naive) query. Each time the independent exerciser catches
its value diverging from the intended reading on the real warehouse, it records the
catch; after consolidating (learning rate K) it writes a skill ("for this metric
family, the obvious reading is wrong -- use the intended interpretation"). It then
uses the intended query for that family. So the skill ENRICHES over the subtle
metric families and the error rate FALLS across cycles.

Rule 1: only the deciding agent learns; the warehouse and the intended readings (the
answer key) stay fixed. Reset: start from scratch. Deterministic (seeded). The
deciding agent is a programmatic learner, not a live LLM (the honest gap).
"""
import json
import os
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0] / "diversity"))     # pool
sys.path.insert(0, str(HERE.parents[0] / "ground-truth"))  # metrics, build_ground_truth
import metrics
import pool as P

DB = HERE.parents[0] / "ground-truth" / "shared" / "base_warehouse.db"
CYCLES = int(os.environ.get("DIV_CYCLES", "100"))
SAMPLE = int(os.environ.get("DIV_SAMPLE", "4"))
SEED = int(os.environ.get("DIV_SEED", "8000"))
CONSOLIDATE_K = int(os.environ.get("DIV_K", "3"))

FAMILIES = ("net_rev", "dau_grain", "active_customer", "survivorship")


def family_of(kind):
    for f in FAMILIES:
        if kind.startswith(f):
            return f
    return kind                      # simple metric: its own family (never diverges)


def ensure_db():
    if not DB.exists():
        import subprocess
        subprocess.run([sys.executable, "build_ground_truth.py"],
                       cwd=HERE.parents[0] / "ground-truth", check=True)


def run(cycles=CYCLES, sample=SAMPLE, seed=SEED, k=CONSOLIDATE_K):
    ensure_db()
    conn = metrics.connect_ro(str(DB))
    sc = lambda sql: metrics._scalar(conn, sql, ())
    rng = random.Random(seed)
    skill, catches = {}, {}
    per_cycle, learned = [], []
    for i in range(1, cycles + 1):
        errors = 0
        for _ in range(sample):
            t = rng.choice(P.POOL)
            fam = family_of(t["kind"])
            chosen = t["intended"] if fam in skill else t["naive"]   # read the skill to act
            if sc(chosen) != sc(t["intended"]):                       # caught by the exerciser
                errors += 1
                catches[fam] = catches.get(fam, 0) + 1
                if fam not in skill and catches[fam] >= k:
                    skill[fam] = {"lesson": f"metric family '{fam}': the obvious query "
                                            f"is a wrong fork; use the intended reading",
                                  "learned_cycle": i}
                    learned.append({"cycle": i, "family": fam})
        per_cycle.append({"cycle": i, "errors": errors,
                          "error_pct": round(100 * errors / sample),
                          "skill_size": len(skill)})
    return per_cycle, skill, learned


def main():
    per, skill, learned = run()
    w = max(1, len(per) // 10)
    early = round(sum(c["errors"] for c in per[:w]) / w, 2)
    late = round(sum(c["errors"] for c in per[-w:]) / w, 2)
    print(f"=== A skill loop: {len(per)} cycles from scratch "
          f"(sample {SAMPLE}, K={CONSOLIDATE_K}, seed {SEED}) ===")
    for c in per:
        if c["cycle"] <= 6 or c["cycle"] % 10 == 0 or c in per[-2:]:
            print(f"  cycle {c['cycle']:>3}: errors {c['errors']:>2}/{SAMPLE}  skill_size {c['skill_size']}")
    print(f"\nskill enriched 0 -> {len(skill)} ({', '.join(sorted(skill))}); learned at "
          f"{[e['cycle'] for e in learned]}; errors first {w} {early} -> last {w} {late}")
    out = {"instance": "A-skill", "cycles": len(per), "sample": SAMPLE, "seed": SEED,
           "consolidate_k": CONSOLIDATE_K, "final_skill_size": len(skill),
           "skills": sorted(skill), "learned_events": learned,
           "errors_first_window_mean": early, "errors_last_window_mean": late,
           "per_cycle": per}
    (HERE / "skill_enrichment_results.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    (HERE / "skill_store.json").write_text(json.dumps(skill, indent=2, sort_keys=True) + "\n")
    print(f"results -> {HERE / 'skill_enrichment_results.json'}")


if __name__ == "__main__":
    main()
