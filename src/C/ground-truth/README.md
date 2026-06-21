# Ground Truth — API Contract Guard (Use Case C, Split Planes)

Implementation of the **Low-Level Sources of Truth** (the executable lower bound)
for the system in [`../ground-truth-spec.md`](../ground-truth-spec.md). Archetype C
("Split Planes") splits correctness across two independent, non-blending tracks:

- a **Document Plane** (static): the canonical OpenAPI-style contract
  `base_schema.json`, validated by a pinned local linter; and
- a **Runtime Plane** (dynamic): a live HTTP server whose behavior must match that
  contract exactly.

The **No-Blend invariant** (§3) is enforced by construction here: nothing in the
runtime code is read by the document linter, and the document contract is never
trusted to excuse a runtime failure. The TY0 baseline (§4) freezes the legacy
route/column signatures so a silent mutation on an unrelated route is detected.

## The two planes (spec §2) + Item Zero (§4)

| Plane / step | Spec | Artifact | Built by |
|---|---|---|---|
| **Document** (Plane 1) | canonical contract, root-owned `0444`, linted | `shared/base_schema.json` | `base_schema.json` source, re-serialized byte-stably |
| **Runtime** (Plane 2) | live server on `127.0.0.1:8000`, clean errors, read-only DB | `reference_server.py` + `run_server.sh` | stdlib `http.server` |
| **Storage** (Plane 2 backing) | frozen users/api_keys, root-owned `0444`, read-only | `shared/app_state.db` | `schema.sql` + `seed_data.py` |
| **Item Zero / TY0** (§4) | content-hashed route+column reflection baseline | `shared/ty0_baseline.json` | `reflection.py` (run against the contract + DB) |

## Files

| File | Role |
|---|---|
| `schema.sql` | Storage schema: `users(id, user_uuid, display_name, updated_at)` + `api_keys(api_key, user_uuid)`. The integer `id` is internal and never serialized. |
| `seed_data.py` | The **canonical fixtures** (u-0001/2/3 + the one API key). Hand-authored constants — no RNG — sorted by PK so the DB is byte-reproducible. |
| `base_schema.json` | The canonical **document-plane contract** (OpenAPI 3.0 style): the two routes, their `X-API-Key` security, request/response schemas, and the 200/400/401/404 shapes. The implementer's `openapi.json` must align with this; the exerciser derives tests from it. |
| `linter.py` | The **document-plane compute engine** (§2 Plane 1): validates a schema file (well-formed JSON; every route has methods, typed request/response schemas, documents its error responses, no blank required descriptions). Exits nonzero on a malformed/incomplete schema. |
| `reference_server.py` | The **runtime-plane answer key** (§2 Plane 2): the correct stdlib `http.server` implementation of the full contract — auth, validation, in-memory mutation over a read-only DB, global exception guard (no leaks), maps to `user_uuid` not `id`. |
| `run_server.sh` | Boots `reference_server.py` bound to `127.0.0.1:8000` (override with `PORT=`). |
| `reflection.py` | The pinned **TY0 reflection engine** (§4): logs every route signature (method, path, response-keys-by-status) + DB columns, and hashes a deterministic manifest. Imported by both build and verify so the baseline can never be hand-typed. |
| `build_ground_truth.py` | Builds `shared/app_state.db` (0444), `shared/base_schema.json`, and `shared/ty0_baseline.json`. Idempotent and byte-deterministic. |
| `verify_ground_truth.py` | The executable self-check (see below). Exits nonzero on any failure. |
| `provision.sh` | Deploys `shared/` → `/opt/squeeze/shared` and the server → `/opt/squeeze/runtime_app` as `root:root 0444` (run as root in the LXC container; idempotent, root-guarded). |
| `shared/` | The generated sources of truth. |

## Stdlib `http.server` adaptation (deviation from the spec text)

The spec text (§2 Plane 2, §5) mentions **FastAPI + Uvicorn** and a `requests`
client. The target LXC container is **offline with no `pip`**, so those are not
installable. Per the coordinator-fixed contract, the runtime plane is implemented
with the **Python standard library only**: `http.server` /
`BaseHTTPRequestHandler` / `socketserver` (server), `urllib` (client in tests),
`sqlite3`, `json`, `datetime`, `re`, `hashlib`. The HTTP contract (paths, headers,
payloads, status codes) is unchanged — this is the only intentional deviation.

## The API contract (base path `/api/v1`, `127.0.0.1:8000`)

Auth is the header `X-API-Key`. The configured key `test_secure_token_abc123`
identifies seeded user `u-0001`.

