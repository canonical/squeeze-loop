# 12-0945-paper-gap-2 — evidence-plane sources unobtainable (companion guides)

STATUS: DONE — guides supplied (/tmp/), archived to bib/archive/ with SHA256SUMS,
Gate C run. See verify/reports/evidence-verification-2026-06-12.md.
Observed by: coordinator (evidence-plane verification setup)
Failure code: GP1 (unobtainable source). Risk of F1/F7 if quotes diverge from source.

## Divergence

The manuscript reproduces **verbatim** material attributed to three companion
guides and treats them as the evidence-plane ground truth for all three case
studies (§4) and the appendices:

- `pycsl-prereqs-impl.md`
- `happy-roadmap-impl.md`
- `typing-global-impl.md`

**None of these files exist anywhere on this machine** (searched `/`). The only
`*-impl.md` present is `paper-impl.md` itself. The squeeze-loop-strategy skill
referenced in `paper-impl.md` §0 is also absent.

## What rests on these unverifiable sources

12 verbatim reproductions in `tex/paper.tex`:

| line | kind | attributed anchor |
|---|---|---|
| 393 | extract | pycsl-prereqs-impl.md §1 rule 2 |
| 402 | figure (verbatim) | adapted from P-series guide pipeline |
| 526 | extract | pycsl-prereqs-impl.md §6 |
| 539 | extract | happy-roadmap-impl.md §0 |
| 556 | extract | happy-roadmap-impl.md §4 |
| 586 | extract | typing-global-impl.md §0 |
| 601 | extract | typing-global-impl.md §4 |
| 857 | verbatim | pseries-driver-agent worker def (P-series guide) |
| 888 | verbatim | happy-threat-agent worker def (HAPPY guide) |
| 923 | extract | pycsl-prereqs-impl.md (closing rule) |
| 929 | extract | happy-roadmap-impl.md (closing rule) |
| 935 | extract | typing-global-impl.md (closing rule) |

Per §1 protocol of `paper-impl.md`, the verifier's authority for a quote is
**the source itself, re-opened at its anchor**. With the sources absent, every
quote above is currently **UNANCHORED / UNOBTAINABLE**: the manuscript asserts
these are verbatim, but nothing in this repo can confirm the wording, the
section anchors (§1/§4/§6/§0), or that the guides say what the surrounding prose
claims they say. This is exactly the F1/F7 risk the engagement exists to
exclude — for the paper's *own* evidence.

## This is the user's call, not the coordinator's

Two legitimate possibilities:
1. The guides are real operating documents the author holds elsewhere (most
   likely — `paper-impl.md` describes them as "internal engineering
   artifacts"). Then the fix is to **add them to the repo** (or
   `bib/archive/`), after which Gate C can re-open each anchor and confirm every
   extract is byte-faithful.
2. They are not available. Then per §3 the affected sentences are not citable as
   support and must be marked GP1 in Limitations, or the extracts cut — a
   destructive change the coordinator must not make unilaterally.

The manuscript already carries a related TODO at line 143 ("decide on
anonymization and attach them as supplementary material or a public
repository"), which intersects this gap.

## Requested action

Provide the three guide files (drop them in repo root or `bib/archive/`). Then
the evidence-plane Gate C runs: each extract re-opened at its anchor, verbatim
fidelity confirmed, section anchors checked, and the surrounding claims
("all three guides end with this sentence", the §-anchors) verified.
