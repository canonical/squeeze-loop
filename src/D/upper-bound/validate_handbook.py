#!/usr/bin/env python3
"""Self-check of the Upper Bound (Use Case D) -- the author's "the ceiling is
dischargeable from below" proof. Exits nonzero on any failure.

  1. STRUCTURE   textbook_manifest.md parses and passes the schema (spec §2):
                 markers, EXERCISE_ID, status, English text, scope boundaries,
                 sequential CLAUSE_1..N, the core negative vector, NOT-claims.
  2. CONTRACT    the manifest targets the canonical interface in
                 ../ground-truth/shared/contract.md EXACTLY: EXERCISE_ID
                 `EX_ROCQ_074`, the negative vector is the identity-flip
                 `n + m = m + S n`, the defense is a `coqc` type-check failure.
  3. GROUNDING   the clause set is dischargeable from below: the ground-truth's
                 example mutation matrix (fixtures/mutation_matrix.json) covers
                 every manifest clause, and its example blueprint (fixtures/spec-1.md)
                 maps every manifest clause -- i.e. a compliant downstream exists.
  4. GATE WIRING the Gate A / Gate C primitives accept a complete plan/matrix and
                 reject one that drops a clause.

This is the D analogue of the ground-truth's "every number recomputes": a
normative claim no compliant blueprint/matrix could satisfy is rejected here, not
discovered downstream. It is PURE Python -- no Rocq required (and none is run).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import gate_checks as gc
import manifest as mf

HERE = Path(__file__).resolve().parent
GT = HERE.parent / "ground-truth"
ACTIVE = "EX_ROCQ_074"

CONTRACT_EXERCISE_ID = "EX_ROCQ_074"
# canonical negative vector tokens from contract.md / spec §2.4
NEGATIVE_VECTOR_TOKENS = ("n + m", "m + S")


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))
    return ok


def main() -> int:
    ok = True

    # 1. structure
    try:
        exercises = mf.parse()
        check("structure", True,
              f"{len(exercises)} exercise(s): " + ", ".join(e.exercise_id for e in exercises))
    except mf.ManifestError as e:
        check("structure", False, str(e))
        print("VALIDATE FAILED")
        return 1

    try:
        active = mf.by_id(exercises, ACTIVE)
    except mf.ManifestError as e:
        check("active exercise present", False, str(e))
        print("VALIDATE FAILED")
        return 1

    # 2. contract alignment
    ok &= check("contract: EXERCISE_ID", active.exercise_id == CONTRACT_EXERCISE_ID,
                f"manifest `{active.exercise_id}` == contract `{CONTRACT_EXERCISE_ID}`")
    ok &= check("contract: status BINDING", active.status == "BINDING", active.status)
    neg = active.target_mutation
    ok &= check("contract: negative vector is identity-flip",
                all(tok in neg for tok in NEGATIVE_VECTOR_TOKENS),
                f"target mutation cites {NEGATIVE_VECTOR_TOKENS}: {neg!r}")
    ok &= check("contract: defense is coqc type-check failure",
                "coqc" in active.expected_defense.lower()
                and "fail" in active.expected_defense.lower(),
                active.expected_defense)
    ok &= check("contract: clause set is CLAUSE_1..3",
                active.clause_ids == ["CLAUSE_1", "CLAUSE_2", "CLAUSE_3"],
                str(active.clause_ids))

    # 3. grounding: a compliant downstream exists (ground-truth example fixtures)
    matrix_path = GT / "fixtures" / "mutation_matrix.json"
    if matrix_path.exists():
        matrix = json.loads(matrix_path.read_text())
        mid = matrix.get("exercise_id")
        ok &= check("grounding: fixture matrix exercise_id matches",
                    mid == active.exercise_id, f"{mid!r} == {active.exercise_id!r}")
        cres = gc.gate_c_coverage(active, matrix)
        ok &= check("grounding: example mutation matrix covers every clause",
                    bool(cres), cres.detail)
    else:
        print(f"[WARN] {matrix_path} not found; skipping matrix grounding")

    blueprint_path = GT / "fixtures" / "spec-1.md"
    if blueprint_path.exists():
        ares = gc.gate_a_plan(active, blueprint_path.read_text())
        ok &= check("grounding: example blueprint maps every clause",
                    bool(ares), ares.detail)
    else:
        print(f"[WARN] {blueprint_path} not found; skipping blueprint grounding")

    # 4. gate wiring (positive + negative per exercise)
    for e in exercises:
        plan_ok = gc.gate_a_plan(e, " ".join(e.clause_ids))
        plan_bad = gc.gate_a_plan(e, " ".join(e.clause_ids[:-1]))   # drop last clause
        matrix_ok = {"mutations": [{"target_clauses": [c]} for c in e.clause_ids]}
        matrix_bad = {"mutations": [{"target_clauses": e.clause_ids[:-1]}]}
        c_ok = gc.gate_c_coverage(e, matrix_ok)
        c_bad = gc.gate_c_coverage(e, matrix_bad)
        wired = bool(plan_ok) and not plan_bad.ok and bool(c_ok) and not c_bad.ok
        ok &= check(f"{e.exercise_id} gate wiring", wired,
                    "Gate A & C accept complete, reject incomplete")

    print("VALIDATE OK" if ok else "VALIDATE FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
