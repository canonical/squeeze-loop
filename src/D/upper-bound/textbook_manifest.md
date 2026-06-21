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
* **Scope Boundary 1:** The formalization must utilize the native inductive type `nat` from the Rocq Standard Library (`Init.Nat`). Re-defining natural numbers under a custom namespace to cheat basic type constraints is prohibited.
* **Scope Boundary 2:** The theorem must preserve intuitionistic logic controls. Introducing classical logic axioms (such as `classic` or the Law of Excluded Middle) to shortcut structural induction paths is unauthorized.

### 3. Enumerated Obligation Clauses
These clauses define the mandatory sub-claims that the formal theorem statement must capture to prevent structural omission:
* **CLAUSE_1:** The formal statement must universally quantify over all elements of the type `nat`.
* **CLAUSE_2:** The formalization must state the property using the exact equality of addition (n + m = m + n), not a weaker or adjacent relation.
* **CLAUSE_3:** The baseline proof structure must depend explicitly on structural induction over the natural number constructors (`O` and `S`).

### 4. The Core Negative Vector (The Target Mutation)
This block specifies the mandatory attack sequence that the testing framework must use to audit the formal definitions against vacuous truth:
* **Target Mutation:** Identity Flip / Contradictory Hypothesis Injection. The Exerciser generates a mutation file in which the commutative statement is altered to a known-false mathematical property (n + m = m + S n).
* **Expected System Defense:** The local Rocq compiler (`coqc`) *must fail* to type-check the mutated statement when evaluated against the implementer's tactical steps. If it succeeds, the `formalizer` has introduced inconsistent axioms or circular definitions and the build must be aborted.

### 5. Explicit NOT-Claims
To keep the engineering ledger transparent about what was formally checked versus what remains unproven, the author bounds the validation footprint:
* **NOT_CLAIM_1:** This exercise block does not verify the computational performance, optimization constraints, or stack depth of the compiled arithmetic terms.
* **NOT_CLAIM_2:** This validation loop does not prove equivalence to binary representation formats or hardware-level floating-point implementations.

# TEXTBOOK_MANIFEST_END

---

## Difficulty ladder (level-up-D)

The richness of the experiment comes from the richness of this upper bound. A
single easy theorem yields ~100% prover success and nothing for the gates to
catch; a *ladder* of increasing mathematical depth is what surfaces the
implementer error gradient (see `level-up-D.md`). Each rung is a binding exercise
with its own obligation clauses; the executable witnesses and the false mutations
live in `../ground-truth/ladder/` and are graded by `../ground-truth/ladder_runner.py`
against the real Rocq kernel.

| Rung | EXERCISE_ID | Tier | Theorem (statement) | Reference proof |
|------|-------------|------|---------------------|-----------------|
| 1 | EX_ROCQ_L1 | trivial   | `ex_triv`  — `forall n, n + 0 = n` | proved |
| 2 | EX_ROCQ_L2 | easy      | `ex_easy`  — `forall n m, n + m = m + n` | proved |
| 3 | EX_ROCQ_L3 | medium    | `ex_med`   — `forall n m p, (n+m)+p = n+(m+p)` | proved |
| 4 | EX_ROCQ_L4 | hard      | `ex_hard`  — `forall n m, n * m = m * n` | proved |
| 5 | EX_ROCQ_L5 | very_hard | `ex_vhard` — `forall n, n <= 2 ^ n` | **open** (Admitted; the axiom audit catches it — the gate stays honest at the boundary) |

Each rung carries: CLAUSE_1 (universal quantification over `nat`), a tier-specific
correctness clause, and a structural clause (which induction / lemma the proof must
use). Each ships a FALSE mutation that the kernel must reject (catchability). The
very-hard rung's reference proof is deliberately left open: it marks the depth
beyond the certified witness, and `Print Assumptions` reports the `Admitted` rather
than letting a vacuous proof pass.
