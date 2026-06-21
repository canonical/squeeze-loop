#!/usr/bin/env python3
"""Seeded coherent-and-wrong PROVER -- a permanent fixture for the Use Case D
evidence harness (the paper's seeded-defect measurement).

This emits a prover deliverable (`exercise.v`) that is INTERNALLY CONSISTENT and
fully discharged with `Qed.` (no syntactic cheat), but proves an ADJACENT, WEAKER
proposition instead of the mandated commutativity: it proves the right-identity
`forall n : nat, n + 0 = n` while still naming the theorem `exercise_42`. It is
"coherent" (the kernel happily type-checks it) yet "wrong" (it discharges the
wrong goal -- it does NOT inhabit `exercise_sig.exercise_42_statement`).

The squeeze MUST catch it. Two independent traps fire (whichever the gate reaches
first, both need the real kernel):

  * Signature preservation / type mismatch: the file's `Check (exercise_42 :
    exercise_42_statement).` assertion fails to type-check, so `coqc` rejects the
    file at Gate B step B2 (the signature was silently weakened).
  * Even absent that assertion, `Top.exercise_42` would have the wrong type, so
    no honest downstream use of the commutativity lemma would type-check.

This is the coherent-and-wrong failure the whole strategy exists to exclude:
a real, axiom-clean Qed proof -- of the wrong theorem.

`--emit <path>` writes the wrong exercise.v to <path> (default: a sibling temp).
It calls NO kernel; whether the trap actually fires is the gate's verdict and is
capability-gated on Rocq.
"""

import argparse
import sys
from pathlib import Path

# A genuine, axiom-clean Qed proof -- of the WEAKER right-identity, not commutativity.
WRONG_SOURCE = """(* exercise.v -- SEEDED COHERENT-AND-WRONG prover deliverable.
 *
 * Internally consistent and closed with Qed. (no Admitted/Axiom escape hatch),
 * but it proves the ADJACENT, WEAKER right-identity  n + 0 = n  instead of the
 * mandated commutativity  n + m = m + n. The signature is silently weakened.
 *
 * Gate B must reject it: the type-level cross-check against the formalizer's
 * exact proposition fails, so `coqc` does not accept the file. A clean compile
 * of the RIGHT theorem is the only thing that passes -- a clean compile of the
 * WRONG theorem is exactly what the squeeze exists to exclude.
 *)

Require Import Top.exercise_sig.

Theorem exercise_42 : forall n : nat, n + 0 = n.
Proof.
  intros n.
  induction n as [| n' IHn].
  - simpl. reflexivity.
  - simpl. rewrite IHn. reflexivity.
Qed.

(* The honest cross-check the correct deliverable carries. Here it FAILS to
 * type-check because exercise_42 has the wrong type -- this is the trap. *)
Check (exercise_42 : exercise_42_statement).
"""


def main():
    ap = argparse.ArgumentParser(description="emit a coherent-and-wrong exercise.v")
    ap.add_argument("--emit", help="path to write the wrong exercise.v")
    a = ap.parse_args()
    if a.emit:
        Path(a.emit).write_text(WRONG_SOURCE)
        print(f"wrote coherent-and-wrong deliverable -> {a.emit}")
        return 0
    sys.stdout.write(WRONG_SOURCE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
