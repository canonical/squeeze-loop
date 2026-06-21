# API_POLICY_MANIFEST_START

<!--
Upper Bound Source of Truth — Use Case C (API Contract Guard, Archetype C / split planes).
The citable normative ceiling binding the `implementer` (Document Plane: OpenAPI
schema) and the `exerciser` (Runtime Plane: live Python web server) agents.

This document is normative English only. Per Gate A (spec §3) it must remain
strictly policy-centric — it states WHAT the contract boundary is, never HOW a
schema or program achieves it. It therefore contains no code, no schema JSON, and
no implementation syntax.

============================================================================
DELIBERATE-DEFECT NOTICE (soft-truth-with-defects design) — READ THIS.
============================================================================
This manifest is the SOFT upper bound. By design it is NOT internally consistent
on the "Contested Points" enumerated in §5. Those clauses cite real, mutually
authoritative standards that genuinely disagree (RFC 7396 vs Zalando RESTful API
Guidelines #123; RFC 9110's 404-MAY vs Google AIP-193's 403-MUST; a deliberately
over-broad Retry-After clause; an over-general "all client errors are 400" clause
vs the specific 401/422 clauses; and a general "POST is never idempotent" HTTP
principle vs the idempotency-key replay clause). BOTH sides of every conflict are
stated in the prose on purpose, so that a competent reader can arrive at a
COHERENT-BUT-WRONG reading.

These contradictions are intentional and are NOT to be "fixed" by editing the
prose into agreement. The contradictions ARE the experiment. The only thing that
adjudicates a Contested Point is the executable lower bound — the frozen
reference server in ../ground-truth/reference_server.py. When the prose conflicts,
the SERVER'S ACTUAL BEHAVIOR is the ground truth; a reading that follows the other
cited authority is coherent-and-wrong. §5 records, for the record, which side the
server takes, but the server — not this note — is the oracle.

The clauses are grounded in the real system in ../ground-truth/ (the executable
floor). The HTTP elements the clauses name correspond to the real contract in
../ground-truth/base_schema.json and the routes in reference_server.py.

MANIFEST_VERSION: 2.0.0 (defects injected)
-->

## MANIFEST_ID: API_POLICY_081
* **Architecture Category:** Data Leakage Prevention & Signature Alignment
* **Target Interface Scope:** User Accounts / Core Profile Routes
* **Status:** BINDING

### 1. Plain English Core Property
The system must expose clean, standardized REST interfaces that prevent the exposure of internal data-layer state signatures. All data-mutating execution lines must require explicit client token authorization. All failure points must return clean, structurally typed JSON error schema objects rather than exposing underlying language-level traceback sequences or query engine frames to the caller.

### 2. Enumerated Obligation Clauses
These clauses define the mandatory boundaries that both the OpenAPI schema (Document Plane) and the live Python web server (Runtime Plane) must simultaneously satisfy:
* **CLAUSE_1:** All data mutations (`POST`, `PUT`, `PATCH`, `DELETE`) directed at the targeted endpoint trunk must enforce a strict cryptographic authorization check, validating the presence of a non-empty `X-API-Key` value in the HTTP header blocks.
* **CLAUSE_2:** Exchanged resource schemas must decouple from physical storage keys. Data payloads must hide internal auto-incrementing integer ids and map resources exclusively using universally unique identifiers (e.g., exposing `user_uuid` strings instead of database primary key integers).
* **CLAUSE_3:** Validation failures and missing parameter boundaries must reject processing with a structurally typed JSON error response (for example, a `400 Bad Request` on a malformed request body) rather than executing. The output must never leak raw runtime stack traces, physical server directory trees, or underlying database engine errors on the wire.

