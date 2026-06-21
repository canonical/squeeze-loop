# Upper Bound — API Contract Guard Policy Manifest

> **Purpose:** the API-governance manifest fixes the contract the service must
> honor (auth on mutations, expose UUIDs not internal ids, clean typed errors),
> so the runtime cannot quietly drift from its published behavior.

Implementation of the **Upper Bound Source of Truth** for the system in
[`../upper-bound-spec.md`](../upper-bound-spec.md), Use Case C (API Contract
Guard, **Archetype C — split planes**). The upper bound is the authored, citable
normative ceiling: it fixes the strongest claims the `implementer` (Document
Plane: the OpenAPI schema) and the `exerciser` (Runtime Plane: the live Python
web server) agents may assert. An agent whose mutation route accepts an empty
`X-API-Key`, leaks the internal integer id, or returns a traceback on a malformed
body has breached the ceiling.

It is the counterpart to [`../ground-truth/`](../ground-truth/) (the executable
floor): the manifest's clauses are grounded in the *same* system. The HTTP
contract elements the clauses name correspond to the real document-plane contract
in [`../ground-truth/base_schema.json`](../ground-truth/base_schema.json): the
`X-API-Key` header security scheme, the mutation route
`POST /api/v1/profile/update`, the public `user_uuid` field (never the internal
integer id), and the `400`/`401` error shapes carrying a clean `{error, message}`
JSON body.

## Files

