(* MUT_001_IDENTITY_FLIP -- EXERCISER BAND mutation (target CLAUSE_2).
 * Off-by-one successor injected into the RHS: n + m = m + S n (FALSE).
 * Self-contained (prelude only). Where Rocq is installed, `coqc` MUST
 * FAIL to type-check this file (nonzero exit) -- that rejection is the
 * catchability guarantee. If it ever compiles, the formalization is
 * vacuous/inconsistent and the coherent-and-wrong trap is sprung.
 *)
Theorem exercise_42_mut : forall n m : nat, n + m = m + S n.
Proof.
  intros n m.
  induction n as [| n' IHn].
  - simpl. rewrite <- plus_n_O. reflexivity.   (* goal: m = S m -- UNPROVABLE *)
  - simpl. rewrite IHn. rewrite <- plus_n_Sm. reflexivity.
Qed.
