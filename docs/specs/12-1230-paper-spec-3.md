# 12-1230-paper-spec-3 — paper-impl loop, circle 3: the barrier ablation (H2)

STATUS: DONE
Same mapping as circle 2: upper bound = bibliography; lower bound = `src/A/`.
Goal of this circle (from circle 2's open questions): turn the Use-Case-A evidence
from *feasibility* toward *comparative* by measuring the strategy's defining
ablation — the physical barrier (C3) on vs off.

## E-item — barrier on/off ablation in the harness

Extended `src/A/evidence/measure_squeeze.py`. For each of the
\ResAblationSeeded=5 seeded coherent-and-wrong implementers (the clause-violating
mutations), the exerciser's verdict depends on where its oracle comes from:
- **barrier ON** — oracle = the handbook (upper bound): expected = correct value.
- **barrier OFF** — the exerciser has seen the implementation and anchors to it:
  expected = the (wrong) implementation's own output.

Result (deterministic, byte-identical on re-run):
- barrier on: **5/5** seeded defects caught.
- barrier off: **0/5** — the oracle degenerates to the implementation, so no
  implementation error is detectable.

New generated macros: `\ResAblationSeeded`, `\ResAblationBarrierOn`,
`\ResAblationBarrierOff`. (Also fixed a harness gating bug: the pass/fail check
was keyed on the `_caught` suffix and wrongly treated the expected
`ablation_barrier_off_caught=0` as a failure; gate is now an explicit key list.)

## L-item — new question → bibliography

The barrier-off failure is precisely the loss of an *independent oracle*. Added
and verified (FULL read) `barr2015oracle` — Barr et al., "The Oracle Problem in
Software Testing: A Survey" (IEEE TSE 2015): the squeeze loop's upper bound is a
*specified oracle* authored independently of the implementation; removing the
barrier collapses the exerciser toward the survey's *no-independent-oracle*
regime. Cited in §\ref{sec:caseD}. Also upgraded `jia2011analysis` from SECONDARY
to **FULL** via the authors' CREST copy (verbatim kill / mutation-score
definitions now in its record). CLM-044; CLM-037 note updated.

## W-item — manuscript

- §\ref{sec:caseD}: new ablation paragraph (barrier on \ResAblationBarrierOn/5
  vs off \ResAblationBarrierOff/5), citing `barr2015oracle` and connecting to the
  self-evaluation effects of §2.2 (`panickssery2024llm`, `huang2023cannot`) and
  to H2; framed as the extreme of barrier-off, with effect size left to §6.
- §6 data-point sentence updated to include the single-instance ablation;
  "no baseline" softened to "no matched-difficulty baseline".
- Ledger CLM-044 (CITE), CLM-045 (RESULT, bound to results.json#ablation).

## Gates

- Gate B: build green (18 pp), all cites/refs/macros resolve, no bibtex warnings.
- Evidence: results.json byte-identical on re-run; macros consistent. See
  `verify/reports/usecaseA-evidence-2026-06-12.md` (ablation section).

## Open questions for the next circle

1. The ablation is the *extreme* barrier-off (full anchoring) on one instance.
   The honest gap to H2 is effect size under *partial* coupling and matched
   difficulty — still the controlled study, still future.
2. A second executable terrain (`src/B`) would settle the instance-vs-archetype
   taxonomy question and give a second data point — deferred by request until the
   paper-impl loop has made more progress here.
3. The reflexive case study (this paper's own loop) now has three circles logged
   (spec-2, spec-3 + the literature/evidence verifications); approaching enough
   to write up as a short section.
