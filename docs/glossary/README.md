# Glossary

Precise, grounded definitions of the project's recurring vocabulary. The paper
(`tex/paper.tex`) and the upper-bound docs are where terms are *used*; this glossary
is where each term has **one** authoritative definition, so usage stays consistent as
the project grows.

## Conventions

- **One term per file**, lower-case kebab filename (`archetype.md`, `tier.md`).
- Each entry opens with a one-sentence **Definition**, then explanation.
- **Sources** section anchors the definition to where it is established in the repo
  (`file §section` / table / clause), so the glossary never drifts from the artifacts.
- **See also** cross-links related entries.
- The glossary *records* the definitions the paper and upper bounds already commit to;
  it does not invent new ones. If a definition needs to change, change it here and in
  the source together.

## Entries

The vocabulary falls into two clusters: the **core strategy** (the pattern and its
parts) and its **self-application** (the strategy turned on its own outputs, including
this paper). The second cluster is the first applied recursively, so its entries point
back into the first.

### About the glossary

- [glossary](glossary.md) — why a *generative* loop needs a glossary: the loop creates
  new concepts, and each must be anchored to one meaning before it is load-bearing.

### Core strategy

- [squeeze-loop](squeeze-loop.md) — the core pattern: every actor held between an upper
  and a lower bound, with disjoint authority pairs and gate-defined done.
- [upper-bound](upper-bound.md) — the soft, normative truth (the strongest claim an
  actor may make); includes `U_self`.
- [ground-truth](ground-truth.md) — the lower bound / hard, executable truth (the
  oracle a gate re-runs).
- [gates](gates.md) — the checkpoints that define "done": Gate A (editorial), B
  (machine acceptance), C (coverage/no-blend), S (skill consistency), and reflexive S
  (S on the paper's own claims).
- [archetype](archetype.md) — the three terrain archetypes (A transcription,
  B authored authority, C split planes); where the sources of truth live.

### Self-application (the strategy turned on its own outputs)

- [reflexive-monitors](reflexive-monitors.md) — the family that applies the Gate S move
  to the paper loop's *other* soft outputs: the category over-reach audit, the
  perturbation gate, and the flag-rate calibration.
- [tier](tier.md) — the disposition ladder (Tier 0–3) and the loud-fail rule used to
  bound graded claims (e.g. the U_self strange-loop claim).
- [strange-loop](strange-loop.md) — the self-applied squeeze; the structural (not
  phenomenal) form of an "I," scoped by `U_self`.
- [connective-tissue](connective-tissue.md) — the checked principle that every section and
  subsection orients itself within the whole (recursively); a reflexive-squeeze step.
