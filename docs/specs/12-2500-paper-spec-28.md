# 12-2500-paper-spec-28 — paper-impl loop, circle 28: full-paper consistency pass

STATUS: DONE
Gate-C over the whole manuscript, repeated after the section polish sweep
(circles 19-27). Verification circle; two real drifts found and fixed (both in the
claim ledger), everything else reproducible.

## Checks
1. Every number recomputes: re-ran all 12 generators; 12/12 macro files
   byte-identical (before the ledger edit). reflexive_measures.py determinism: OK.
2. Citations: 45 \cite keys, all with records + bib entries; ledger reconciled.
3. Internal consistency: build green, no undefined/multiply-defined, no bibtex
   warnings; ledger tally == reflexive macros.
4. Polish-sweep regression guards (circles 19-27): all held (0 TODO/sentinel/
   thirteen/hand-typed Section-number; 1 intentional "engagement").

## Findings (both FIXED)
- 3 cited sources had NO CITE ledger row: amodei2016concrete,
  krakovna2020specification, manheim2018goodhart (the grouped proxy-gaming cite,
  sec:sota 2.2 + intro). All read:FULL; a ledger comment flagged them as "records
  pending" but that was stale (records exist) and no row was added. -> added
  CLM-063/064/065 (CITE, SUPPORTED); updated the stale comment.
- CLM-047 binding hard-coded a stale snapshot ("42 records, 40 FULL; 39 CITE +
  8 RESULT") -> de-numberized; values now defer to tex/macros/reflexive.tex.

## Effect on numbers
- ledger: 43 -> 46 CITE rows (RESULT unchanged at 19).
- tex/macros/reflexive.tex regenerated: ResReflexCiteRows 43 -> 46; all others
  unchanged. Reflexive section now reads "46 citation rows".
- Post-fix audit: every cited key has a CITE row; only baudin_acsl ledgered-but-
  uncited (intentional).

## Strange-loop fixed point (as circle 27)
This spec doc (spec-28) is counted in ResReflexSpecDocs: trail written first
(-> 27 spec files), harness regenerated (-> SpecDocs 27), committed together so
the committed macro == committed file count.

## Gates
- Gate B: build green (18 pp), all cites/refs/macros resolve, no bibtex warnings.
- Determinism: reflexive harness re-run byte-identical.
- Ledger now adds claims (CLM-063..065) -> this IS a ledger change, but the claims
  document existing, read, cited sources (traceability completion, stabilizer 12),
  not new empirical results.

## Report
verify/reports/full-consistency-2026-06-12-circle28.md
