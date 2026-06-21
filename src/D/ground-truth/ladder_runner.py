#!/usr/bin/env python3
"""Run the difficulty LADDER for Use Case D (level-up-D.md).

The richness of the experiment comes from the richness of the upper bound. For D
that richness is mathematical depth: this ladder holds rungs from trivial
(`n + 0 = n`) to very hard (`n <= 2^n`). For each rung the squeeze's lower bound
(the Rocq kernel) is applied for real:

  * compile the reference proof              -> must type-check (exit 0)
  * axiom audit (Print Assumptions)          -> must be "Closed under the global
                                                context" (no Admitted / axiom)
  * compile the FALSE mutation               -> must be REJECTED (catchability)

Verdict per rung:
  PASS  proof type-checks, axiom-clean, mutation caught       (provable rung)
  OPEN  proof type-checks but the audit catches an Admitted   (rung beyond the
        reference witness -- the gate stays honest, never fakes a verdict)
  FAIL  anything else (a real defect)

Capability-gated: if the kernel is absent every rung is SKIPPED, never faked.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rocq_kernel as K

LADDER = HERE / "ladder"
STDLIB = HERE / "shared" / "rocq_stdlib"


def run_rung(r):
    good = LADDER / r["good"]
    mut = LADDER / r["mut"]
    thm = r["theorem"]

    comp = K.coqc_compile(str(good), str(STDLIB))
    if not comp.available:
        return {"verdict": "SKIP", "reason": "DEPENDENCY UNMET: Rocq absent"}
    compiles = comp.ok

    audit = K.print_assumptions(str(good), thm, str(STDLIB))
    clean = audit.ok and not K.audit_has_leak(audit.stdout + audit.stderr)

    mres = K.coqc_compile(str(mut), str(STDLIB))
    mutation_caught = mres.available and not mres.ok  # false stmt must be rejected

    if r["proof_status"] == "open":
        # expected: compiles but the audit catches the Admitted, and the mutation
        # is still caught. That is the honest boundary, not a failure.
        verdict = "OPEN" if (compiles and not clean and mutation_caught) else "FAIL"
    else:
        verdict = "PASS" if (compiles and clean and mutation_caught) else "FAIL"

    return {"verdict": verdict, "compiles": compiles, "axiom_clean": clean,
            "mutation_caught": mutation_caught}


def main():
    ladder = json.loads((LADDER / "ladder.json").read_text())
    if not K.have_coqc():
        print("DEPENDENCY UNMET: Rocq (coqc/rocq) not installed -- ladder SKIPPED "
              "(no fabricated verdicts).")
        sys.exit(3)

    print("=== Use Case D difficulty ladder (level-up-D) ===")
    rows, ok = [], True
    for r in ladder["rungs"]:
        res = run_rung(r)
        rows.append({**r, **res})
        mark = {"PASS": "[PASS]", "OPEN": "[OPEN]", "FAIL": "[FAIL]", "SKIP": "[SKIP]"}[res["verdict"]]
        print(f"{mark} {r['tier']:<10} {r['theorem']:<9} ({r['statement']})"
              + (f"  compiles={res.get('compiles')} clean={res.get('axiom_clean')} "
                 f"mut_caught={res.get('mutation_caught')}" if "compiles" in res else ""))
        if res["verdict"] == "FAIL":
            ok = False

    n_pass = sum(1 for r in rows if r["verdict"] == "PASS")
    n_open = sum(1 for r in rows if r["verdict"] == "OPEN")
    print(f"\nladder: {n_pass} proved+clean+caught, {n_open} open(beyond witness), "
          f"of {len(rows)} rungs")

    # emit the evidence artifact (sibling to evidence/results.json)
    out = {
        "instance": "D-ladder",
        "rungs": len(rows),
        "proved_clean_caught": n_pass,
        "open_beyond_witness": n_open,
        "all_mutations_caught": all(r.get("mutation_caught") for r in rows),
        "per_rung": [{"tier": r["tier"], "theorem": r["theorem"],
                      "verdict": r["verdict"], "axiom_clean": r.get("axiom_clean"),
                      "mutation_caught": r.get("mutation_caught")} for r in rows],
    }
    ev = HERE.parents[0] / "evidence" / "ladder_results.json"
    ev.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(f"results -> {ev}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
