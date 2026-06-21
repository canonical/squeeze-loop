# Ground Truth — Rocq Formal-Verification Squeeze (Use Case D)

Implementation of the **Low-Level Sources of Truth** for the system in
[`../ground-truth-spec.md`](../ground-truth-spec.md). These planes are the
executable lower bound the whole squeeze is squeezed against: the pinned
mathematical environment proofs are checked in, the certified registry their
results may never silently break, and the frozen Rocq kernel that delivers the
definitive verdict of proof validity.

The governing rule is enforced by construction: **correctness is a machine
verdict, never an assertion.** A proof counts only if a real Rocq kernel
type-checks it (exit 0) AND the axiom audit shows no escape hatch AND every
false mutation is genuinely rejected. Nothing here fakes a green check.

## HONESTY / capability gating (read this first)

Rocq is **not** installed on the authoring machine (`coqc`, `rocqchk`, `rocq`,
`coqtop` are all absent; only `opam` exists), and the LXC runs offline. So:

* Every `coqc`/`rocqchk` call goes through `rocq_kernel.py`, which is
  **capability-gated**. If the binary is present it runs FOR REAL; if absent the
  harness prints `DEPENDENCY UNMET: Rocq (coqc/rocqchk) not installed` and exits
  **3 (SKIPPED)**. There is no code path that returns "compiled OK" /
  "axiom-clean" / "mutation caught" without a real kernel saying so.
* Everything that does NOT need Rocq (registry signing/verification, manifest &
  mutation-matrix parsing, clause→coverage mapping, Gate A/C logic, leak-token
  detection, gate orchestration) actually RUNS and is self-checked by
  `verify_ground_truth.py`.
* The `.v` fixtures are real: where Rocq IS installed, `gate_sentinel.py
  --fixtures` genuinely type-checks a correct proof and genuinely REJECTS the
  false `n + m = m + S n` mutation and the `Admitted` cheat. Catchability is
  demonstrable, not asserted.

## The three planes (spec §2)

| Plane | Spec | Artifact | Built / pinned by |
|---|---|---|---|
| **Storage** (Step 1) | pinned stdlib, `0555` read/exec only | `shared/rocq_stdlib/` (PIN.md here; real `.vo` tree in container) | `provision.sh` (`opam install coq`) |
| **Invariant** (Step 2) | certified proof registry + signature | `shared/proof_registry/*.v`, `shared/proof_registry/registry.sig` | `build_ground_truth.py` (signs trunk) |
| **Compute** (Step 3) | frozen Rocq kernel, no overrides | pinned `coqc`/`rocqchk` (8.20.1) | LXC image; gated by `rocq_kernel.py` |

## Four-POSIX-user isolation model (spec §1)

| User | Workspace (0700) | Role |
|---|---|---|
| `sentinel` | `/opt/squeeze/orchestrator` | orchestrator + `gate_sentinel.py` |
| `formalizer` | `/home/formalizer/definition` | naked theorem statements (`.v`) |
| `prover` | `/home/prover/solution` | tactical proof scripts (`.v`) |
| `exerciser` | `/home/exerciser/mutation` | negative mutation matrix + mutation `.v` |

The directory/permission MODEL is documented and printed by
`build_ground_truth.py`; the actual `chown`/`chmod` to these users (and laying
down the read-only stdlib tree) needs root and lives in `provision.sh` /
the LXC step — we are unprivileged here, so it is guarded.

## Files

| File | Role |
|---|---|
| `rocq_kernel.py` | The ONLY shell-out to `coqc`/`rocqchk`. Capability-gated; never fabricates a verdict. |
| `registry.py` | Pure-Python certified-registry trunk: enumerate, sign, verify (`registry.sig`). |
| `gate_sentinel.py` | The gate referee. Gates A/C (pure parse) + Gate B (kernel, gated). `--fixtures` mode runs against the in-repo `.v`. |
| `build_ground_truth.py` | Pins the stdlib contract, signs the registry, prints the four-user model. Deterministic. |
| `verify_ground_truth.py` | Self-check: pin present, registry sig recompute, pure-Python gate logic sanity, kernel availability (honest SKIP). |
| `provision.sh` | Root-only: `opam install coq` (networked), create the four users, deploy planes with correct owners/modes. |
| `fixtures/` | Real `.v` + manifest + matrix used by `--fixtures` and the self-check (see below). |
| `shared/contract.md` | **Machine-readable CONTRACT** the other two layers target (paths, names, invocations, schema). |

