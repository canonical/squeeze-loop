# System Specification: Ground Truth & Lower Bound Engine (Example C: API Contract Guard)

This specification defines the low-level source of truth (the executable lower bound) and environmental isolation parameters for **Archetype C (Split Planes)**. The system handles the **API Contract Guard** workflow, where system correctness splits clean across a **Document Plane** (the public OpenAPI `openapi.json` schema) and a **Runtime Plane** (the live execution behavior of the local API endpoints). Correctness is defined as the exact fixed point where both planes match, preventing the characteristic "blending" failure where compliant documentation masks broken application behavior.

---

## 1. System Environment & Directory Architecture

The system operates inside an isolated LXC container. To guarantee physical context barriers and eliminate conversational leaks between roles, it enforces separation of duties via three distinct POSIX user accounts.

* `sentinel` (The Orchestrator and Gate Evaluator)
* `implementer` (The Code/Route-Writing Agent workspace)
* `exerciser` (The Test/Conformance Agent workspace)

### Directory Layout

```text
/opt/squeeze/
├── shared/                  # Immutable Low-Level Sources of Truth
│   ├── base_schema.json     # Step 1: Document Plane Baseline Schema
│   ├── app_state.db         # Storage database used by the runtime app
│   └── ty0_baseline.json    # Step 3: Cryptographic baseline of legacy endpoints
│
├── runtime_app/             # Step 2: Runtime Plane Environment
│   ├── main.py              # The live server script (e.g., FastAPI + Uvicorn)
│   └── run_server.sh        # Controlled process script bound to localhost:8000
│
├── orchestrator/            # Owned by 'sentinel' (Mode 0700)
│   ├── ledger/              # Tracks spec-N.md and gap-N.md documents
│   └── gate_sentinel.py     # Execution arbiter and gate evaluator
│
/home/implementer/           # Owned by 'implementer' (Mode 0700)
│   └── src/                 # Workspace for editing code routes and schemas
│
/home/exerciser/             # Owned by 'exerciser' (Mode 0700)
    └── conformance/         # Workspace for independent contract test scripts

```

---

## 2. The Split Lower Bound Planes

The executable lower bound consists of two separate, unalterable local evaluation tracks that run independently within the container.

### Plane 1: The Document/Declaration Ground Truth (Static Track)

* **The Artifact:** `/opt/squeeze/shared/base_schema.json`
* **The Compute Engine:** A pinned local Python linter package (or JSON-schema validation script) executed by the orchestrator.
* **The Rule:** The `implementer` must output an updated OpenAPI schema description. The static track validates that this file conforms perfectly to standard API formatting rules, possesses complete type mappings, and documents all error response payloads. If a required property description is left blank or possesses invalid structural nesting, the linter aborts the execution track.



### Plane 2: The Runtime/Execution Ground Truth (Dynamic Track)

* **The Artifact:** A live-running backend process initialized via `/opt/squeeze/runtime_app/run_server.sh` and exposed on `http://127.0.0.1:8000`.
* **The Compute Engine:** A native system network-loop inspector or a programmatic Python HTTP client executed by the orchestrator.
* **The Rule:** The server code is dynamically booted. The system monitors live interactions to ensure the code executes cleanly without throwing raw `500 Internal Server Errors`, leaking internal stack traces, or diverging from expected database constraints in `app_state.db`.



---

## 3. The "No-Blend" Invariant Engine

To enforce the **Disjointness Principle (C1)**, the automated sentinel prevents the evaluation paths from polluting or compensating for one another.

* 
**The Rule:** Beautifully written OpenAPI text files can never excuse a runtime server failure or unhandled exception. Conversely, a server route that happens to execute cleanly cannot excuse a failure to update the public-facing contract document.


* 
**Enforcement:** The orchestrator forces a cross-plane verification check. The `exerciser` agent generates its functional test suites using **only** the static schema file (`base_schema.json`), without viewing the implementation code. The orchestrator runs these client tests directly against the `implementer's` live running server. Any divergence in query parameters, undocumented data types, or unexpected HTTP status headers triggers an immediate failure.



---

## 4. Item Zero (TY0) Local Base Move

The system enforces a strict stabilization sequence: no new endpoint additions or parameter changes can be developed over an unmeasured or volatile codebase.

* **The Artifact:** `/opt/squeeze/shared/ty0_baseline.json`
* 
**The Mechanic:** Before processing any new feature request (`spec-N.md`), the orchestrator runs a mandatory route-discovery reflection check on the container's legacy code trunk. It logs every listening socket route, parameter name, and database column state, writing the output to a signed, content-hashed file.


* **The Constraint:** During subsequent gate evaluations, the sentinel cross-checks this baseline file. If an agent modifies a specific target route, but the change causes a silent structural or signature mutation on a completely unrelated legacy route, the Item Zero validation file flags the mutation and blocks deployment.

---

## 5. Automated Gate Evaluation Framework

When an iteration is submitted for clearance, `gate_sentinel.py` evaluates the artifacts using the following programmatic gate sequence:

```text
GATE A: Asserts the coordinator performed active text modifications to the plan before execution.
                  │
                  ▼
GATE B: 1. Boots local server at 127.0.0.1:8000.
        2. Fires the Exerciser's contract client scripts against the live runtime.
        3. Fails if server responses do not match the expected validation matrix.
                  │
                  ▼
GATE C: Machine-checks that every individual route and data block declared in the 
        OpenAPI document explicitly correlates to a passing test assertion block.

```

### Gate B Verification Execution Loop (Python Snippet)

```python
import subprocess
import requests
import json
import sys
import time

def verify_split_planes():
    # 1. Enforce Item Zero Snapshot Consistency
    with open("/opt/squeeze/shared/ty0_baseline.json") as b:
        baseline_hash = json.load(b).get("hash")
    # (Sentinel re-runs reflection script to verify current state matches baseline_hash)

    # 2. Spin up the local runtime environment server (Plane 2)
    server_proc = subprocess.Popen(
        ["/opt/squeeze/runtime_app/run_server.sh"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    time.sleep(2)  # Allow local network socket to bind

    try:
        # 3. Load the independent contract cases generated by the Exerciser
        with open("/home/exerciser/conformance/test_matrix.json") as f:
            test_cases = json.load(f)

        for case in test_cases["endpoints"]:
            # Fire the programmatic HTTP request into local host runtime
            url = f"http://127.0.0.1:8000{case['path']}"
            response = requests.request(case["method"], url, json=case.get("payload"))

            # Enforce strict contract match (No-Blend verification)
            if response.status_code != case["expected_status"]:
                print(f"GATE B CRASH: Interface Drift Detected on route {case['path']}!")
                print(f"Expected HTTP Status: {case['expected_status']}, Got: {response.status_code}")
                sys.exit(1)

            if response.json().keys() != set(case["expected_schema_keys"]):
                print(f"GATE B CRASH: Schema Mismatch! Undocumented structural keys returned on the wire.")
                sys.exit(1)

        print("GATE B SUCCESS: Split planes run in total alignment.")
        
    finally:
        server_proc.terminate()

if __name__ == "__main__":
    verify_split_planes()

```
