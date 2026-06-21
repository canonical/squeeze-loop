(* FALSE mutation of EASY: n + m = m + S n (off-by-one successor). *)
Theorem ex_easy_mut : forall n m : nat, n + m = m + S n.
Proof. intros n m. induction n as [|n' IH]; simpl.
  - rewrite <- plus_n_O. reflexivity.
  - rewrite IH. rewrite <- plus_n_Sm. reflexivity. Qed.
