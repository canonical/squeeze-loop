# System Specification: Squeeze-Loop Upper Bound (API Governance Manifest - Example C)

This specification defines the format, file system placement, and programmatic structural constraints of the **Upper Bound Source of Truth** inside the LXC container for **Archetype C (Split Planes)**.

In this API Contract Guard architecture, the upper bound acts as the immutable normative authority fixing the strongest claims the system components may assert. It translates high-level company API design mandates into a token-parsable manifest file that forces the `implementer` and `exerciser` to reconcile structural contract files against live execution profiles.

---

## 1. Environment & Physical Isolation Permissions

To maintain strict compliance with physical context barriers (**C3**), the upper bound document must be frozen away from the writeable home workspaces of the engineering agents.

* **File Path:** `/opt/squeeze/shared/api_policy_manifest.md`
* **Permissions:** Owned exclusively by `root:root` with permissions set to `0444` (Universally Read-Only).
* 
**Isolation Mechanics:** At dispatch time, the automated orchestrator reads this file, extracts only the target `MANIFEST_ID` block scheduled for the active cycle, and writes it to `/home/implementer/spec.txt` and `/home/exerciser/spec.txt` respectively.



---

## 2. The Upper Bound Document Schema

The `/opt/squeeze/shared/api_policy_manifest.md` file must adhere to a strict, machine-readable Markdown structural boundary. Every protocol directive must layout the clear, atomized obligation clauses that **Gate C** will use to evaluate interface compliance.

```markdown
# API_POLICY_MANIFEST_START

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
* **CLAUSE_3:** Validation failures and missing parameter boundaries must reject processing by triggering a strict `400 Bad Request` schema payload. The output must never leak raw runtime stack traces, physical server directory trees, or underlying database engine errors on the wire.

### 3. The Core Negative Vector (The Target Attack)
This section outlines the mandatory operational test scenario that the validation framework must run to probe for a hidden split-plane mismatch:
* **Target Exploit:** Traceback Exfiltration Injection (An unauthenticated client transmits a deliberately malformed payload lacking required schema elements to a profile modification route).
* **Expected System Defense:** The runtime must drop execution safely, asserting a `400 Bad Request` or `401 Unauthorized` status response. The output validator must explicitly verify that the response text string contains zero framework-level trace lines, code snippets, or raw file path definitions.

### 4. Explicit NOT-Claims
[cite_start]To make what is *not* proven by this workflow as legible as what is, the author must explicitly define the limits of the verification horizon[cite: 142]:
* **NOT_CLAIM_1:** This specification does not audit transport-layer vulnerabilities, network-level eavesdropping, or SSL/TLS certificate rotation policies.
* **NOT_CLAIM_2:** This manifest block does not validate the algorithmic entropy, execution safety, or cryptographic strength of the encryption libraries processing session tokens.

# API_POLICY_MANIFEST_END

```

---

## 3. Enforcement Mechanisms at the Automated Gates

The orchestration evaluator (`gate_sentinel.py`) parses this document structure to drive the validation checks:

### Gate A: Structural Plan Integrity

* 
**Plan Audit:** Before allowing any container processes to execute, the orchestrator parses the forward technical design document (`spec-N.md`) compiled by the agent framework.


* 
**Rule Check:** **Gate A** confirms that every single `CLAUSE_X` listed under the active `MANIFEST_ID` is explicitly cited, referenced, and addressed in the code blueprint.



### Gate C: Structural Coverage Map

* 
**The Coverage Guard:** To defeat the "coherent-and-wrong" trap—where an agent generates an internally consistent OpenAPI schema and working server that completely omits the data leakage rules—**Gate C** acts as an unyielding cross-plane evaluator.


* **Traceability Audit:** The sentinel scans `/home/exerciser/conformance/test_matrix.json`. It matches each unique `CLAUSE_ID` from the manifest file directly to a concrete, executed request assertion block in the client test output.


* **Disposition:** If the exerciser agent fails to map a dedicated test case to **every single clause** listed in the upper bound manifest, **Gate C fails the entire build instantly**, locking out the production code trunk from an unverified deployment.
