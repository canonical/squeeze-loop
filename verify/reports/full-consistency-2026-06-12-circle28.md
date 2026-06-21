# Full-paper consistency pass — 2026-06-12 (circle 28)

Gate-C discipline over the whole manuscript, repeated after the section-by-section
polish sweep (circles 19-27): every number re-derived from its artifact, every
citation checked for a reading record + bib entry + ledger row, all refs/macros
resolved, ledger reconciled with the reflexive section.

## 1. Every number recomputes (evidence plane)
Re-ran all 12 generators (src/{A,B,C}/evidence/measure_squeeze.py;
verify/{coupling_measure,synthesis,eval_protocol,reflexive_measures}.py;
eval/{pilot,pilot2,pilot3,study}/score.py; eval/swebench/run_protocol.py).
- **12 of 12 macro files byte-identical** on regeneration (before the ledger edit
  below) -> the paper's numbers are reproducible.
- reflexive_measures.py re-run is byte-identical (determinism).

## 2. Citations (literature plane)
- 45 distinct `\cite` keys in the manuscript.
- All 45 have a reading record AND a references.bib entry.
- **Finding (FIXED): 3 cited sources had no CITE ledger row** ---
  amodei2016concrete, krakovna2020specification, manheim2018goodhart (the grouped
  "proxies under optimization pressure invite gaming" cite, sec:sota 2.2 + intro).
  All three are read:FULL with claim cards; a ledger footer comment even flagged
  them as "records pending ... claim covered by amodei2016concrete record" --- but
  that comment was stale (records now exist) and no row was ever added. Added
  CLM-063/064/065 (CITE, SUPPORTED, per-source notes); updated the stale comment.
- **Finding (FIXED): CLM-047's binding note hard-coded a stale snapshot**
  ("42 reading records, 40 read FULL; 39 CITE + 8 RESULT") --- frozen early-circle
  numbers in the row that points at the regenerated macro. De-numberized the note
  so it describes what is counted and defers the values to tex/macros/reflexive.tex.
- Post-fix: every cited key has a CITE row; only baudin_acsl is ledgered-but-
  uncited (intentional, post-circle-10).

## 3. Internal consistency
- Build green (18 pp); no undefined references/citations/macros; no
  multiply-defined labels; no bibtex warnings.
- Ledger tally after fix: **46 CITE + 19 RESULT** = regenerated
  ResReflexCiteRows (46) and ResReflexResultRows (19). Consistent.
- Reading records: ResReflexRecords (46), ResReflexRecordsFull (43) match disk.

## 4. Polish-sweep regression guards (circles 19-27 held)
- 0 `\TODO` (and the macro is removed, so a stray one fails the build).
- 0 "sentinel"; 0 "thirteen" (count is now \ref-driven); 0 hand-typed
  "Section~<number>" (all \ref).
- Exactly 1 "engagement" (the intentional generic amortization usage); 0
  "engagement notes".

## Outcome
Two real drifts found and fixed (3 unledgered cited sources; one stale hand-typed
snapshot in CLM-047), both in the claim ledger; everything else recomputes and
resolves. The manuscript is internally consistent: every cited source recorded
AND ledgered, every number regenerated from a committed artifact, every
cross-reference resolved, every polish-sweep fix intact.

## Residual (honest)
- baudin_acsl ledgered but uncited (intentional).
- ResReflexCiteRows (46) and ResReflexRecords (46) are numerically equal but
  distinct quantities (CITE ledger rows vs reading records); the prose
  distinguishes them.
