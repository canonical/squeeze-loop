# Upper Bound — Squeeze-Loop Textbook Manifest (Use Case D, Rocq)

> **Purpose:** the textbook specification manifest fixes the exact theorem to be
> proven (the statement, scope boundaries, and obligation clauses), so the prover
> cannot discharge a vacuous or adjacent weaker proposition instead.

Implementation of the **Upper Bound Source of Truth** for the system in
[`../upper-bound-spec.md`](../upper-bound-spec.md). The upper bound is the citable
normative ceiling: it translates the English mathematics of a reference textbook
into a strict, token-parsable form that fixes the strongest claim the
`formalizer` (property author) and `exerciser` agents may make. An agent that
softens a mathematical claim to clear a stuck proof, or quietly drops an
obligation, has breached the ceiling.

It is the counterpart to [`../ground-truth/`](../ground-truth/) (the executable
floor — the pinned Rocq kernel, signed proof registry, capability-gated `coqc`
verdicts): the manifest's obligation clauses are the *same* clauses the ground
truth's `gate_sentinel.py` enforces against the deployed
`/opt/squeeze/shared/textbook_manifest.md`.

## Binding to the contract

This layer targets [`../ground-truth/shared/contract.md`](../ground-truth/shared/contract.md)
**exactly** — that file is canonical where the spec drafts disagreed:

| Concept | Canonical value (this layer uses it verbatim) |
|---|---|
| Exercise id (`## EXERCISE_ID:` key) | `EX_ROCQ_074` |
| Theorem name | `exercise_42` |
| Module term / logical root | `Top.exercise_42` / `Top` |
| Deployed manifest path | `/opt/squeeze/shared/textbook_manifest.md` (root:root `0444`) |
| Obligation clause ids | `CLAUSE_1 .. CLAUSE_3` |
| Core negative vector | identity flip `n + m = m + S n`, defense = `coqc` type-check FAIL |

The clause ids, `EXERCISE_ID:` key, and `# TEXTBOOK_MANIFEST_START/END` markers
are token-identical to what the ground-truth sentinel's `parse_manifest_clauses`
reads, so the manifest authored here and the gates that consume it agree by
construction.

## Files

| File | Role |
|---|---|
| `textbook_manifest.md` | **The upper bound itself** — the normative ceiling, in the strict schema of spec §2 (`# TEXTBOOK_MANIFEST_START … END`): an `EX_ROCQ_074` block with English text, scope boundaries, sequential obligation clauses `CLAUSE_1..3`, the core negative vector (target mutation), and explicit NOT-claims. The D analogue of A's `metric_handbook.md`. |
| `manifest.py` | The single parser + structural validator. Turns the manifest into `Exercise` objects; `extract_block()` yields the per-exercise markdown the dispatch loop copies into `spec.txt` (§1). |
| `gate_checks.py` | The upper-bound-driven gate primitives (§3): `gate_a_plan` (blueprint maps every `CLAUSE_X`) and `gate_c_coverage` (mutation matrix targets every `CLAUSE_X`). PURE Python — no Rocq. |
| `validate_handbook.py` | Self-check: structure + **contract alignment** + **grounding** against the ground-truth fixtures + gate wiring. Exits nonzero on failure. |
| `provision.sh` | Deploys `textbook_manifest.md` to `/opt/squeeze/shared/textbook_manifest.md` (`root:root 0444`) and extracts the active `EXERCISE_ID` block to `/home/formalizer/spec.txt` and `/home/exerciser/spec.txt` (hidden from `prover`). Root-only ops are guarded. |

## Usage

```bash
python3 manifest.py            # list the parsed exercises
python3 validate_handbook.py   # structure + contract + grounding + gate wiring; exit 0 == sound
python3 gate_checks.py         # pilot: Gate A / Gate C on good and bad inputs
sudo ./provision.sh            # deploy (inside the LXC container)
```

## The schema (spec §2)

The active exercise block declares, in fixed tokens the parser keys on:

- `## EXERCISE_ID: EX_ROCQ_074`
- `**Textbook Reference:**`, `**Mathematical Domain:**`, `**Status:**` (`BINDING` | `DRAFT` | `DEPRECATED`)
- `### 1. English Exercise Text` — the verbatim natural-language claim
- `### 2. Explicit Mathematical Bounds (The Ceiling)` — `**Scope Boundary N:**` bullets
- `### 3. Enumerated Obligation Clauses` — `**CLAUSE_N:**` bullets (Gate A/C targets)
- `### 4. The Core Negative Vector (The Target Mutation)` — `**Target Mutation:**` + `**Expected System Defense:**`
- `### 5. Explicit NOT-Claims` — `**NOT_CLAIM_N:**` bullets

`manifest.py` enforces: markers present, unique exercise ids, all required fields,
valid status, English text present, at least one scope boundary, clause ids that
are **sequential `CLAUSE_1..N`** (no gaps) with at least one clause for every
`BINDING` exercise, a present target mutation + defense, and at least one
NOT-claim (the validation footprint must be bounded).

## How the upper bound drives the gates (spec §3)

Both gates are PURE Python and need no Rocq; their semantics match the ground-truth
sentinel exactly (set subset):

- **Gate A — Structural Specification Validation** — `gate_a_plan(exercise, plan_text)`
  asserts the coordinator's `spec-N.md` blueprint maps every `CLAUSE_X` of the
  active exercise (the id named verbatim, not a bare copy of the English text), so
  no obligation is silently dropped before any `.v` is compiled.
- **Gate C — Structural Coverage Map (coherent-and-wrong guard)** —
  `gate_c_coverage(exercise, matrix)` reads the code-blind exerciser's
  `mutation_matrix.json` and fails the build unless every `CLAUSE_X` appears in
  some mutation's `target_clauses`. This blocks the trap where `coqc` happily
  accepts an internally consistent proof of an adjacent, weaker, or vacuous
  statement.

`mutation_matrix.json` (written by the exerciser; full schema in `contract.md`):

```json
{
  "exercise_id": "EX_ROCQ_074",
  "theorem_name": "exercise_42",
  "mutations": [
    {"mutation_id": "MUT_001_IDENTITY_FLIP", "target_clauses": ["CLAUSE_2"], "...": "..."}
  ]
}
```

## Honesty / capability gating (no Rocq here)

Rocq is **not** installed on this machine, and nothing in this layer needs it.
Everything here — manifest parsing, contract alignment, clause→coverage mapping,
Gate A and Gate C — is pure Python and actually runs. The kernel-bound work
(Gate B: `coqc` compile, `rocqchk` axiom audit, mutation rejection) lives in
[`../ground-truth/`](../ground-truth/) behind `rocq_kernel.py`, which prints
`DEPENDENCY UNMET` and exits 3 (SKIPPED) when `coqc`/`rocqchk` are absent. This
layer never fabricates a kernel verdict; it constrains *what* the kernel must be
asked to prove.

## Relationship to A's `metric_handbook.md`

This is the structural twin of [`../../A/upper-bound/`](../../A/upper-bound/): A's
`metric_handbook.md` ceiling over a SQL warehouse becomes D's `textbook_manifest.md`
ceiling over a Rocq exercise; A's `handbook.py` → `manifest.py`; A's
`gate_a_plan`/`gate_c_assertions` → `gate_a_plan`/`gate_c_coverage`. A grounds
each metric against the warehouse (every number recomputes); D grounds each clause
against the ground-truth's example blueprint and mutation matrix (a compliant
downstream exists) and against the canonical contract.
