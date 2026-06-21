# In-Band Deliverable Layer — Use Case D (Rocq / Coq)

Implementation of [`../in-band-deliverable-spec.md`](../in-band-deliverable-spec.md):
the two **deliverable bands** that sit between the upper bound (the textbook
specification manifest) and the lower bound (the Rocq type-checker + axiom
auditor), forced to collide over the kernel.

```
        [ UPPER BOUND: ../ground-truth/fixtures/textbook_manifest.md (EX_ROCQ_074) ]
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
   implementer/  (PROVER band)       exerciser/  (EXERCISER band)
   solution/exercise.v               mutation/mutation_matrix.json + *.v
              │                               │
              └───────────────┬───────────────┘
                              ▼  runner/execute_squeeze.py  (the squeeze)
        [ LOWER BOUND: coqc + rocqchk  (../ground-truth/rocq_kernel.py, gated) ]
```

The two bands are **physically isolated** (Physical Context Barrier): neither
imports, reads, or parses the other. The prover sees only the formalizer's naked
signature and the textbook ceiling — never the mutations. The exerciser sees only
the signature and the ceiling — never the tactical proof. Their alignment is
forced exclusively by the kernel verdict the runner collects.

## Canonical contract

This layer targets [`../ground-truth/shared/contract.md`](../ground-truth/shared/contract.md)
**exactly**:

| Concept | Value |
|---|---|
| Exercise id | `EX_ROCQ_074` |
| Theorem name | `exercise_42` |
| Module term (audited) | `Top.exercise_42` |
| Logical root | `Top` |
| Prover solution | `/home/prover/solution/exercise.v` |
| Formalizer signature | `/home/formalizer/definition/exercise_sig.v` (`Require Import Top.exercise_sig.`) |
| Exerciser output | `/home/exerciser/mutation/mutation_matrix.json` (+ mutation `.v`) |
| Compile | `coqc -R /opt/squeeze/shared/rocq_stdlib Top <file>` |
| Axiom audit | `rocqchk --print-assumptions Top.exercise_42` |

The in-band-spec draft (§1) and the contract agree on `exercise_42` /
`EX_ROCQ_074`; nothing was overridden. The spec's §2 example used a vacuous-
hypothesis guard with `phase: axiom_audit` and a prose `error_token`; the
contract's machine schema only recognises `type_check | axiom_audit` phases and
treats any `status: FAIL` mutation as "coqc must reject", so the emitted matrix
keeps the guard but pairs it with a real `Unable to unify` error_token (what the
kernel actually emits for the synthesized discharge).

## Layout

| Path | Band | Role |
|---|---|---|
| `implementer/solution/exercise.v` | Prover | The deliverable: imports `Top.exercise_sig`, restates `Theorem exercise_42` verbatim, discharges it by induction (`plus_n_O` / `plus_n_Sm`), ends in `Qed.`. No `Admitted/Axiom/Skip/Parameter`. Blind to the mutations. |
| `implementer/build_solution.py` | Prover | Emits/validates `exercise.v`; self-checks signature preservation, the `Qed.` terminator, and the absence of escape hatches. Does NOT call the kernel. |
| `exerciser/mutation/mutation_matrix.json` | Exerciser | The deliverable: `MUT_001_IDENTITY_FLIP` (`n+m = m+S n`, type_check) and `MUT_002_VACUOUS_HYPOTHESIS_GUARD` (`False -> comm`, axiom_audit), each with `target_clauses` + `mutated_theorem_statement` + `expected_compiler_feedback`. |
| `exerciser/mutation/*.v` | Exerciser | The mutated Rocq sources the kernel must reject. |
| `exerciser/build_mutation_matrix.py` | Exerciser | Authors the matrix + `.v` from the signature/ceiling alone. Blind to the proof. Does NOT call the kernel. |
| `runner/mutations.py` | Sentinel | Resolves a mutation's `.v` (shipped or synthesized per the contract) and hands it to the gated kernel. |
| `runner/execute_squeeze.py` | Sentinel | The Squeeze Connector. Verifies isolation, then CALLS the ground-truth referee (`gate_sentinel`'s Gate A/C + the kernel boundary `rocq_kernel`) for Gate B. Never reimplements the gate. |

## Usage

```bash
# Prereqs: ../ground-truth present (gate_sentinel.py, rocq_kernel.py, fixtures, registry).
python3 implementer/build_solution.py --check       # validate the prover deliverable
python3 exerciser/build_mutation_matrix.py          # (re)generate matrix + mutation .v
python3 runner/execute_squeeze.py                   # run the squeeze
```

## What the runner checks

- **ISOLATION** — prover and exerciser bands have zero import/path linkage to each
  other (Physical Context Barrier), verified by AST + path scan.
- **GATE A** (pure) — every manifest `CLAUSE_x` is accounted for in the plan
  blueprint (`spec-1.md`). Delegated to `gate_sentinel.gate_a`.
- **GATE C** (pure) — every manifest `CLAUSE_x` has a `target_clauses` entry in
  the mutation matrix. Delegated to `gate_sentinel.gate_c`.
- **GATE B** (Rocq, capability-gated) — recompile the certified registry trunk;
  compile the prover solution (exit 0); axiom-audit it (no `Admitted`/`Axiom`
  leak); confirm **every FALSE mutation is rejected** by the kernel. A mutation
  that type-checks is the *coherent-and-wrong* crash.

## Honesty / capability gating

Rocq is **not** installed on the authoring machine (`coqc`, `rocqchk` absent;
only `opam`). Every kernel step goes through `../ground-truth/rocq_kernel.py`,
which is capability-gated. With Rocq absent the runner prints

```
DEPENDENCY UNMET: Rocq (coqc) not installed
```

and exits **3 (Gate B SKIPPED)** — it never fabricates a compile, an axiom-clean
audit, or a caught mutation. The pure gates (A, C) and the isolation check still
run and can fail honestly. Where Rocq IS present (e.g. inside the LXC after
`provision.sh`), Gate B runs for real: the correct proof type-checks, the
identity-flip and vacuous-guard mutations are genuinely rejected, and an
`Admitted` cheat is caught by the audit.