| File | Role |
|---|---|
| `api_policy_manifest.md` | **The upper bound itself** — the normative ceiling, in the strict token-parsable schema of spec §2 (`# API_POLICY_MANIFEST_START … END`). Normative English only: no code, schema JSON, or implementation syntax. |
| `handbook.py` | The single parser + structural validator. Turns the manifest into `Manifest` objects (with `clause_ids`); `extract_block()` yields the per-manifest markdown the dispatch loop copies into `spec.txt` (§1). |
| `gate_checks.py` | The upper-bound-driven gate primitives (§3): `gate_a_policy_centric` (manifest stays WHAT-not-HOW) and `gate_c_coverage` (exerciser's matrix covers every `CLAUSE_n`). |
| `validate_handbook.py` | Self-check: structure + Gate A + **grounding** against `../ground-truth/base_schema.json` + gate wiring. Exits nonzero on failure. |
| `provision.sh` | Deploys `api_policy_manifest.md` to `/opt/squeeze/shared/api_policy_manifest.md` as `root:root 0444` (§1), refusing to deploy a malformed or non-policy-centric ceiling. |

## Usage

```bash
python3 handbook.py            # list the parsed manifest
python3 validate_handbook.py   # structure + Gate A + grounding + gate wiring; exit 0 == sound
python3 gate_checks.py         # pilot: Gate A / Gate C on good and bad inputs
sudo ./provision.sh            # deploy (inside the LXC container)
```

Python standard library only; deterministic.

## The schema (spec §2)

The manifest block declares, in fixed tokens the parser keys on:

- `# API_POLICY_MANIFEST_START` … `# API_POLICY_MANIFEST_END` markers
- `## MANIFEST_ID: API_POLICY_081`
- `**Architecture Category:**`, `**Target Interface Scope:**`, `**Status:**`
  (`BINDING` | `DRAFT` | `DEPRECATED`)
- `### 1. Plain English Core Property`
- `### 2. Enumerated Obligation Clauses` — `**CLAUSE_n:**` bullets
- `### 3. The Core Negative Vector` — `**Target Exploit:**` +
  `**Expected System Defense:**`
- `### 4. Explicit NOT-Claims` — `**NOT_CLAIM_n:**` bullets

`handbook.py` enforces: markers present, valid status, a non-empty core property,
clause ids that are **sequential `CLAUSE_1..N`** (≥1), a negative vector with both
a target exploit and an expected defense, and at least one NOT-claim (so the
validation horizon is explicitly bounded). A malformed manifest raises
`HandbookError`.

### The three clauses (grounded in `../ground-truth/`)

| Clause | Obligation | Grounding in `base_schema.json` |
|---|---|---|
| `CLAUSE_1` | All mutations (`POST`/`PUT`/`PATCH`/`DELETE`) require a non-empty `X-API-Key`. | `securitySchemes.ApiKeyAuth` (header `X-API-Key`); `POST /api/v1/profile/update` carries `security: [ApiKeyAuth]`, `401` shape |
| `CLAUSE_2` | Expose `user_uuid` strings, never internal auto-increment integer ids. | `user_uuid` field on the `200` response schemas; the internal integer `id` is never serialized |
| `CLAUSE_3` | Validation failures return a clean `400` JSON `{error,message}` — no traceback / stack / SQL leak. | `400` response with `{error, message}` shape on the mutation route |

The **Core Negative Vector** (unauthenticated + malformed payload to the mutation
route → safe `400`/`401`, zero trace lines) is the live ground-truth probe: the
runtime-plane answer key returns `401`/`400` with a body containing none of
`[Traceback, 'File "', 'line ', sqlite3., SELECT]`.

## How the upper bound drives the gates (spec §3)

- **Gate A (Structural Plan Integrity)** — `gate_a_policy_centric(text)` blocks
  the compilation track if the published manifest contains code fragments
  (` ``` `, `def `, `import `, `class `), schema JSON (`{`-heavy blocks,
  `"type":`, `"properties":`, `"required":`), SQL/DDL (`SELECT `, `CREATE TABLE`,
  `INSERT INTO`), or web-framework route syntax (`@app.`, `@router.`). The
  manifest must state *what* the contract boundary is, never *how* a schema or
  server achieves it.
- **Gate C (Structural Coverage Map)** — `gate_c_coverage(manifest, matrix)` reads
  the exerciser's `test_matrix.json` and fails the build unless every `CLAUSE_n`
  is mapped to a targeted, non-trivial request assertion — even if the OpenAPI
  schema and the live server are internally coherent. This is the
  "coherent-and-wrong" trap defense: a build that quietly drops the CLAUSE_2
  `user_uuid` rule is caught because no test case covers it.

`test_matrix.json` (written by the independent exerciser) schema:

```json
[
  {"name": "unauthenticated POST rejected", "clause": "CLAUSE_1", "check": "no X-API-Key -> 401"},
  {"name": "profile exposes user_uuid",     "clause": "CLAUSE_2", "check": "200 body has user_uuid, no id"},
  {"name": "malformed body -> clean 400",   "clause": "CLAUSE_3", "check": "bad payload -> 400, no traceback"}
]
```

(The fenced JSON above lives in this README, not in the normative
`api_policy_manifest.md` — Gate A forbids such syntax inside the manifest itself.)

## Grounding (spec / reality alignment)

`validate_handbook.py`'s grounding step is the upper-bound analogue of the ground
truth's "every behavior is exercised against the real contract". It proves the
ceiling is dischargeable by confirming, against
`../ground-truth/base_schema.json`, that each HTTP element the clauses / negative
vector reference actually exists:

1. the `X-API-Key` header security scheme;
2. the public `user_uuid` field (with the manifest also asserting the *internal*
   id is hidden);
3. the `400 Bad Request` status code on validation failure;
4. the `401 Unauthorized` defense status code;
5. the mutation route `POST /api/v1/profile/update`.

A normative claim no live route could satisfy is rejected here, not discovered
downstream.

## Adaptations (surfaced, not hidden)

- **Schema fidelity.** `api_policy_manifest.md` uses the spec §2 schema verbatim,
  including `MANIFEST_ID: API_POLICY_081`, `CLAUSE_1..3`, the negative vector, and
  both NOT-claims. The `[cite_start]` / `[cite: …]` citation artifacts present in
  the spec source (on the NOT-Claims intro line) are authoring metadata and are
  stripped from the published manifest.
- **Header marker `X-API-Key` is allowed.** Gate A forbids implementation syntax,
  but the manifest legitimately names the HTTP header `X-API-Key` and status codes
  `400`/`401` — these are *contract vocabulary* (the WHAT), not code. They appear
  inline as plain prose / backticked terms and trigger no forbidden marker.
- **No spec/reality conflict found.** Every clause and the negative vector map
  cleanly onto `base_schema.json` (header scheme, mutation route, `user_uuid`,
  `400`/`401` shapes). The grounding check passes without weakening any clause.
