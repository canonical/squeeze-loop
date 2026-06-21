# Full-paper consistency pass — 2026-06-12 (circle 18)

Gate-C discipline applied to the whole manuscript: every number re-derived from
its artifact, every citation checked for a reading record + bib entry, all
refs/macros resolved, the claim ledger reconciled with the paper.

## 1. Every number recomputes (evidence plane)
Re-ran all 12 generators (src/{A,B,C}/evidence/measure_squeeze.py;
verify/{coupling_measure,synthesis,eval_protocol,reflexive_measures}.py;
eval/{pilot,pilot2,pilot3,study}/score.py; eval/swebench/run_protocol.py) and
diffed the generated macros against the committed versions.

- **11 of 12 macro files byte-identical** on regeneration -> the paper's numbers
  are reproducible, not stale.
- **1 stale file caught and fixed: `tex/macros/reflexive.tex`.** Its
  self-application counts were frozen at circle 9 while the loop ran 8 more
  circles. Corrected:
  - ResReflexCiteRows 42 -> 43, ResReflexRecords 45 -> 46,
    ResReflexResultRows 12 -> 19, ResReflexSpecDocs 8 -> 16.
  All legitimate growth (new reading records, ledger rows, and per-circle spec
  docs). The reflexive section now reports the full 17-circle loop accurately.

## 2. Citations (literature plane)
- 45 distinct `\cite` keys in the manuscript.
- **All 45 have a reading record** in `bib/records/` AND a `references.bib` entry.
- Uncited bib entry: `baudin_acsl` only (orphaned when the field engagements were
  removed in circle 10; harmless, entry + record retained).
- Deep per-source re-derivation was done earlier (verify/reports/
  lit-verification, fulltext-verification, evidence-verification, and the
  per-use-case reports); this pass verifies structural completeness, not a second
  full re-read.

## 3. Internal consistency
- Build green (18 pp); **no undefined references, citations, or macros; no
  multiply-defined labels; no bibtex warnings.**
- Ledger tally: **43 CITE + 19 RESULT** rows = the regenerated
  ResReflexCiteRows (43) and ResReflexResultRows (19). Ledger and reflexive
  section are mutually consistent.

## Outcome
One real drift found (reflexive macros stale) and fixed; everything else
recomputes and resolves. The manuscript is internally consistent: every cited
source recorded, every number regenerated from a committed artifact, every
cross-reference resolved.

## Residual (honest)
- `baudin_acsl` uncited (intentional, post-removal).
- The deep literature re-derivation is incremental across the per-circle reports,
  not repeated in full here.
