#!/usr/bin/env python3
"""Test that the B skill store ENRICHES across cycles and that the enrichment is
what reduces the deciding agent's error rate.

Asserts:
  1. starts from scratch (skill_size 0 at cycle 1's start) and reaches full
     coverage (all manipulation tactics learned);
  2. enrichment is GRADUAL -- lessons consolidate across several distinct cycles,
     not in a single step;
  3. skill_size is monotonically non-decreasing across cycles;
  4. the error rate falls -- the first window has errors, the last window is clean;
  5. the skill is CAUSAL -- a bot reset to an empty skill re-makes the errors the
     trained bot no longer makes (the squeeze, via the fixed oracle, taught it);
  6. the run is deterministic (re-run is identical).
Exit 0 iff all hold.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import skill_loop as SK

N_TACTICS = sum(1 for c in SK.CHARACTERS.values() if c is not None)


def main():
    per, skill, learned = SK.run()
    sizes = [c["skill_size"] for c in per]
    w = max(1, len(per) // 10)
    early = sum(c["errors"] for c in per[:w]) / w
    late = sum(c["errors"] for c in per[-w:]) / w
    learned_cycles = sorted({e["cycle"] for e in learned})

    checks = []
    checks.append(("starts from scratch (cycle 1 skill_size 0)", sizes[0] == 0))
    checks.append((f"reaches full coverage ({len(skill)}/{N_TACTICS} tactics learned)",
                   len(skill) == N_TACTICS))
    checks.append((f"enrichment is gradual (learned across {len(learned_cycles)} distinct cycles >= 3)",
                   len(learned_cycles) >= 3))
    checks.append(("skill_size monotonically non-decreasing",
                   all(b >= a for a, b in zip(sizes, sizes[1:]))))
    checks.append((f"error rate falls (first window {early} > last window {late})",
                   early > late))
    checks.append(("late window is clean (0 errors)", late == 0))

    # 5. causality: replay the last window's chats against an EMPTY skill -> errors return.
    import random
    rng = random.Random(SK.SEED)
    discs = SK.DV.load_discussions()
    chars = list(SK.CHARACTERS)
    # advance the stream to the last window, collecting those chats
    last_chats = []
    total = len(per) * SK.SAMPLE
    for idx in range(total):
        sit, oid, opening = rng.choice(discs)
        char = rng.choice(chars)
        cust, order = SK.DV.SITUATIONS[sit]
        msgs = [opening] + ([SK.CHARACTERS[char]] if SK.CHARACTERS[char] else [])
        if idx >= total - w * SK.SAMPLE:
            last_chats.append((cust, {oid: order}, msgs))
    empty_errors = sum(1 for c, o, m in last_chats
                       if SK.learning_bot({}, c, o, m) != SK.RP.decide(c, o, m))
    trained_errors = sum(1 for c, o, m in last_chats
                         if SK.learning_bot(skill, c, o, m) != SK.RP.decide(c, o, m))
    checks.append((f"skill is causal (empty-skill remakes {empty_errors} errors the "
                   f"trained skill avoids: trained={trained_errors})",
                   empty_errors > 0 and trained_errors == 0))

    # 6. determinism
    per2, skill2, _ = SK.run()
    checks.append(("deterministic (re-run identical)",
                   per2 == per and sorted(skill2) == sorted(skill)))

    ok = all(p for _, p in checks)
    for label, p in checks:
        print(f"  [{'PASS' if p else 'FAIL'}] {label}")
    print("SKILL-ENRICHMENT TEST:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
