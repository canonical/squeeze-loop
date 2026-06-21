# CONTRACT -- Use Case D (Rocq) interface the three layers MUST target

This is the single source of truth for the paths, names, and invocations the
**upper-bound** and **in-band-deliverable** layers must align to. Where the three
spec drafts disagreed on naming, THIS file is canonical. (`ground-truth-spec.md`,
`upper-bound-spec.md`, and `in-band-deliverable-spec.md` showed `exercise_42`,
`exercise_theorem`, and `EX_ROCQ_074` interchangeably; resolved below.)

## Canonical identifiers

| Concept | Canonical value | Notes |
|---|---|---|
| Exercise id (manifest-level) | `EX_ROCQ_074` | the `## EXERCISE_ID:` key in `textbook_manifest.md` |
| Coq/Rocq theorem name | `exercise_42` | the discharged `Theorem exercise_42 : ...` |
| Fully-qualified module term | `Top.exercise_42` | what the axiom audit queries |
| Logical root of the stdlib plane | `Top` | from `coqc -R <stdlib> Top` |
| Registry trunk entry (example) | theorem `registry_add_comm` in `chapter1_ex1.v` | independent of the active exercise |

`exercise_theorem` (from the ground-truth draft §3.2 example) is RETIRED in favour
of `exercise_42`.

## Canonical file paths (deployed, inside the container)

| Path | Owner / mode | Producer | Consumer |
|---|---|---|---|
| `/opt/squeeze/shared/rocq_stdlib/` | root:root `0555` | provision.sh (pins stdlib) | all `coqc` calls |
| `/opt/squeeze/shared/proof_registry/*.v` | root:root `0444` | ground-truth (signed trunk) | Gate B regression |
| `/opt/squeeze/shared/proof_registry/registry.sig` | root:root `0444` | ground-truth | verify / Gate B |
| `/opt/squeeze/shared/textbook_manifest.md` | root:root `0444` | upper-bound | Gate A / Gate C |
| `/opt/squeeze/orchestrator/gate_sentinel.py` | sentinel `0700` | ground-truth | the runner |
| `/opt/squeeze/orchestrator/ledger/spec-N.md` | sentinel `0700` | coordinator | Gate A |
| `/home/formalizer/definition/exercise_sig.v` | formalizer `0700` | formalizer | prover (read-only import) |
| `/home/prover/solution/exercise.v` | prover `0700` | prover | Gate B (`coqc`) |
| `/home/exerciser/mutation/mutation_matrix.json` | exerciser `0700` | exerciser | Gate B/C |
| `/home/exerciser/mutation/*.v` | exerciser `0700` | exerciser | Gate B catchability |

## Canonical kernel invocations

Compile (Gate B, every `.v`):

    coqc -R /opt/squeeze/shared/rocq_stdlib Top /home/prover/solution/exercise.v

Axiom audit (Gate B introspection):

    rocqchk --print-assumptions Top.exercise_42
    # implemented as: <rocqchk|coqchk> -R <stdlib> Top -R <module_dir> Top -o Top.exercise_42
    # LEAK if output contains any of: Admitted, Axiom, Axioms, admit
    # CLEAN if output contains: "Closed under the global context"

Both are CAPABILITY-GATED (rocq_kernel.py): if `coqc`/`rocqchk` are absent the
gate prints `DEPENDENCY UNMET: Rocq (...) not installed` and exits 3 (SKIPPED).
No layer may treat absence as a pass.

## `mutation_matrix.json` schema (exerciser output)

```json
{
  "exercise_id": "EX_ROCQ_074",
  "theorem_name": "exercise_42",
  "mutations": [
    {
      "mutation_id": "MUT_001_IDENTITY_FLIP",
      "target_clauses": ["CLAUSE_2"],
      "description": "human text",
      "mutation_file": "exercise_mut_identity_flip.v",   // optional .v in the mutation dir
      "mutated_theorem_statement": "Theorem exercise_42_mut : forall n m : nat, n + m = m + S n.",
      "expected_compiler_feedback": {
        "status": "FAIL",            // FAIL means coqc MUST reject (catchability)
        "phase": "type_check",       // type_check | axiom_audit
        "error_token": "Unable to unify"
      }
    }
  ]
}
```

If `mutation_file` is present and exists, the gate compiles that file; otherwise
it synthesizes `<mutated_theorem_statement>\nProof. intros. reflexivity. Qed.`
For any mutation with `status == "FAIL"`, `coqc` exiting 0 trips the
"coherent-and-wrong" Gate B failure.

## registry.sig format

sha256sum(1)-compatible, sorted by filename, with a final trunk line:

    <sha256-of-file>  <filename.v>
    ...
    <sha256-of-the-per-file-block>  registry.sig.trunk

## Gate responsibilities

| Gate | Owner | Needs Rocq? | Does |
|---|---|---|---|
| **A** | sentinel | no | every manifest `CLAUSE_X` is accounted for in the plan blueprint (`spec-N.md`) |
| **B** | sentinel | YES | recompile registry trunk; compile solution (exit 0); axiom audit (no leak); every FALSE mutation rejected |
| **C** | sentinel | no | every manifest `CLAUSE_X` has a `target_clauses` entry in the mutation matrix |
