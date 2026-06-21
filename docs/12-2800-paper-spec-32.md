# 12-2800-paper-spec-32 — paper-impl loop, circle 32: integrate the level-up findings

STATUS: DONE
Content circle. Integrates the level-up / diversity work (src/{A,B,C,D}/diversity,
the four level-up-*.md, level-up-synthesis.md, 10-cycles-after-level-up.md) into
the manuscript's evaluation section, with numbers that recompute and an OPN-typed
honest scope.

## Why
The reviewer's near-zero implementer error rate = a thin upper bound. The level-up
apparatus enriches the upper bound per terrain (a difficulty ladder + a 100-task
random pool) and shows that random sampling restores a real, varying trial. This
directly extends §sec:eval and quantifies the soft/hard remark from circle 31.

## Changes
- NEW generator verify/levelup_measures.py -> tex/macros/levelup.tex (reads the
  four src/*/diversity/diversity_results.json so the numbers recompute; no
  hand-typed figures). Preamble \input added.
- §sec:eval new paragraph "Enriching the upper bound": the thin-upper-bound
  diagnosis; the level-up apparatus across \ResLevelupTerrains{} terrains; the one
  detection primitive (re-derive intended, flag divergence); the soft-truth
  richness = number of separable forks; the whole-pool error surfaces
  (\ResLevelupDNotFound/\ResLevelupADiverge/\ResLevelupCBlend %); and that random
  sampling RESTORES the trial (fixed ladder byte-identical across
  \ResLevelupCycles cycles vs the pool's per-cycle variance \ResLevelupDMin--Max,
  up to \ResLevelupDistinctMax distinct outcomes).
- Honest scope: variance is TASK SAMPLING, not model stochasticity; a live-model
  per-drawn-task study is future work.
- Ledger: CLM-066..069 RESULT (the four diversity experiments, bound to their
  diversity_results.json artifacts), CLM-070 OPN (the per-model gradient -- built,
  not measured; the first OPN row in the ledger).

## Numbers (all macro-driven)
ResLevelupTerrains 4, Pool 100, Sample 20, Cycles 10; DNotFound 19, ADiverge 30,
CBlend 50; D per-cycle 14-20 solved; max distinct outcomes 7/10.

## Additivity
No prior claim altered. The deterministic-mechanism / honest-null story is
unchanged; this ADDS the level-up apparatus and explicitly marks its gradient claim
OPN (conjecture). Ledger: +4 RESULT (19->23), +1 OPN.

## Gates
- Gate B: build green, all cites/refs/macros resolve, no bibtex warnings.
- Gate C: ledger RESULT count (23) == regenerated ResReflexResultRows (23).
- Determinism: levelup_measures.py + reflexive_measures.py re-run byte-identical.

## Note
levelup_measures.py added to the reflexive instance's generator list
(src/paper/_paperlib.py GENERATORS) so the consistency pass regenerates it too.
