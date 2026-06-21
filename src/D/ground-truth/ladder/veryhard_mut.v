(* FALSE mutation of VERY HARD: 2^n <= n (false for n >= 1). PeanoNat in scope, so
 * rejection is because the statement is false. *)
Require Import PeanoNat.
Theorem ex_vhard_mut : forall n : nat, Nat.pow 2 n <= n.
Proof. intros n. apply Nat.le_refl. Qed.
