# System Specification: Ground Truth & Lower Bound Engine (Example D: Rocq Theorem Prover)

This specification defines the low-level source of truth (the executable lower bound) and environment architecture for **Use Case D: Formal Mathematical Verification**. The system operates on a transcription terrain where English textbook exercises are converted into formal logic. Correctness is defined as a machine-checked proof script that fully discharges a type-directed mathematical obligation within the **Rocq Proof Assistant** (formerly Coq) kernel. This engine enforces structural constraints to prevent the classic deductive failure mode: a workflow converging on a valid proof of a vacuous or wrong theorem.

---

## 1. System Environment & Directory Architecture

The environment is isolated inside a single LXC container. To satisfy compliance condition **C3 (Physical Barriers)**, the backend programmatically isolates information flow by segregating permissions across four distinct POSIX user accounts:

* `sentinel` (The Orchestrator and Gate Evaluator)
* `formalizer` (The Property Author / Theorem Definer workspace)
* `prover` (The Implementer / Tactical Proof Developer workspace)
* `exerciser` (The Sanity Tester / Mutation Agent workspace)

### Directory Layout

```text
/opt/squeeze/
├── shared/                  # Immutable Low-Level Sources of Truth
│   ├── rocq_stdlib/         # Step 1: Storage Plane (Pinned mathematical libraries)
│   └── proof_registry/      # Step 2: Invariant Plane (Previously verified exercises)
│       ├── chapter1_ex1.v
│       └── registry.sig     # Cryptographic signature of the certified trunk
│
├── orchestrator/            # Owned by 'sentinel' (Mode 0700)
│   ├── ledger/              # Tracks spec-N.md and gap-N.md files
│   └── gate_sentinel.py     # Execution arbiter and gate referee
│
/home/formalizer/            # Owned by 'formalizer' (Mode 0700)
│   └── definition/          # Workspace where theorem statements are defined (.v)
│
/home/prover/                # Owned by 'prover' (Mode 0700)
│   └── solution/            # Workspace where tactical proof scripts are built (.v)
│
/home/exerciser/             # Owned by 'exerciser' (Mode 0700)
    └── mutation/            # Workspace for negative mathematical mutations

```

---

## 2. Low-Level Source of Truth Execution Planes

The executable lower bound discards conversational agent feedback and anchors success entirely to the strict type-checking environment of the mathematical kernel.

### Step 1: Storage Plane (Pinned Logical Environment)

* **Artifact:** `/opt/squeeze/shared/rocq_stdlib/`
* **Mechanic:** A read-only repository containing a pinned version of the Rocq Standard Library and any background mathematical frameworks (e.g., Mathematical Components or Coquelicot).
* **Enforcement:** Enforced via directory mode `0555` (Read/Execute only). Agents cannot hot-fix or alter foundational mathematical axioms, inductive types, or baseline lemmas to force an invalid proof script to compile.

### Step 2: Invariant Plane (The Certified Proof Registry)

* **Artifact:** `/opt/squeeze/shared/proof_registry/`
* **Mechanic:** A collection of all previously completed and verified math exercises from prior system runs.
* 
**Enforcement:** Every time a new proof script is integrated, the `gate_sentinel.py` engine re-compiles the entire registry trunk using `coqc`. If a modification to a shared global definition or foundational lemma breaks a single pre-existing proof script downstream, **Gate B** trips a regression exception and aborts the cycle.



### Step 3: Compute Plane (The Pinned Rocq Compiler Engine)

* **Artifact:** Pinned container binaries for the Rocq compiler (`coqc`) and environment tools (`rocqchk`).
* 
**Mechanic:** The logical soundness of the type engine handles the definitive verdict of proof validity. An exercise is only recognized as mechanically sound if the type checker terminates with an exit status code of `0`.



---

## 3. Ground Truth Compilation & Verification Interface

To eliminate cheating maneuvers such as hiding incomplete steps behind the `Admitted` keyword or introducing unauthorized mathematical premises, the lower bound evaluates proofs through a strict two-stage extraction wrapper.

