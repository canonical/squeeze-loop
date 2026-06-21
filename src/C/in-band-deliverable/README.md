# In-Band Deliverable Layer — Use Case C (API Contract Guard)

Implementation of [`../in-band-deliverable-spec.md`](../in-band-deliverable-spec.md):
the **Deliverable Band** (split planes) that sits between the two bounds and is
forced to collide over the frozen lower bound (the document-plane linter + TY0
baseline) and a live localhost runtime.

```
        [ UPPER BOUND: ../upper-bound/api_policy_manifest.md  (API_POLICY_081 clauses) ]
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
   implementer/  (main.py + openapi.json)   exerciser/  (test_matrix.json)
              │                               │
              └───────────────┬───────────────┘
                              ▼  runner/execute_squeeze.py  (the squeeze)
   [ LOWER BOUND: ../ground-truth/  linter.py + base_schema.json + ty0_baseline.json ]
```

The two bands are **physically isolated** (Zero Import Linkage): neither imports,
reads, or parses the other. The only reconciliation paths are (a) the live HTTP
runtime the runner boots from the implementer's `main.py`, and (b) the exerciser's
JSON matrix — joined by the runner.

## Layout

| Path | Band | Role |
|---|---|---|
| `implementer/src/main.py` | Implementer | The stdlib `http.server` implementation of the full Profile API contract, derived independently from the clauses + `base_schema.json`. CLI `python3 main.py --port 8000 --db <path>`. Global exception guard → constant clean 400 (no trace). Maps to `user_uuid`; the integer `id` is never loaded. Blind to the exerciser. |
| `implementer/src/openapi.json` | Implementer | The implementer's public contract doc, aligned with `base_schema.json` (same routes / security / response shapes); passes the ground-truth linter. |
| `exerciser/build_test_matrix.py` | Exerciser | Generates the conformance matrix. Expected statuses / key sets derived independently from the clauses — not from `main.py`, not from `reference_server.py`. Blind to the implementer. |
| `exerciser/conformance/test_matrix.json` | Exerciser | The deliverable: 5 cases covering CLAUSE_1/2/3 + the Core Negative Vector. |
| `runner/execute_squeeze.py` | Sentinel | The Squeeze Connector: ISOLATION → GATE C → boot server → GATE B → DOCUMENT PLANE → TY0. |
| `evidence/coherent_wrong_server.py` | Sentinel | Negative control — a coherent-and-wrong server the runner loads with `--bad`. |

## The API contract (served on 127.0.0.1:8000)

Auth is the `X-API-Key` header; configured key `test_secure_token_abc123` → `u-0001`.

| Method + path | Auth | Body | Success | Errors |
|---|---|---|---|---|
| `POST /api/v1/profile/update` | `X-API-Key` | `{display_name:<non-empty str>}` | `200 {status,user_uuid,updated_at}` (in-memory) | `400 {error,message}` malformed; `401 {error,message}` bad key |
| `GET /api/v1/profile` | `X-API-Key` | — | `200 {user_uuid,display_name,updated_at}` (no `id`) | `401 {error,message}` |
| unknown route | — | — | — | `404 {error,message}` |
| any internal error | — | — | — | clean `400 {error,message}`, never a trace |

The DB is opened `?mode=ro` and snapshotted into memory at boot; updates mutate the
in-memory overlay only, so the file is never written.

## Decision logic (independently derived from the clauses)

Derived from [`../upper-bound-spec.md`](../upper-bound-spec.md) §2 and the SHARED
CONTRACT — **not** from `../ground-truth/reference_server.py` (the implementer is
barred from reading it):

- **CLAUSE_1** — mutations require a non-empty, configured `X-API-Key`; auth is
  checked *before* any body parsing, so a missing/empty/wrong key → `401`.
- **CLAUSE_2** — the integer `id` column is never `SELECT`ed into the in-memory
  store, so it cannot appear on the wire; only `user_uuid` is exposed.
- **CLAUSE_3** — every error body is a hand-written constant (never built from an
  exception), and `_dispatch` wraps every request in a global `try/except` that
  converts *any* unexpected exception to a constant clean 400 — no traceback /
  file path / source line / SQL / `sqlite3.` text can reach the client.

## The gates the runner enforces

- **ISOLATION** — AST import scan + filesystem-path scan; `implementer/` and
  `exerciser/` have zero cross-references.
- **GATE C** — clause set parsed from `../upper-bound/api_policy_manifest.md` via
  that band's `handbook.py` (`handbook.parse(...)[0].clause_ids`, imported by
  path); asserts every clause is named by some case's `target_clauses`. Degrades
  to a **warning** with the canonical set if the upper bound is absent.
- **SERVER** — boots `implementer/src/main.py` on 127.0.0.1:8000, waits until the
  socket binds, tears it down at the end.
- **GATE B (runtime plane)** — per case: send method+path+headers+payload via
  `urllib`; assert `status == expected_status`, the response key set ==
  `expected_schema_keys`, and no `forbidden_string_patterns` appear. Any mismatch
  is a GATE B CRASH.
