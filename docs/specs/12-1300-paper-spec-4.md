# 12-1300-paper-spec-4 — paper-impl loop, circle 4: the reflexive case study

STATUS: DONE
The strategy applied to the production of this paper itself, now that the loop
has logged enough circles (lit verification, evidence circles 2-3) to report.

## E-item — reflexive measures, recomputable

- `verify/manuscript_defects.tsv`: the auditable list of coherent-and-wrong /
  over-claim defects the gates caught in the manuscript's OWN claims (7: 4 on the
  literature plane, 3 on the evidence plane), each F-coded and sourced to a gap
  doc / verification report. Metadata-only fixes (e.g. baudin_acsl year) are
  excluded — they are not coherent-and-wrong claims.
- `verify/reflexive_measures.py`: counts the loop's self-application artifacts
  from the repo (defects, reading records + access level, ledger CITE/RESULT
  rows, spec/gap docs) and emits `tex/macros/reflexive.tex`. So the reflexive
  numbers recompute like every other paper number.

Measured: 7 own-claim defects (4 lit, 3 evidence); 42 reading records, 40 read
in full; 39 CITE + (after this circle) 8 RESULT ledger rows; 3 spec docs, 2 gap
docs.

## W-item — manuscript

- New Section~\ref{sec:reflexive} "The Reflexive Case Study: This Paper as a
  Squeeze Loop", all counts via `\ResReflex*` macros. Honest framing: n=1, a
  single authoring team is not independent of itself; the gate's independence was
  only approximated (verifying pass separated from writing pass; one defect — the
  false LXC/execution-environment claim — was caught only by an external
  challenge). Reported as a mechanism illustration, not a controlled result.
- `\IfFileExists{macros/reflexive.tex}` input added to the preamble.
- Ledger CLM-046, CLM-047 (RESULT, bound to the reflexive artifacts).

## L-item — new bibliography question

None required. The conceptual content (an evaluator anchored to its own work
loses detection power) is already covered by the self-evaluation literature in
§2.2 (panickssery2024llm, huang2023cannot) and the oracle problem
(barr2015oracle, added circle 3). No source was invented to decorate the section
(that would itself be F1).

## Gates

- Gate B: build green; all cites/refs/macros resolve; no bibtex warnings.
- Evidence: `reflexive_measures.py` re-run reproduces `reflexive.tex`; macro
  values consistent with the repo state at commit time.

## Open questions for the next circle

1. H2 effect size under partial coupling at matched difficulty — still the
   controlled study (future).
2. `src/B` as a second executable terrain (instance vs. archetype) — now unblocked
   by the user's "make progress first" instruction having been met across circles
   2-4.
3. The reflexive section's independence is approximated, not real; a cross-model
   or cross-author verifier would strengthen it (ties to the H2 independence
   measures in §\ref{sec:eval}).
