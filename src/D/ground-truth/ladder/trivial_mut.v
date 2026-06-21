(* FALSE mutation of TRIVIAL: n + 0 = S n. Honest attempt cannot close it -> coqc REJECTS. *)
Theorem ex_triv_mut : forall n : nat, n + 0 = S n.
Proof. intros n. reflexivity. Qed.
