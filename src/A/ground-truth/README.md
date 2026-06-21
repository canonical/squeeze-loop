# Ground Truth — Squeeze-Loop Analytics Engine

Implementation of the **Low-Level Sources of Truth** for the system in
[`../ground-truth-spec.md`](../ground-truth-spec.md) §2. These three planes are
the executable lower bound the whole squeeze loop is squeezed against: the data
the agents query, the certified baseline their results may never silently move,
and the frozen engine that makes every number reproducible.

The governing rule of the *"Every number recomputes"* workflow is enforced here
by construction: **no figure in the baseline ledger is hand-typed** — each is
computed by read-only SQL (`metrics.py`) against the warehouse, serialized
deterministically, and pinned by a SHA-256 signature.

## The three planes (spec §2)

| Plane | Spec | Artifact | Built by |
|---|---|---|---|
| **Storage** (Step 1) | raw transaction event log, root-owned `0444` | `shared/base_warehouse.db` | `schema.sql` + `seed_data.py` |
| **Invariant** (Step 2) | certified baseline metrics + signature | `shared/history_ledger.json`, `shared/history_ledger.sig` | `metrics.py` (queried against the DB) |
| **Compute** (Step 3) | frozen SQLite engine, no overrides | the pinned `sqlite3` (3.46.1) | container image; opened `?mode=ro` |

## Files

| File | Role |
|---|---|
| `schema.sql` | Storage-plane schema. UTC ISO-8601 timestamps (lexicographic = chronological); money as integer **cents** (no floats in the warehouse). |
| `seed_data.py` | Deterministic event generator — a fixed LCG, **no stdlib RNG**, so the warehouse is byte-reproducible. Includes quarter-boundary witnesses. |
| `metrics.py` | The single read-only definition of every certified number, and the byte-stable JSON serializer. Imported by both builder and verifier. |
| `build_ground_truth.py` | Builds the three artifacts into `shared/`. Idempotent and deterministic. |
| `verify_ground_truth.py` | The executable self-check (see below). Exits nonzero on any failure. |
| `provision.sh` | Deploys `shared/` into `/opt/squeeze/shared` as `root:root 0444` (run as root in the LXC container). |
| `shared/` | The generated sources of truth. |

## Usage

```bash
python3 build_ground_truth.py     # generate shared/ (deterministic)
python3 verify_ground_truth.py    # self-check; exit 0 == ground truth sound
sudo ./provision.sh               # deploy to /opt/squeeze/shared (inside container)
```

## What `verify_ground_truth.py` guarantees

1. **Signature** — `sha256(history_ledger.json)` equals `history_ledger.sig`
   (the integrity check `gate_sentinel.py` runs before any test suite, §2 Step 2).
2. **Recompute == ledger** — re-running the metric queries against the warehouse
   reproduces `history_ledger.json` **byte-for-byte**. This is the **Total
   Additivity** invariant of Gate B (§5): if a past metric shifts by a single
   byte, this fails.
3. **Read-only** — opening the warehouse with `?mode=ro` and attempting an
   `INSERT` is rejected by the engine (§2 Step 1 enforcement).
4. **Permissions** — artifacts are `0444` (warn-only off-container, where we are
   not root; enforced for real by `provision.sh`).

## Certified metrics

Per past quarter (`2025_Q1`…`2025_Q4`), the ledger certifies:

- `*_gross_revenue_USD` — Σ purchase amounts
- `*_refunds_USD` — Σ refund amounts
- `*_revenue_USD` — net (`gross − refunds`)
- `*_purchase_count` — number of purchase events
- `*_active_users` — `COUNT(DISTINCT user_id)` with ≥1 event in the quarter
- `*_new_users` — signups in the quarter

Two edge cases are baked into the data so the downstream Gate C coverage map has
something real to catch (§5 Gate C):

- **Quarter/timezone boundaries** — purchases at `…03-31T23:59:59Z` and
  `…04-01T00:00:00Z` (UTC) observed from non-UTC regions; a query that bins by
  local time instead of the canonical UTC `ts` lands them in the wrong quarter.
- **Survivorship** — ~20% of users carry a `deleted_ts` but their rows (and the
  events before deletion) remain. `*_active_users` counts them; a query that
  inner-joins only currently-undeleted users undercounts.

## Determinism / compute-plane pin

`base_warehouse.db` content and `history_ledger.json`/`.sig` are reproducible
from source because `seed_data.py` uses a fixed LCG and `metrics.py` works in
integer cents. The **engine is part of the ground truth**: pin `sqlite3 3.46.1`
in the LXC image. A different engine version can change date/string/float edge
behaviour, which is exactly the drift Step 3 freezes out. If you intentionally
change the data or metric logic, the ledger and signature change with it — that
is the ground truth being re-certified, and it must go through the state machine
(§3), not a silent edit.
