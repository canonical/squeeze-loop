(* Tier TRIVIAL -- one rewrite, no real induction depth. A capable prover passes ~100%. *)
Theorem ex_triv : forall n : nat, n + 0 = n.
Proof. intros n. induction n as [|n' IH]; simpl; [reflexivity | rewrite IH; reflexivity]. Qed.
