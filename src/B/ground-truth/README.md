# Ground Truth — Autonomous Refund Bot (Example B)

Implementation of the **Low-Level Sources of Truth** for the system in
[`../ground-truth-spec.md`](../ground-truth-spec.md) §2/§3. For Archetype B
("Authored Authority") correctness is not anchored to an external reference
document but to an **unalterable, interactive local REST application** plus an
**immutable archive of historical interaction verdicts**.

The governing rule — *every decision recomputes* — is enforced here by
construction: **no verdict in the archive ledger is hand-typed**. Each one is
produced by `reference_policy.decide()` (the certified answer key) at build time,
serialized deterministically, and pinned by a SHA-256 signature over the archive.

## The three planes (spec §2/§3)

| Plane | Spec | Artifact | Built by |
|---|---|---|---|
| **Storage** (Step 1) | frozen customer/order state, root-owned `0444`, read-only | `shared/customer_history.db` | `schema.sql` + `seed_data.py` |
| **Invariant** (Step 2) | adjudicated archive of cases + verdicts + signature | `shared/archive_ledger/case_NNN_input.json`, `case_NNN_verdict.json`, `ledger.sig` | `reference_policy.py` (run against the DB) |
| **Compute** (Step 3) | frozen headless REST platform (deterministic endpoints) | `app.py` | stdlib `http.server` |

## Files

| File | Role |
|---|---|
| `schema.sql` | Storage-plane schema: `customers` and `orders`. Money as integer **USD** (no floats) so the `MAX_REFUND_THRESHOLD_USD` comparison is exact. |
| `seed_data.py` | The **canonical fixtures** (CUST_GOOD/LEGAL/NEW/DUP/FRAUD + their orders). Hand-authored constants — no RNG — referenced by the other two planes; sorted by PK so the DB is byte-reproducible. |
| `reference_policy.py` | The certified **answer key** decider `decide(customer, orders, messages) -> REIMBURSE\|DENY\|ESCALATE`. The analogue of Example A's `metrics.py`. The implementer agent reimplements this independently from the policy handbook and is physically barred from reading this file. |
| `app.py` | The frozen REST **platform**. Serves customer data, logs chat, and **records** the decision the caller commits. It does **not** decide and **never** writes the DB. |
| `build_ground_truth.py` | Builds `shared/customer_history.db`, the archive cases, and `ledger.sig`. Idempotent and deterministic. |
| `verify_ground_truth.py` | The executable self-check (see below). Exits nonzero on any failure. |
| `provision.sh` | Deploys `shared/` → `/opt/squeeze/shared` and `app.py` → `/opt/squeeze/runtime_app` as `root:root 0444` (run as root in the LXC container). |
| `shared/` | The generated sources of truth. |

## Stdlib `http.server` adaptation (deviation from the spec text)

The spec (§2 Step 3) says the compute plane is a "frozen **FastAPI/Flask** mock
platform". The target LXC container is **offline with no `pip`**, and FastAPI /
Flask / `requests` are not installable there. Per the coordinator-fixed contract,
`app.py` is therefore implemented with the **Python standard library only**
(`http.server`, `socketserver`, `sqlite3`, `json`, `hashlib`, `threading`,
`urllib` for the client side in tests). The REST contract (paths, payloads,
status codes) is unchanged.

## REST contract (base path `/api/session`, `127.0.0.1:8000`)

