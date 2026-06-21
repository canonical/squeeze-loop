# Upper Bound — Squeeze-Loop Metric Handbook

> **Purpose:** the metric handbook fixes what each business figure must mean
> (e.g. net, not gross), so the implementer's query cannot over-claim or compute
> the wrong number.

Implementation of the **Upper Bound Source of Truth** for the system in
[`../upper-bound-spec.md`](../upper-bound-spec.md). The upper bound is the citable
normative ceiling: it fixes the strongest claim the `implementer` and `exerciser`
agents may make. An agent that uses an unauthorized filter, or expands scope to
over-report a number, has breached the ceiling.

It is the counterpart to [`../ground-truth/`](../ground-truth/) (the executable
floor): the handbook's metrics are defined over the *same* warehouse
(`base_warehouse.db`), and each metric's in-scope computation reproduces the
certified figure in `../ground-truth/shared/history_ledger.json`.

## Files

| File | Role |
|---|---|
| `metric_handbook.md` | **The upper bound itself** — the normative ceiling, in the strict token-parsable schema of spec §2 (`# METRIC_HANDBOOK_START … END`). |
| `handbook.py` | The single parser + structural validator. Turns the handbook into `Metric` objects; `extract_block()` yields the per-metric markdown the dispatch loop copies into `spec.txt` (§1). |
| `gate_checks.py` | The upper-bound-driven gate primitives (§3): `gate_a_plan` (plan cites every `CLAUSE_X`) and `gate_c_assertions` (exerciser's tests cover every `CLAUSE_X`). |
| `validate_handbook.py` | Self-check: structure + **grounding** against the warehouse + gate wiring. Exits nonzero on failure. |
| `provision.sh` | Deploys `metric_handbook.md` to `/opt/squeeze/shared/metric_handbook.md` as `root:root 0444` (§1), refusing to deploy a malformed ceiling. |

## Usage

```bash
python3 handbook.py            # list the parsed metrics
python3 validate_handbook.py   # structure + grounding + gate wiring; exit 0 == sound
python3 gate_checks.py         # pilot: Gate A / Gate C on good and bad inputs
sudo ./provision.sh            # deploy (inside the LXC container)
```

## The schema (spec §2)

Each metric block declares, in fixed tokens the parser keys on:

- `## METRIC_ID: METRIC_00N`
- `**Name:**`, `**Status:**` (`BINDING` | `DRAFT` | `DEPRECATED`), `**Target Table:**`
- `### 1. Normative Formula` — a fenced ```text``` formula (the ceiling, not runnable SQL)
- `### 2. Explicit Scope Boundaries (The Ceiling)` — `**Exclusion N:**` bullets
- `### 3. Enumerated Obligation Clauses (Gate C Targets)` — `**CLAUSE_N:**` bullets

`handbook.py` enforces: markers present, unique metric ids, all required fields,
valid status, a formula block, and clause ids that are **sequential `CLAUSE_1..N`**
with at least one clause for every `BINDING` metric (else Gate C would be vacuous).

## How the upper bound drives the gates (spec §3)

- **Gate A (Plan Validation)** — `gate_a_plan(metric, plan_text)` asserts the
  Coordinator's `spec-N.md` cites every `CLAUSE_X` of the active metric, so no
  obligation is silently dropped before code is unlocked.
- **Gate C (Coherent-and-Wrong Guard)** — `gate_c_assertions(metric, assertions)`
  reads the exerciser's `assertions.json` and fails the build unless every
  `CLAUSE_X` is covered by a targeted, non-trivial test — even if the SQL ran
  without a single runtime error. Coverage requires an assertion that *names* the
  clause and carries a non-empty `check`.

`assertions.json` (written by the independent exerciser) schema:

```json
[
  {"name": "q1 boundary lands in Q1", "clauses": ["CLAUSE_1"], "check": "Q1 == 1987.21"},
  {"name": "logins excluded",         "clause":  "CLAUSE_2",   "check": "sum ignores login rows"},
  {"name": "refunds subtracted",      "clause":  "CLAUSE_3",   "check": "net < gross"}
]
```

## Note on the spec's example metrics (adaptation, surfaced not silent)

The spec illustrates the schema with `METRIC_001` over a `billing_events` table
(`event_status='BOOKED'`, `test_`-prefixed accounts) and `METRIC_002` over
`user_sessions`. **Those tables/columns do not exist in the ground truth**
(`events`/`users`, `purchase`/`refund`/`login`, `users.deleted_ts`). An upper
bound over phantom tables cannot bind an agent querying `base_warehouse.db` — the
squeeze requires the ceiling and the floor to constrain the same system. So this
handbook keeps the spec's exact schema and the *same kinds* of scope boundaries
the example demonstrates — UTC-only boundaries, status/type filtering,
test/survivorship bias guards — but targets the real warehouse:

| Spec example | Implemented as | Real edge case it guards |
|---|---|---|
| METRIC_001 Recognized Revenue (BOOKED filter) | METRIC_001 Net Revenue (`purchase` − `refund`) | UTC quarter boundaries; exclude `login`; subtract refunds |
| METRIC_002 Churn Denominator (`session_active`) | METRIC_002 Active Users (distinct user_id with in-window event) | dedup at `user_id`; survivorship (deleted-but-active users retained) |

`validate_handbook.py`'s grounding step proves each metric is dischargeable
against the warehouse (target table + every referenced column exists), and the
metrics reproduce the certified ledger keys `*_revenue_USD` and `*_active_users`.

If you instead want the literal example metrics, the ground truth needs a
`status` column and `test_` accounts added first — say so and I'll extend
`../ground-truth/` and re-target the handbook.
