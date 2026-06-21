#!/usr/bin/env python3
"""Self-check of the Use Case D ground truth -- the executable lower bound.

Runs the parts that DO NOT need Rocq for real, and capability-gates the parts
that do. Exits nonzero on any honest failure of the non-kernel logic.

Checks:
  1. PIN          storage-plane pin contract (rocq_stdlib/PIN.md) present
  2. REGISTRY SIG recompute the trunk and compare to registry.sig (Invariant Plane)
  3. GATE LOGIC   pure-Python gate orchestration (A/C clause mapping, mutation
                  matrix parse, leak-token detection) behaves correctly on the
                  in-repo fixtures -- a tiny sanity of the non-kernel logic
  4. KERNEL       report whether coqc/rocqchk are available. If present, this is
                  where the gate genuinely type-checks; if absent we SKIP (and
                  say so) rather than fake a verdict.

Exit: 0 == non-kernel ground truth sound (kernel checks may be SKIPPED).
      1 == an honest failure in the non-kernel logic.
"""

import json
import sys
from pathlib import Path

import rocq_kernel
import registry
import gate_sentinel as gs

HERE = Path(__file__).resolve().parent
SHARED = HERE / "shared"
STDLIB = SHARED / "rocq_stdlib"
REGISTRY = SHARED / "proof_registry"
FX = HERE / "fixtures"


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))
    return ok


def main():
    ok = True

    # 1. pin contract
    ok &= check("storage-plane pin", (STDLIB / "PIN.md").exists(),
                "rocq_stdlib/PIN.md")

    # 2. registry signature recompute
    sig_ok, detail = registry.verify_signature(REGISTRY)
    ok &= check("registry signature", sig_ok, detail)

    # 3. pure-python gate logic sanity (no Rocq)
    manifest = FX / "textbook_manifest.md"
    mclauses = gs.parse_manifest_clauses(manifest, "EX_ROCQ_074")
    ok &= check("manifest clause parse", mclauses == {"CLAUSE_1", "CLAUSE_2", "CLAUSE_3"},
                f"{sorted(mclauses)}")

    matrix = json.loads((FX / "mutation_matrix.json").read_text())
    covered = gs.matrix_clauses(matrix)
    ok &= check("Gate C coverage map", mclauses <= covered,
                f"covered={sorted(covered)}")

    bclauses = gs.spec_clauses(FX / "spec-1.md")
    ok &= check("Gate A plan mapping", mclauses <= bclauses,
                f"blueprint={sorted(bclauses)}")

    # leak-token detector: a clean banner must pass, an Admitted line must trip
    clean = "Closed under the global context"
    dirty = "Axioms:\n  some_admitted_lemma : ..."
    ok &= check("axiom-leak detector", (not rocq_kernel.audit_has_leak(clean))
                and rocq_kernel.audit_has_leak(dirty))

    # 4. kernel availability (honest skip)
    have = rocq_kernel.have_coqc() and rocq_kernel.have_rocqchk()
    if have:
        check("rocq kernel present", True, "coqc + rocqchk available -- run "
              "gate_sentinel.py --fixtures for the real type-check")
    else:
        print("[SKIP] rocq kernel -- coqc/rocqchk ABSENT on this host. "
              "DEPENDENCY UNMET for Gate B; no proof verdict is fabricated. "
              "Run gate_sentinel.py --fixtures where Rocq is installed.")

    print("VERIFY OK" if ok else "VERIFY FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
