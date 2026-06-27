# 14-0730-paper-spec-63 — paper-impl loop, circle 63: discharge O3 (closure check)

STATUS: APPROVED
Circle B of 14-0649-plan.md. Move clause O3 of paper_upper_bound.md from CANDIDATE
to discharged by EXECUTING the traversal (not asserting it): a closure check that
verifies the regenerated self-record returns to origin (output re-enters input),
plus a closed-cycle diagram, plus a ledger RESULT row.

## Changes
1. New verify/closure_check.py: executes one full traversal and asserts
   return-to-origin --- (a) reflexive.tex is a REGENERATION FIXED POINT (re-running
   verify/reflexive_measures.py leaves it byte-identical), and (b) its
   ResReflexCiteRows/ResReflexResultRows equal the ledger CITE/RESULT counts the
   next circle reads. Emits tex/macros/closure.tex with ResLoopClosure = number of
   ledger-reconciled self-counts that round-trip (2: citation + result rows). Exits
   nonzero (loud-fail) if the cycle is not a fixed point or the counts diverge --
   then O3 stays CANDIDATE.
2. Preamble: \input{macros/closure}. _paperlib GENERATORS: add closure_check.py
   (after reflexive_measures.py). execute_squeeze.py STEPS: add closure_check.py so
   closure is executed every circle in the reflexive squeeze.
3. sec:reflexive: add a compact closed-cycle figure (fig:closure) and a sentence
   naming closure_check.py as the executed O3 witness (the regenerated self-record
   is a fixed point; its ResLoopClosure self-counts re-enter the ledger).
4. claims/ledger.tsv: CLM-078 RESULT (O3 discharge, bound to verify/closure_check.py
   + fig:closure). RESULT 29 -> 30; ResReflexResultRows 29 -> 30.

## Scope discipline
With O2 (circle 62) and O3 now discharged, the Tier-2 claim is fully grounded
(ladder: Tier 2 = O2+O3 discharged, O1/O4/O5 not). This advances NOTHING toward
Tier 1 (O1/O5 still PARTIAL -- no live self-model). CLM-073 stays OPN at Tier 2;
Tier 0 / NOT-claims untouched. (§8 refresh is Circle C.)

## Gates
- Gate B: build green; ResLoopClosure used (no orphan); closure.tex \input resolves;
  no hand-typed number; previously-SUPPORTED text byte-stable outside planned hunks.
- Gate C: ledger CITE 46 + RESULT 30 == regenerated reflexive macros; closure_check
  passes (fixed point + counts match); strange_loop/reflexive/closure re-run
  byte-identical.

## Note
closure_check.py regenerates reflexive.tex as its fixed-point probe; because
reflexive_measures is deterministic and current, this is a no-op rewrite (that
no-op IS the closure evidence). Order it after reflexive_measures in GENERATORS.
