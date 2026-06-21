# shared contract — the reflexive instance's interface

The reflexive squeeze targets the REAL repository (no sandbox). Canonical paths,
discovered by `_paperlib.py` (walks up to the dir holding `tex/paper.tex`):

- manuscript:        tex/paper.tex
- macros:            tex/macros/*.tex          (generated; never hand-edited)
- bibliography:      tex/references.bib
- reading records:   bib/records/*.md          (one per cited source, read in full)
- claim ledger:      claims/ledger.tsv         (CITE / RESULT rows)
- manuscript defects: verify/manuscript_defects.tsv
- generators:        the (cwd, script) list in _paperlib.py::GENERATORS

Invariants the gates enforce: every \cite in bib AND records; every macro
recomputes byte-identical; ledger CITE/RESULT counts == the reflexive macros;
every ledgered claim traces to a record or an artifact.