- **DOCUMENT PLANE** — lints `implementer/src/openapi.json` with the ground-truth
  `linter.py` (imported by path) and cross-checks it declares every (non-404)
  route the tests hit (no-blend doc side).
- **TY0 REGRESSION** — loads `../ground-truth/shared/ty0_baseline.json` and asserts
  `openapi.json` preserves every legacy route signature (method, path,
  response-keys-by-status) — no silent drop/mutation.

## Usage

```bash
python3 exerciser/build_test_matrix.py   # (re)generate the matrix
python3 runner/execute_squeeze.py        # the squeeze; exit 0 == aligned
python3 runner/execute_squeeze.py --bad  # load the coherent-and-wrong server
# SERVER_CMD="python3 <path>" overrides the server under test
```

The runner boots the server itself; do not have another listener on port 8000.

## Verified end-to-end result

Correct implementer → all gates green (exit 0):

```
[PASS] ISOLATION  -- implementer and exerciser bands are import-isolated
[PASS] GATE C    -- all upper-bound clauses covered ['CLAUSE_1', 'CLAUSE_2', 'CLAUSE_3']
[ OK ] SERVER    -- listening on http://127.0.0.1:8000
=== GATE B: 5 conformance cases (policy API_POLICY_081) ===
[PASS] GATE B    -- TC_001_AUTHENTICATED_MUTATION: 200 ['status', 'updated_at', 'user_uuid'] ['CLAUSE_1']
[PASS] GATE B    -- TC_002_UNAUTHENTICATED_REJECTION: 401 ['error', 'message'] ['CLAUSE_1']
[PASS] GATE B    -- TC_003_DECOUPLED_PROFILE_READ: 200 ['display_name', 'updated_at', 'user_uuid'] ['CLAUSE_2']
[PASS] GATE B    -- TC_004_TRACEBACK_EXFILTRATION_ATTEMPT: 400 ['error', 'message'] ['CLAUSE_3']
[PASS] GATE B    -- TC_005_CORE_NEGATIVE_VECTOR: 401 ['error', 'message'] ['CLAUSE_1', 'CLAUSE_3']
GATE B SUCCESS: runtime plane aligns with the conformance matrix.
[PASS] DOC PLANE  -- openapi.json passes the ground-truth linter
[PASS] DOC PLANE  -- openapi.json declares every route the tests exercise
[PASS] TY0       -- openapi.json preserves all 2 legacy route signatures
[ OK ] SERVER    -- torn down
SQUEEZE OK: ISOLATION + GATE C + GATE B + DOCUMENT-PLANE + TY0 all green.
```

Negative control (`--bad`) → rejected (exit 1): it passes the nominal mutation and
the unauth rejection, then Gate B catches the leaked internal `id` key on the
profile read (a CLAUSE_2 violation). The same server also leaks a raw traceback on
malformed input (CLAUSE_3); the runner stops at the first crash:

```
[PASS] GATE B    -- TC_001_AUTHENTICATED_MUTATION: 200 ['status', 'updated_at', 'user_uuid'] ['CLAUSE_1']
[PASS] GATE B    -- TC_002_UNAUTHENTICATED_REJECTION: 401 ['error', 'message'] ['CLAUSE_1']
[FAIL] GATE B CRASH: TC_003_DECOUPLED_PROFILE_READ key-set mismatch -- expected ['display_name', 'updated_at', 'user_uuid'], got ['display_name', 'id', 'updated_at', 'user_uuid']
SQUEEZE FAILED
```

## Adaptations surfaced

- **Stdlib only.** Server is `http.server`/`BaseHTTPRequestHandler`; the runner's
  client is `urllib` (not `requests`); `sqlite3`/`json` for state. This matches the
  offline/no-pip constraint that already governs `../ground-truth`. The spec's
  illustrative runner uses `requests` and FastAPI; the HTTP contract
  (paths/headers/payloads/status) is unchanged.
- **Lower bound is split, not a frozen REST app.** Unlike Use Case B (whose runner
  boots a frozen `app.py`), here the runner boots the *implementer's own* `main.py`
  as the runtime plane and uses the ground truth only as the document plane
  (`linter.py`, `base_schema.json`) and the TY0 baseline. Gate B (runtime) and the
  document-plane + TY0 checks are therefore the C analogue of B's Gate B + archive
  regression.
- **Core Negative Vector status is 401, not 400.** The manifest's expected defense
  is "400 *or* 401". Because auth is correctly checked before body parsing, an
  unauthenticated + malformed POST returns `401`; `TC_005` pins that exact status
  and still asserts zero leaked patterns. (A server that parsed the body before
  authenticating — and leaked a trace — would fail this case.)
- **Gate C order.** Gate C is evaluated before booting the server (it is a static
  coverage check), so a coverage deficiency fails fast without a live process.
- **Gate C source present.** `../upper-bound` is built, so Gate C parses
  `api_policy_manifest.md` via `handbook.py` and reports `[PASS]`; the degraded
  `[WARN]` path is retained for when the upper bound is absent.
```