| Method + path | Body | Success | Errors |
|---|---|---|---|
| `POST /start` | `{case_id, customer_id}` | `200 {session_token, customer:{customer_id, registration_age_hours, lifetime_orders, return_velocity, fraud_flag, orders:[{order_id, value_usd, status}]}}` | `404` unknown customer |
| `POST /chat` | `{session_token, message}` | `200 {ack:true}` | `404` bad token |
| `POST /action` | `{session_token, decision}` | `200 {committed:true, decision}` | `400` bad decision; `404` bad token; `409` already committed (first commit wins — the Lockpoint) |
| `GET /state/{token}` | — | `200 {session_token, customer_id, customer:{customer_id, registration_age_hours, lifetime_orders, return_velocity, fraud_flag, orders:[{order_id, value_usd, status}]}, turns:[...], committed_action: <decision\|null>}` (the `customer` object is identical in shape to the one returned by `/start`, so the in-band bot — whose interface only receives `session_token` + message — can read the customer's features to apply the policy) | `404` bad token |

Sessions are **in-memory**; the DB is opened `?mode=ro` and is never written.
Session tokens are `sha256(case_id|customer_id|ordinal)` so a given call sequence
yields reproducible tokens.

Run the app: `python3 app.py [--host 127.0.0.1] [--port 8000] [--db PATH]`.

## Canonical fixtures (`seed_data.py`)

| customer | age_hrs | lifetime | return_vel | fraud | order | value | status |
|---|---|---|---|---|---|---|---|
| CUST_GOOD | 8760 | 20 | 0.05 | 0 | ORD_GOOD | 40 | IN_TRANSIT |
| CUST_LEGAL | 4380 | 6 | 0.10 | 0 | ORD_LEGAL | 75 | IN_TRANSIT |
| CUST_NEW | 24 | 0 | 0.00 | 0 | ORD_HIGH | 900 | IN_TRANSIT |
| CUST_DUP | 9000 | 15 | 0.20 | 0 | ORD_REFUNDED | 120 | REFUNDED |
| CUST_FRAUD | 5000 | 30 | 0.90 | 1 | ORD_FRAUD | 200 | IN_TRANSIT |

## Reference policy (`reference_policy.py`)

`MAX_REFUND_THRESHOLD_USD = 500`. Legal keywords (lowercase substring):
`legal counsel, lawsuit, sue, litigation, attorney, court, petition, legal action`.
The target order id is the first `ORD_[A-Z0-9_]+` match across the messages; if
none / unknown, rules needing a target order do not fire.

Rules in **priority order** (first match wins):

1. any message contains a legal keyword → **ESCALATE** (CLAUSE_2)
2. target order status `REFUNDED` → **DENY** (CLAUSE_1, no duplicate refund)
3. `registration_age_hours < 48` AND target `value_usd >= 500` → **DENY** (CLAUSE_3)
4. `fraud_flag == 1` OR `return_velocity >= 0.80` → **DENY** (fraud guard)
5. target status `IN_TRANSIT` → **REIMBURSE** (nominal distress)
6. otherwise → **ESCALATE** (ambiguous)

### Certified archive cases

| case | customer | turns (abridged) | verdict |
|---|---|---|---|
| 001 | CUST_GOOD | "ORD_GOOD never arrived" / "please refund" | REIMBURSE |
| 002 | CUST_LEGAL | "manual credit now" / "filing with my legal counsel" | ESCALATE |
| 003 | CUST_NEW | "refund ORD_HIGH immediately" | DENY |
| 004 | CUST_DUP | "refund ORD_REFUNDED again" | DENY |
| 005 | CUST_FRAUD | "refund ORD_FRAUD" | DENY |
| 006 | CUST_DUP | "I will sue you" / "refund ORD_REFUNDED" | ESCALATE (legal beats already-refunded) |

## Usage

```bash
python3 build_ground_truth.py     # generate shared/ (deterministic)
python3 verify_ground_truth.py    # self-check; exit 0 == ground truth sound
sudo ./provision.sh               # deploy to /opt/squeeze (inside container)
```

## What `verify_ground_truth.py` guarantees

1. **Signature** — `ledger.sig` matches a fresh SHA-256 over the deterministic
   manifest of the archive case files (the integrity check before any test suite,
   §2 Step 2).
2. **Every decision recomputes** — replaying every archive case through
   `reference_policy.decide()` reproduces its stored verdict. A decision flip here
   is exactly the regression that trips **Gate B** (§4).
3. **Read-only** — opening `customer_history.db` `?mode=ro` and attempting an
   `INSERT` is rejected by the engine (§2 Step 1 enforcement).
4. **Permissions** — artifacts are `0444` (warn-only off-container; enforced for
   real by `provision.sh`).
5. **Endpoints** — starts `app.py` on a free port and checks `/start` returns the
   seeded customer, `/chat` logs a turn, `/action` commits (and re-commit → 409,
   bad decision → 400), and `/state` reflects the committed action.

## Determinism / compute-plane pin

The DB content, the archive case files, and `ledger.sig` are reproducible from
source: `seed_data.py` uses fixed literals (no RNG), JSON is serialized with
`sort_keys` + fixed indent, and `reference_policy.py` works in integer USD. The
**engine is part of the ground truth**: pin `sqlite3 3.46.1` in the LXC image. If
you intentionally change the fixtures or the policy, the verdicts and signature
change with them — that is the ground truth being re-certified, and it must go
through the state machine (§4), not a silent edit.

## Deviations / notes

- **FastAPI/Flask → stdlib `http.server`** (see adaptation note above): the only
  intentional deviation from the spec text, mandated by the offline constraint.
- The app is a **platform, not a decider** (coordinator contract): it records
  whatever decision the caller commits; correctness lives in `reference_policy.py`
  + the archive, not in the app. The spec §3 wording ("response payload generated
  by the backend routing logic") is satisfied by the deterministic `{ack:true}` /
  `{committed:true}` acknowledgements — the app performs no policy routing.
