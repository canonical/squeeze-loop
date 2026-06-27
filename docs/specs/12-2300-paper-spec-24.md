# 12-2300-paper-spec-24 — paper-impl loop, circle 24: polish the SoTA section (kill hand-typed section numbers)

STATUS: DONE
Editorial circle (no new evidence). §sec:sota is well-cited and accurate; the one
real defect was hand-typed cross-reference numbers --- the exact brittle
anti-pattern the paper's own "no hand-typed numbers" discipline forbids (they go
silently wrong if sections reorder).

## Audit of §sec:sota
The six subsections (single-agent loops, self-evaluation problem, multi-agent
pipelines, verifier-in-the-loop, classical antecedents, the gap) are accurate,
well-cited, and flow well -- prose kept as is.

## Changes (cross-reference robustness; no claim or number altered)
- Added \label{sec:selfeval} to \subsection{The self-evaluation problem}.
- Replaced three hand-typed "Section~2.2 / Sections~2.1--2.4" with proper refs:
  - L243 (multi-agent pipelines): "biases of Section~2.2" -> "Section~\ref{sec:selfeval}".
  - L600 (archetypes section, OUT of SoTA but same defect class, references the
    same subsection): "self-preference ... effects of Section~2.2" ->
    "Section~\ref{sec:selfeval}".
  - L315 (the gap): "the loops of Sections~2.1--2.4" -> "the loops surveyed
    above" (a subsection range is awkward to \ref; the prose meaning is exactly
    the loops just surveyed).

## Additivity
No claim or number altered. The two numeric cross-references now track LaTeX's
counters instead of a hand-typed "2.2"; the range reference is rephrased to prose.
Same defect class as the engagement-vocabulary cleanup (circle 22): a residual
that the paper's stated discipline says should not exist.

## Gates
- Gate B: build green (18 pp), all cites/refs/macros resolve (no "??"), no bibtex
  warnings.
- grep: zero "Section~<number>" occurrences in paper.tex.
- No ledger change (prose/reference-only).
