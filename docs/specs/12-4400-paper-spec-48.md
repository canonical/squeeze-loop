# 12-4400-paper-spec-48 — paper-impl loop, circle 48: polish the limitations section

STATUS: APPROVED
Polish of sec:limitations that transcribes a NOT-claim the section was missing. The
methodology (paper-impl.md §5.7) makes the Limitations section the home of the
NOT-claims; since circle 37 the paper foregrounds the generativity / skill-
accumulation result (contribution vii, CLM-075/076) with an explicit honest scope
-- deterministic programmatic learners over fixed catalogs, NOT live models -- but
that caveat lives only in sec:eval and the conclusion, not in Limitations. Add a
limitation entry so the section is complete w.r.t. the paper's current claims.

## Changes
- tex/paper.tex sec:limitations: add one entry after "Provenance of the evidence"
  and before "Terminology":
    "Generativity is shown for programmatic learners, not live models." -- the
    squeeze's generativity (new distinctions in the paper itself; skill that
    accumulates in the squeezed agents, Section~\ref{sec:eval}) is established with
    deterministic programmatic learners over fixed catalogs, not live LLMs; a live
    model's learning curve, and how the deductive instance's deferred
    conceptual-leap wall is crossed, remain open.
- Regenerate reflexive.tex (ResReflexSpecDocs 47->48 for this new spec doc).

## Gates
- Gate B: build green; the entry restates the body-SUPPORTED caveat from sec:eval
  (CLM-075/076 carry it; CLM-070 OPN for the per-model gradient), no new
  cite/number/macro/CLM; sec:eval ref resolves; previously-SUPPORTED text
  byte-stable outside the inserted entry.
- Gate C: ledger unchanged (CITE 46 + RESULT 28); reflexive macros reconcile;
  reflexive re-run byte-identical.

## Note
NOT-claim transcription, not new content: the caveat already appears verbatim in
sec:eval's skill-accumulation paragraph and in the conclusion. Putting it in
Limitations is the section's stated job; it adds no claim the body has not already
discharged.
