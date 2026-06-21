# System Specification: Squeeze-Loop Upper Bound (Textbook Specification Manifest - Example D)

This specification defines the format, file system placement, and structural constraints of the **Upper Bound Source of Truth** inside the LXC container for **Use Case D: Formal Mathematical Verification**.

In this Rocq deductive-verification workflow, the upper bound acts as the immutable epistemic ceiling. It fixes the strongest mathematical claims the agent system may assert. It translates natural language mathematics from a reference textbook into a strict, token-parsable format that forces the `formalizer` (Property Author) and `exerciser` to reconcile formal logic definitions against the original English source.

---

## 1. Environment & Physical Isolation Permissions

To prevent the AI agents from quietly altering the problem definitions or softening mathematical claims to clear a stuck proof script, the textbook manifest must be physically locked out of the agents' writeable environments.

* **File Path:** `/opt/squeeze/shared/textbook_manifest.md`
* **Permissions:** Owned strictly by `root:root` with permissions set to `0444` (Universally Read-Only).
* 
**Isolation Mechanics:** During the dispatch sequence, the automated orchestrator reads this manifest, extracts only the specific `EXERCISE_ID` scheduled for the active loop, and writes it directly to `/home/formalizer/spec.txt` and `/home/exerciser/spec.txt`. The raw file is hidden from the `prover` user space.



---

## 2. The Upper Bound Document Schema

The `/opt/squeeze/shared/textbook_manifest.md` file must utilize a strict, machine-readable Markdown structural boundary. Every exercise block must declare explicit mathematical scope limits and atomized obligation clauses that **Gate C** will use to cross-verify structural coverage.

```markdown
# TEXTBOOK_MANIFEST_START

## EXERCISE_ID: EX_ROCQ_074
* **Textbook Reference:** Chapter 3: Induction and Algebraic Structures, Exercise 4.2
* **Mathematical Domain:** Peano Arithmetic / Monoid Properties
* **Status:** BINDING

### 1. English Exercise Text
"Prove that addition over the natural numbers ($nat$) is commutative. You must construct your proof natively from the foundational inductive definitions of addition, verifying that for all $n, m \in nat$, $n + m = m + n$."

### 2. Explicit Mathematical Bounds (The Ceiling)
* **Scope Boundary 1:** The formalization must utilize the native inductive type `nat` from the Rocq Standard Library (`Init.Nat`). Re-defining natural numbers under a custom namespace to cheat basic type constraints is prohibited.
* **Scope Boundary 2:** The theorem must preserve intuitionistic logic controls. Introducing classic logic axioms (such as `classic` or the Law of Excluded Middle) to shortcut structural induction paths is unauthorized.

### 3. Enumerated Obligation Clauses
[cite_start]These clauses define the mandatory sub-claims that the formal theorem statement must capture to prevent structural omission[cite: 92]:
* **CLAUSE_1:** The formal statement must universally quantify over all elements of the type `nat`.
* **CLAUSE_2:** The formalization must state the property using the exact left-to-right and right-to-left equality properties of addition ($n + m = m + n$).
* **CLAUSE_3:** The baseline proof structure must depend explicitly on structural induction over the natural number constructors (`O` and `S`).

### 4. The Core Negative Vector (The Target Mutation)
[cite_start]This block specifies the mandatory attack sequence that the testing framework must use to audit the formal definitions against vacuous truth[cite: 56]:
* **Target Mutation:** Contradictory Hypothesis Injection or Identity Flip. The Exerciser generates a mutation file where the commutative statement is altered to a known false mathematical property (e.g., $n + m = m + S(n)$).
* **Expected System Defense:** The local Rocq compiler (`coqc`) *must fail* to type-check this statement when evaluated against the implementer's tactical steps. If it succeeds, it indicates the `formalizer` has introduced inconsistent axioms or circular definitions, and the build must be aborted.

### 5. Explicit NOT-Claims
[cite_start]To keep the engineering ledger transparent regarding what was formally checked versus what remains unproven, the author must bound the validation footprint[cite: 142]:
* **NOT_CLAIM_1:** This exercise block does not verify the computational performance, optimization constraints, or stack depth of the compiled arithmetic terms.
* **NOT_CLAIM_2:** This validation loop does not prove equivalence to binary representation formats or hardware-level floating-point implementations.

# TEXTBOOK_MANIFEST_END

```

---

## 3. Enforcement Mechanisms at the Automated Gates

The automated orchestration sentinel (`gate_sentinel.py`) parses this governance manifest file to regulate transition states across the pipeline:

### Gate A: Structural Specification Validation

* 
**The Plan Audit:** Before any code compilation tracks are initialized, the sentinel parses the forward design blueprint (`spec-N.md`) generated by the coordinator.


* 
**Rule Check:** **Gate A** requires that every individual `CLAUSE_X` listed under the active `EXERCISE_ID` manifest entry is explicitly accounted for, cited, and mapped within the blueprint. If the plan simply copies the textbook text without detailing how the inductive types map, the loop rejects the transition.



### Gate C: Structural Coverage Map

* 
**The Vacuous Proof Guard:** To block the "coherent-and-wrong" trap—where an agent generates an internally consistent proof script that successfully runs through `coqc` but proves a completely adjacent, weaker, or vacuous statement—**Gate C** executes a complete contract-to-test verification.


* 
**Traceability Audit:** The sentinel programmatically scans the independent testing outputs (`validation_matrix.json`) generated by the code-blind `exerciser` account.


* 
**Enforcement:** It verifies that every single entry from the manifest's `Enumerated Obligation Clauses` array correlates to an executed and verified checking assert in the output logs. If the testing file lacks a targeted assertion for `CLAUSE_2`, **Gate C drops a hard clearance exception and kills the branch**, forcing the pipeline to re-evaluate the item.
