---
name: use-case-d
description: The Squeeze Loop instance for Use Case D — formally verified Rocq (Coq) proofs of textbook arithmetic (e.g. commutativity of + on nat), on terrain A with a deductive lower bound (the Rocq kernel). The dominant failure is the prover discharging (Qed.) an adjacent weaker claim under the intended theorem name (e.g. right-identity n+0=n instead of n+m=m+n), or smuggling an axiom. The kernel (coqc) plus the axiom auditor (rocqchk --print-assumptions) is the immutable lower bound none of the actors can alter, and the exerciser authors false-theorem mutations the kernel must reject. Use when working on src/D — the textbook manifest, the formal theorem statement, the tactical proof, the false-theorem mutation matrix, the pinned Rocq stdlib, the prior-proofs regression registry, or the axiom audit. Trigger phrasings: "use case D", "instance D", "Rocq/Coq proof squeeze", "adjacent weaker theorem", "smuggled axiom / Admitted", "mutation must fail to compile", "Closed under the global context".
---

# Use Case D — the deductive-kernel proof squeeze loop

Use Case D is a **base** squeeze loop (`instance-d`, terrain **A** with a *deductive* lower
bound): formally verified Rocq proofs of textbook arithmetic. Its SL-1.0 self-description is
[`src/D/instance-d.sl.json`](../../../instance-d.sl.json); the companion write-up is
[`src/D/docs/use-case-d.md`](../../../docs/use-case-d.md).

## The dominant failure it guards

**Coherent-and-wrong here = the prover discharges `Qed.` on an adjacent weaker claim under
the intended theorem name** — proving right-identity `n+0=n` where the exercise asked for
commutativity `n+m=m+n` — **or smuggles an axiom** to close a goal it could not prove. The
proof compiles, the name matches, and the wrong theorem is "proved."

## The bounds

- **Upper bound `U`** — the textbook exercise manifest (English + scope clauses
  `CLAUSE_1..N`), sharpened by the **formalizer** into a precise formal theorem statement
  (the formalizer's lower bound is *expressibility*: the statement must type-check under
  `coqc` + the pinned stdlib).
- **Lower bound `L`** — the **deductive kernel**: `coqc 8.20.1` (the proof must compile to
  `Qed.`) **plus** the axiom auditor `rocqchk --print-assumptions` (must report *"Closed
  under the global context"* — rejecting `Admitted`/`Axiom`). The pinned stdlib is immutable
  (`root 0555`), and the prior-proofs registry is recompiled each cycle (no regression).

## The cast (four actors)

| Actor | Builds | `U` | `L` | Must not see |
|---|---|---|---|---|
| **Gate sentinel** (coordinator) | plan approval, gate verdicts, the axiom audit, the `.sl.json` | manifest clauses | registry recompiled + proof compiled + axiom audit clean + every mutation rejected | — |
| **Theorem formalizer** (property author) | the formal theorem statement (the precise `U`) | the textbook exercise + scope clauses | expressibility: the statement type-checks under `coqc` + stdlib | the proof, the mutations |
| **Tactical prover** (implementer) | the tactical proof | the immutable formal statement | compiles to `Qed.` + passes the axiom audit | the mutations |
| **Mutation exerciser** | false-theorem mutations the kernel must reject | manifest clauses + the formal statement | each mutation must **FAIL** to compile (it is genuinely false) | the proof |

## The barrier (physical, not honorary)

The prover never sees the mutations and the exerciser never sees the proof; the formalizer
sees neither — Unix `0700` homedirs, and the prover imports the statement one-way via
`coqc Require` only. The prover cannot tune to the mutations; the exerciser cannot crib the
proof's structure.

## The gates

- **Gate A (editorial).** The plan cites every manifest scope clause.
- **Gate B (machine).** The registry recompiles (no regression), the proof compiles to
  `Qed.`, the **axiom audit is clean** (no `Admitted`/`Axiom`/`admit`), and **every false
  mutation is rejected** by the kernel.
- **Gate C (coverage).** Every manifest clause appears in some mutation's `target_clauses`.

## Disjointness

The formalizer holds only the English manifest (never the proof or mutations); the prover
holds only the formal statement and the kernel (never the mutations); the exerciser holds
the manifest and the statement and authors falsehoods the kernel must reject (never the
proof). The deductive kernel (`coqc` + `rocqchk`) is the immutable lower bound none of them
can alter, and the registry pins prior proofs against regression. Catchability: a vacuous /
inconsistent statement is caught by the exerciser's vacuous-hypothesis mutation (and the
axiom audit catches smuggled axioms); an adjacent weaker theorem under the intended name is
caught by the exerciser's identity-flip mutations the kernel must reject; a missing mutation
for some clause is caught by the sentinel (Gate C).

```sh
python config/skills/sl-internal/scripts/sl_disjointness_check.py src/D/instance-d.sl.json
```

(0 FAIL / 11 checks.)
