# 12-2000-paper-spec-18 — paper-impl loop, circle 18: full-paper consistency pass

STATUS: DONE
Gate-C discipline applied to the whole manuscript (verification circle, no new
content).

## Checks run
1. Every number recomputes: re-ran all 12 generators, diffed generated macros
   against committed.
2. Citations: every \cite key has a reading record + a bib entry; flag uncited
   entries.
3. Internal consistency: build green, no undefined refs/cites/macros, ledger
   reconciled with the reflexive macros.

## Findings
- 11/12 macro files byte-identical -> numbers reproducible.
- 1 staleness caught + FIXED: tex/macros/reflexive.tex (self-application counts
  frozen at circle 9 while the loop grew 8 circles): CiteRows 42->43,
  Records 45->46, ResultRows 12->19, SpecDocs 8->16. Legitimate growth;
  reflexive section now reports the full loop. The §6 prose auto-updates via
  macros.
- 45/45 cited keys have reading records AND bib entries; only baudin_acsl uncited
  (intentional, post-circle-10).
- Build green (18 pp); no undefined refs/cites/macros; no bibtex warnings.
- Ledger 43 CITE + 19 RESULT == ResReflexCiteRows/ResReflexResultRows: consistent.

## Output
- verify/reports/full-consistency-2026-06-12.md (the report).
- tex/macros/reflexive.tex updated (regenerated); paper rebuilt.

## Gates
- Gate B: build green; all resolve; no warnings.
- This pass IS Gate C over the whole paper: every number re-derived from its
  artifact, every cite checked for a record.

## Note
No ledger change (the reflexive counts the ledger; updating reflexive does not add
a claim). The one drift (stale reflexive macros) is the kind of regression the
"every number recomputes" discipline exists to catch -- here caught on the paper
about that discipline.
