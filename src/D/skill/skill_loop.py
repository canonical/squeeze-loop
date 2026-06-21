#!/usr/bin/env python3
"""Skill-accumulation loop for Use Case D (docs/skill-accumulation-design.md).

D's deciding agent is the prover, and its SKILL is tactics. It starts knowing no
tactic; when it hits a wall (an exercise it cannot discharge), it acquires the
catalog tactic that the exercise needs (lia, then nia) -- a bounded conceptual
leap. So the skill ENRICHES and the not-found rate FALLS across cycles.

The honest D signature: the catalog (lia, nia) cannot crack every exercise. A
residual WALL remains (exponentials, amgm-style inequalities) that needs a real
conceptual leap -- a manual lemma / induction -- which docs/skill-accumulation-design.md
explicitly defers. So the not-found rate falls to a FLOOR (the wall), not to zero.
That floor is the frontier where the deferred conceptual-leap mechanism would act.

Tiers are real Rocq verdicts cached by precompute_tiers.py; the loop is then
deterministic and kernel-free. Rule 1: only the deciding agent learns. Reset: from
scratch. Programmatic learner over a fixed tactic catalog, not a live LLM.
"""
import json
import os
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0] / "diversity"))
import pool as P

TIERS = json.loads((HERE / "d_tactic_tiers.json").read_text())
CATALOG = {"lia", "nia"}            # the tactics the prover can acquire
CYCLES = int(os.environ.get("DIV_CYCLES", "100"))
SAMPLE = int(os.environ.get("DIV_SAMPLE", "5"))
SEED = int(os.environ.get("DIV_SEED", "7000"))


def run(cycles=CYCLES, sample=SAMPLE, seed=SEED):
    rng = random.Random(seed)
    skill = set()                  # acquired tactics (start from scratch)
    per_cycle, learned = [], []
    for i in range(1, cycles + 1):
        solvable_miss = wall_hits = 0
        for ex in (rng.choice(P.POOL) for _ in range(sample)):
            tier = TIERS[ex["id"]]
            if tier in skill:
                continue              # solved with a known tactic
            if tier in CATALOG:       # a catalog tactic cracks it but isn't learned yet
                solvable_miss += 1    # ... so this is a miss the skill will remove
                skill.add(tier)       # acquire (learn) the tactic
                learned.append({"cycle": i, "tactic": tier})
            else:
                wall_hits += 1        # conceptual-leap wall: no catalog tactic (a floor)
        per_cycle.append({"cycle": i, "solvable_miss": solvable_miss, "wall_hits": wall_hits,
                          "not_found": solvable_miss + wall_hits, "skill_size": len(skill)})
    return per_cycle, sorted(skill), learned


def main():
    per, skill, learned = run()
    w = max(1, len(per) // 10)
    early = round(sum(c["solvable_miss"] for c in per[:w]) / w, 2)
    late = round(sum(c["solvable_miss"] for c in per[-w:]) / w, 2)
    wall_total = sum(1 for v in TIERS.values() if v not in CATALOG)
    print(f"=== D skill loop: {len(per)} cycles from scratch (sample {SAMPLE}, seed {SEED}) ===")
    for c in per:
        if c["cycle"] <= 6 or c["cycle"] % 10 == 0 or c in per[-2:]:
            print(f"  cycle {c['cycle']:>3}: solvable-miss {c['solvable_miss']} "
                  f"wall {c['wall_hits']}/{SAMPLE}  tactics {c['skill_size']}")
    print(f"\nskill enriched 0 -> {len(skill)} tactics ({', '.join(skill)}); learned at "
          f"{[(e['cycle'], e['tactic']) for e in learned]}")
    print(f"solvable-miss/cycle first {w} {early} -> last {w} {late} (learned away); "
          f"residual conceptual-leap wall = {wall_total}/100 exercises (deferred floor)")
    out = {"instance": "D-skill", "cycles": len(per), "sample": SAMPLE, "seed": SEED,
           "final_skill": skill, "learned_events": learned,
           "solvable_miss_first_window_mean": early, "solvable_miss_last_window_mean": late,
           "conceptual_leap_wall": wall_total, "per_cycle": per}
    (HERE / "skill_enrichment_results.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(f"results -> {HERE / 'skill_enrichment_results.json'}")


if __name__ == "__main__":
    main()
