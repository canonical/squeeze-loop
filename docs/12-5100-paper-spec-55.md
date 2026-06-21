# 12-5100-paper-spec-55 — paper-impl loop, circle 55: reframe the introduction (review2 #2/#5)

STATUS: APPROVED
Second review2 circle. Reviewer #2: state plainly and EARLY that this is a
methods/architecture paper presenting a pattern + existence demonstrations, with the
comparison deferred. Reviewer #5: skill accumulation is over-framed; demote it.

## Changes (tex/paper.tex introduction)
1. Lead paragraph (after "...report every number from a re-runnable harness
   (Section~\ref{sec:archetypes})."): add a positioning sentence -- this is a
   methods paper contributing the pattern and four existence demonstrations that the
   squeeze instantiates end-to-end on each terrain; a controlled comparison against
   alternative pipelines is deferred (Section~\ref{sec:eval}), the natural-bug route
   having met a near-zero implementer error rate.
2. Contribution (vii): demote skill from a co-equal "measurably enriches ...
   finding" to a deterministic MECHANISM DEMONSTRATION. Replace "and exhibited again
   in the squeezed agents, where a caught-then-consolidate loop measurably enriches
   each instance's skill base across cycles (Section~\ref{sec:eval}, with the caveat
   ...)" with "; a deterministic mechanism demonstration exhibits the same
   caught-then-consolidate move in the squeezed agents (Section~\ref{sec:eval})".

## Gates
- Gate B: build green; no new \cite/number/macro/CLM; refs resolve; previously-
  SUPPORTED text byte-stable outside the two intro hunks; positioning sentence
  restates body-SUPPORTED scope (sec:eval, existence demonstrations).
- Gate C: ledger unchanged (CITE 46 + RESULT 28); reflexive macros reconcile;
  reflexive re-run byte-identical.

## Note
Safe direction: the positioning weakens the paper's implied empirical scope (pattern
+ existence demonstrations, comparison deferred), and (vii) relabels skill as a
mechanism demonstration rather than a learning finding -- matching the abstract
(circle 54) and the user's decision.