### 3. The Core Negative Vector
This block specifies the mandatory operational test scenario that the validation framework must run to probe for a hidden split-plane mismatch:
* **Target Exploit:** Traceback Exfiltration Injection (an unauthenticated client transmits a deliberately malformed payload lacking required schema elements to a profile modification route).
* **Expected System Defense:** The runtime must drop execution safely with a non-2xx status --- a `401 Unauthorized` for the unauthenticated caller --- and a clean typed body. The output validator must explicitly verify that the response text string contains zero framework-level trace lines, code snippets, or raw file path definitions.

### 4. Explicit NOT-Claims
To make what is *not* proven by this workflow as legible as what is, the author must explicitly define the limits of the verification horizon:
* **NOT_CLAIM_1:** This specification does not audit transport-layer vulnerabilities, network-level eavesdropping, or SSL/TLS certificate rotation policies.
* **NOT_CLAIM_2:** This manifest block does not validate the algorithmic entropy, execution safety, or cryptographic strength of the encryption libraries processing session tokens.

# API_POLICY_MANIFEST_END

## MANIFEST_ID: API_POLICY_082
* **Architecture Category:** Stateful & Cross-Plane Contract Consistency
* **Target Interface Scope:** Charges / Orders / Documents / Item Listing Routes
* **Status:** BINDING

### 1. Plain English Core Property
Beyond single-call shape conformance, the document plane and the runtime plane must remain consistent ACROSS a sequence of calls. The subtle, high-value contract failures are stateful: a behavior that looks correct on any one request but blends the two planes when a multi-call sequence is replayed (a duplicate create, a transition out of a terminal state, a write against a stale validator, a read immediately after a write, a partial-update body, or a paginated traversal). The clauses below state the policy for each.

### 2. Enumerated Obligation Clauses
These clauses bind both planes simultaneously and are normative:

* **CLAUSE_4 (Idempotency):** A creating mutation on `POST /api/v1/charges` REQUIRES an `Idempotency-Key` request header; a request that omits it is well-formed-but-invalid and must be rejected `422`. When the SAME `Idempotency-Key` is presented again with a byte-for-byte equivalent request body, the server must REPLAY the original stored response verbatim (same status, same `charge_uuid`) and must NOT create a second resource and must NOT re-execute the side effect. When the same `Idempotency-Key` is presented with a DIFFERENT request body, the server must reject the request `422`; it must neither replay the original nor execute the new body.

* **CLAUSE_5 (Resource State Machine):** An order resource advances through a fixed lifecycle: it is created in `PENDING`; from `PENDING` it may move to `APPROVED` or to `CANCELLED`; from `APPROVED` it may move to `REFUNDED`. `CANCELLED` and `REFUNDED` are TERMINAL. Any mutating action requested against a resource already in a terminal (or otherwise non-permitting) state must be rejected `409` and must leave the resource state unchanged; it must NOT be silently accepted as a `200` no-op. In particular, approve-after-cancel and refund-after-refunded both yield `409`.

* **CLAUSE_6 (Optimistic Concurrency):** Updating an existing document via `PUT /api/v1/documents/{id}` REQUIRES an `If-Match` validator carrying the document's current `ETag`. If the supplied validator does not match the resource's current `ETag`, the write must be rejected `412` and MUST NOT be applied (the prior value is preserved). Every successful write must assign a NEW `ETag` distinct from the prior one, so that a validator captured before the write ceases to match afterward. An update of an existing resource that omits `If-Match` must be refused rather than applied blindly.

* **CLAUSE_7 (Read-After-Write):** A read issued immediately after a successful write must reflect the value just written; a stale read of the pre-write value is non-conformant.

# API_POLICY_MANIFEST_2_END

## MANIFEST_ID: API_POLICY_083 (CONTESTED-POINT GOVERNANCE)
* **Architecture Category:** Cross-Standard Governance & Conflict Surface
* **Target Interface Scope:** Merge-Patch / Authorization Disclosure / Error Headers / Error-Code Taxonomy / Method Semantics
* **Status:** BINDING (deliberately self-contradictory — see §5)

