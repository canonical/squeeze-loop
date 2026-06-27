# 12-3600-paper-spec-40 — paper-impl loop, circle 40: polish the introduction

STATUS: APPROVED
Polish that fixes a residual F6 self-inconsistency. Circle 36 introduced D as the
FOURTH executable instance (sec:caseG) and updated the abstract, synthesis,
reflexive, and conclusion to "four executable instances over three archetypes" --
but two spots in the introduction were missed and still say "three": the narrative
instantiation paragraph (it says "three executable, reproducible squeezes ... three
different epistemic terrains") and contribution (iii) (it cites the range
Sections~\ref{sec:caseD}--\ref{sec:caseF}, stopping one short of caseG). Bring both
into line with the rest of the paper. Restatement of body-SUPPORTED counts
(ResNTerrains 4, ResNArchetypes 3) and a valid cross-ref (sec:caseG exists); no new
claim, number, citation, or macro.

## Changes
- tex/paper.tex intro narrative paragraph (~line 154): "three executable,
  reproducible squeezes that occupy three different epistemic terrains" ->
  "four executable, reproducible instances over three different epistemic
  terrains", noting the transcription terrain carries two of them (tabular
  analytics + machine-checked proofs), mirroring the abstract's framing.
- tex/paper.tex contribution (iii) (~line 171-174): three archetypes "each
  instantiated as one or more executable, reproducible squeezes -- four instances
  in all"; fix the section range \ref{sec:caseD}--\ref{sec:caseF} ->
  \ref{sec:caseD}--\ref{sec:caseG}.
- Regenerate reflexive.tex (ResReflexSpecDocs 39->40 for this new spec doc).

## Gates
- Gate B: build green; no new \res macro, number, \cite, or CLM; the caseG ref
  resolves (label exists); previously-SUPPORTED text byte-stable outside the two
  intro hunks; zero remaining "three executable" instance-count mentions.
- Gate C: ledger unchanged (CITE 46 + RESULT 28); reflexive macros reconcile;
  reflexive re-run byte-identical.

## Note
This is an accuracy fix, not new content: the counts (4 instances, 3 archetypes)
and the caseG instance are already SUPPORTED in the body (synthesis, sec:caseG).
The intro merely stops contradicting them.
