# upper-bound — the manuscript's normative ceiling (soft truth)

The literature plus the paper-spec fix the strongest claims the paper may make.

- `validate_handbook.py` — the read-before-cite rule: every `\cite` key has a
  `references.bib` entry AND a `bib/records/<key>.md` reading record. Uncited bib
  entries are reported (the known orphan is `baudin_acsl`).
- `gate_checks.py` — Gate A (the spec `paper-impl.md` and the per-circle plan
  trail exist) and Gate C (the claim ledger's CITE/RESULT counts equal the
  reflexive macros, so ledger and manuscript agree).

The upper bound is a *soft* truth (prose, norms, interpretation); the squeeze
binds it to the hard lower bound above.