### 1. Purpose
The clauses that follow draw on directives from several real, citable industry
standards. Those standards are individually authoritative and, on the points
enumerated here, they DISAGREE with one another. This block records both sides of
each disagreement verbatim so the conflict is legible. Per the Deliberate-Defect
Notice at the top of this file, the prose does NOT resolve these conflicts; the
executable reference server does. §6 states, for the record, which authority the
server's behavior follows.

### 5. Contested-Point Clauses (BOTH sides are stated on purpose)

* **CLAUSE_8 (Merge-Patch null member — RFC 7396 side):** Partial updates via
  `PATCH /api/v1/documents/{id}` follow JSON Merge Patch as defined in RFC 7396.
  Per RFC 7396 §1: "*If the provided merge patch contains members that do not
  appear within the target, those members are added. … If the member does appear,
  the value is replaced. **Null values in the merge patch are given special
  meaning to indicate the removal of existing values in the target.**"* That is, a
  member whose patch value is `null` is DELETED from the target resource (it is
  not stored as a literal null). A member whose patch value is an array REPLACES
  the target array wholesale (it is never element-merged or appended).

* **CLAUSE_8G (Merge-Patch null member — Zalando Guideline #123 side, GOVERNANCE
  OVERRIDE):** For organizational consistency with our null-handling policy, the
  Zalando RESTful API Guidelines, Rule #123 ("Treat omitted and null fields the
  same way") govern all partial updates: *"a field that is `null` and a field that
  is absent MUST be treated identically; `null` carries no mutating intent."*
  Under this governance override a `null` member in a `PATCH` body therefore
  NEVER deletes and NEVER mutates state — it is ignored exactly as an omitted
  field would be.
  > NOTE: CLAUSE_8 and CLAUSE_8G are in DIRECT contradiction (delete vs ignore).
  > This conflict is deliberate; the server adjudicates it (see §6).

