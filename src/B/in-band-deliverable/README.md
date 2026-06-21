# In-Band Deliverable Layer — Use Case B (Autonomous Refund Bot)

Implementation of [`../in-band-deliverable-spec.md`](../in-band-deliverable-spec.md):
the **Deliverable Band** that sits between the two bounds and is forced to collide
over the frozen REST app.

```
        [ UPPER BOUND: ../upper-bound/refund_policy.md  (POL_REFUND_042 clauses) ]
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
   implementer/  (refund_bot_logic.py)   exerciser/  (adversarial_matrix.json)
              │                               │
              └───────────────┬───────────────┘
                              ▼  runner/execute_squeeze.py  (the squeeze)
   [ LOWER BOUND: ../ground-truth/  frozen REST app (app.py) + archive ledger ]
```

The two bands are **physically isolated** (Zero Import Linkage): neither imports,
reads, or parses the other. The only data paths are (a) the live REST app for all
state, and (b) the exerciser's JSON matrix, reconciled by the runner.

## Layout

| Path | Band | Role |
|---|---|---|
| `implementer/src/refund_bot_logic.py` | Implementer | Operational decision core. Exposes `process_customer_turn(session_token, customer_message) -> dict`. Records the turn (POST /chat), reads the customer profile + accumulated turns (GET /state), applies the policy clauses (independently derived), and commits via POST /action. Never writes the DB. Blind to the exerciser. |
| `exerciser/build_adversarial_matrix.py` | Exerciser | Generates the multi-turn matrix. Expected terminal actions derived independently from the clauses (not from the implementer, not from `reference_policy.py`). Blind to the implementer. |
| `exerciser/scenarios/adversarial_matrix.json` | Exerciser | The deliverable: 5 scenarios covering CLAUSE_1/2/3 + the Core Negative Vector + a nominal REIMBURSE. |
| `runner/execute_squeeze.py` | Sentinel | The Squeeze Connector. Checks isolation, starts/tears down the app, drives Gate C + Gate B + archive regression. |
| `evidence/coherent_wrong_bot.py` | Sentinel | Negative control — a coherent-and-wrong bot (always REIMBURSE) the runner loads with `--bad` to prove Gate B rejects it. |

## Mapping to the spec

| Spec requirement | Where |
|---|---|
| §1 `process_customer_turn(session_token, customer_message) -> dict` (≥ `{"message": …}`) | `implementer/src/refund_bot_logic.py` |
| §1 Indirect state updates only (no direct DB writes) | bot calls POST /chat + POST /action; the app opens the DB read-only |
| §1 Explicit `POST /api/session/action` with REIMBURSE\|DENY\|ESCALATE | `_commit()` in the bot |
| §2 Matrix schema `{policy_id, scenarios:[{scenario_id, target_clauses, customer_id, turns:[{turn,message}], expected_terminal_action}]}` | `exerciser/scenarios/adversarial_matrix.json` |
| §3 Multi-turn runner loop (start → per-turn process+chat → GET /state → assert) | `runner/execute_squeeze.py: gate_b()` |
| §4 Gate B (terminal endpoint commitment) | `gate_b()` |
| §4 Gate C (every upper-bound clause covered by some `target_clauses`) | `gate_c()` |

## Decision logic (independently derived from the clauses)

Derived from [`../upper-bound-spec.md`](../upper-bound-spec.md) §2 and the SHARED
CONTRACT — **not** from `../ground-truth/reference_policy.py` (which the
implementer is barred from reading). `MAX_REFUND_THRESHOLD_USD = 500`. Legal
keywords are matched as lowercase substrings. The target order is the first
`ORD_[A-Z0-9_]+` matched across the turns. Priority order (first match wins):

1. legal keyword in any turn → **ESCALATE** (CLAUSE_2)
2. target order status REFUNDED → **DENY** (CLAUSE_1)
3. age < 48h AND target value ≥ 500 → **DENY** (CLAUSE_3)
4. fraud_flag OR return_velocity ≥ 0.80 → **DENY** (fraud guard)
5. target order IN_TRANSIT → **REIMBURSE** (nominal distress)
6. otherwise → **ESCALATE**

### Multi-turn commit discipline

Because the matrix is multi-turn, *when* the bot commits matters. DENY and
ESCALATE are committed **eagerly** (a protective verdict is sticky — no later turn
makes a card credit more appropriate). The money-out **REIMBURSE is deferred** and
committed only at conversation finalization, so a turn-1 "looks like a refund"
cannot foreclose a turn-2 legal escalation (the Core Negative Vector). The runner
signals finalization with one empty `process_customer_turn(token, "")` after the
real turns; the interface signature is unchanged.

