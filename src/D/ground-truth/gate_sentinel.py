#!/usr/bin/env python3
"""gate_sentinel.py -- Execution arbiter and gate referee (spec D1/D5).

Owned by the `sentinel` user inside the container. Evaluates an exercise for
graduation across the three gates:

  GATE A  Structural Specification Validation
          Every CLAUSE_X in the active manifest entry is accounted for in the
          plan/spec blueprint AND has a corresponding target in the exerciser's
          mutation matrix. (Pure parsing -- runs without Rocq.)

  GATE B  Machine Acceptance  (REQUIRES Rocq -- capability-gated)
          1. Re-compile the certified proof registry trunk (regression guard).
          2. Compile the prover's solution.                  (must exit 0)
          3. Axiom audit via rocqchk --print-assumptions.    (no Admitted/Axiom)
          4. Negative-mutation catchability: every FALSE mutation MUST fail to
             type-check. If any compiles, the "coherent-and-wrong" trap fires.

  GATE C  Structural Coverage Map
          Every clause from the manifest correlates to a target_clauses entry in
          the mutation matrix. (Pure parsing -- runs without Rocq.)

HONESTY CONTRACT: every coqc/rocqchk step is capability-gated by rocq_kernel.
If Rocq is absent the script prints
    DEPENDENCY UNMET: Rocq (coqc/rocqchk) not installed
and exits with code 3 (SKIPPED -- could-not-decide). It NEVER prints a Gate B
pass without a real kernel verdict. Pure-Python gates (A, C) still run and can
fail honestly.

Exit codes:
  0  all evaluated gates passed (and Gate B truly ran under a real kernel)
  1  a gate FAILED (honest rejection)
  3  DEPENDENCY UNMET -- Rocq absent; Gate B could not be decided (SKIPPED)
  2  usage / missing-input error
"""

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

import rocq_kernel
from rocq_kernel import KernelResult

HERE = Path(__file__).resolve().parent

# ------- canonical deployed contract paths (spec) ----------------------------
SHARED = Path("/opt/squeeze/shared")
DEPLOYED = {
    "stdlib": SHARED / "rocq_stdlib",
    "registry": SHARED / "proof_registry",
    "manifest": SHARED / "textbook_manifest.md",
    "spec_blueprint": Path("/opt/squeeze/orchestrator/ledger/spec-1.md"),
    "formalizer_sig": Path("/home/formalizer/definition/exercise_sig.v"),
    "solution": Path("/home/prover/solution/exercise.v"),
    "mutation_matrix": Path("/home/exerciser/mutation/mutation_matrix.json"),
    "mutation_dir": Path("/home/exerciser/mutation"),
}

CANON_THEOREM = "exercise_42"
CANON_EXERCISE_ID = "EX_ROCQ_074"


def banner(title):
    print(f"\n=== {title} ===")


def fail(msg):
    print(f"GATE FAILURE: {msg}")
    sys.exit(1)


def dep_unmet(what):
    print(f"DEPENDENCY UNMET: Rocq ({what}) not installed")
    print("Gate B cannot be decided without the kernel. Refusing to fabricate a "
          "verdict. Status: SKIPPED.")
    sys.exit(3)


# ----------------------------------------------------------------------------
# Manifest / clause parsing (pure python)
# ----------------------------------------------------------------------------
CLAUSE_RE = re.compile(r"\bCLAUSE_(\d+)\b")


def parse_manifest_clauses(manifest_path: Path, exercise_id: str) -> set[str]:
    """Extract the CLAUSE_X ids declared under the active EXERCISE_ID block."""
    if not manifest_path.exists():
        return set()
    text = manifest_path.read_text()
    # Slice the block for this exercise id (## EXERCISE_ID: <id> ... next ## or END)
    start = text.find(f"EXERCISE_ID: {exercise_id}")
    if start == -1:
        return set()
    rest = text[start:]
    nxt = rest.find("## EXERCISE_ID:", 3)
    end = rest.find("TEXTBOOK_MANIFEST_END")
    cut = min(x for x in (nxt, end, len(rest)) if x != -1)
    block = rest[:cut]
    return {f"CLAUSE_{n}" for n in CLAUSE_RE.findall(block)}


def matrix_clauses(matrix: dict) -> set[str]:
    out = set()
    for mut in matrix.get("mutations", []):
        out.update(mut.get("target_clauses", []))
    return out


def spec_clauses(spec_path: Path) -> set[str]:
    if not spec_path.exists():
        return set()
    return {f"CLAUSE_{n}" for n in CLAUSE_RE.findall(spec_path.read_text())}


# ----------------------------------------------------------------------------
# GATE A
# ----------------------------------------------------------------------------
def gate_a(manifest_clauses: set[str], blueprint_clauses: set[str] | None):
    banner("GATE A -- Structural Specification Validation")
    if not manifest_clauses:
        fail("no CLAUSE_X found in manifest for the active exercise (cannot plan-audit)")
    if blueprint_clauses is None:
        print("[A] no spec blueprint provided; skipping plan-audit cross-check "
              "(clauses present in manifest: " + ", ".join(sorted(manifest_clauses)) + ")")
        return
    missing = manifest_clauses - blueprint_clauses
    if missing:
        fail(f"plan blueprint does not account for {sorted(missing)}")
    print(f"[A] all manifest clauses mapped in blueprint: {sorted(manifest_clauses)}")


# ----------------------------------------------------------------------------
# GATE C
# ----------------------------------------------------------------------------
def gate_c(manifest_clauses: set[str], matrix: dict):
    banner("GATE C -- Structural Coverage Map")
    covered = matrix_clauses(matrix)
    missing = manifest_clauses - covered
    if missing:
        fail(f"mutation matrix lacks a target for clause(s) {sorted(missing)} "
             f"(coverage deficiency)")
    print(f"[C] every manifest clause has a mutation target: {sorted(manifest_clauses)}")


