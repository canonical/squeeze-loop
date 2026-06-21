(* exercise_good.v -- PROVER fixture: a CORRECT, fully discharged proof.
 *
 * Canonical deployed path: /home/prover/solution/exercise.v
 * EXERCISE_ID: EX_ROCQ_074   (theorem name: exercise_42, module Top.exercise_42)
 *
 * This is the positive witness: where Rocq is installed, the gate MUST
 * type-check this (exit 0), and `rocqchk --print-assumptions Top.exercise_42`
 * MUST report "Closed under the global context" (no Admitted / no Axiom).
 *
 * Self-contained (prelude only: nat, Nat.add, plus_n_O, plus_n_Sm) so it
 * compiles under a bare `coqc` even before the full stdlib plane is laid down.
 * Terminates with Qed. (no Admitted/Axiom/Parameter escape hatch).
 *)

Theorem exercise_42 : forall n m : nat, n + m = m + n.
Proof.
  intros n m.
  induction n as [| n' IHn].
  - simpl. rewrite <- plus_n_O. reflexivity.
  - simpl. rewrite IHn. rewrite <- plus_n_Sm. reflexivity.
Qed.
