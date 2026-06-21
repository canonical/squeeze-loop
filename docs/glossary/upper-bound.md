# Upper bound (the soft / normative truth)

**Definition.** A **citable normative artifact fixing the strongest claim an actor may
make** — the soft truth of a squeeze. It is authoritative but *interpretation-laden*:
the same precise English admits more than one faithful reading. A deliverable is
in-band only if it claims no more than the upper bound licenses (and is not refuted by
the [ground truth](ground-truth.md)).

The upper bound says *what ought to be* (the norm, spec, or standard); it cannot say
*what is* — that is the lower bound's job. The characteristic failure it guards against
is **over-claiming**: asserting more than the source supports. Understatement
(claiming less) is always in-band; the safe direction is down.

## Forms it takes (per terrain)

- **Transcription (A/D):** an external written specification — a metric handbook, a
  textbook manifest.
- **Authored authority (B):** a property spec *authored upstream* (no external authority
  exists), anchored to a flagship use case — e.g. a refund policy.
- **Split planes (C):** one authority per plane plus a precedence rule — e.g. an API
  governance manifest over a schema.

In the repository, upper bounds live under `src/<X>/upper-bound/`. A use case may carry
more than one: e.g. an object-level upper bound (the policy) and a **self** upper bound
(`src/<X>/self_upper_bound.md`).

## `U_self` — an authored-authority upper bound on a *self*-claim

`paper_upper_bound.md` is an upper bound (Archetype B) bounding any claim that the loop
instantiates Hofstadter's account of selfhood. It shows the general shape: a cap, a
disposition ladder ([tier](tier.md)), obligation clauses, falsification tests, and
explicit NOT-claims. When the soft normative artifact does not exist as a formal
definition (as with selfhood), the upper bound *constructs a defensible
operationalization* and says so.

## An upper bound for every soft output, not just deliverables

Over-claiming is the failure the upper bound guards, and a *deliverable* is not the only
thing that can over-claim. Any soft output the loop produces is checked against an upper
bound by a disjoint monitor ([squeeze-loop](squeeze-loop.md), recursion note):

- a learned **skill** over-claims when it generalises past the loop's upper bound —
  caught by [Gate S](gates.md);
- a **generated category** over-claims when it asserts a generality the artifacts do not
  support — caught by the over-reach audit;
- a **citation claim** over-claims when it rests on the abstract and the full text does
  not bear it out — caught by the perturbation gate.

The last two are the [reflexive-monitors](reflexive-monitors.md) family. In each case
"in-band" means the same thing as for a deliverable: claim no more than the upper bound
licenses. The safe direction is still down.

## Sources

- `tex/paper.tex` §`sec:strategy`: Definition 1 (the upper bound `U`); the
  hard/soft-truth remark; "strictness has a safe direction."
- `paper-impl.md` §0: "Upper bound — the state of the art, as a verified corpus."
- `paper_upper_bound.md`; `src/<X>/upper-bound/`, `src/<X>/self_upper_bound.md`.

## See also

- [ground-truth](ground-truth.md) — the hard, executable counterpart.
- [squeeze-loop](squeeze-loop.md) — the pattern the upper bound is one half of.
- [archetype](archetype.md) — what the upper bound is *made of* per terrain.
- [tier](tier.md) — how an authored upper bound expresses graded admissibility.
- [gates](gates.md) · [reflexive-monitors](reflexive-monitors.md) — the monitors that
  check soft outputs (skills, claims, categories, anchors) against an upper bound.
