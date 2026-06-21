# 12-3900-paper-spec-43 — paper-impl loop, circle 43: polish the terrain archetypes section

STATUS: APPROVED
Polish of sec:archetypes that closes two residual F6 consistency gaps left by
circle 36 (which added D as a SECOND transcription instance, sec:caseG, sharing
archetype A). The rest of the paper -- abstract, intro (after circle 40),
synthesis table, conclusion -- says "four instances over three archetypes, two on
transcription", but sec:archetypes still reads as one-instance-per-archetype in two
spots:
  1. Lead paragraph: "We instantiate each [archetype] as an executable squeeze"
     (implies 3) while the section range is Sections caseD--caseG (4 sections).
  2. tab:archetypes "Executable instance" row maps archetype A to only "tabular
     analytics (caseD)", omitting that the deductive instance (caseG) is ALSO
     archetype A.
Both are accuracy fixes; the taxonomy stays three archetypes (table remains
3-column). Restatement of body-SUPPORTED structure (ResNTerrains 4, ResNArchetypes
3; caseG is transcription per its own subsection line "the same archetype as~A").

## Changes
- tex/paper.tex lead paragraph (~line 539-542): "We instantiate each as an
  executable, reproducible squeeze" -> "We instantiate them as four executable,
  reproducible squeezes --- the transcription terrain twice, on very different
  lower bounds --- each run as a coordinator--worker loop ...". Range caseD--caseG
  unchanged (already correct).
- tex/paper.tex tab:archetypes "Executable instance" row (~line 567), archetype A
  cell: "tabular analytics (\S\ref{sec:caseD})" -> "tabular analytics
  (\S\ref{sec:caseD}); also formal proofs (\S\ref{sec:caseG})".
- Regenerate reflexive.tex (ResReflexSpecDocs 42->43 for this new spec doc).

## Gates
- Gate B: build green; no new \cite, number, macro, or CLM; caseG ref resolves;
  previously-SUPPORTED text byte-stable outside the two sec:archetypes hunks;
  zero remaining one-instance-per-archetype phrasing in the section.
- Gate C: ledger unchanged (CITE 46 + RESULT 28); reflexive macros reconcile;
  reflexive re-run byte-identical.

## Note
Taxonomy unchanged: three archetypes (tab:archetypes stays 3-column). The fix only
makes the section acknowledge that archetype A carries two instances (analytics +
deductive proofs), exactly as the synthesis table, intro, abstract, and the caseG
subsection already do.
