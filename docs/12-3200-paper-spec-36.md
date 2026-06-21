# 12-3200-paper-spec-36 — paper-impl loop, circle 36: introduce D as a fourth executable instance

STATUS: DONE
Resolves the 3-vs-4 inconsistency flagged in circle 35 by introducing D (the Rocq
deductive use case) as the FOURTH executable instance. Framing: three terrain
archetypes UNCHANGED; four executable instances, with A and D both on the
transcription terrain (English -> formal logic).

## Changes
- New generator verify/results_d.py -> tex/macros/results_d.tex (reads the committed
  src/D/evidence/results.json; no kernel needed): ResDSeededDefects 2,
  ResDDefectsCaught 2, ResDBarrierOff 0, ResDClauses 3, ResDDetectionPct 100%.
  Preamble \input added; results_d.py added to src/paper/_paperlib generators
  (NOT D's measure_squeeze.py, which needs the kernel and would clobber the
  committed real results.json).
- verify/synthesis.py: TERRAINS += D (key-mapped to D's Rocq field names); ResNTerrains
  now 4 (instances), ResNArchetypes pinned to 3 (taxonomy). Aggregate now
  15/15 caught on, 0 off across four instances.
- verify/reflexive_measures.py: count_terrains() includes D -> ResReflexTerrains 4.
- Manuscript:
  - new subsection sec:caseG "A fourth instance, deductively: formal proofs in Rocq"
    (the deductive transcription instance; Rocq kernel lower bound; textbook manifest
    upper bound; formalizer/prover/exerciser; axiom audit; 2/2 on, 0/2 off).
  - synthesis prose + table extended to four instances (D column; coupling = n/a,
    deductive); soundness-gate paragraph gains D's axiom-audit gate ("per instance").
  - all "three executable instances" -> "four" EXCEPT the two coupling-specific
    mentions, which become "three text-producing instances" (D has no text coupling).
  - "three terrain archetypes" kept (taxonomy unchanged).
  - abstract instance list + the section ranges (caseD--caseF -> caseD--caseG) updated.
- Ledger: CLM-074 RESULT (D's squeeze result, src/D/evidence/results.json). RESULT 25 -> 26.

## Gates
- Gate B: build green (21pp), all cites/refs/macros resolve, no bibtex warnings;
  zero remaining "three executable instances".
- Gate C: ledger 46 CITE + 26 RESULT == regenerated reflexive macros; synthesis
  aggregate 15/15 on, 0 off; results_d/synthesis/reflexive re-run byte-identical.

## Note
Coupling and Figure 2 remain the three text-producing instances (A/B/C) -- the
deductive instance's independence is enforced by the axiom audit, not measured as
text overlap; stated explicitly. D shares archetype A (transcription), so the
three-archetype taxonomy and Table 1 are unchanged.