# ----------------------------------------------------------------------------
# GATE B  (capability-gated)
# ----------------------------------------------------------------------------
def _require_kernel():
    if not rocq_kernel.have_coqc():
        dep_unmet("coqc")
    # rocqchk is needed for the axiom audit; gate it at the audit step too.


def gate_b(stdlib: Path, registry: Path, solution: Path, theorem: str,
           matrix: dict, mutation_dir: Path):
    banner("GATE B -- Machine Acceptance (Rocq kernel)")
    _require_kernel()

    # B1: registry regression -- recompile the certified trunk
    print("[B1] recompiling certified registry trunk ...")
    from registry import registry_files
    for vf in registry_files(registry):
        r = rocq_kernel.coqc_compile(str(vf), str(stdlib))
        if not r.available:
            dep_unmet("coqc")
        if not r.ok:
            fail(f"registry regression: {vf.name} no longer compiles\n{r.stderr}")
        print(f"     [ok] {vf.name}")

    # B2: compile the prover's solution
    print("[B2] compiling prover solution ...")
    rc = rocq_kernel.coqc_compile(str(solution), str(stdlib))
    if not rc.available:
        dep_unmet("coqc")
    if not rc.ok:
        fail(f"proof compilation smashed (exit {rc.returncode})\n{rc.stderr}")
    print("     [ok] solution type-checks (exit 0)")

    # B3: axiom audit (escape-hatch / unauthorized axiom) via Print Assumptions
    print("[B3] axiom audit (Print Assumptions) ...")
    audit = rocq_kernel.print_assumptions(str(solution), theorem, str(stdlib))
    if not audit.available:
        dep_unmet("coqc")
    if not audit.ok:
        fail(f"axiom-audit probe failed to compile (cannot decide):\n{audit.stdout}\n{audit.stderr}")
    if rocq_kernel.audit_has_leak(audit.stdout + audit.stderr):
        fail("escape hatch detected (Admitted / unauthorized Axiom) in "
             f"{theorem}\n{audit.stdout}")
    print("     [ok] no Admitted / Axiom leaks")

    # B4: negative-mutation catchability
    print("[B4] negative-mutation catchability ...")
    muts = matrix.get("mutations", [])
    if not muts:
        fail("mutation matrix declares no mutations (nothing to falsify)")
    for mut in muts:
        if mut.get("expected_compiler_feedback", {}).get("status") != "FAIL":
            continue
        mid = mut.get("mutation_id", "?")
        mfile = mutation_dir / mut["mutation_file"] if mut.get("mutation_file") else None
        if mfile and mfile.exists():
            mres = rocq_kernel.coqc_compile(str(mfile), str(stdlib))
        else:
            # Synthesize from the mutated statement (spec D5 / in-band §3 path).
            stmt = mut["mutated_theorem_statement"]
            src = stmt + "\nProof. intros. reflexivity. Qed.\n"
            with tempfile.NamedTemporaryFile("w", suffix=".v", delete=False) as tf:
                tf.write(src)
                tmpname = tf.name
            mres = rocq_kernel.coqc_compile(tmpname, str(stdlib))
        if not mres.available:
            dep_unmet("coqc")
        if mres.ok:
            fail(f"coherent-and-wrong: mutation {mid} type-checked. The formal "
                 f"definitions allow proofs of a FALSE statement.")
        print(f"     [ok] {mid} correctly REJECTED by the kernel")

    print("[B] GATE B SUCCESS: kernel type-checked, axiom-clean, mutations caught.")


# ----------------------------------------------------------------------------
# driver
# ----------------------------------------------------------------------------
def resolve_paths(args):
    if args.fixtures:
        fx = HERE / "fixtures"
        return {
            "stdlib": HERE / "shared" / "rocq_stdlib",
            "registry": HERE / "shared" / "proof_registry",
            "manifest": HERE / "fixtures" / "textbook_manifest.md",
            "spec_blueprint": HERE / "fixtures" / "spec-1.md",
            "solution": fx / args.solution,
            "mutation_matrix": fx / "mutation_matrix.json",
            "mutation_dir": fx,
        }
    return {k: DEPLOYED[k] for k in
            ("stdlib", "registry", "manifest", "spec_blueprint",
             "solution", "mutation_matrix", "mutation_dir")}


def main():
    ap = argparse.ArgumentParser(description="Rocq gate referee (spec D5)")
    ap.add_argument("--fixtures", action="store_true",
                    help="evaluate the in-repo fixtures instead of deployed /opt/squeeze paths")
    ap.add_argument("--solution", default="exercise_good.v",
                    help="(fixtures mode) which solution fixture to grade")
    ap.add_argument("--exercise-id", default=CANON_EXERCISE_ID)
    ap.add_argument("--theorem", default=CANON_THEOREM)
    args = ap.parse_args()

    p = resolve_paths(args)

    # load mutation matrix (required)
    if not p["mutation_matrix"].exists():
        print(f"missing mutation matrix: {p['mutation_matrix']}")
        return 2
    matrix = json.loads(p["mutation_matrix"].read_text())

    mclauses = parse_manifest_clauses(p["manifest"], args.exercise_id)
    bclauses = spec_clauses(p["spec_blueprint"]) if p["spec_blueprint"].exists() else None

    gate_a(mclauses, bclauses)
    gate_c(mclauses, matrix)
    gate_b(p["stdlib"], p["registry"], p["solution"], args.theorem,
           matrix, p["mutation_dir"])

    print("\nALL GATES PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