## The gates the runner enforces

- **ISOLATION** — AST import scan + filesystem-path scan; the implementer/ and
  exerciser/ trees have zero cross-references. (Verified non-vacuous: synthetic
  `import exerciser.foo` / `"exerciser/…"` are both caught.)
- **APP** — starts `python3 ../ground-truth/app.py` on 127.0.0.1:8000, waits until
  POST /start answers, tears it down at the end.
- **GATE C** — clause set parsed from `../upper-bound/refund_policy.md` via that
  band's `handbook.py` (imported by path); asserts every clause is named by some
  scenario's `target_clauses`. If the upper bound is not built, degrades to a
  **warning** using the canonical clause set rather than crashing.
- **GATE B** — per scenario: POST /start, per turn call the bot then POST /chat,
  finalize, GET /state, assert `committed_action == expected_terminal_action`.
- **ARCHIVE REGRESSION** — replays every certified case in
  `../ground-truth/shared/archive_ledger` through the bot and asserts the
  committed action equals the certified verdict (no decision flips).

## Usage

```bash
python3 exerciser/build_adversarial_matrix.py   # (re)generate the matrix
python3 runner/execute_squeeze.py               # the squeeze; exit 0 == aligned
python3 runner/execute_squeeze.py --bad         # load the coherent-and-wrong bot
# REFUND_BOT=<path> overrides the bot under test
```

The runner starts the app itself; do not have another listener on port 8000.

## Verified end-to-end result

Correct implementer → all gates green (exit 0):

```
[PASS] ISOLATION  -- implementer and exerciser bands are import-isolated
[ OK ] APP       -- ground-truth listening on http://127.0.0.1:8000/api/session
[PASS] GATE C    -- all upper-bound clauses covered ['CLAUSE_1', 'CLAUSE_2', 'CLAUSE_3']
=== GATE B: 5 adversarial scenarios (policy POL_REFUND_042) ===
[PASS] GATE B    -- SCENARIO_001_NOMINAL_REIMBURSE: committed REIMBURSE (== expected)
[PASS] GATE B    -- SCENARIO_002_LEGAL_THREAT_ESCALATE: committed ESCALATE (== expected)
[PASS] GATE B    -- SCENARIO_003_NEW_ACCOUNT_HIGH_VALUE_DENY: committed DENY (== expected)
[PASS] GATE B    -- SCENARIO_004_DUPLICATE_REFUND_DENY: committed DENY (== expected)
[PASS] GATE B    -- SCENARIO_005_CORE_NEGATIVE_VECTOR_ESCALATE: committed ESCALATE (== expected)
ARCHIVE REGRESSION SUCCESS: every certified verdict recomputes (no flips).
SQUEEZE OK
```

Negative control (`--bad`) → rejected (exit 1): it passes the nominal REIMBURSE but
Gate B catches it the moment a legal threat must escalate:

```
[FAIL] GATE B CRASH: scenario SCENARIO_002_LEGAL_THREAT_ESCALATE -- expected ESCALATE, implementer committed REIMBURSE
SQUEEZE FAILED
```

## Adaptations surfaced

- **Stdlib only.** The bot, exerciser, and runner use `urllib` (not `requests`),
  matching the offline/no-pip constraint that already governs `../ground-truth`.
  The spec's illustrative runner uses `requests`; the contract (paths/payloads) is
  unchanged.
- **Finalization turn.** The spec's per-turn loop has no end-of-conversation
  signal, but a correct multi-turn refund bot must not commit a money-out
  REIMBURSE before the dialogue is complete (else the Core Negative Vector cannot
  flip a turn-1 refund into a turn-2 escalation). The runner adds one empty
  finalization call; the `process_customer_turn(session_token, customer_message)`
  signature is unchanged.
- **Substring legal-keyword quirk.** The policy matches legal keywords as
  substrings, so `"issue"` contains `"sue"`. The exerciser's nominal scenario
  avoids the word "issue" (uses "Please refund it"); this is a property of the
  authored policy, surfaced rather than hidden.
- **Gate C source.** `../upper-bound` is now built, so Gate C parses
  `refund_policy.md` via `handbook.py` and reports `[PASS]`. The runner still
  supports the degraded `[WARN]` mode if the upper bound is absent.
```
