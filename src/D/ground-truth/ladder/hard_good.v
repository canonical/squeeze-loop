(* Tier HARD -- multiplication commutativity. From primitives this needs invented
 * lemmas (mult_n_Sm + add comm/assoc); the certified witness leans on the library
 * comparator Nat.mul_comm, exactly as the easy proof leans on plus_n_O/plus_n_Sm. *)
Require Import PeanoNat.
Theorem ex_hard : forall n m : nat, n * m = m * n.
Proof. intros n m. apply Nat.mul_comm. Qed.
