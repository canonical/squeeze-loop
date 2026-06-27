# Use Case D — formally verified proofs that the kernel checks

Use Case D is a **base** squeeze loop (`id: instance-d`, **`kind: base`**, terrain **A**
with a *deductive* lower bound), encoded as [`src/D/instance-d.sl.json`](../instance-d.sl.json)
and written up as the skill
[`src/D/config/skills/use-case-d`](../config/skills/use-case-d/SKILL.md). Its deliverable:
**formally verified Rocq (Coq) proofs of textbook arithmetic — e.g. commutativity of `+` on
`nat` — that the kernel itself certifies.**

## Rationale — why this loop exists

The terrain is **transcription with a deductive lower bound**: the textbook states what
must be proved, and the Rocq kernel decides mechanically whether it *was*. The dominant
failure is the proof that closes the wrong goal:

> **Coherent-and-wrong = the prover discharges `Qed.` on an adjacent weaker claim under the
> intended theorem name** (right-identity `n+0=n` instead of commutativity `n+m=m+n`), **or
> smuggles an axiom** to close a goal it could not prove.

The squeeze pins three actors against an immutable kernel:

- **Upper bound `U`** — the textbook manifest (English + scope clauses), sharpened by the
  **formalizer** into a precise formal statement (whose own lower bound is *expressibility*:
  it must type-check under `coqc` + the pinned stdlib).
- **Lower bound `L`** — the **deductive kernel**: `coqc` (proof must reach `Qed.`) plus the
  axiom auditor `rocqchk --print-assumptions` (must report *"Closed under the global
  context"*, rejecting `Admitted`/`Axiom`). The stdlib is immutable; the prior-proofs
  registry recompiles each cycle.

## Graphical representation

![The `instance-d` SL — sentinel, theorem formalizer, tactical prover, and mutation
exerciser (orange) between the textbook manifest / formal statement (green, `U`) and the
Rocq kernel: stdlib, coqc, rocqchk, registry (pink, `L`); the prover and exerciser are
barriered (red dashed) from each other's artifacts](img/use-case-d.svg)

*Rendered from `instance-d.sl.json`. Solid edges are bounds (`U` / `L`) and `produces`; red
dashed edges are the `✗ must-not-see` barriers.*

| Actor | Role | Builds | `U` | `L` |
|---|---|---|---|---|
| **Gate sentinel** | coordinator | plan approval, gate verdicts, the axiom audit | the manifest clauses | registry recompiled + proof compiled + axiom audit clean + every mutation rejected |
| **Theorem formalizer** | property author | the formal theorem statement (the precise `U`) | the textbook exercise + scope clauses | expressibility: the statement type-checks under `coqc` + stdlib |
| **Tactical prover** | implementer | the tactical proof | the immutable formal statement | compiles to `Qed.` + passes the axiom audit |
| **Mutation exerciser** | exerciser | false-theorem mutations the kernel must reject | the manifest + the formal statement | each mutation must **fail** to compile |

## Disjointness at a glance

> **The hypothesis.** The formalizer holds only the English manifest (never the proof or
> mutations); the prover holds only the formal statement and the kernel (never the
> mutations); the exerciser holds the manifest and the statement and authors falsehoods the
> kernel must reject (never the proof). The **deductive kernel (`coqc` + `rocqchk`) is the
> immutable lower bound none of them can alter**, and the registry pins prior proofs against
> regression.

**Load-bearing barrier.** The prover never sees the mutations and the exerciser never sees
the proof; the formalizer sees neither (Unix `0700` homedirs; the prover imports the
statement one-way via `coqc Require` only). So the prover cannot tune to the tests and the
exerciser cannot crib the proof.

**Catchability — each blind spot is caught by a different actor:**

| Actor | Characteristic blind spot | Caught by | Via |
|---|---|---|---|
| Theorem formalizer | a vacuous / inconsistent statement (a false hypothesis that trivialises the goal) | **Mutation exerciser** | a vacuous-hypothesis mutation that should be rejected; the axiom audit catches smuggled axioms |
| Tactical prover | discharges an adjacent weaker theorem under the intended name | **Mutation exerciser** | identity-flip mutations the kernel must reject; type cross-check of the proof against the statement |
| Mutation exerciser | omits a mutation for some scope clause | **Gate sentinel** | Gate C requires every manifest clause to appear in some mutation's `target_clauses` |

**No terminus.** Instance D is a fully **mechanical** loop (`terminus: null`): the kernel
is the judge of last resort, so every claim is settled deductively — a wrong or
axiom-smuggling proof cannot survive `coqc` + the axiom audit. This is the strongest form
of the terrain-A soundness argument: the lower bound is a proof checker, not a test suite.

**Mechanical floor.** `sl_disjointness_check.py instance-d.sl.json` returns
**0 FAIL / 11 checks** — every actor reads no source it produced (D1), every barrier is
consistent with its bounds (D2), and each blind spot above is caught by a *different* actor
(C2). A green check certifies the **authorities are disjoint**, never that any theorem is
*done* — that lives in the `Qed.` + clean axiom audit + rejected mutations.

---

*Generated from [`src/D/instance-d.sl.json`](../instance-d.sl.json). Regenerate the
diagrams with:*

```sh
python config/skills/sl-internal/scripts/sl2plantuml.py \
    src/D/instance-d.sl.json -o src/D/docs/img/use-case-d.png
python config/skills/sl-internal/scripts/sl2plantuml.py \
    src/D/instance-d.sl.json --svg -o src/D/docs/img/use-case-d.svg
```
