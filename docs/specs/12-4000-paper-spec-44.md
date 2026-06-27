# 12-4000-paper-spec-44 — paper-impl loop, circle 44: polish the stabilizers section

STATUS: APPROVED
Polish of sec:stabilizers. One residual F6 stale-count gap left by circle 36 (which
made D a fourth executable instance): the section opener still says "The three
instances converged on [13] rules that block collapse", while the abstract, intro,
archetypes, synthesis, and conclusion all say "four executable instances". The
stabilizers list already spans all four archetypes including D -- rule 4 names
"standing proof counts" (D's Rocq standing invariant) and rule 13 is the
authored-authority independence the caseG deductive instance invokes (axiom audit
as the soundness argument). So "four" is the accurate, consistent count.

## Changes
- tex/paper.tex sec:stabilizers opener (~line 862): "The three instances converged
  on \ref{item:laststab}~rules that block collapse structurally" -> "The four
  executable instances converged on \ref{item:laststab}~rules that block collapse
  structurally". (\ref{item:laststab} renders 13; unchanged.)
- Regenerate reflexive.tex (ResReflexSpecDocs 43->44 for this new spec doc).

## Gates
- Gate B: build green; no new \cite, number, macro, or CLM; \ref{item:laststab}
  still resolves to 13; previously-SUPPORTED text byte-stable outside the one
  opener hunk; zero remaining "three instances" count in the section.
- Gate C: ledger unchanged (CITE 46 + RESULT 28); reflexive macros reconcile;
  reflexive re-run byte-identical.

## Note
Accuracy/consistency fix only -- restates the body-SUPPORTED instance count
(ResNTerrains 4). The 13 stabilizers and tab:collapse are unchanged; the list
already encompasses the deductive instance (rules 4 and 13), so attributing the
convergence to all four instances is faithful, not an overclaim.
