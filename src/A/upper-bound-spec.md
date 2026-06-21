In the **Transcription: "Every number recomputes"** use case, the upper bound acts as the immutable **epistemic ceiling**. As defined in `main.tex`, it is the citable normative authority fixing the strongest claim an actor may make. If an agent calculates a metric using a filter not explicitly authorized here, or over-reports a number by expanding the scope, it violates the upper bound.

To ensure an AI coding agent can digest and execute against it without dropping the squeeze, the upper bound cannot be a loose, conversational text file. It must be a highly structured, versioned, and machine-traceable reference file.

Here is the specification of the upper bound source of truth for Use Case A, formatted so you can pass it directly to your coding agent.

---

# System Specification: Squeeze-Loop Upper Bound (Metric Handbook)

This specification defines the format, placement, and programmatic constraints of the **Upper Bound Source of Truth** inside the LXC container. It provides the strict normative rules that bind both the `implementer` and `exerciser` agents.

## 1. Physical Location and Access Control

To satisfy compliance condition **C3 (Physical Barriers)** from `main.tex`, the upper bound must be completely read-only and globally accessible within the container, preventing any agent from modifying the definitions to pass a broken test.

* **File Path:** `/opt/squeeze/shared/metric_handbook.md`
* **Permissions:** Owned strictly by `root:root` with permissions set to `0444` (Universally Read-Only).
* **Agent Deployment:** The orchestrator dispatch loop copies the relevant markdown block of a specific metric into `/home/implementer/spec.txt` and `/home/exerciser/spec.txt` at delegation time.



---

## 2. The Upper Bound Document Schema

The `metric_handbook.md` file must utilize a strict, token-parsable Markdown structure. Every metric must explicitly declare its **Scope Limits**, **Formula**, and **Traceable Obligation Clauses** (which **Gate C** will map directly to the test outcomes).

```markdown
# METRIC_HANDBOOK_START

## METRIC_ID: METRIC_001
*   **Name:** Quarterly Recognized Revenue (ARR-Rec)
*   **Status:** BINDING
*   **Target Table:** `billing_events`

### 1. Normative Formula
```text
Recognized_Revenue = SUM(event_amount) 
WHERE event_status = 'BOOKED' 
AND timestamp >= quarter_start 
AND timestamp <= quarter_end

```

### 2. Explicit Scope Boundaries (The Ceiling)

* **Exclusion 1:** Do not include events marked as 'PROVISIONED', 'PENDING', or 'FAILED'.
* **Exclusion 2:** Test accounts (where `user_id` starts with `test_`) must be aggressively stripped before aggregation.
* **Exclusion 3:** Timezone boundaries must be evaluated strictly using Coordinated Universal Time (UTC). Local offset shifts are unauthorized.

### 3. Enumerated Obligation Clauses (Gate C Targets)

* **CLAUSE_1:** The system must evaluate the exact millisecond boundary of the quarter in UTC.
* **CLAUSE_2:** The calculation must filter out non-booked statuses to prevent revenue inflation.
* **CLAUSE_3:** The aggregation must explicitly handle and exclude internal QA/test account transactions to prevent survivorship and test data bias.

---

## METRIC_ID: METRIC_002

* **Name:** Net Customer Churn Denominator
* **Status:** BINDING
* **Target Table:** `user_sessions`

### 1. Normative Formula

```text
Churn_Denominator = COUNT(DISTINCT user_id) 
WHERE session_active = 1

```

### 2. Explicit Scope Boundaries (The Ceiling)

* **Exclusion 1:** A `login` event does not constitute an active user status unless an explicit interaction session state is verified.
* **Exclusion 2:** Users deactivated or marked for deletion prior to the first day of the fiscal quarter must be excluded.

### 3. Enumerated Obligation Clauses (Gate C Targets)

* **CLAUSE_1:** De-duplication must happen at the `user_id` level, never the raw session/login packet level.
* **CLAUSE_2:** Historical state checks must validate user status as of Day 1 of the targeted analysis window.

# METRIC_HANDBOOK_END

```

---

## 3. How the Upper Bound Drives the Gates

The automated evaluator (`gate_sentinel.py`) uses this file to enforce structural correctness across two critical points[cite: 2]:

### Gate A: Plan Validation
Before code execution is unlocked, the Coordinator agent translates the handbook's English criteria into a technical implementation layout (`spec-N.md`)[cite: 2]. The orchestrator asserts that every single `CLAUSE_X` listed under the active `METRIC_ID` is explicitly cited and accounted for in the plan[cite: 2].

### Gate C: Coherent-and-Wrong Guard
To prevent the system from passing a query that is "coherent and wrong" (e.g., a query that computes a beautiful, internally consistent number but ignores timezone offsets), **Gate C** acts as a parser checker[cite: 2]:
*   It reads the `assertions.json` file written by the independent `exerciser` agent[cite: 2].
*   It verifies that the test suite includes a targeted test case explicitly validating the exact scenario demanded by each clause (e.g., a test data subset containing test accounts to verify they are dropped)[cite: 2].
*   If `CLAUSE_3` exists in the upper bound handbook, but no test case maps to it in the exerciser's suite, **Gate C fails the build instantly**, even if the underlying SQLite database queries ran successfully without a single runtime error[cite: 2].

```
