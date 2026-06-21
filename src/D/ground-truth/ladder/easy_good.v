(* Tier EASY -- structural induction + two prelude lemmas. *)
Theorem ex_easy : forall n m : nat, n + m = m + n.
Proof. intros n m. induction n as [|n' IH]; simpl.
  - rewrite <- plus_n_O. reflexivity.
  - rewrite IH. rewrite <- plus_n_Sm. reflexivity. Qed.
