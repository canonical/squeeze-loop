(* chapter1_ex1.v -- CERTIFIED PROOF REGISTRY entry (Invariant Plane, spec D2)
 *
 * A previously verified exercise from a prior system run. The gate_sentinel
 * re-compiles this trunk on every cycle (Gate B regression guard, spec D2):
 * if a shared global definition or foundational lemma is altered in a way that
 * breaks this proof, the cycle aborts.
 *
 * This file is INTENTIONALLY self-contained: it depends only on the Rocq/Coq
 * prelude (the native inductive `nat` and `Nat.add`), so it type-checks under a
 * bare `coqc` with no external libraries. That makes it a real, runnable
 * lower-bound witness wherever Rocq is installed.
 *
 * Canonical EXERCISE_ID for this trunk entry: EX_ROCQ_001
 * Canonical theorem name:                     registry_add_comm
 *)

Theorem registry_add_comm : forall n m : nat, n + m = m + n.
Proof.
  intros n m.
  induction n as [| n' IHn].
  - simpl. rewrite <- plus_n_O. reflexivity.
  - simpl. rewrite IHn. rewrite <- plus_n_Sm. reflexivity.
Qed.
