# 12-4700-paper-spec-51 — paper-impl loop, circle 51: polish the synthesis section (stale title count)

STATUS: APPROVED
Polish of sec:synthesis fixing a stale count in the SUBSECTION TITLE -- the last
holdover from the pre-D (three-instance) era. The title reads "Synthesis: one
topology, three materials", but the section now synthesizes FOUR executable
instances with four distinct material-sets (tab:synthesis is 4-column; the caption
and prose say "different materials"). "Three materials" also undersells D's
contribution: the transcription archetype is instantiated with two radically
different materials (signed SQL warehouse vs Rocq kernel). Bring the title in line
with the four-instance framing used throughout (after circles 40/43/44).

## Changes
- tex/paper.tex (line 750): subsection title "Synthesis: one topology, three
  materials" -> "Synthesis: one topology, four materials". The phrase appears only
  here; \ref{sec:synthesis} uses the number, so no cross-reference is affected.
- Regenerate reflexive.tex (ResReflexSpecDocs 50->51 for this new spec doc).

## Gates
- Gate B: build green; no new \cite/number/macro/CLM; section refs unaffected
  (numbered, not by title); previously-SUPPORTED text byte-stable outside the title;
  zero remaining "three materials".
- Gate C: ledger unchanged (CITE 46 + RESULT 28); reflexive macros reconcile;
  reflexive re-run byte-identical.

## Note
Accuracy/consistency fix: four instances, four material-sets (ResNTerrains 4),
matching the table, caption, and the rest of the paper. The three-archetype taxonomy
is unchanged and stated as such in the body ("two on the transcription terrain").