| Method + path | Auth | Body | Success | Errors |
|---|---|---|---|---|
| `POST /api/v1/profile/update` | `X-API-Key` | `{display_name: <non-empty str>}` | `200 {status, user_uuid, updated_at}` (in-memory mutation only) | `400 {error,message}` malformed body; `401 {error,message}` missing/empty/wrong key |
| `GET /api/v1/profile` | `X-API-Key` | — | `200 {user_uuid, display_name, updated_at}` (no integer `id`) | `401 {error,message}` |
| any unknown route | — | — | — | `404 {error,message}` |
| any unexpected internal error | — | — | — | clean JSON `{error,message}`, never a traceback |

The 400 error body MUST NOT contain a traceback, file path, source line, SQL, or
`sqlite3.` text. This is enforced because error bodies are hand-written constants
(never derived from an exception) and every request is wrapped in a global
exception guard.

`user_uuid` is always the public UUID; the internal integer `id` is **never** put
on the wire.

## Data model (`app_state.db`)

| table | columns | seed |
|---|---|---|
| `users` | `id` (internal PK, never serialized), `user_uuid` (public), `display_name`, `updated_at` | `(1,'u-0001','Ada Lovelace',…)`, `(2,'u-0002','Alan Turing',…)`, `(3,'u-0003','Grace Hopper',…)` |
| `api_keys` | `api_key`, `user_uuid` | `('test_secure_token_abc123','u-0001')` |

The DB is opened `?mode=ro` and is **never written**: profile updates accumulate in
an in-memory overlay for the process lifetime, so the on-disk ground truth stays
immutable and the build stays byte-deterministic. (A live update returns a
request-time `updated_at`; that value may vary — tests check response *keys*, not
the timestamp value.)

## Item Zero / TY0 (`ty0_baseline.json`)

The TY0 snapshot is the route-reflection of the legacy trunk: the canonical route
signatures (`method`, `path`, `responses` = response-keys-by-status, derived from
`base_schema.json`) plus the DB `db_columns`, with a `"hash"` = SHA-256 over a
deterministic manifest of that snapshot. `verify_ground_truth.py` re-runs the
reflection and asserts the hash recomputes — the "every signature recomputes"
invariant. A silent structural mutation on any route or column flips the hash and
blocks deployment (§4).

## Usage

```bash
python3 build_ground_truth.py     # generate shared/ (deterministic)
python3 verify_ground_truth.py    # self-check; exit 0 == ground truth sound
python3 linter.py shared/base_schema.json   # document-plane lint (also runs in verify)
./run_server.sh                   # boot the runtime plane on 127.0.0.1:8000
sudo ./provision.sh               # deploy to /opt/squeeze (inside container)
```

## What `verify_ground_truth.py` guarantees

1. **Lint** — `base_schema.json` passes the document-plane linter.
2. **TY0 recomputes** — the stored `ty0_baseline.json` hash matches a freshly
   recomputed reflection (the §4 invariant).
3. **Read-only** — opening `app_state.db` `?mode=ro` and attempting an `INSERT` is
   rejected by the engine (§2 Plane 2 enforcement).
4. **Permissions** — artifacts are `0444` (warn-only off-container; enforced for
   real by `provision.sh`).
5. **Endpoints** — boots `reference_server.py` on a free port and checks the
   canonical behaviors: authed `POST update` → 200 `{status,user_uuid,updated_at}`;
   unauthenticated/wrong-key `POST` → 401 `{error,message}`; malformed `POST` →
   400 `{error,message}` containing **none** of `[Traceback, 'File "', 'line ',
   sqlite3., SELECT]`; authed `GET profile` → 200 with `user_uuid` and **no** `id`
   key; unauthenticated `GET` → 401; unknown route → 404. Then it tears the server
   down.

## Determinism / compute-plane pin

`app_state.db`, `base_schema.json`, and `ty0_baseline.json` are byte-reproducible
from source: `seed_data.py` uses fixed literals (no RNG), all JSON is serialized
with `sort_keys` + fixed indent, and the TY0 manifest is canonically serialized.
The **engine is part of the ground truth**: pin `sqlite3 3.46.1` in the LXC image.
If you intentionally change the fixtures, the contract, or the routes, the DB /
schema / TY0 hash change with them — that is the ground truth being re-certified,
and it must go through the gate state machine (§5), not a silent edit.

## Deviations / notes

- **FastAPI/Uvicorn/requests → stdlib `http.server` + `urllib`** (see adaptation
  note above): the only intentional deviation from the spec text, mandated by the
  offline constraint.
- The runtime plane is a **frozen answer key**, not the agent's code: it defines
  the correct runtime behavior the implementer's server is squeezed against and the
  exerciser derives conformance tests for (No-Blend, §3).
- Mutations are **in-memory only**; the DB file is never written, keeping the
  ground truth immutable and the rebuild byte-identical.
```