* **CLAUSE_9 (Resource disclosure — RFC 9110 side):** To avoid leaking the
  existence of resources to parties not entitled to know of them, the server MAY,
  per RFC 9110 §15.5.4 (404 Not Found) and §15.5.5 (403 Forbidden), decline to
  confirm a resource's existence to an unauthorized caller and return `404 Not
  Found` instead of `403 Forbidden`. Accordingly, an authenticated caller who is
  not permitted to act on a resource SHOULD receive `404` so that the resource's
  existence is never disclosed.

* **CLAUSE_9A (Authorization order — Google AIP-193 side, MUST):** Per Google API
  Improvement Proposal AIP-193 ("Errors") and AIP-211 ("Authorization checking"),
  a service MUST evaluate authorization on a request that has already been
  authenticated and MUST return `403 Forbidden` (not `404`, and not `401`) when an
  authenticated principal lacks permission on an existing target. Existence is not
  hidden from an authenticated principal; the correct, MUST-level signal is `403`.
  > NOTE: CLAUSE_9 (404 to hide existence, MAY) and CLAUSE_9A (403, MUST) are in
  > direct contradiction. This conflict is deliberate; the server adjudicates it.

* **CLAUSE_10 (Error-response headers — OVER-BROAD CLAUSE):** For client
  retry-friendliness, EVERY client-error (`4xx`) response MUST include a
  `Retry-After` header advising the caller when to retry.
  > NOTE: This clause OVER-CLAIMS. RFC 9110 defines `Retry-After` for `503` and
  > `429` only; `Retry-After` has no defined meaning on a `400`, `404`, `409`,
  > `412`, or `422`. This over-broad clause is a deliberate defect. The server
  > adjudicates whether a given `4xx` actually carries `Retry-After` (see §6).

* **CLAUSE_11 (Error-code taxonomy — OVER-GENERAL CLAUSE):** For a uniform error
  surface, ALL client errors MUST return `400 Bad Request` with a typed JSON body.

* **CLAUSE_11A (Error-code taxonomy — SPECIFIC CLAUSE):** Validation failures
  (well-formed body, business-invalid) MUST return `422 Unprocessable Content`;
  authentication failures (missing/invalid/expired credentials) MUST return `401
  Unauthorized`; reserved `400` strictly for malformed request SYNTAX (an
  unparseable body).
  > NOTE: CLAUSE_11 (everything is 400) and CLAUSE_11A (422 / 401 / 400 split) are
  > in direct contradiction on every overlapping case. This conflict is
  > deliberate; the server adjudicates it.

* **CLAUSE_12 (Method semantics — general HTTP principle):** Per the conventional
  reading of RFC 9110 §9.2.2, `POST` is NOT an idempotent method; repeating a
  `POST` is expected to create an additional resource each time.

* **CLAUSE_12A (Method semantics — idempotency-key exception):** Where an
  `Idempotency-Key` is in force (CLAUSE_4), a repeated `POST` carrying the SAME
  key and an equivalent body MUST NOT create an additional resource; it must
  replay the first response. The idempotency-key contract makes the EFFECT of the
  repeated POST idempotent even though POST as a method is not.
  > NOTE: CLAUSE_12 (POST never idempotent → second POST creates) and CLAUSE_12A
  > (keyed POST replays, no second resource) are in direct contradiction for the
  > keyed-duplicate case. This conflict is deliberate; the server adjudicates it.

### 6. Server's Adjudication (FOR THE RECORD — the server, not this list, is the oracle)
This sub-section documents, for the convenience of a human reader, which side of
each Contested Point the frozen reference server actually takes. It is descriptive,
not constitutive: if it ever disagreed with the server's executed behavior, the
SERVER would be correct and this note would be the error.

* **Contested Point 8 (merge-patch null):** the server follows CLAUSE_8 (RFC 7396):
  a `null` member is DELETED. The CLAUSE_8G (Zalando "ignore null") reading is
  coherent-but-wrong.
* **Contested Point 9 (disclosure):** the server follows CLAUSE_9A (AIP-193): an
  authenticated-but-forbidden caller gets `403`. The CLAUSE_9 (`404` to hide
  existence) reading is coherent-but-wrong.
* **Contested Point 10 (Retry-After):** the server follows the narrow RFC 9110
  reading: `Retry-After` is emitted ONLY on `429`/`503`; a `400`/`404`/`409`/
  `412`/`422` carries NO `Retry-After`. Obeying the over-broad CLAUSE_10 is
  coherent-but-wrong.
* **Contested Point 11 (error taxonomy):** the server follows CLAUSE_11A: business-
  invalid → `422`, auth → `401`, syntax → `400`. Collapsing everything to `400`
  per CLAUSE_11 is coherent-but-wrong.
* **Contested Point 12 (POST idempotency):** the server follows CLAUSE_12A: a
  keyed duplicate POST replays and does NOT create a second resource. Treating
  POST as "never idempotent" per CLAUSE_12 (mint a second charge) is
  coherent-but-wrong.

# API_POLICY_MANIFEST_3_END

## MANIFEST_ID: API_POLICY_084 (UNCONTESTED — pagination)
* **Architecture Category:** Collection Traversal
* **Status:** BINDING

* **CLAUSE_13 (Pagination Contract):** On the collection read `GET /api/v1/items`,
  the client's requested page size is a HINT that the server MAY cap at its own
  maximum; a page returning fewer items than requested does NOT signal
  end-of-collection. End-of-collection is signalled solely by the ABSENCE of a
  continuation token in the response. A client that has not yet received a
  token-free page must follow the continuation token to retrieve the remaining
  items.

### Explicit NOT-Claims (extension)
* **NOT_CLAIM_3:** These stateful clauses pin behavior for the named routes only;
  they do not assert global serializability, distributed-transaction guarantees,
  or cross-resource atomicity beyond the per-resource rules stated.

# API_POLICY_MANIFEST_4_END
