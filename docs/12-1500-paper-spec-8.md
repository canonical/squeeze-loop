# 12-1500-paper-spec-8 — paper-impl loop, circle 8: synthesis of the three terrains

STATUS: DONE
Draw the three executable instances together into one synthesis, making the
paper's central structural claim — invariant topology, materials rebuilt per
terrain — measurable across all three archetypes.

## E-item — aggregate, recomputably
- Extended `verify/coupling_measure.py` to include terrain C (test_matrix.json vs
  main.py): coupling now A 2.6%, B 0.7%, C 1.4% (all low) -> tex/macros/coupling.tex.
- New `verify/synthesis.py`: reads src/{A,B,C}/evidence/results.json and emits the
  cross-terrain aggregate -> tex/macros/synthesis.tex (\ResNTerrains=3,
  \ResNArchetypes=3, \ResAllSeeded=13, \ResAllCaught=13, \ResAllBarrierOff=0).
  Totals recompute; not hand-summed.

## W-item — manuscript
- New §\ref{sec:synthesis} "Synthesis: one topology, three materials" + a
  comparison table (Table~\ref{tab:synthesis}) of the three executable instances:
  use case, what each bound is made of, dominant failure, seeded caught (on/off),
  evidence-implementation coupling. Every cell is an existing per-terrain macro;
  aggregate totals from synthesis.py.
- Conclusion: one clause noting the three executable instances demonstrate the
  portable core measurably (13/13 caught barrier-on, 0/13 off).
- Ledger: CLM-051 updated (coupling now incl. C), CLM-054 (synthesis aggregate).

## L-item
None. The synthesis is internal (the cross-terrain generalisation is the paper's
own claim); no external source needed, none invented (would be F1).

## Gates
- Gate B: build green (20 pp), all cites/refs/macros resolve, no bibtex warnings.
- Evidence: coupling_measure.py + synthesis.py re-run cleanly; synthesis exits 0
  (on==seeded, off==0 across all terrains).

## Honest scope
The synthesis aggregates three constructed, deterministic instances (n=3, one per
archetype); it is generalisation across terrains in kind, still not the
controlled, cross-model, matched-difficulty study (§\ref{sec:eval}).

## Open questions for the next circle
1. The controlled comparative study remains the one genuine future gap.
2. The reflexive section (§6) could now reference the completed three-terrain
   synthesis as additional self-application evidence.
