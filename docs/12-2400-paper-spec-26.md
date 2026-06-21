# 12-2400-paper-spec-26 — paper-impl loop, circle 26: polish the stabilizers section (drift-proof the count)

STATUS: DONE
Editorial circle (no new evidence). §sec:stabilizers (13 anti-collapse rules +
the collapse-modes table) is accurate; the real defect was a hand-typed count of
its own list -- the exact anti-pattern the paper's "no hand-typed numbers"
discipline forbids, same class as the section numbers fixed in circle 24.

## Audit
- Verified the enumerate has exactly 13 \item entries (matches the prose count).
- Collapse-modes table (Table~\ref{tab:collapse}) maps each mode to valid rule
  numbers; rule 11 (sequencing) legitimately has no collapse-mode row. The table's
  compact numeric rule-pointers are a within-table index (caption explains them),
  kept as is -- same convention as the \S\ref pointers in the archetype tables.

## Change (drift-proof the count; no claim altered)
- "thirteen" was hand-typed in THREE places, all naming the same 13-item list:
  abstract (L87), intro contribution (iv) (L174), and §stabilizers (L790). If a
  14th rule were ever added, all three would silently lie -- the drift this paper
  warns against.
- Added \label{item:laststab} to the last (13th) stabilizer and replaced all three
  "thirteen" with \ref{item:laststab} (resolves to 13, page 11). The count now
  tracks the list automatically.

## Additivity
No claim altered. The number is unchanged (13) but is now computed by LaTeX from
the list rather than hand-typed -- the same reflexive application of the paper's
discipline as circles 24 (section numbers) and 18 (reflexive macros).

## Gates
- Gate B: build green (18 pp), all cites/refs/macros resolve (no "??"), no bibtex
  warnings.
- .aux: \newlabel{item:laststab} = 13; pdftotext confirms "13 stabilizers" /
  "13 rules" rendered; zero "thirteen" left in source.
- No ledger change (prose/reference-only).
