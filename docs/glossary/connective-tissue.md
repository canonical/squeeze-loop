# Connective tissue (every part orients itself)

**Definition.** The property that a paper reads as a *whole*, not a set of independently
coherent paragraphs: **every part says why it exists and how it relates to the bigger
picture** before it dives into its content. The relation is **recursive** — a subsection
orients itself within its section, a section within the paper — so the principle applies at
every level of the document tree.

A part has connective tissue when a reader arriving cold can answer "why am I reading this,
and where does it sit in the argument?" from its opening, without having to reconstruct the
relation themselves. Concretely, each `\section` and `\subsection` opens with an
**orienting paragraph** (its role, and a preview of its parts) before the first
sub-header, definition, or other environment.

## A checked principle (proxy vs. editorial)

Connective tissue is enforced like the rest of the strategy's soft properties — by an
objective proxy plus an editorial judgement:

- **The proxy (machine).** `verify/connective_tissue.py`, a reflexive-squeeze step, checks
  that an orienting paragraph is *present*: it loud-fails on any `\section`/`\subsection`
  that dives straight into a sub-header or environment. This is structural and
  deterministic — it guarantees presence, not quality.
- **The judgement ([Gate A](gates.md), editorial).** Whether the orientation *genuinely*
  connects the part to the big picture — rather than being a token sentence — is a human
  editorial call, the same division of labour the [reflexive-monitors](reflexive-monitors.md)
  use (objective marker; interpretive part to review).

Legitimate exceptions (a header that needs no prose) are carved in
`claims/connective_carveouts.tsv`.

## Why it belongs in this project

The principle is itself recursive, which is the paper's own subject: a document is a tree
of parts, and the squeeze discipline ("claim no more than the whole licenses; show how each
part fits") applies to its *prose structure* as much as to its claims and numbers. Making
it a checked step keeps the manuscript navigable as the loop keeps generating and rewriting
sections.

## Sources

- `verify/connective_tissue.py` — the executable check (the proxy).
- `paper-impl.md` §4 — the principle stated (recursive; Gate A judges quality, the check
  guarantees presence).
- `tex/paper.tex` §`sec:strategy` — the worked example (the section and its "The squeeze"
  subsection both open with an orienting paragraph).

## See also

- [gates](gates.md) — Gate A, which judges whether the orientation is genuine.
- [reflexive-monitors](reflexive-monitors.md) — the family of checks (proxy + route) this
  one joins.
- [glossary](glossary.md) — the related anchoring discipline for the paper's *vocabulary*.
- [squeeze-loop](squeeze-loop.md) — the discipline, here applied to prose structure.
