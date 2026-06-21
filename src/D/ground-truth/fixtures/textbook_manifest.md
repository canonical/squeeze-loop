# TEXTBOOK_MANIFEST_START

## EXERCISE_ID: EX_ROCQ_074
* **Textbook Reference:** Chapter 3: Induction and Algebraic Structures, Exercise 4.2
* **Mathematical Domain:** Peano Arithmetic / Monoid Properties
* **Status:** BINDING

### 1. English Exercise Text
"Prove that addition over the natural numbers (nat) is commutative. You must
construct your proof natively from the foundational inductive definitions of
addition, verifying that for all n, m in nat, n + m = m + n."

### 2. Explicit Mathematical Bounds (The Ceiling)
* **Scope Boundary 1:** Use the native inductive type `nat` (Init.Nat). No custom redefinition.
* **Scope Boundary 2:** Intuitionistic only -- no `classic` / excluded middle.

### 3. Enumerated Obligation Clauses
* **CLAUSE_1:** The formal statement must universally quantify over all elements of the type `nat`.
* **CLAUSE_2:** The formalization must state the exact equality n + m = m + n.
* **CLAUSE_3:** The proof must depend on structural induction over `O` and `S`.

### 4. The Core Negative Vector (The Target Mutation)
* **Target Mutation:** Identity Flip -- n + m = m + S(n).
* **Expected System Defense:** `coqc` must FAIL to type-check the mutated statement.

### 5. Explicit NOT-Claims
* **NOT_CLAIM_1:** Does not verify performance / stack depth of compiled terms.
* **NOT_CLAIM_2:** Does not prove equivalence to binary / floating-point formats.

# TEXTBOOK_MANIFEST_END
