# 12-3500-paper-spec-39 — paper-impl loop, circle 39: polish the abstract

STATUS: APPROVED
Polish only, under the abstract rule (may only weaken or restate sentences already
SUPPORTED in the body; a compression that strengthens is forbidden). The abstract's
generativity sentence is slightly muddled ("Applied to the production of this paper
itself ... squeezing an agent ... forces it to invent new distinctions") and, since
circle 37, incomplete: the generativity finding now has TWO body-SUPPORTED
witnesses -- the paper's self-application (sec:reflexive) and the squeezed agents'
skill accumulation (sec:eval, CLM-075). Restructure into two crisp sentences:
(1) the generativity finding with both witnesses, (2) the strange-loop scoping tied
specifically to the self-applying construction. No new claim, number, citation, or
macro; restatement of body-SUPPORTED material only.

## Changes
- tex/paper.tex abstract: replace the final generativity/strange-loop sentence
  (lines ~90-95) with two sentences -- generativity shown both in the paper's
  construction and in the squeezed agents (skill bases enrich across cycles,
  Section~\ref{sec:eval}); strange-loop form scoped to the self-applying
  construction (Section~\ref{sec:reflexive}), structural not phenomenal. The
  strange-loop clause stays tied to the paper's self-application (the agent skill
  loops are NOT claimed to be strange loops). Refs sec:eval and sec:reflexive both
  already appear in the abstract.
- Regenerate reflexive.tex (ResReflexSpecDocs 38->39 for this new spec doc).

## Gates
- Gate B: build green; abstract introduces no \res macro, no number, no new \cite,
  no new CLM; previously-SUPPORTED body text byte-stable (only the abstract hunk
  changes); the new abstract sentences restate body-SUPPORTED claims and do not
  strengthen any existing abstract claim.
- Gate C: ledger unchanged (CITE 46 + RESULT 28); reflexive macros reconcile;
  reflexive re-run byte-identical.

## Note
Honesty guard: the abstract restates "skill bases enrich across cycles" (true of
the programmatic learners, = CLM-075); the body carries the programmatic-not-live
caveat. The strange-loop claim is NOT extended to the agent skill loops -- only the
paper's self-applying construction bears it, exactly as in the body.
