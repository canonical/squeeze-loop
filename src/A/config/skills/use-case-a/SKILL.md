---
name: use-case-a
description: The Squeeze Loop instance for Use Case A — verified business metrics (net revenue, active users per quarter) computed from a frozen SQLite warehouse against a binding metric handbook, on terrain A (transcription / "every number recomputes"). It pins an analytical implementer and an independent exerciser between the handbook clauses (upper bound) and the warehouse + certified history-ledger invariant (lower bound), physically isolated in an LXC container, and gates the deliverable on three planes agreeing (ceiling, band, floor). Use when working on src/A — the metric handbook, compute_metric query, validation matrix, the execute_squeeze runner, Gate A/B/C for metrics, the frozen warehouse / history ledger, or the coherent-and-wrong "a consistent number that violates a handbook clause" (gross instead of net; login-only users counted as active). Trigger phrasings: "use case A", "instance A", "metric handbook squeeze", "the warehouse metric loop", "net-vs-gross coherent-and-wrong", "validation matrix negatives must diverge".
---

# Use Case A — the metric-handbook squeeze loop

Use Case A is a concrete **base** squeeze loop (`instance-a`, terrain **A**): it
delivers **business metrics that recompute** — net revenue and active-users-per-quarter
figures computed from a frozen warehouse — and guarantees each figure is the one the
**metric handbook** mandates, not merely an internally consistent number. Its SL-1.0
self-description is [`src/A/instance-a.sl.json`](../../../instance-a.sl.json); the
companion write-up with the diagram is [`src/A/docs/use-case-a.md`](../../../docs/use-case-a.md).

## The dominant failure it guards

**Coherent-and-wrong here = a query that returns an internally consistent, numerically
valid figure that violates a handbook clause** — gross revenue where the handbook says
net; users counted active on a login alone where the handbook requires a qualifying
action. The number "looks right," passes the author's own spot-check, and is wrong. The
whole loop exists to make that catchable by someone other than the query's author.

## The bounds

- **Upper bound `U` — the metric handbook.** `/opt/squeeze/shared/metric_handbook.md`
  (`root:root 0444`), obligation clauses `CLAUSE_1..5` in a strict token-parsable
  schema. It fixes the strongest claim the implementer and exerciser may make; an
  unauthorized filter or a scope expansion that over-reports breaches the ceiling.
- **Lower bound `L` — the frozen warehouse + the certified invariant.** The read-only
  SQLite warehouse (`base_warehouse.db`, `?mode=ro`) re-executed for every claim, plus
  the signed `history_ledger.json` (total-additivity invariant, re-verified each run).
  The verdict is mechanical: the query returns a value or it does not, and the value
  matches the certified figure or it does not.

A figure is **in-band** only when it is the handbook's reading of the metric that the
warehouse does not refute — and, for quarter windows, equals the certified ledger value.

## The cast (three actors)

| Actor | Builds | `U` | `L` | Must not see |
|---|---|---|---|---|
| **Gate sentinel / orchestrator** (coordinator) | approvals, gate verdicts, the loop's `.sl.json` | handbook clauses it gates against | gate output: warehouse re-execution + additivity invariant + both bands compared | — |
| **Analytical implementer** | the metric query (`compute_metric.py`) | the handbook clause for the metric | the value the frozen warehouse returns | the validation matrix |
| **Independent exerciser** | positive expected values + clause-violating negative mutations (the validation matrix) | the handbook acceptance clauses, read independently | values recomputed over the warehouse, seeded from the certified ledger | the implementation / query code |

## The barrier (physical, not honorary)

The implementer and exerciser bands are **physically isolated** — Unix `0700` homedirs +
AST/import isolation inside the LXC container, *Zero Import Linkage*: neither imports,
reads, or parses the other. The only data paths are read-only SQLite to the warehouse
and JSON strings reconciled by the runner (*Strict Serialization*). An agent that has the
other band's artifact in context will eventually use it; here it simply is not there.

## The gates

- **Gate A (editorial).** The plan must cite every `CLAUSE_X` of the target metric; the
  sentinel judges it, never rubber-stamps.
- **Gate B (machine).** *Positives:* the implementer's value equals the exerciser's
  independently computed expected value **and** (for quarter windows) the certified
  `history_ledger.json` value — ceiling, band, and floor agree on the number.
  *Negatives:* each named clause-violating mutation must **diverge** from the correct
  value over the same window (a mutation that fails to diverge is a vacuous-negative
  failure — the clause was not load-bearing). This is the "proves WITH the clause, fails
  WITHOUT it" payoff.
- **Gate C (coverage).** Every obligation `CLAUSE_X` read from the handbook is named by
  some test case's `target_clauses`.

## Disjointness

Implementer and exerciser read the **same handbook** but are barriered from each other's
products and produce independently; the exerciser additionally anchors to the **invariant
ledger the implementer never reads**, and the sentinel certifies only by comparing both
bands plus the invariant — **no single band's evidence base certifies the metric**.
Catchability: the implementer's coherent-and-wrong query is caught by the exerciser's
independently recomputed expected value (Gate B mismatch); the exerciser's vacuous
negative is caught by the sentinel (Gate B negatives must diverge; Gate C coverage).

Validate the self-description with:

```sh
python config/skills/sl-internal/scripts/sl_disjointness_check.py src/A/instance-a.sl.json
```

(0 FAIL / 8 checks — every actor reads no source it produced, both barriers are
consistent with their bounds, and each blind spot is caught by a different actor.)
