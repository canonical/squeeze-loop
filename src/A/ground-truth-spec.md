# System Specification: Squeeze-Loop Analytics Engine (SQLite & LXC Edition)

This specification defines an orchestration backend designed to run inside a single **LXC container**. It implements a physical, context-blocked multi-agent environment for the **Transcription: "Every number recomputes"** workflow. It guarantees strict separation of duties and data between LLM agents by utilizing Unix file system permissions, isolated POSIX user accounts, and immutable local data planes.

---

## 1. System Environment & Directory Architecture

The system operates within an LXC container (Ubuntu/Debian base image). To ensure physical context barriers (**C3**), three distinct Unix user accounts must be created inside the container:

* `sentinel` (The Orchestrator and Gate Evaluator)
* `implementer` (The Coding Agent workspace)
* `exerciser` (The Testing Agent workspace)

### Directory Layout

The file system must be provisioned exactly as follows to prevent cross-agent context contamination:

```text
/opt/squeeze/
├── shared/                  # Read-Only Low-Level Sources of Truth
│   ├── base_warehouse.db    # Step 1: Storage Plane (SQLite)
│   ├── history_ledger.json  # Step 2: Invariant Plane (Baseline numbers)
│   └── history_ledger.sig   # SHA-256 signature of the historical baseline
│
├── orchestrator/            # Owned by 'sentinel' (Mode 0700)
│   ├── ledger/              # Tracks spec-N.md and gap-N.md documents
│   └── gate_sentinel.py     # Referees executions and evaluates gates
│
/home/implementer/           # Owned by 'implementer' (Mode 0700)
│   └── src/                 # Workspace where Implementer writes SQL/Python
│
/home/exerciser/             # Owned by 'exerciser' (Mode 0700)
    └── tests/               # Workspace where Exerciser writes tests

```

### File System Isolation Permissions

To enforce strict data isolation, execute the following configuration commands during container provisioning:

```bash
# Create isolated POSIX users
useradd -m -s /bin/bash implementer
useradd -m -s /bin/bash exerciser
useradd -m -s /bin/bash sentinel

# Harden home directories to prevent cross-reading
chmod 700 /home/implementer
chmod 700 /home/exerciser
chmod 700 /opt/squeeze/orchestrator

# Secure the Low-Level Sources of Truth
chown root:root /opt/squeeze/shared/base_warehouse.db
chmod 444 /opt/squeeze/shared/base_warehouse.db  # Universally read-only

```

---

## 2. Execution of Low-Level Sources of Truth

The system codifies the three low-level sources of truth locally, removing all external cloud or remote dependencies.

### Step 1: Storage Plane (Local SQLite Event Log)

* **Artifact:** `/opt/squeeze/shared/base_warehouse.db`
* **Mechanic:** This database holds the raw transaction event logs. It is strictly root-owned and set to mode `0444`.
* **Enforcement:** When the `gate_sentinel.py` script spawns execution runs for either the `implementer` or `exerciser`, it must open the SQLite connection using the read-only URI parameter: `file:/opt/squeeze/shared/base_warehouse.db?mode=ro`. Any attempt to execute `INSERT`, `UPDATE`, `DROP`, or `ALTER` will fail at the database engine level.

### Step 2: Invariant Plane (Cryptographic Baseline Ledger)

* **Artifacts:** `/opt/squeeze/shared/history_ledger.json` and `history_ledger.sig`
* **Mechanic:** The JSON file contains a flat key-value mapping of previously certified financial metrics for past quarters (e.g., `{"2025_Q1_revenue_USD": 1450023.12}`).
* **Enforcement:** Before any test suite runs, `gate_sentinel.py` hashes `history_ledger.json` and verifies it against `history_ledger.sig`. During the evaluation phase, the sentinel executes the newly generated queries against past epochs. If the computed output shifts a past metric by even a single byte compared to the JSON baseline, **Gate B** fails immediately (**Total Additivity Violation**).

### Step 3: Compute Plane (Frozen SQLite Engine)

* **Artifact:** The system-wide `sqlite3` binary package pinned inside the LXC container configuration.
* **Mechanic:** All time, date, math, and string operations are bound to the core behavior of this specific, unalterable database engine configuration. Agents cannot override runtime dependencies or mutate configurations to obscure edge-case handling bugs.

