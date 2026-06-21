# Glossary (the role of this glossary)

**Definition.** The *glossary* is the place where each concept the project uses is
**anchored to one authoritative meaning**, grounded in the artifacts that establish it.
It exists because a squeeze loop is **generative**: running the loop *creates new
concepts*, and a newly created concept is a soft output that has no fixed meaning until
it is anchored.

## Why a generative loop needs a glossary

Holding an agent between a fixed authority and a fixed ground truth
([squeeze-loop](../../../../docs/glossary/squeeze-loop.md)) **forces new distinctions into existence** — the O4
"self-referential categorization" finding (`paper_upper_bound.md`; the generated
categories in `claims/category_generation_log.tsv`). The hard/soft-truth split,
"richness as the number of separable forks", "diversity restores the trial",
[archetype](../../../../docs/glossary/archetype.md)s, [tier](../../../../docs/glossary/tier.md)s, [Gate S](../../../../docs/glossary/gates.md), the
[reflexive-monitors](../../../../docs/glossary/reflexive-monitors.md) — none of these existed before the loop
needed them; each was carved while resolving a squeeze.

A freshly carved concept is **soft**: like any [upper-bound](../../../../docs/glossary/upper-bound.md)-side output
it is interpretation-laden, and the same word can drift to more than one reading across
circles. If it is used before it is pinned down, the loop's own prose
becomes *coherent-and-wrong* — fluent sentences that quietly mean different things in
different sections. So a generated concept must be **anchored** before it is load-bearing:
given one definition, sourced to where it is established (`file §section` / clause / TSV),
so every later use carries the same meaning. **That anchoring is what this glossary is
for.** It is the loop's terminology under the same discipline as everything else it
produces.

## What anchoring is, and is not

- **One term, one file, one definition**, with a **Sources** section so the entry never
  drifts from the artifacts (it *records* the meaning the paper and upper bounds already
  commit to — it does not invent one; see the README conventions).
- Anchoring a concept is **naming**, not **validating**. A generated concept can be
  clearly defined here *and still over-reach* in use. Naming and checking are kept
  separate: the [reflexive-monitors](../../../../docs/glossary/reflexive-monitors.md) (e.g. the over-reach audit)
  test whether a generated category actually generalises, and **carve** it where it does
  not. An entry fixes what a term *means*; the monitors fix where it *applies*.

## Recursive: one glossary per loop

Because *every* squeeze loop is generative, this applies recursively. Each use case
carries its own glossary (`src/{A,B,C,D}/in-band-deliverable/glossary/`), seeded with
this same entry, since each instance generates and must anchor its own concepts. The
paper's glossary (`docs/glossary/`) is simply the reflexive instance's.

## So the glossary is part of the squeeze

The glossary closes a small loop of its own: the loop generates a distinction → the
distinction is anchored here → later circles use the anchored term → the monitors check
it has not over-reached → an entry is narrowed if it has. It is the standing record that
the project's vocabulary, like its claims and its numbers, is held to a bound rather than
left to drift.

## Sources

- `paper_upper_bound.md` (O4 self-referential categorization; the generativity finding)
  and `claims/category_generation_log.tsv` (concepts dated as they were carved).
- `tex/paper.tex` §`sec:reflexive` ("forces new distinctions into existence", scoped).
- `docs/glossary/README.md` (the conventions every entry follows).

## See also

- [README](README.md) — the index and the per-entry conventions.
- [squeeze-loop](../../../../docs/glossary/squeeze-loop.md) — the generative pattern that creates the concepts.
- [reflexive-monitors](../../../../docs/glossary/reflexive-monitors.md) — the checks that test a generated concept
  for over-reach after it is anchored.
- [strange-loop](../../../../docs/glossary/strange-loop.md) — the self-applying construction whose generativity is
  what makes new concepts appear.
- [connective-tissue](../../../../docs/glossary/connective-tissue.md) — the companion discipline: this anchors the
  paper's *vocabulary*, that one anchors its *structure*.
