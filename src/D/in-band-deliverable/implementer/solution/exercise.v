(* exercise.v -- PROVER BAND deliverable (in-band-deliverable-spec D1).
 *
 * Canonical deployed path: /home/prover/solution/exercise.v
 * EXERCISE_ID: EX_ROCQ_074   (theorem name: exercise_42, module Top.exercise_42)
 *
 * The prover imports the formalizer's UNALTERABLE signature module
 * (Top.exercise_sig) and discharges the goal with a tactical proof terminating
 * in `Qed.`. It is CODE-BLIND to the exerciser's mutation matrix: it sees only
 * the naked theorem statement and the textbook ceiling, never the tests.
 *
 * Execution constraints honoured (spec D1):
 *   - Signature preservation: the `Theorem exercise_42 : ...` line is a verbatim
 *     restatement of `exercise_sig.exercise_42_statement`; not a token is altered
 *     to make the path easier.
 *   - No escape hatches: the script terminates with `Qed.`; there is no
 *     `Admitted` / `Axiom` / `Skip` / `Parameter` block. The gate's axiom audit
 *     (rocqchk --print-assumptions Top.exercise_42) MUST report
 *     "Closed under the global context".
 *
 * Proof: commutativity of nat addition by structural induction over the first
 * argument, using the prelude lemmas `plus_n_O` (n = n + 0) and `plus_n_Sm`
 * (S (n + m) = n + S m). Self-contained (prelude only) so it type-checks under a
 * bare `coqc` as well as under the full pinned stdlib plane.
 *)

Require Import Top.exercise_sig.

Theorem exercise_42 : forall n m : nat, n + m = m + n.
Proof.
  intros n m.
  induction n as [| n' IHn].
  - simpl. rewrite <- plus_n_O. reflexivity.
  - simpl. rewrite IHn. rewrite <- plus_n_Sm. reflexivity.
Qed.

(* Cross-check that the discharged theorem inhabits the formalizer's exact
 * proposition (no signature drift). This is a type-level assertion, not a new
 * axiom: it adds nothing to Print Assumptions. *)
Check (exercise_42 : exercise_42_statement).