---

## 3. The Traceability State Machine

The system progress is handled via an automated file-based state machine managed by `gate_sentinel.py`. The machine transitions through the following lifecycle states:

```
[DRAFT] --(Coordinator Editorial)--> [APPROVED] --(Sandbox Run)--> [DONE]
                                         ^                            |
                                         |_____(Gate Failure / GAP)___|

```

* **DRAFT:** The file `/opt/squeeze/orchestrator/ledger/spec-N.md` is created with a `STATUS: DRAFT` header. This file contains the targeted metric-definition handbook excerpt (Upper Bound).
* **APPROVED:** The Coordinator agent reviews the plan. The sentinel transitions the file state to `STATUS: APPROVED` only if a text diff proves that the Coordinator has actively annotated, edited, or modified the draft (preventing instant rubber-stamping).
* **GAP OPEN / ITERATION:** If any automated execution gate fails, the sentinel freezes the current workspace branch, outputs an immutable `/opt/squeeze/orchestrator/ledger/gap-N.md` report detailing the precise code/assertion mismatch, and increments the state machine to generate `spec-(N+1).md`.

---

## 4. The Context-Blocked Dispatch Loop

When an item hits `STATUS: APPROVED`, the orchestration engine must execute the pipeline using physical context separation:

### 1. Implementer Provisioning

The orchestrator reads the metric specification from `spec-N.md` and copies **only** the markdown plain text into `/home/implementer/spec.txt`.

* The `implementer` agent has read access to `/home/implementer/spec.txt` and read-only access to `/opt/squeeze/shared/base_warehouse.db`.
* The `implementer` agent is completely blind to `/home/exerciser/` and cannot see any test files.
* **Deliverable:** The implementer writes its analytical SQL query or Python calculation script to `/home/implementer/src/query.sql`.

### 2. Exerciser Provisioning

The orchestrator copies the exact same markdown plain text into `/home/exerciser/spec.txt`.

* The `exerciser` agent has read access to `/home/exerciser/spec.txt` and read-only access to `/opt/squeeze/shared/base_warehouse.db`.
* The `exerciser` agent is completely blind to `/home/implementer/` and cannot see the production query code.
* **Deliverable:** The exerciser writes its assertions to `/home/exerciser/tests/assertions.json` (defining expected scalar numbers) along with a deliberate negative verification criteria (e.g., specifying that a mis-scoped query counting logins-not-users must fail or output a divergent number at a specific target location).

---

## 5. Automated Gate Sentinel Validation

Once both agents complete their deliverables, `gate_sentinel.py` runs as the `sentinel` user, ingestion-checking both directories against the three verification gates:

### Gate A: Structural Alignment

Verifies that the file states match, timelines track linearly, and the human or coordinating agent has performed editorial oversight on the requirements documentation before the code files were produced.

### Gate B: Machine Execution (The Squeeze)

The sentinel copies `/home/implementer/src/query.sql` and `/home/exerciser/tests/assertions.json` into a temporary execution sandbox. It fires the code directly against the local SQLite database container and verifies:

1. **Positive Match:** The query outputs match the exact scalar figures calculated by the independent exerciser.
2. **Negative Fault:** The exerciser's seeded negative test is executed. The engine confirms that the query breaks or diverges exactly where and how the exerciser predicted.
3. **Standing Invariant:** The transaction calculations are executed against past data checkpoints. The output is cross-referenced against `/opt/squeeze/shared/history_ledger.json`. Any byte-level mismatch triggers an immediate rollback.

### Gate C: Structural Coverage Map

The sentinel parses `spec-N.md` to extract the individual numbered metric logic clauses. It then programmatically scans `assertions.json` to verify that every single requirement index matches a specific, non-trivial validation check. If an agent writes a sweeping, generic test assertion that skips checking timezone boundaries or survivorship bias exclusions, Gate C aborts the cycle.

If all gates pass successfully, the sentinel appends `STATUS: DONE` to the ledger item and commits `/home/implementer/src/query.sql` to the production repository tree.
