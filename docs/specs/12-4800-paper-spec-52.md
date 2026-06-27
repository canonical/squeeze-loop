# 12-4800-paper-spec-52 — paper-impl loop, circle 52: polish the case study sections

STATUS: APPROVED
Polish of the case-study subsections (sec:caseD--sec:caseG). They are parallel and
macro-bound (no hand-typed numbers); the one residual one-instance-per-archetype
seam from circle 36's append-D approach is in sec:caseF (the third instance, C),
which closes "all three archetypes of Section~\ref{sec:archetypes} now have AN
executable instance" -- implying exactly one per archetype. After D (sec:caseG) the
transcription archetype has TWO instances (A and D). This is the same implication
fixed in the intro (circle 40) and the archetypes table (circle 43). Minimal,
honest fix: "an executable instance" -> "at least one executable instance".

## Changes
- tex/paper.tex sec:caseF (~line 718): "all three archetypes of
  Section~\ref{sec:archetypes} now have an executable instance" -> "... now have at
  least one executable instance". (Still completes the three-archetype coverage; now
  forward-consistent with caseG adding a second transcription instance.)
- Regenerate reflexive.tex (ResReflexSpecDocs 51->52 for this new spec doc).

## Gates
- Gate B: build green; no new \cite/number/macro/CLM; previously-SUPPORTED text
  byte-stable outside the one phrase; refs unaffected.
- Gate C: ledger unchanged (CITE 46 + RESULT 28); reflexive macros reconcile;
  reflexive re-run byte-identical.

## Note
Accuracy/consistency fix only. The three-archetype taxonomy is unchanged; "at least
one" reflects that transcription carries two instances (A analytics + D deductive),
matching ResNTerrains 4 / ResNArchetypes 3 and the rest of the paper.
