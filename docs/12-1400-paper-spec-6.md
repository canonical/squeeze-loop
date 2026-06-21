# 12-1400-paper-spec-6 — paper-impl loop, circle 6: discharge the coupling first-cut

STATUS: DONE
"Do 1" = make honest progress on the controlled study (effect size under partial
coupling). Scope decision, stated plainly:

- A genuine H1-H4 controlled study needs real LLM runs, baselines, and statistics
  — out of reach here; it stays future work.
- A deterministic *partial-coupling sweep* would be TAUTOLOGICAL (detection
  = 1 - coupling by construction). Presenting that as a finding would itself be a
  coherent-and-wrong move — exactly what the strategy forbids — so it was NOT done.
- What IS honest and available: discharge one of §6's own proposed measures. The
  section already says "naive n-gram overlap is probably sufficient as a first
  cut" for evidence--implementation coupling. We implemented and ran that.

## E-item — `verify/coupling_measure.py`
Token-bigram Jaccard overlap between the exerciser's acceptance evidence and the
implementer's code, on the REAL (barrier-on, physically isolated) artifacts of
both terrains. Emits `tex/macros/coupling.tex` (\ResCouplingA, \ResCouplingB).

Measured: A = 2.6%, B = 0.7%. The independently authored artifacts are weakly
coupled to the implementation while still catching every seeded defect — a real,
non-tautological instance of H2's predicted relationship. Barrier-off coupling is
not "measured": an anchored exerciser embeds the implementation by construction
(coupling -> maximal) and, per the ablation, catches none.

## W-item — manuscript
- §6 eval: the evidence--implementation coupling TODO replaced with the measured
  n-gram first cut (A 2.6%, B 0.7%) + honest note that the embedding estimator,
  MI proxies, and the continuous matched-difficulty / cross-model estimate remain
  future. One eval TODO discharged.
- `\input{macros/coupling}` added; ledger CLM-051 (RESULT bound to the measure).
- Build green, 19 pp.

## L-item
None. The coupling/oracle concepts are already covered (barr2015oracle,
panickssery2024llm). No source invented (would be F1).

## Honest status of "the controlled study"
Still future. This circle discharges the *first-cut coupling measure* on the two
worked instances; it does not provide the comparative, matched-difficulty,
cross-model effect size, which requires model access and a baseline configuration.

## Open questions for the next circle
1. The embedding-based coupling estimator + the cross-model self-preference
   replication (§6) still need model access.
2. A third executable terrain (split planes, Archetype C) would complete archetype
   coverage.
