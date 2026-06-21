#!/usr/bin/env python3
"""Test that the A skill store enriches across cycles and that the enrichment is
what removes the implementer's wrong-fork errors. Exit 0 iff all checks hold."""
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
    early = sum(c["errors"] for c in per[:w]) / w
    late = sum(c["errors"] for c in per[-w:]) / w
    learned_cycles = sorted({e["cycle"] for e in learned})

    checks = [
        ("starts from scratch (cycle 1 skill_size 0)", sizes[0] == 0),
        (f"reaches full coverage ({len(skill)}/{len(SK.FAMILIES)} families)",
         len(skill) == len(SK.FAMILIES)),
        (f"gradual (learned across {len(learned_cycles)} distinct cycles >= 3)",
         len(learned_cycles) >= 3),
        ("skill_size monotonically non-decreasing", all(b >= a for a, b in zip(sizes, sizes[1:]))),
        (f"error rate falls (first {early} > last {late})", early > late),
        ("late window clean (0 errors)", late == 0),
    ]

    # causality: replay the last window's drawn tasks against an empty skill.
    conn = SK.metrics.connect_ro(str(SK.DB))
    sc = lambda sql: SK.metrics._scalar(conn, sql, ())
    rng = random.Random(SK.SEED)
    total = len(per) * SK.SAMPLE
    empty_err = trained_err = 0
    for idx in range(total):
        t = rng.choice(SK.P.POOL)
        if idx >= total - w * SK.SAMPLE:
            fam = SK.family_of(t["kind"])
            if sc(t["naive"]) != sc(t["intended"]):            # empty skill -> naive
                empty_err += 1
            chosen = t["intended"] if fam in skill else t["naive"]
            if sc(chosen) != sc(t["intended"]):
                trained_err += 1
    checks.append((f"skill is causal (empty remakes {empty_err}, trained {trained_err})",
                   empty_err > 0 and trained_err == 0))

    per2, skill2, _ = SK.run()
    checks.append(("deterministic (re-run identical)", per2 == per and sorted(skill2) == sorted(skill)))

    ok = all(p for _, p in checks)
    for label, p in checks:
        print(f"  [{'PASS' if p else 'FAIL'}] {label}")
    print("SKILL-ENRICHMENT TEST (A):", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
