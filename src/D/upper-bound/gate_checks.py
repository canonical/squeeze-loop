"""Upper-bound-driven gate primitives for Use Case D (spec §3): how the textbook
manifest drives the structural gates. These are PURE Python (no Rocq) and are the
checks `gate_sentinel.py` runs before/around the kernel work. They read the
ceiling and refuse plans/matrices that do not account for every obligation clause.

Gate A -- Structural Specification Validation: the coordinator's `spec-N.md`
          blueprint must explicitly map every CLAUSE_X of the active exercise, so
          no obligation is silently dropped before any code is compiled.
Gate C -- Structural Coverage Map ("coherent-and-wrong" guard): the exerciser's
          `mutation_matrix.json` must contain a mutation whose `target_clauses`
          names every CLAUSE_X. A clause with no mutation target fails the build
          even if `coqc` accepted an internally consistent but adjacent/vacuous
          theorem.

Semantics are identical to the ground-truth sentinel (set subset):
  Gate A passes  iff  manifest_clauses ⊆ blueprint_clauses
  Gate C passes  iff  manifest_clauses ⊆ matrix target_clauses
(see ../ground-truth/gate_sentinel.py and ../ground-truth/shared/contract.md).

mutation_matrix.json schema (written by the code-blind exerciser; contract.md):
    {
      "exercise_id": "EX_ROCQ_074",
      "theorem_name": "exercise_42",
      "mutations": [
        {"mutation_id": "...", "target_clauses": ["CLAUSE_2"], ...}
      ]
    }
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import manifest as mf

# A blueprint "maps" a clause by naming its id verbatim (CLAUSE_2), exactly as the
# sentinel's spec_clauses() scans for. A bare copy of the English text does not.
_CLAUSE_TOKEN = re.compile(r"\bCLAUSE_(\d+)\b")


@dataclass(frozen=True)
class GateResult:
    ok: bool
    gate: str
    exercise_id: str
    missing: list[str]      # clause ids not mapped / not covered
    detail: str = ""

    def __bool__(self) -> bool:
        return self.ok

    def __str__(self) -> str:
        verdict = "PASS" if self.ok else "FAIL"
        return f"Gate {self.gate} [{verdict}] {self.exercise_id}: {self.detail}"


def blueprint_clauses(plan_text: str) -> set[str]:
    """The CLAUSE_X ids a coordinator blueprint (`spec-N.md`) explicitly maps."""
    return {f"CLAUSE_{n}" for n in _CLAUSE_TOKEN.findall(plan_text)}


def matrix_clauses(matrix: dict) -> set[str]:
    """Union of every mutation's `target_clauses` in a mutation_matrix.json dict."""
    out: set[str] = set()
    for mut in matrix.get("mutations", []):
        if isinstance(mut, dict):
            out.update(mut.get("target_clauses", []) or [])
    return out


def gate_a_plan(exercise: mf.Exercise, plan_text: str) -> GateResult:
    """Gate A: every CLAUSE_X of `exercise` must be explicitly mapped in the
    coordinator's blueprint text."""
    mapped = blueprint_clauses(plan_text)
    missing = [cid for cid in exercise.clause_ids if cid not in mapped]
    ok = not missing
    return GateResult(
        ok, "A", exercise.exercise_id, missing,
        f"all clauses mapped in blueprint: {exercise.clause_ids}"
        if ok else f"blueprint does not account for {missing}")


def gate_c_coverage(exercise: mf.Exercise, matrix: dict) -> GateResult:
    """Gate C: every CLAUSE_X of `exercise` must be a `target_clauses` entry in the
    exerciser's mutation matrix."""
    covered = matrix_clauses(matrix)
    missing = [cid for cid in exercise.clause_ids if cid not in covered]
    ok = not missing
    return GateResult(
        ok, "C", exercise.exercise_id, missing,
        f"every clause has a mutation target: {exercise.clause_ids}"
        if ok else f"mutation matrix lacks a target for {missing} (coverage deficiency)")


if __name__ == "__main__":
    # Pilot: exercise both gates on the active exercise with a good and a bad input.
    exercises = mf.parse()
    e = mf.by_id(exercises, "EX_ROCQ_074")

    good_plan = ("Plan: map CLAUSE_1 (forall n m : nat), CLAUSE_2 "
                 "(goal n + m = m + n), CLAUSE_3 (induction over O and S).")
    bad_plan = "Plan: map CLAUSE_1 and CLAUSE_2."  # drops CLAUSE_3
    print(gate_a_plan(e, good_plan))
    print(gate_a_plan(e, bad_plan))

    good_matrix = {"mutations": [
        {"mutation_id": "MUT_001", "target_clauses": ["CLAUSE_2"]},
        {"mutation_id": "MUT_002", "target_clauses": ["CLAUSE_1", "CLAUSE_3"]},
    ]}
    bad_matrix = {"mutations": [
        {"mutation_id": "MUT_001", "target_clauses": ["CLAUSE_2"]},  # CLAUSE_1,3 uncovered
    ]}
    print(gate_c_coverage(e, good_matrix))
    print(gate_c_coverage(e, bad_matrix))
