# In-Band Deliverable Layer — Use Case A

Implementation of [`../in-band-deliverable-spec.md`](../in-band-deliverable-spec.md):
the **Deliverable Band** that sits between the two bounds and is forced to collide
over the warehouse.

```
        [ UPPER BOUND: ../upper-bound/metric_handbook.md (clauses) ]
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
   implementer/  (builds query)     exerciser/  (builds validation matrix)
              │                               │
              └───────────────┬───────────────┘
                              ▼  runner/execute_squeeze.py  (the squeeze)
        [ LOWER BOUND: ../ground-truth/ frozen SQLite DB + ledger ]
```

The two bands are **physically isolated** (Zero Import Linkage): neither imports,
reads, or parses the other; the only data paths are (a) read-only SQLite to the
warehouse and (b) JSON strings reconciled by the runner (Strict Serialization).

## Layout

| Path | Band | Role |
|---|---|---|
| `implementer/src/compute_metric.py` | Implementer | Stateless analytical engine. `--metric/--start/--end` (or `METRIC_ID`/`START_DATE`/`END_DATE`); emits one JSON line `{metric_id, value, window, execution_utc_timestamp}`. Reads only the read-only DB. Blind to the tests. |
| `exerciser/build_validation_matrix.py` | Exerciser | Independently computes expected values from the DB + handbook clauses (not hand-typed) and emits the matrices. Blind to the implementer. |
| `exerciser/tests/validation_matrix.*.json` | Exerciser | The deliverable: `positives` (expected values) + `negatives` (a named mutation per clause, with an edge-case-bearing window). |
| `runner/mutations.py` | Sentinel | Mutation catalog — clause-violating variant queries used to exercise negatives. |
| `runner/execute_squeeze.py` | Sentinel | The Squeeze Connector. Runs the implementer as a subprocess, reads the exerciser JSON, drives the gates. |

## Usage

```bash
# Prereqs: ../ground-truth built, ../upper-bound present.
python3 exerciser/build_validation_matrix.py     # (re)generate the matrices
python3 runner/execute_squeeze.py                # run the squeeze; exit 0 == aligned
```

The runner resolves the implementer at the spec's deployed path
`/home/implementer/src/compute_metric.py`, falling back to the repo copy;
`COMPUTE_METRIC=<path>` overrides it.

## What the runner checks

- **ISOLATION** — implementer and exerciser bands have no import or path linkage
  to each other (spec Summary 1), verified by AST + path scan.
- **GATE C** (coverage, §3) — every obligation `CLAUSE_x` of the metric (read from
  the upper-bound handbook) is named by some test case's `target_clauses`.
- **GATE B positives** (§3) — the implementer's value equals the exerciser's
  expected value (a mismatch is the *coherent-and-wrong* crash); for quarter
  windows it also equals the certified `history_ledger.json` value (Total
  Additivity / the lower-bound invariant). So a passing positive ties all three
  layers together: ceiling, band, and floor agree on the number.
- **GATE B negatives** (§2 behavioral requirement) — each named mutation's value
  must **diverge** from the correct value over the same window. A mutation that
  failed to diverge would mean the clause is not load-bearing; the runner reports
  that as a vacuous-negative failure. This is the "proves WITH the clause, fails
  WITHOUT it" payoff.

## Verified behaviour

Correct implementer → `SQUEEZE OK` (exit 0): every positive matches expected and
ledger; every negative diverges, e.g.

- `OMIT_REFUND_SUBTRACTION`: 1987.21 → 2047.99 (gross; == ledger `Q1_gross_revenue`)
- `NO_TYPE_FILTER`: 1987.21 → 2108.77 (gross + refunds)
- `JOIN_EXCLUDE_DELETED`: 10 → 6 (survivorship: deleted-but-active users dropped)

Negative control — a coherent-and-wrong implementer that omits the refund
subtraction is caught:

```
[FAIL] GATE B CRASH (coherent-and-wrong): TC_M001_2025_Q1_STANDARD_RUN implementer=2047.99 exerciser=1987.21
SQUEEZE FAILED   (exit 1)
```

## Note on the spec's example (adaptation, surfaced)

The spec illustrates the matrix with a `COUNT_ALL_USERS_INCLUDING_TEST` mutation
over `test_`-prefixed accounts — data that does not exist in the ground truth.
As with the upper bound, the bands target the real warehouse (`events`/`users`),
and the mutations exercise the clauses that are actually load-bearing there (UTC
boundaries, event-type filtering, refund signing, user-id dedup, survivorship).
The schema (`metric_id` / `positives` / `negatives`, `target_clauses`,
`mutation`, `expected_fault{site,reason}`) follows the spec exactly.
