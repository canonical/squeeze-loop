(* MUT_002_VACUOUS_HYPOTHESIS_GUARD -- EXERCISER BAND mutation (target CLAUSE_1, CLAUSE_3).
 * Goal guarded by a False hypothesis; the dishonest discharge ignores the hypothesis and tries `reflexivity` on a non-reflexive goal.
 * Self-contained (prelude only). Where Rocq is installed, `coqc` MUST
 * FAIL to type-check this file (nonzero exit) -- that rejection is the
 * catchability guarantee. If it ever compiles, the formalization is
 * vacuous/inconsistent and the coherent-and-wrong trap is sprung.
 *)
Theorem exercise_42_vacuous : False -> forall n m : nat, n + m = m + n.
Proof.
  intros _ n m.
  reflexivity.   (* goal: n + m = m + n -- NOT closed by reflexivity *)
Qed.
