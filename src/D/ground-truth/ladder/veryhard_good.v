(* Tier VERY HARD -- n <= 2^n needs induction with 2^(S n) = 2*2^n and a bound
 * step. The reference witness is left OPEN (Admitted): this rung is beyond the
 * cheap certified comparator. The axiom audit MUST catch the Admitted -- the gate
 * stays honest rather than letting a vacuous proof through. Left to a live prover. *)
Require Import PeanoNat.
Theorem ex_vhard : forall n : nat, n <= Nat.pow 2 n.
Proof. intros n. Admitted.
