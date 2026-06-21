#!/usr/bin/env python3
"""The Squeeze Connector for Use Case D (in-band-deliverable-spec D3).

The structural bridge the `sentinel` runs to force the prover's proof and the
exerciser's mutation matrix to reconcile over the frozen Rocq kernel. It imports
NEITHER band as a band: the prover deliverable is a `.v` file handed to the
kernel, and the exerciser deliverable is JSON + `.v` files handed to the kernel.
The two bands have zero import/path linkage to each other (Physical Context
Barrier); the runner verifies that first.

It does NOT reimplement the gate. The kernel boundary and the gate referee logic
are OWNED by the ground-truth (`rocq_kernel.py`, `gate_sentinel.py`); this runner
CALLS them:

  ISOLATION  prover/ and exerciser/ contain zero cross-references to each other.
  GATE A     (pure) every manifest CLAUSE_x is accounted for in the plan blueprint.
  GATE C     (pure) every manifest CLAUSE_x has a target_clauses entry in the matrix.
  GATE B     (Rocq, capability-gated) compile the prover solution (exit 0),
             axiom-audit it (no Admitted/Axiom leak), and confirm every FALSE
             mutation is REJECTED by the kernel.

HONESTY: every coqc/rocqchk step is capability-gated by rocq_kernel. With Rocq
absent the runner prints `DEPENDENCY UNMET` and exits 3 (Gate B SKIPPED) -- it
never fabricates a compile/audit/catch verdict. The pure gates (A, C) and the
isolation check still run and can fail honestly.

Exit codes mirror gate_sentinel.py:
  0  all gates passed (Gate B truly ran under a real kernel)
  1  a gate / isolation check FAILED (honest rejection)
  3  DEPENDENCY UNMET -- Rocq absent; Gate B SKIPPED
  2  usage / missing-input error
"""

import ast
import json
import os
import re
import sys
from pathlib import Path

RUNNER = Path(__file__).resolve().parent
ROOT = RUNNER.parent                         # src/D/in-band-deliverable
ROOT_D = ROOT.parent                         # src/D
GT = ROOT_D / "ground-truth"

# The kernel boundary + gate referee are OWNED by the ground-truth. Import them.
sys.path.insert(0, str(GT))
import rocq_kernel                            # noqa: E402  (the ONLY shell-out to coqc/rocqchk)
import gate_sentinel as gate                  # noqa: E402  (Gate A/B/C referee)
import registry as gt_registry                # noqa: E402  (certified-trunk enumeration)

import mutations                              # noqa: E402  (sentinel-side .v synthesis)

# --- band deliverables -------------------------------------------------------
PROVER_SOLUTION = ROOT / "implementer" / "solution" / "exercise.v"
EXERCISER_DIR = ROOT / "exerciser" / "mutation"
EXERCISER_MATRIX = EXERCISER_DIR / "mutation_matrix.json"

# --- ceiling / floor artifacts (read sentinel-side, not by either band) ------
FORMALIZER_SIG = GT / "fixtures" / "exercise_sig.v"
MANIFEST = GT / "fixtures" / "textbook_manifest.md"
SPEC_BLUEPRINT = GT / "fixtures" / "spec-1.md"
STDLIB = GT / "shared" / "rocq_stdlib"
REGISTRY = GT / "shared" / "proof_registry"

CANON_THEOREM = "exercise_42"
CANON_EXERCISE_ID = "EX_ROCQ_074"


class GateFail(Exception):
    pass


# ---------------------------------------------------------------------------
# ISOLATION -- zero import/path linkage between the two bands
# ---------------------------------------------------------------------------
def _links_to(pyfile: Path, other: str) -> str | None:
    text = pyfile.read_text()
    for node in ast.walk(ast.parse(text)):
        if isinstance(node, ast.Import):
            for n in node.names:
                if other in n.name.split("."):
                    return f"imports {n.name}"
        elif isinstance(node, ast.ImportFrom):
            if node.module and other in node.module.split("."):
                return f"from {node.module} import ..."
    if re.search(rf"\b{other}/", text) or f"/home/{other}" in text:
        return f"path reference to {other}/"
    return None


def check_isolation():
    bad = []
    for f in (ROOT / "implementer").rglob("*.py"):
        link = _links_to(f, "exerciser")
        if link:
            bad.append(f"{f.name} {link}")
    for f in (ROOT / "exerciser").rglob("*.py"):
        link = _links_to(f, "implementer")
        if link:
            bad.append(f"{f.name} {link}")
    if bad:
        raise GateFail("Physical Context Barrier violated (cross-band linkage): "
                       + "; ".join(bad))
    print("[PASS] ISOLATION -- prover and exerciser bands are import/path isolated")


