# Squeeze loop

**Definition.** An organizational pattern in which every actor is held between two
constraints it does not control — a normative **upper bound** (the strongest claim it
may make) and an executable **lower bound** (a ground truth whose verdict it cannot
alter) — and, the load-bearing decision, **every actor answers to a *different* pair of
authorities, chosen so the intersection of all constraints is the correct deliverable
while no single actor's evidence base suffices to certify it.**

A deliverable is **in-band** only when it is a reading of the upper bound that the
lower bound does not refute. Anything above the band is over-claiming; anything below
it is unfaithful to reality. The dominant failure the pattern targets is
**coherent-and-wrong**: a fluent, internally consistent artifact that passes its own
checks while missing the intended property.

## The four compliance conditions

- **C1 — Disjointness.** The authority pairs are pairwise distinct and chosen so their
  intersection is the correct deliverable; no single pair certifies it.
- **C2 — Catchability.** Every actor's characteristic failure is detectable from some
  *other* actor's pair (a different evidence base, no shared blind spot).
- **C3 — Physical barriers.** Each actor's context contains exactly its authorities and
  the interfaces it must exercise; denied evidence (e.g. the implementation, for those
  who judge it) is *absent*, not merely off-limits by instruction.
- **C4 — Gate-defined done.** Done is a fixed set of machine-checked gates passing —
  never an actor's self-report.

## Notes

- The pattern is **recursive**: a squeeze loop can monitor another squeeze loop's soft
  outputs — itself a squeeze holding an upper and lower bound
  (`config/skills/sl-monitoring-sl/`). The monitored output need not be a deliverable:
  a learned **skill** is checked by [Gate S](gates.md), and a *claim*, a *generated
  category*, or a *citation anchor* by the [reflexive-monitors](reflexive-monitors.md)
  family. The justification is C2: a soft output shares its producer's blind spot, so a
  *disjoint* monitor is required.
- Applied to its own construction (this paper), the loop is self-referential — see
  [strange-loop](strange-loop.md). The honest limit it cannot dodge is that a
  self-monitor shares the authoring blind spot, so it **routes** what it cannot
  independently verify to a disjoint base rather than self-certifying.

## Sources

- `tex/paper.tex` §`sec:strategy`: Definition 1 (Squeeze), Definition 2
  (squeeze-loop compliance, C1–C4), the hard/soft-truth remark, the canonical cast.
- `paper-impl.md`: the operating loop (agents, gates A/B/C, paired documents).

## See also

- [upper-bound](upper-bound.md) · [ground-truth](ground-truth.md) — the two bounds.
- [archetype](archetype.md) — where the bounds' materials come from.
- [gates](gates.md) — how "done" is defined (C4); Gate S applies the pattern recursively
  to a loop's learned skills.
- [reflexive-monitors](reflexive-monitors.md) — the pattern applied to the loop's own
  claims, categories, and citation anchors.
- [tier](tier.md) · [strange-loop](strange-loop.md) — graded claims and the reflexive case.
