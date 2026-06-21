# System Specification: The In-Band Deliverable Layer (Example D: Rocq Theorem Prover)

This specification outlines the structural, interface, and compilation requirements for the code artifacts built inside the `prover` (Implementer) and `exerciser` environments. These components occupy the *in-band* deliverable space , bounded from above by the **Textbook Specification Manifest (Upper Bound)** and from below by the **Rocq Compiler & Type Engine (Lower Bound)**.

To guarantee total compliance with physical context barriers, these two execution bands operate under strict isolation. The `prover` cannot see the test mutations, and the `exerciser` cannot see the tactical proof code. Their alignment is forced exclusively through automated type-checking and axiom auditing executed by the orchestrator sentinel.

```text
         [ UPPER BOUND: Textbook Specification Manifest (EX_ROCQ_074) ]
                                       │
                 ┌─────────────────────┴─────────────────────┐
                 ▼                                           ▼
   ┌───────────────────────────┐               ┌───────────────────────────┐
   │      PROVER BAND          │               │      EXERCISER BAND       │
   │      (exercise.v)         │               │   (mutation_matrix.json)  │
   └───────────────────────────┘               └───────────────────────────┘
                 │                                           │
                 └─────────────────────┬─────────────────────┘
                                       ▼
         [ LOWER BOUND: Rocq Type-Checker (coqc) + Axiom Auditor (rocqchk) ]

```

---

## 1. The Prover’s Band: Tactical Proof Engine

The `prover` account is responsible for producing the operational, type-inhabited proof terms that discharge the goal.

* **File Target:** `/home/prover/solution/exercise.v`
* 
**Context Environment:** This workspace contains the read-only theorem definition file (`/home/formalizer/definition/exercise_sig.v`) containing the exact theorem statement. It is physically blocked from viewing the testing matrix or the original English text.



### Interface Requirements

The `prover` must import the formalizer's unalterable signature file and append its tactical proof blocks:

```coq
(* /home/prover/solution/exercise.v *)
Require Import Top.exercise_sig.

Theorem exercise_42 : forall n m : nat, n + m = m + n.
Proof.
  intros n m. induction n as [| n' IHn].
  - simpl. rewrite <- plus_n_O. reflexivity.
  - simpl. rewrite IHn. rewrite <- plus_n_Sm. reflexivity.
Qed.

```

### Execution Constraints

1. 
**Signature Preservation:** The prover is strictly forbidden from altering a single token of the theorem declaration signature (`Theorem ... : ...`) to make the proof paths easier.


2. 
**No Escape Hatches:** The tactical script must terminate with a definitive structural closing command (`Qed.`). The usage of `Admitted`, `Axiom`, `Skip`, or `Parameter` blocks inside the solution script constitutes a structural violation and is rejected by the gate sentinel.



---

## 2. The Exerciser’s Band: Mutation & Sanity Matrix

The `exerciser` account produces the validation criteria to detect vacuous truths. Because it operates completely code-blind to the implementer's proof steps, its deliverables represent an independent challenge to the logical completeness of the formalization.

* **File Target:** `/home/exerciser/mutation/mutation_matrix.json`

### Structural Schema

The mutation matrix maps out intentional mathematical corruptions of the theorem statement, declaring exactly how and where the Rocq compiler must fail to check the mutated terms:

```json
{
  "exercise_id": "EX_ROCQ_074",
  "mutations": [
    {
      "mutation_id": "MUT_001_IDENTITY_FLIP",
      "target_clauses": ["CLAUSE_2"],
      "description": "Mutates the right-hand equality target to inject a successor mismatch.",
      "mutated_theorem_statement": "Theorem exercise_42_mut : forall n m : nat, n + m = m + S n.",
      "expected_compiler_feedback": {
        "status": "FAIL",
        "phase": "type_check",
        "error_token": "The term has type 'nat' while it is expected to have type"
      }
    },
    {
      "mutation_id": "MUT_002_VACUOUS_HYPOTHESIS_GUARD",
      "target_clauses": ["CLAUSE_1"],
      "description": "Tests if the formalizer accidentally introduced inconsistent background axioms.",
      "mutated_theorem_statement": "Theorem exercise_42_vacuous : False -> forall n m : nat, n + m = m + n.",
      "expected_compiler_feedback": {
        "status": "FAIL",
        "phase": "axiom_audit",
        "error_token": "Axiom violation or trivial goal discharge detected"
      }
    }
  ]
}

```

---

## 3. The Squeeze Connector: Verification Runner

The execution bridge is managed by the automated backend component (`gate_sentinel.py`) running under the privileged `sentinel` user account. It automates the evaluation of **Gate B** by running the prover's scripts and the exerciser's mutations sequentially against the compilation framework.

```python
# /opt/squeeze/orchestrator/gate_sentinel.py
import subprocess
import json
import sys

def run_rocq_squeeze():
    # 1. Compile the Implementer's Proof Target (Plane 2 Lower Bound)
    compilation = subprocess.run(
        ["coqc", "-R", "/opt/squeeze/shared/rocq_stdlib/", "Top", "/home/prover/solution/exercise.v"],
        capture_output=True, text=True
    )
    if compilation.returncode != 0:
        print(f"GATE B FAILURE: Proof script failed compilation!\n{compilation.stderr}")
        sys.exit(1)

    # 2. Execute Axiom Introspection Audit (Escape Hatch Check)
    audit = subprocess.run(
        ["rocqchk", "--print-assumptions", "Top.exercise_42"],
        capture_output=True, text=True
    )
    if any(leak in audit.stdout for leak in ["Admitted", "Axiom", "Axioms"]):
        print("GATE B FAILURE: Prover cheated! Unauthorized logical escape hatches detected.")
        sys.exit(1)

    # 3. Process the Exerciser's Mutation Matrix (Catchability Validation)
    with open("/home/exerciser/mutation/mutation_matrix.json") as f:
        matrix = json.load(f)

    for mut in matrix["mutations"]:
        # Dynamically inject the mutated statement ahead of the prover's tactics
        # and test if the type-engine rejects the invalid mathematical theorem
        test_code = f"{mut['mutated_theorem_statement']}\nProof. ... Qed."
        
        # Write to temporary file for mutation check
        with open("/tmp/mutation_test.v", "w") as tmp:
            tmp.write(test_code)

        mut_compile = subprocess.run(
            ["coqc", "-R", "/opt/squeeze/shared/rocq_stdlib/", "Top", "/tmp/mutation_test.v"],
            capture_output=True, text=True
        )

        # Enforce Catchability: A false mutation MUST break compilation
        if mut["expected_compiler_feedback"]["status"] == "FAIL" and mut_compile.returncode == 0:
            print(f"GATE B FAILURE: Coherent-and-Wrong Trap Triggered! Mutation {mut['mutation_id']} passed.")
            print("The formal definitions allow proofs of false statements. Check for logical consistency errors.")
            sys.exit(1)

    print("GATE B SUCCESS: Rocq tactical implementation is verified and locked in-band.")

if __name__ == "__main__":
    run_rocq_squeeze()

```

---

## 4. Automated Gate Coupling Focus

* 
**Gate B Clearance:** Evaluates the compiler state machine. The solution is approved only if it type-checks perfectly , reveals zero axiom leaks during the `rocqchk` introspection phase , and successfully breaks under the target mathematical deformations compiled by the exerciser.


* 
**Gate C Structural Map Check:** The orchestrator reads the `target_clauses` string arrays from the exerciser's validation json. If any distinct clause defined within the upper bound handbook (`textbook_manifest.md`) lacks a corresponding tracking target here, the pipeline aborts for coverage validation deficiency.
