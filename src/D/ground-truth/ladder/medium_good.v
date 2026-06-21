(* Tier MEDIUM -- associativity; induction with the IH applied under a context. *)
Theorem ex_med : forall n m p : nat, (n + m) + p = n + (m + p).
Proof. intros n m p. induction n as [|n' IH]; simpl; [reflexivity | rewrite IH; reflexivity]. Qed.
