(* exercise_admitted.v -- PROVER fixture: an ESCAPE-HATCH cheat.
 *
 * The statement is TRUE and the file COMPILES (exit 0), but the proof is closed
 * with `Admitted.` instead of `Qed.`. This is the classic deductive cheat:
 * Gate B's compile stage passes, but the axiom-audit stage
 * (`rocqchk --print-assumptions Top.exercise_42`) MUST report the admitted
 * obligation, and the gate MUST reject it.
 *
 * Use: where Rocq is installed, this demonstrates that compile-success alone is
 * insufficient and the introspection stage genuinely catches the hatch.
 *)

Theorem exercise_42 : forall n m : nat, n + m = m + n.
Proof.
  intros n m.
Admitted.
