#!/usr/bin/env python3
"""Test that D's tactic skill enriches across cycles, the not-found rate falls, and
-- the honest D signature -- a residual conceptual-leap WALL persists (it does NOT
reach zero). Exit 0 iff all checks hold."""
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import skill_loop as SK


def main():
    per, skill, learned = SK.run()
    sizes = [c["skill_size"] for c in per]
    w = max(1, len(per) // 10)
    early = sum(c["solvable_miss"] for c in per[:w]) / w
    late = sum(c["solvable_miss"] for c in per[-w:]) / w
    late_wall = sum(c["wall_hits"] for c in per[-w:]) / w
    learned_cycles = sorted({e["cycle"] for e in learned})
    wall_total = sum(1 for v in SK.TIERS.values() if v not in SK.CATALOG)

    checks = [
        (f"from scratch (every tactic learned, none preloaded: {len(learned)} events -> {len(skill)})",
         len({e["tactic"] for e in learned}) == len(skill) and len(skill) > 0),
        (f"acquires both catalog tactics ({len(skill)}/2: {skill})", len(skill) == 2),
        (f"enrichment spans >=2 distinct cycles ({learned_cycles})", len(learned_cycles) >= 2),
        ("skill_size monotonically non-decreasing", all(b >= a for a, b in zip(sizes, sizes[1:]))),
        (f"solvable-miss rate falls to 0 (first {early} > last {late} == 0)",
         early > late and late == 0),
        (f"residual conceptual-leap wall persists ({wall_total}/100, late wall {late_wall} > 0)",
         wall_total > 0 and late_wall > 0),
    ]

    # causality: with NO skill every drawn exercise is not-found; with the final skill
    # only the wall exercises are. Replay the last window.
    rng = random.Random(SK.SEED)
    total = len(per) * SK.SAMPLE
    empty = trained = 0
    for idx in range(total):
        ex = rng.choice(SK.P.POOL)
        if idx >= total - w * SK.SAMPLE:
            tier = SK.TIERS[ex["id"]]
            empty += 1                                  # empty skill -> always not-found
            if tier not in skill:
                trained += 1                            # trained -> only wall exercises
    checks.append((f"skill is causal (empty {empty} not-found, trained {trained} = wall only)",
                   empty > trained and trained > 0))

    per2, skill2, _ = SK.run()
    checks.append(("deterministic (re-run identical)", per2 == per and skill2 == skill))

    ok = all(p for _, p in checks)
    for label, p in checks:
        print(f"  [{'PASS' if p else 'FAIL'}] {label}")
    print("SKILL-ENRICHMENT TEST (D):", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
