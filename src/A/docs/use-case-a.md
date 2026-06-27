# Use Case A — verified business metrics that recompute

Use Case A is a **base** squeeze loop (`id: instance-a`, **`kind: base`**, terrain
**A**), encoded as the SL-1.0 self-description
[`src/A/instance-a.sl.json`](../instance-a.sl.json) and written up as the skill
[`src/A/config/skills/use-case-a`](../config/skills/use-case-a/SKILL.md). Its
deliverable: **business metrics — net revenue, active users per quarter — computed from a
frozen warehouse and guaranteed to be the figure the metric handbook mandates.**

## Rationale — why this loop exists

The terrain is **transcription** ("every number recomputes"): an external authority — the
**metric handbook** — already states what each figure must mean, and the truth lives in a
frozen warehouse anyone can re-query. The dominant failure is therefore not a crash but a
plausible wrong number:

> **Coherent-and-wrong = a query that returns an internally consistent, numerically valid
> figure that violates a handbook clause** — gross revenue where the handbook says *net*;
> login-only users counted as *active* where the handbook requires a qualifying action.

Such a figure passes the author's own spot-check (it *is* a real number from the real
warehouse) yet betrays the handbook's intent. The loop makes it catchable by pinning two
independent bands between the same two bounds and forcing them to collide over the
warehouse:

- **Upper bound `U`** — the **metric handbook** (`root:root 0444`, clauses
  `CLAUSE_1..5`): the normative ceiling fixing the strongest claim any agent may make.
- **Lower bound `L`** — the **read-only SQLite warehouse** re-executed for every claim,
  plus the **signed history ledger** (total-additivity invariant, re-verified each run).

A figure is in-band only when it is the handbook's reading of the metric that the
warehouse does not refute — and, for quarter windows, equals the certified ledger value.
A passing positive ties **all three planes together: ceiling, band, and floor agree on
the number.**

## Graphical representation

![The `instance-a` SL — the sentinel, analytical implementer, and independent exerciser
(orange) squeezed between the metric handbook (green, `U`) and the frozen warehouse +
certified ledger (pink, `L`), barriered (red dashed) from each other's
artifacts](img/use-case-a.svg)

*Rendered from `instance-a.sl.json` with
`config/skills/sl-internal/scripts/sl2plantuml.py … --svg`. Solid edges are bounds (`U` /
`L`) and `produces`; the red dashed edges are the `✗ must-not-see` barriers between the
two bands.*

The three actors:

| Actor | Role | Builds | Upper bound `U` | Lower bound `L` |
|---|---|---|---|---|
| **Gate sentinel / orchestrator** | coordinator | approvals, gate verdicts, the loop's `.sl.json` | the handbook clauses | warehouse re-execution + additivity invariant + both bands compared |
| **Analytical implementer** | implementer | the metric query (`compute_metric.py`) | the handbook clause for the metric | the value the frozen warehouse returns |
| **Independent exerciser** | exerciser | positive expected values + clause-violating negatives (the validation matrix) | the handbook acceptance clauses, read independently | values recomputed over the warehouse, seeded from the certified ledger |

The gates: **A** — the plan cites every `CLAUSE_X`; **B** — positives have
implementer = exerciser = ledger, and each negative mutation must *diverge* from the
correct value (a non-diverging mutation is a vacuous-negative failure); **C** — every
handbook clause is named by some test case.

## Disjointness at a glance

> **The hypothesis.** The implementer and exerciser read the **same handbook** but are
> physically barriered from each other's products and produce independently; the
> exerciser additionally anchors to the **invariant ledger the implementer never reads**,
> and the sentinel certifies only by comparing both bands plus the invariant — so **no
> single band's evidence base certifies the metric**. The correct figure is the
> *intersection*: the value on which the handbook-reading query, the independently
> recomputed expectation, and the certified ledger all agree.

**Load-bearing barrier.** The implementer and exerciser cannot see each other's artifacts
— Unix `0700` homedirs + AST/import isolation in the LXC container (*Zero Import
Linkage*); the only data paths are read-only SQLite to the warehouse and JSON strings
reconciled by the runner.

**Catchability — each blind spot is caught by a different actor:**

| Actor | Characteristic blind spot | Caught by | Via |
|---|---|---|---|
| Analytical implementer | a coherent-and-wrong query: a consistent number that violates a handbook clause | **Independent exerciser** | independently recomputed expected value; Gate B value mismatch |
| Independent exerciser | a vacuous negative mutation that fails to diverge from the correct value | **Gate sentinel** | Gate B negatives require each named mutation to actually diverge; Gate C clause-coverage |

**No terminus.** Instance A is a fully **mechanical** loop (`terminus: null`): the truth
lives in the frozen warehouse and the signed ledger, so every claim is settled by
re-execution — there is no soft-vs-soft residual needing a human/cross-provider close.
That is the signature of terrain A: the soundness load rests on the machine gate plus the
standing invariant, where a wrong result cannot survive re-execution.

**Mechanical floor.** `sl_disjointness_check.py instance-a.sl.json` returns
**0 FAIL / 8 checks** — every actor reads no source it produced (D1), both barriers are
consistent with their bounds (D2, the `✗ must-not-see` between the bands is real), and
each blind spot above is caught by a *different* actor (C2). A green check certifies the
**authorities are disjoint**, never that any metric is *done* — that lives in the Gate
A/B/C evidence.

---

*Generated from [`src/A/instance-a.sl.json`](../instance-a.sl.json). Regenerate the
diagrams with:*

```sh
python config/skills/sl-internal/scripts/sl2plantuml.py \
    src/A/instance-a.sl.json -o src/A/docs/img/use-case-a.png
python config/skills/sl-internal/scripts/sl2plantuml.py \
    src/A/instance-a.sl.json --svg -o src/A/docs/img/use-case-a.svg
```