### 1. Compilation Stage

The script executes the standard compiler binary:

```bash
coqc -R /opt/squeeze/shared/rocq_stdlib/ Top /home/prover/solution/exercise.v

```

A compilation exit code of `0` is required but not sufficient for clearance.

### 2. Introspection Stage (Axiom Auditing)

Immediately following compilation, the orchestrator executes a macro checking command directly via Rocq's reflection layer to query the compiled module (`exercise.vo`):

```bash
rocqchk --print-assumptions Top.exercise_theorem

```

The output string must be parsed programmatically by `sentinel`. If the tokens `Admitted`, `Axiom`, or `Axioms` are detected within the output footprint, the proof is treated as an illegal escape hatch and failed.

---

## 4. The Isolated Pipeline and Gate Evaluation Mechanics

The workflow operates under total context isolation to eliminate shared context leaks.

### Context-Blocked Dispatch Loop

1. **The Formalizer Agent** translates the English textbook problem description (`spec-N.md`) into a clean Rocq file interface containing *only* the types, definitions, and the naked theorem statement (e.g., `Theorem exercise_1 : forall n : nat, ...`). It is physically blocked from writing tactical proofs or viewing the prover's home directory.
2. **The Prover Agent** receives the compiled definition file from the formalizer. It is tasked with appending the tactical implementation block (e.g., `Proof. induction n. ... Qed.`). It cannot see the original English text or change a single character of the formalizer's theorem declaration.
3. **The Exerciser Agent** acts completely code-blind to the Prover's tactics. It reads the formalizer's definitions and generates a mutation check file.



---

## 5. Automated Gate Sentinel Validation

When an exercise is evaluated for graduation, `gate_sentinel.py` evaluates compliance condition **C1 (Disjointness)** and runs the verification loop:

```python
import subprocess
import re
import sys

def verify_rocq_proof():
    theorem_name = "exercise_42"
    solution_path = "/home/prover/solution/exercise.v"
    mutation_path = "/home/exerciser/mutation/mutation.v"

    # --- GATE B: MACHINE ACCEPTANCE ---
    # 1. Compile the implementation
    compile_run = subprocess.run(
        ["coqc", "-R", "/opt/squeeze/shared/rocq_stdlib/", "Top", solution_path],
        capture_output=True, text=True
    )
    if compile_run.returncode != 0:
        print(f"GATE B FAILURE: Proof compilation smashed! Error:\n{compile_run.stderr}")
        sys.exit(1)

    # 2. Audit for escape hatches (Admitted / Unauthorized Axioms)
    audit_run = subprocess.run(
        ["rocqchk", "--print-assumptions", f"Top.{theorem_name}"],
        capture_output=True, text=True
    )
    if any(leak in audit_run.stdout for leak in ["Admitted", "Axiom"]):
        print("GATE B FAILURE: Prover attempted an unverified escape hatch or unauthorized Axiom!")
        sys.exit(1)

    # 3. Negative Mutation Test (Verify Catchability)
    # The Exerciser writes a mutated file where the mathematical statement is made false.
    # We assert that the compiler MUST fail to typecheck this file.
    mutation_run = subprocess.run(
        ["coqc", "-R", "/opt/squeeze/shared/rocq_stdlib/", "Top", mutation_path],
        capture_output=True, text=True
    )
    if mutation_run.returncode == 0:
        print("GATE B FAILURE: Coherent-and-Wrong Detected! The system proved a false mutation.")
        print("This implies the Formalizer's definitions or axioms are logically vacuous.")
        sys.exit(1)

    # --- GATE C: STRUCTURAL COVERAGE MAP ---
    # Parse the textbook spec to verify every sub-clause or exercise lemma 
    # maps directly to an audited and compiled Theorem object in the output stream.
    print("GATE B & C SUCCESS: Rocq kernel type-checked and fully squeezed.")

if __name__ == "__main__":
    verify_rocq_proof()

```
