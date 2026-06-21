(* exercise_sig.v -- FORMALIZER fixture (Property Author / Theorem Definer)
 *
 * Canonical deployed path: /home/formalizer/definition/exercise_sig.v
 * EXERCISE_ID: EX_ROCQ_074   (theorem name: exercise_42)
 *
 * The formalizer translates the English textbook problem into ONLY the types,
 * definitions, and the NAKED theorem statement -- no tactical proof. This file
 * is the unalterable contract the prover must import and the exerciser must
 * mutate. Compiled (with `coqc -R <stdlib> Top`) it becomes module Top.exercise_sig.
 *
 * The statement is left as a Definition of the *proposition* so the signature
 * file itself type-checks (kind-checks) without asserting a proof. The prover's
 * file restates the Theorem and discharges it; the gate audits Top.exercise_42.
 *)

(* The mandated formal statement (CLAUSE_1 universal quantification over nat,
 * CLAUSE_2 the exact equality n + m = m + n). Self-contained: prelude only. *)
Definition exercise_42_statement : Prop := forall n m : nat, n + m = m + n.
