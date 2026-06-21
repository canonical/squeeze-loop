(* exercise_mut_identity_flip.v -- EXERCISER fixture: a FALSE mutation.
 *
 * Mutation MUT_001_IDENTITY_FLIP (target CLAUSE_2). The commutative target is
 * deformed to a known-false property:  n + m = m + S n  (off by one successor).
 *
 * This is the negative witness for "catchability" (gate §5 step 3): where Rocq
 * is installed, `coqc` MUST FAIL to type-check this file (nonzero exit). If it
 * ever succeeds, the formalizer's definitions are vacuous/inconsistent and the
 * build is aborted -- the "coherent-and-wrong" trap is sprung.
 *
 * We attempt the SAME honest tactic block the prover would use; it cannot close
 * the goal because the statement is false, so `reflexivity` (or the final goal)
 * is rejected by the kernel. Self-contained (prelude only).
 *)

Theorem exercise_42_mut : forall n m : nat, n + m = m + S n.
Proof.
  intros n m.
  induction n as [| n' IHn].
  - simpl. rewrite <- plus_n_O. reflexivity.   (* goal: m = S m  -- UNPROVABLE *)
  - simpl. rewrite IHn. rewrite <- plus_n_Sm. reflexivity.
Qed.
