To hold your agents in a vice where they cannot cheat, the space **between** the Upper Bound (the Handbook ) and the Lower Bound (the SQLite Database ) must contain the **Deliverable Band**. This band consists of two physically isolated code artifacts that are forced to collide in the execution sandbox.

If you pass this exact Markdown specification to your coding agent, it will know exactly how to build the code that sits between your bounds.

---

# System Specification: The In-Band Deliverable Layer (Use Case A)

This document specifies the structural requirements for the code artifacts built by the `implementer` and `exerciser` user accounts. These artifacts exist purely to bridge the **Metric Handbook (Upper Bound)** and the **SQLite Database (Lower Bound)** under the supervision of the `gate_sentinel.py` runtime.

```text
       [ UPPER BOUND: Metric Handbook Clauses ]
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
 ┌───────────────────────┐   ┌───────────────────────┐
 │   IMPLEMENTER BAND    │   │    EXERCISER BAND     │
 │  (Builds query.sql)   │   │ (Builds validation)   │
 └───────────────────────┘   └───────────────────────┘
             │                           │
             └─────────────┬─────────────┘
                           ▼
       [ LOWER BOUND: Frozen SQLite DB + Invariants ]

```

## 1. The Implementer’s Band: The Analytical Engine

The `implementer` account is tasked with producing a stateless, programmatically executable query module. It is strictly forbidden from knowing how it will be tested.

### File Target

`/home/implementer/src/query.sql` (or a Python wrapper executing SQLite queries, e.g., `/home/implementer/src/compute_metric.py`).

### Interface Requirements

To ensure the automated sentinel can run it dynamically, the script must accept standardized runtime parameters via environment variables or CLI arguments:

* 
`START_DATE` (ISO 8601 string, e.g., `"2026-01-01T00:00:00Z"`) 


* `END_DATE` (ISO 8601 string, e.g., `"2026-03-31T23:59:59Z"`)

### Output Requirements

The script must output a strict, single-row JSON string to `stdout` containing the calculated scalar metrics matching the `METRIC_ID` requested. No decorative log prose is permitted.

```json
{
  "metric_id": "METRIC_001",
  "value": 1450023.12,
  "execution_utc_timestamp": "2026-06-12T12:11:39Z"
}

```

---

## 2. The Exerciser’s Band: The Validation Matrix

The `exerciser` account is tasked with producing the acceptance evidence. Because it is blind to the implementation code, its deliverables represent an independent interpretation of the Handbook.

### File Target

`/home/exerciser/tests/validation_matrix.json`

### Structural Schema

The validation matrix must be partitioned into two strict arrays: `positives` and `negatives`.

```json
{
  "metric_id": "METRIC_001",
  "positives": [
    {
      "test_case_id": "TC_001_STANDARD_RUN",
      "description": "Validates nominal transaction sums inside the clean UTC window.",
      "target_clauses": ["CLAUSE_1", "CLAUSE_2"],
      "expected_output": {
        "value": 1450023.12
      }
    }
  ],
  "negatives": [
    {
      "test_case_id": "TC_002_EXCLUDE_TEST_ACCOUNTS",
      "description": "Forces evaluation of test account stripping by asserting a mis-scoped query failure.",
      "target_clauses": ["CLAUSE_3"],
      "mutation": "COUNT_ALL_USERS_INCLUDING_TEST",
      "expected_fault": {
        "site": "user_id_filter_block",
        "reason": "DIVERGENT_VALUE_ERROR"
      }
    }
  ]
}

```

### Behavioral Requirements for Negatives

To satisfy **Gate B**, the exerciser cannot just write passive tests; it must define a *deliberate negative criteria*. It must specify how an intentional, minor implementation failure (e.g., failing to strip `test_` accounts) causes a distinct structural or numerical divergence.

---

## 3. The Squeeze Connector: Execution Runner

This is a structural bridge utility executed by `gate_sentinel.py`. It is the engine that forces the Implementer's code and the Exerciser's tests to reconcile over the local SQLite database.

When a validation cycle is fired, the runner executes this exact logic loop:

```python
import subprocess
import json
import sys

def execute_squeeze_pass():
    # 1. Mount SQLite in Read-Only Mode (Lower Bound Enforcement)
    db_uri = "file:/opt/squeeze/shared/base_warehouse.db?mode=ro"
    
    # 2. Run Implementer's query for a positive test case
    result = subprocess.run(
        ["python3", "/home/implementer/src/compute_metric.py", "--metric", "METRIC_001"],
        capture_output=True, text=True, check=True
    )
    computed_data = json.loads(result.stdout)
    
    # 3. Read Exerciser's expected positive data
    with open("/home/exerciser/tests/validation_matrix.json") as f:
        validation = json.load(f)
        
    expected_value = validation["positives"][0]["expected_output"]["value"]
    
    # 4. Enforce the Squeeze Match (Gate B)
    if computed_data["value"] != expected_value:
        print(f"GATE B CRASH: Coherent-and-Wrong Detected! Implementer got {computed_data['value']}, Exerciser expected {expected_value}")
        sys.exit(1)
        
    print("GATE B SUCCESS: In-band alignment verified.")

```

---

## Summary of Constraints to Provide Your Agent

When you task your coding agent to implement this "between" layer, instruct it to verify that:

1. 
**Zero Import Linkage:** The code in `/home/implementer/` never imports, reads, or parses files inside `/home/exerciser/` (and vice versa).


2. 
**Strict Serialization:** The only way data moves between the Implementer's work and the database is through standard SQLite read connections; the only way it interacts with the Exerciser is via the structural JSON strings validated by the sentinel.
