# Naive vs intended (A's fork)

**Definition.** The pairing, per metric task, of the **naive** reading (the obvious SQL
that looks right but is wrong on a subtle metric) against the **intended** reading (the
handbook-correct one). A's instance of the *separable fork* — the wrong-vs-correct pair
the squeeze must tell apart (the paper's "richness = number of separable forks" category,
[reflexive-monitors](../../../../docs/glossary/reflexive-monitors.md)).

This is where *coherent-and-wrong* lives in A: the naive query runs, returns a plausible
number, and passes its own sanity checks while diverging from the intended value (e.g.
counting gross instead of net by omitting the refund subtraction). The exerciser's
validation matrix catches the divergence; the skill loop consolidates the lesson.

## Sources

- `src/A/diversity/pool.py` — each task pairs `naive` and `intended` readings.
- `src/A/in-band-deliverable/runner/mutations.py` — the clause-violating variants (one
  dropped obligation each) that make a fork numerically separable.
- `src/A/in-band-deliverable/exerciser/build_validation_matrix.py` — names which mutation
  must diverge for each clause.

## See also

- [metric-handbook](metric-handbook.md) — the authority that says which reading is intended.
- [diversity-pool](diversity-pool.md) — the gallery of such forks.
- [squeeze-loop](../../../../docs/glossary/squeeze-loop.md) — coherent-and-wrong is the
  failure the squeeze targets.