# ---------------------------------------------------------------------------
# GATE B -- machine acceptance (capability-gated)
# ---------------------------------------------------------------------------
def gate_b(matrix: dict):
    gate.banner("GATE B -- Machine Acceptance (Rocq kernel)")
    if not rocq_kernel.have_coqc():
        gate.dep_unmet("coqc")                # prints DEPENDENCY UNMET, exits 3

    # B0: compile the formalizer signature so `Top.exercise_sig` is importable.
    #     The prover solution `Require Import`s it -- this is the formalizer/prover
    #     separation, so the sig dir must be on the loadpath (mapped to Top) for
    #     the solution compile (B2) and the axiom audit (B3).
    sig_R = [(str(FORMALIZER_SIG.parent), rocq_kernel.LOGICAL_ROOT)]
    print("[B0] compiling formalizer signature ...")
    sr = rocq_kernel.coqc_compile(str(FORMALIZER_SIG), str(FORMALIZER_SIG.parent))
    if not sr.available:
        gate.dep_unmet("coqc")
    if not sr.ok:
        raise GateFail(f"formalizer signature failed to compile\n{sr.stderr}")
    print(f"     [ok] {FORMALIZER_SIG.name} -> {rocq_kernel.LOGICAL_ROOT}.exercise_sig")

    # B1: certified registry regression (trunk must still compile)
    print("[B1] recompiling certified registry trunk ...")
    for vf in gt_registry.registry_files(REGISTRY):
        r = rocq_kernel.coqc_compile(str(vf), str(STDLIB))
        if not r.available:
            gate.dep_unmet("coqc")
        if not r.ok:
            raise GateFail(f"registry regression: {vf.name} no longer compiles\n{r.stderr}")
        print(f"     [ok] {vf.name}")

    # B2: compile the prover's solution (must exit 0)
    print("[B2] compiling prover solution ...")
    rc = rocq_kernel.coqc_compile(str(PROVER_SOLUTION), str(STDLIB), extra_R=sig_R)
    if not rc.available:
        gate.dep_unmet("coqc")
    if not rc.ok:
        raise GateFail(f"prover solution failed to type-check (exit {rc.returncode})\n{rc.stderr}")
    print("     [ok] solution type-checks (exit 0)")

    # B3: axiom audit (no Admitted / unauthorized Axiom) via Print Assumptions
    print("[B3] axiom audit (Print Assumptions) ...")
    audit = rocq_kernel.print_assumptions(str(PROVER_SOLUTION), CANON_THEOREM, str(STDLIB), extra_R=sig_R)
    if not audit.available:
        gate.dep_unmet("coqc")
    if not audit.ok:
        raise GateFail("axiom-audit probe failed to compile (cannot decide)\n"
                       f"{audit.stdout}\n{audit.stderr}")
    if rocq_kernel.audit_has_leak(audit.stdout + audit.stderr):
        raise GateFail("escape hatch detected (Admitted / unauthorized Axiom) in "
                       f"{CANON_THEOREM}\n{audit.stdout}")
    print("     [ok] no Admitted / Axiom leaks")

    # B4: negative-mutation catchability -- every FALSE mutation MUST be rejected
    print("[B4] negative-mutation catchability ...")
    muts = matrix.get("mutations", [])
    if not muts:
        raise GateFail("mutation matrix declares no mutations (nothing to falsify)")
    for mut in muts:
        if mut.get("expected_compiler_feedback", {}).get("status") != "FAIL":
            continue
        mid = mut.get("mutation_id", "?")
        mres = mutations.compile_mutation(rocq_kernel, mut, EXERCISER_DIR, str(STDLIB))
        if not mres.available:
            gate.dep_unmet("coqc")
        if mres.ok:
            raise GateFail(f"coherent-and-wrong: mutation {mid} type-checked. The "
                           "formal definitions admit a proof of a FALSE statement.")
        print(f"     [ok] {mid} correctly REJECTED by the kernel")

    print("[B] GATE B SUCCESS: kernel type-checked, axiom-clean, mutations caught.")


# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------
def main():
    # required band deliverables present?
    if not PROVER_SOLUTION.exists():
        print(f"error: prover deliverable missing: {PROVER_SOLUTION}")
        return 2
    if not EXERCISER_MATRIX.exists():
        print(f"error: exerciser matrix missing: {EXERCISER_MATRIX} "
              "(run exerciser/build_mutation_matrix.py)")
        return 2
    matrix = json.loads(EXERCISER_MATRIX.read_text())

    # contract conformance: exercise id + theorem name
    if matrix.get("exercise_id") != CANON_EXERCISE_ID:
        print(f"error: matrix exercise_id {matrix.get('exercise_id')!r} != "
              f"canonical {CANON_EXERCISE_ID!r}")
        return 2
    if matrix.get("theorem_name") not in (None, CANON_THEOREM):
        print(f"error: matrix theorem_name {matrix.get('theorem_name')!r} != "
              f"canonical {CANON_THEOREM!r}")
        return 2

    mclauses = gate.parse_manifest_clauses(MANIFEST, CANON_EXERCISE_ID)
    bclauses = gate.spec_clauses(SPEC_BLUEPRINT) if SPEC_BLUEPRINT.exists() else None

    try:
        check_isolation()
        # Pure gates (no Rocq) -- delegated to the ground-truth referee.
        gate.gate_a(mclauses, bclauses)
        gate.gate_c(mclauses, matrix)
        # Machine acceptance (capability-gated; may SystemExit(3) honestly).
        gate_b(matrix)
    except GateFail as e:
        print(f"\n[FAIL] {e}")
        print("SQUEEZE FAILED")
        return 1

    print("\nALL GATES PASSED")
    print("SQUEEZE OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
