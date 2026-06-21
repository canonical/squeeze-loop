# Tactic tiers (`lia` / `nia` / `wall`) — a capability rank

**Definition.** A rank that partitions D's exercise pool by the *minimal Rocq tactic that
solves each exercise*: `lia` (linear integer arithmetic), `nia` (nonlinear), or `wall`
(neither catalog tactic solves it — a real conceptual leap is required, and it is deferred).
The assignments are genuine kernel verdicts, cached in `d_tactic_tiers.json`.

> **Name-collision warning.** A "tactic tier" is a **capability/difficulty rank of a proof
> tactic**, *not* a rung of the admissibility
> [disposition ladder](../../../../docs/glossary/tier.md) (Tier 0–3). The disposition ladder
> grades *how strong a claim may be made*; the tactic tier grades *how hard an exercise is
> to discharge*. They share a word and nothing else — the paper's `tier` entry flags exactly
> this collision.

The `wall` set is the honest floor: D does not pretend a catalog tactic closes an exercise
that needs manual induction. The `solvable_miss` (a learner failed an exercise a catalog
tactic *would* solve) is kept distinct from `wall_hits` (the exercise was unsolvable by the
catalog) so the skill measure does not credit the learner for the wall.

## Sources

- `src/D/skill/d_tactic_tiers.json` — the cached `lia`/`nia`/`wall` assignments.
- `src/D/skill/precompute_tiers.py` — the solver (`solves()` tries `lia` then `nia`).
- `src/D/skill/README.md` — the skill design and the `wall` floor.

## See also

- [tier](../../../../docs/glossary/tier.md) — the *unrelated* disposition ladder this must
  not be confused with (the warning above).
- [rocq-kernel](rocq-kernel.md) — the oracle that decides each tactic-tier assignment.
