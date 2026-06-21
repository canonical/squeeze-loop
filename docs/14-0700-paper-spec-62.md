# 14-0700-paper-spec-62 — paper-impl loop, circle 62: discharge O2 (level-crossing log)

STATUS: APPROVED
Circle A of 14-0649-plan.md. Move clause O2 of paper_upper_bound.md from CANDIDATE
to discharged with a first-class, recomputable level-crossing log. Today
ResLoopLevelCrossings is a raw count of manuscript_defects.tsv (8) -- conflating
"defects the gates caught" with "downward-causation events". Replace it with a log
of only genuine self-representation -> substrate-change chains, and exhibit the
canonical endogenous chain as the O2 witness. Honest outcome: the count drops 8 ->
3 (loud-fail; report the true number).

## Changes
1. New artifact claims/level_crossings.tsv -- columns id, cycle,
   high_level_representation, gate, substrate_change, evidence. Three genuinely
   traceable events:
   - LX-1 (endogenous, recurring): the loop's own regenerated self-counts ->
     reconciliation gate flags drift -> tex/macros/reflexive.tex rewritten.
   - LX-2: the paper's self-description ("three executable instances") ->
     F6 self-consistency check -> edits across intro/archetypes/stabilizers/
     synthesis/caseF (circles 40/43/44/51/52).
   - LX-3: a claim that the gates are machine-checked -> external review (review1)
     -> Figure 1 caption + sec:mechanics gate descriptions edited (D8).
2. verify/strange_loop.py: source ResLoopLevelCrossings from level_crossings.tsv
   (count LX- rows) instead of manuscript_defects.tsv; update docstring.
   ResLoopLevelCrossings 8 -> 3.
3. sec:reflexive: reword the one level-crossing sentence to name the canonical
   ENDOGENOUS O2 chain (self-count -> reconciliation gate -> reflexive.tex) and cite
   the log -- the loop crossing its own levels, not an external catch.
4. claims/ledger.tsv: CLM-077 RESULT (O2 discharge, bound to
   claims/level_crossings.tsv). RESULT 28 -> 29; ResReflexResultRows 28 -> 29.

## Scope discipline (from the plan)
O2 discharge grounds the Tier-2 claim the paper already makes (ladder defines Tier 2
= O2+O3 discharged, O1/O4/O5 not). It advances NOTHING toward Tier 1 (O1/O5 still
PARTIAL). CLM-073 stays OPN at Tier 2. Tier 0 / NOT-claims untouched. Loud-fail: the
count is the honest 3, not the old 8.

## Gates
- Gate B: build green; ResLoopLevelCrossings still used (no orphan); no hand-typed
  number; previously-SUPPORTED text byte-stable outside the planned hunks.
- Gate C: ledger CITE 46 + RESULT 29 == regenerated reflexive macros; strange_loop +
  reflexive_measures re-run byte-identical.

## Note
O3 (closure) and the §8 refresh are Circles B and C (separate). manuscript_defects.tsv
remains the source for the 8-defect self-audit (ResReflexDefects) -- only the O2
source changes.
