(* FALSE mutation of MEDIUM: (n+m)+p = n+(m+S p). *)
Theorem ex_med_mut : forall n m p : nat, (n + m) + p = n + (m + S p).
Proof. intros n m p. induction n as [|n' IH]; simpl; [reflexivity | rewrite IH; reflexivity]. Qed.
