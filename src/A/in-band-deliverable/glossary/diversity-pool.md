# Diversity pool (A's varying trial)

**Definition.** A gallery of 100 metric tasks of graded subtlety (simple → subtle), each a
[naive-vs-intended](naive-vs-intended.md) pair, over which a learner is sampled across
seeded cycles so its error rate is a *real, varying trial* rather than a fixed point. A's
instance of "diversity restores the trial"
([reflexive-monitors](../../../../docs/glossary/reflexive-monitors.md), CAT-3).

Random sampling per cycle (seeded `base + cycle`) makes the measured error rate vary; as
the skill loop consolidates learned skills over metric families, the rate falls from 1.0
toward 0. Because it samples across seeds, the result is the kind the perturbation gate
re-runs at different seeds rather than trusting one draw.

## Sources

- `src/A/diversity/pool.py` — the 100 tasks (simple/subtle), by metric family.
- `src/A/diversity/run_diversity.py` — the seeded sampling harness.
- `src/A/skill/skill_loop.py`, `src/A/skill/README.md` — the skill accumulation it measures.

## See also

- [naive-vs-intended](naive-vs-intended.md) — what each pool task is.
- [ground-truth](../../../../docs/glossary/ground-truth.md) — diversity re-runs against
  the oracle at varying seeds.
- [reflexive-monitors](../../../../docs/glossary/reflexive-monitors.md) — the over-reach
  audit checks "diversity restores the trial" generalises across instances.
