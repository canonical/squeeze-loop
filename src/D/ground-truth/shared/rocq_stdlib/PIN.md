# Storage Plane -- Pinned Logical Environment (spec D2, Step 1)

This directory is the **immutable mathematical environment** the whole squeeze is
type-checked against. It pins the Rocq Standard Library (and optionally a
background framework such as MathComp / Coquelicot) to an exact version, so that
no agent can hot-fix a foundational axiom, inductive type, or baseline lemma to
force an invalid proof script to compile.

## What is pinned

| Item | Pinned value | Where it actually comes from |
|---|---|---|
| Rocq / Coq compiler (`coqc`) | **8.20.1** (Coq) / Rocq 9.x equiv. | baked into the LXC image via `provision.sh` (`opam install coq.8.20.1`) |
| Rocq Standard Library | the stdlib shipped with that exact `coqc` | the same opam switch |
| Logical root for this plane | `Top` (via `coqc -R <this dir> Top ...`) | the `gate_sentinel.py` invocation |

## Why this directory is (mostly) empty here

The Coq/Rocq stdlib is **thousands of `.v`/`.vo` files** that are an artifact of
the pinned compiler install, not source we author. Vendoring them into git would
be (a) enormous and (b) a lie about provenance — the canonical stdlib is the one
that ships with the pinned `coqc`. So:

* **In the container** (`provision.sh`): this directory is populated read-only
  (`0555`) by symlinking / copying the stdlib of the pinned opam switch, then
  frozen. That is the real Storage Plane.
* **In this repo**: we ship only this `PIN.md` (the version contract) plus the
  small, self-contained witness proofs the gate genuinely needs. The witness
  proofs deliberately depend ONLY on the prelude (`nat`, `Nat.add`), so they
  type-check under a bare `coqc` even before the full stdlib is laid down.

Enforcement: directory mode `0555` (read/execute only) is applied by
`provision.sh` as root inside the container. Off-container (no root) it is
best-effort and the verifier warns rather than fails.
