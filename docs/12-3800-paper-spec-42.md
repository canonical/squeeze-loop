# 12-3800-paper-spec-42 — paper-impl loop, circle 42: polish the strategy section

STATUS: APPROVED
Polish of sec:strategy. The section is the conceptual core and already tight
(Def 1 squeeze, the hard/soft-truth remark, C1-C4 compliance, the cast table, loop
mechanics + gates, the disjointness operationalization). The one coherence gap: the
section's closing list in sec:disjoint walks each actor's failure being caught by
another -- a prose instantiation of compliance condition (C2) catchability -- and
ends "Correctness is the fixed point satisfying all squeezes at once", but points
to neither the formal condition it instantiates nor the section that measures it.
Add a forward pointer tying the closing claim to (C2) and to sec:synthesis, where
catchability is made measurable (every seeded coherent-and-wrong implementer caught
barrier-on, none off). Pure restatement/cross-reference of body-SUPPORTED material.

## Changes
- tex/paper.tex, end of sec:disjoint (~line 528-529): extend the closing sentence
  "Correctness is the fixed point satisfying all squeezes at once." with a clause
  naming compliance condition (C2) and forward-pointing to Section~\ref{sec:synthesis}
  (catchability made measurable rather than merely asserted). No number restated
  inline (the figures live in synthesis under macros); plain "(C2)" text matches the
  paper's existing "(C1)" usage (lines 398, 516).
- Regenerate reflexive.tex (ResReflexSpecDocs 41->42 for this new spec doc).

## Gates
- Gate B: build green; no new \cite, number, macro, or CLM; sec:synthesis ref
  resolves; previously-SUPPORTED text byte-stable outside the one sec:disjoint hunk.
- Gate C: ledger unchanged (CITE 46 + RESULT 28); reflexive macros reconcile;
  reflexive re-run byte-identical.

## Note
This connects the conceptual section to its formal compliance condition and its
evidence without adding a claim: (C2) is defined in def:compliance, and
sec:synthesis already SUPPORTS the catchability result. No new number is typed
(synthesis keeps the macro-bound figures).