### `fixtures/`

| File | What it proves |
|---|---|
| `exercise_sig.v` | formalizer's naked statement (`exercise_42_statement : Prop`) |
| `exercise_good.v` | CORRECT proof of `exercise_42` — must type-check, axiom-clean |
| `exercise_admitted.v` | `Admitted` cheat — compiles but the audit must catch it |
| `exercise_mut_identity_flip.v` | FALSE mutation `n + m = m + S n` — `coqc` must reject |
| `mutation_matrix.json` | canonical exerciser output (schema in `shared/contract.md`) |
| `textbook_manifest.md`, `spec-1.md` | manifest + plan blueprint for Gate A/C |

## Usage

```bash
python3 build_ground_truth.py          # pin stdlib contract, sign registry trunk
python3 verify_ground_truth.py         # self-check (non-kernel runs; kernel SKIPs if absent)
python3 gate_sentinel.py --fixtures    # full gate; Gate B is REAL where Rocq exists, else DEPENDENCY UNMET (exit 3)
sudo ./provision.sh                     # deploy + install Rocq (run as root, while networked)
```

To prove catchability where Rocq is installed:

```bash
python3 gate_sentinel.py --fixtures --solution exercise_good.v      # -> ALL GATES PASSED
python3 gate_sentinel.py --fixtures --solution exercise_admitted.v  # -> GATE B FAILURE (axiom leak)
# the identity-flip mutation is exercised automatically in Gate B step B4
```

## What `verify_ground_truth.py` guarantees (off-Rocq)

1. **Pin contract** — `rocq_stdlib/PIN.md` (the Storage-Plane version contract) exists.
2. **Registry signature** — recomputing the per-file digests and the trunk digest
   reproduces `registry.sig` exactly; a single changed byte in any certified
   proof fails this (the Invariant Plane integrity check Gate B relies on).
3. **Gate logic sanity** — manifest clause parse = `{CLAUSE_1,2,3}`, Gate C
   coverage map and Gate A plan mapping hold on the fixtures, and the axiom-leak
   detector passes a clean banner while tripping on an `Admitted`/`Axiom` line.
4. **Kernel availability** — reports coqc/rocqchk present-or-SKIPPED honestly.

## CONTRACT (canonical for the other layers)

Full machine-readable form: [`shared/contract.md`](shared/contract.md). Summary:

* **Exercise id** `EX_ROCQ_074`; **theorem name** `exercise_42`; **module term**
  `Top.exercise_42`; **logical root** `Top`. (`exercise_theorem` is retired.)
* **Paths**: solution `/home/prover/solution/exercise.v`; signature
  `/home/formalizer/definition/exercise_sig.v`; mutations
  `/home/exerciser/mutation/mutation_matrix.json` (+ `*.v`); stdlib
  `/opt/squeeze/shared/rocq_stdlib`; registry `/opt/squeeze/shared/proof_registry`;
  manifest `/opt/squeeze/shared/textbook_manifest.md`.
* **Compile**: `coqc -R /opt/squeeze/shared/rocq_stdlib Top <file.v>`.
* **Audit**: `rocqchk --print-assumptions Top.exercise_42`; LEAK on
  `Admitted`/`Axiom`/`Axioms`/`admit`.
* **Gates**: A = manifest clauses ⊆ plan blueprint; B = registry recompiles +
  solution compiles + axiom-clean + every FALSE mutation rejected; C = manifest
  clauses ⊆ mutation `target_clauses`.

## Determinism / compute-plane pin

`registry.sig` is reproducible from the `.v` files (sorted sha256 trunk). The
**engine is part of the ground truth**: pin `coqc`/`rocqchk` 8.20.1 in the LXC
image (`provision.sh`). A different kernel version can change tactic/notation
behaviour — exactly the drift Step 3 freezes out. Changing a certified proof
re-certifies the trunk (the signature changes with it) and must go through the
state machine, not a silent edit.
