# 12-2200-paper-spec-22 — paper-impl loop, circle 22: polish the strategy section (+ engagement-residual cleanup)

STATUS: DONE
Editorial circle (no new evidence). Polish §sec:strategy and clean the residual
"engagement" vocabulary left by the circle-10 removal of the field engagements
(same defect class as the "engagement notes" fixed in circle 20).

## Audit of §sec:strategy
Definitions (Squeeze, Compliance C1-C4), the canonical-cast table, loop
mechanics / three gates, the pipeline figure, and the disjointness-operationally
subsection are all accurate and internally consistent -- kept. The only issue was
stale vocabulary.

## Changes (vocabulary consistency; no claim or number altered)
In-scope (strategy section):
- L479 "instantiated for the engagement" -> "instantiated for the case at hand".
- L498 "first act in a new engagement" -> "first act on a new instance".

Same-defect cleanup elsewhere (dangling references to the REMOVED field
engagements -- these were genuine contradictions, not just style):
- L704 "not argued from the field engagements alone" -> "not argued from
  narrative alone" (the field engagements no longer exist in the paper, so the
  contrast referenced nothing).
- L791 "The three engagements converged on thirteen rules" -> "The three
  instances converged ..." (the paper's three artifacts are executable instances).
- L895 "the same paired documents as the engineering engagements" -> "... as the
  engineering instances".

Deliberately KEPT:
- L999 "amortizes on engagements with long regression horizons" -- generic
  forward-looking usage (real-world projects in general), not a reference to the
  removed examples. Correct as is.

## Additivity
No new claim, no number altered. Pure terminology alignment to the post-circle-10
vocabulary ("instances", not "engagements"). One "engagement" remains by design.

## Gates
- Gate B: build green (18 pp), all cites/refs/macros resolve, no bibtex warnings.
- grep: exactly one "engagement" left (L999, intentional generic).
- No ledger change (prose-only).
