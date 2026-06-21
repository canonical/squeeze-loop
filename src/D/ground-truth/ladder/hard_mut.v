(* FALSE mutation of HARD: n * m = S (m * n). Nat.mul_comm is in scope, so the
 * rejection is genuinely because the statement is false (unification fails). *)
Require Import PeanoNat.
Theorem ex_hard_mut : forall n m : nat, n * m = S (m * n).
Proof. intros n m. apply Nat.mul_comm. Qed.
