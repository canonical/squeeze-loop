#!/usr/bin/env python3
"""Exerciser Band -- generate the Mutation & Sanity Matrix (in-band-spec D2).

The exerciser is CODE-BLIND to the prover's tactics: it imports / reads nothing
under the implementer band. It authors its negative challenge from the formalizer
signature and the textbook ceiling alone -- an independent attack on the logical
completeness of the formalization.

It emits, into mutation/ :
  * mutation_matrix.json   -- the schema from shared/contract.md (exercise_id,
                              theorem_name, mutations[]). Each mutation carries
                              target_clauses + a mutated_theorem_statement +
                              expected_compiler_feedback {status, phase, error_token}
                              and (where one exists) a mutation_file.
  * the mutated .v files    -- self-contained Rocq sources the gate compiles to
                              prove catchability (a FALSE statement the kernel
                              MUST reject).

Two mutations, per spec D2:
  MUT_001_IDENTITY_FLIP            n + m = m + S n  -> type_check FAIL (off-by-one)
  MUT_002_VACUOUS_HYPOTHESIS_GUARD False -> (comm)  -> axiom_audit guard: catches a
                                   formalization that could only be discharged by
                                   smuggling an inconsistent background hypothesis.

This generator does NOT call the Rocq kernel; the FAIL/PASS verdict is the gate's
job and is capability-gated on Rocq.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MUT = HERE / "mutation"

EXERCISE_ID = "EX_ROCQ_074"
THEOREM_NAME = "exercise_42"

# Header stamped onto every emitted mutation .v so the artifacts are self-describing.
def _v_header(mid, clauses, why):
    return (f"(* {mid} -- EXERCISER BAND mutation (target {', '.join(clauses)}).\n"
            f" * {why}\n"
            " * Self-contained (prelude only). Where Rocq is installed, `coqc` MUST\n"
            " * FAIL to type-check this file (nonzero exit) -- that rejection is the\n"
            " * catchability guarantee. If it ever compiles, the formalization is\n"
            " * vacuous/inconsistent and the coherent-and-wrong trap is sprung.\n"
            " *)\n")


# MUT_001: the canonical identity flip. We attempt the SAME honest induction the
# prover would use; the final `reflexivity` cannot close `m = S m`, so the kernel
# rejects the file.
IDENTITY_FLIP_STMT = "Theorem exercise_42_mut : forall n m : nat, n + m = m + S n."
IDENTITY_FLIP_V = (
    _v_header("MUT_001_IDENTITY_FLIP", ["CLAUSE_2"],
              "Off-by-one successor injected into the RHS: n + m = m + S n (FALSE).")
    + IDENTITY_FLIP_STMT + "\n"
    "Proof.\n"
    "  intros n m.\n"
    "  induction n as [| n' IHn].\n"
    "  - simpl. rewrite <- plus_n_O. reflexivity.   (* goal: m = S m -- UNPROVABLE *)\n"
    "  - simpl. rewrite IHn. rewrite <- plus_n_Sm. reflexivity.\n"
    "Qed.\n"
)

# MUT_002: vacuous-hypothesis guard. A formalization is only worth proving if the
# background context is CONSISTENT. This mutation states the commutativity goal
# under a `False` hypothesis and tries to discharge it WITHOUT using that
# hypothesis (the dishonest "I proved it anyway" path: intros then reflexivity on
# `n + m = m + n`, which is NOT closed by reflexivity). `coqc` rejects it.
# Catchability here means: the matrix declares that a vacuous/escape-hatch
# discharge must NOT type-check; the gate enforces it at compile (and, for a real
# admitted cheat, the axiom audit B3 backs it up).
VACUOUS_STMT = "Theorem exercise_42_vacuous : False -> forall n m : nat, n + m = m + n."
VACUOUS_V = (
    _v_header("MUT_002_VACUOUS_HYPOTHESIS_GUARD", ["CLAUSE_1", "CLAUSE_3"],
              "Goal guarded by a False hypothesis; the dishonest discharge ignores "
              "the hypothesis and tries `reflexivity` on a non-reflexive goal.")
    + VACUOUS_STMT + "\n"
    "Proof.\n"
    "  intros _ n m.\n"
    "  reflexivity.   (* goal: n + m = m + n -- NOT closed by reflexivity *)\n"
    "Qed.\n"
)


def build_matrix() -> dict:
    return {
        "exercise_id": EXERCISE_ID,
        "theorem_name": THEOREM_NAME,
        "mutations": [
            {
                "mutation_id": "MUT_001_IDENTITY_FLIP",
                "target_clauses": ["CLAUSE_2"],
                "description": ("Mutates the right-hand equality target to inject a "
                                "successor mismatch (n + m = m + S n)."),
                "mutation_file": "exercise_mut_identity_flip.v",
                "mutated_theorem_statement": IDENTITY_FLIP_STMT,
                "expected_compiler_feedback": {
                    "status": "FAIL",
                    "phase": "type_check",
                    "error_token": "Unable to unify",
                },
            },
            {
                "mutation_id": "MUT_002_VACUOUS_HYPOTHESIS_GUARD",
                "target_clauses": ["CLAUSE_1", "CLAUSE_3"],
                "description": ("Guards against a vacuous/inconsistent formalization: "
                                "a False-hypothesis-guarded goal must not be "
                                "discharged dishonestly (ignoring the hypothesis)."),
                "mutation_file": "exercise_mut_vacuous_guard.v",
                "mutated_theorem_statement": VACUOUS_STMT,
                "expected_compiler_feedback": {
                    "status": "FAIL",
                    "phase": "axiom_audit",
                    "error_token": "Unable to unify",
                },
            },
        ],
    }


def main():
    MUT.mkdir(parents=True, exist_ok=True)
    (MUT / "exercise_mut_identity_flip.v").write_text(IDENTITY_FLIP_V)
    (MUT / "exercise_mut_vacuous_guard.v").write_text(VACUOUS_V)
    matrix = build_matrix()
    out = MUT / "mutation_matrix.json"
    out.write_text(json.dumps(matrix, indent=2) + "\n")
    print(f"wrote {out.name}: {len(matrix['mutations'])} mutations "
          f"({', '.join(m['mutation_id'] for m in matrix['mutations'])})")
    for m in matrix["mutations"]:
        print(f"  + {m['mutation_file']}  target={m['target_clauses']} "
              f"phase={m['expected_compiler_feedback']['phase']}")
    print("NOTE: catchability (coqc must REJECT each) is the gate's verdict, "
          "capability-gated on Rocq.")


if __name__ == "__main__":
    main()
