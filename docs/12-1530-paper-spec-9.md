# 12-1530-paper-spec-9 — paper-impl loop, circle 9: reflexive three-terrain evidence

STATUS: DONE
Extend the reflexive case study (§\ref{sec:reflexive}) with the three-terrain
evidence: the loop's self-application spans not only the manuscript's prose
(citations) but its evidence base — the three executable instances it produced
and verified under the same barriers and gates.

## E-item
- `verify/reflexive_measures.py` extended with `count_terrains()` (executable
  instances with an evidence/results.json: A, B, C) -> new macro
  `\ResReflexTerrains`. Re-run regenerates tex/macros/reflexive.tex; the
  spec-doc count (`\ResReflexSpecDocs`) auto-updates to include this circle.

## W-item
- §\ref{sec:reflexive}: the lower bound updated from "the executable instance of
  §\ref{sec:caseD}" to the \ResReflexTerrains{} executable instances of
  §\ref{sec:caseD}--§\ref{sec:caseF}; a new sentence records that the loop
  produced and verified those instances under the strategy itself --- across them
  the gates caught \ResAllCaught/\ResAllSeeded{} seeded coherent-and-wrong
  implementers and \ResAllBarrierOff{} with the barrier off (§\ref{sec:synthesis})
  --- so the self-application covers the evidence base, not just the prose.
- Ledger CLM-055 (RESULT, reflexive three-terrain self-application).

## L-item
None. Internal self-application; no external source (none invented; F1 guard).

## Gates
- Gate B: build green; all cites/refs/macros resolve; no bibtex warnings.
- Evidence: reflexive_measures.py re-run reproduces reflexive.tex; macro values
  consistent with the repo state.

## Honest scope
Still n=1 reflexive instance (this paper), now citing its own three-terrain
evidence base; the independence remains approximated (verifying pass separated
from writing pass), not the controlled study.

## Open questions for the next circle
1. The controlled, cross-model, matched-difficulty study remains the future gap.
