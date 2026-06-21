#!/usr/bin/env python3
"""The reflexive squeeze runner: hold the manuscript between its literature upper
bound and its executable lower bound, and let the gates decide.

Mirrors src/A..D/in-band-deliverable/runner/execute_squeeze.py, but the deliverable
being squeezed is THIS paper (tex/paper.tex), and the sources/artifacts are the
real repo. Runs the four planes and passes iff every gate is green.
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import _paperlib as L

PAPERDIR = Path(__file__).resolve().parents[2]
STEPS = [
    ("ISOLATION (verifier re-derives from sources/artifacts, not the prose)",
     None),  # structural note, asserted below
    ("UPPER BOUND -- literature read-before-cite", PAPERDIR / "upper-bound" / "validate_handbook.py"),
    ("UPPER BOUND -- Gates A & C", PAPERDIR / "upper-bound" / "gate_checks.py"),
    ("CONNECTIVE TISSUE -- every section/subsection orients itself (recursive)", PAPERDIR.parents[1] / "verify" / "connective_tissue.py"),
    ("SELF-CONTAINED -- every key term introduced before use (no dangling forward refs)", PAPERDIR.parents[1] / "verify" / "self_contained.py"),
    ("CLAIM CONSISTENCY -- framing claims may not silently diverge (invariants ledger)", PAPERDIR.parents[1] / "verify" / "claim_consistency.py"),
    ("APPARATUS DESCRIBED -- the manuscript names every gate it is built from (no code-vs-prose drift)", PAPERDIR.parents[1] / "verify" / "apparatus_described.py"),
    ("LOWER BOUND -- determinism + build + cites resolve", PAPERDIR / "ground-truth" / "verify_ground_truth.py"),
    ("IN-BAND -- verifier re-derives every ledgered claim", PAPERDIR / "in-band-deliverable" / "exerciser" / "verify_claims.py"),
    ("O4 -- category-generation log: each enforced on a strictly later circle", PAPERDIR.parents[1] / "verify" / "category_log_measures.py"),
    ("O1+O5 -- live self-model: derived, read->act, redirects", PAPERDIR.parents[1] / "verify" / "self_model_check.py"),
    ("GATE S -- skill<->upper-bound consistency (carve-outs recorded)", PAPERDIR.parents[1] / "verify" / "skill_consistency.py"),
    ("REFLEXIVE GATE S -- the paper's own claims classified + routed to a disjoint base", PAPERDIR.parents[1] / "verify" / "reflexive_gate_s.py"),
    ("CATEGORY OVER-REACH -- do the paper's generated categories generalise across instances?", PAPERDIR.parents[1] / "verify" / "category_overreach.py"),
    ("PERTURBATION -- does each claim survive a perturbed anchor (full-text re-open / different seed)?", PAPERDIR.parents[1] / "verify" / "perturbation.py"),
    ("FLAG-RATE CALIBRATION -- does each monitor discriminate (not rubber-stamp, not saturated)?", PAPERDIR.parents[1] / "verify" / "flag_rate.py"),
    ("EDITORIAL GATE -- a standing, disjoint Gate A review is current (not author self-judging)", PAPERDIR.parents[1] / "verify" / "editorial_gate.py"),
    ("CLOSURE (O3) -- reflexive cycle executed, returns to origin", PAPERDIR.parents[1] / "verify" / "closure_check.py"),
]


def main():
    print("=== reflexive squeeze: the paper as its own use case ===")
    print("[note] the manuscript (tex/paper.tex) is the in-band deliverable;")
    print("       the verifier re-derives claims from records/artifacts, never the writer's prose.\n")
    ok = True
    for label, script in STEPS:
        if script is None:
            print(f"[PASS] {label}")
            continue
        print(f"--- {label}")
        r = subprocess.run(["python3", str(script)], capture_output=True, text=True)
        sys.stdout.write(r.stdout)
        if r.returncode != 0:
            sys.stdout.write(r.stderr)
            ok = False
    print()
    if ok:
        print("SQUEEZE OK: literature + evidence + build + claim re-derivation all green.")
        sys.exit(0)
    print("SQUEEZE FAILED: a plane did not reconcile.")
    sys.exit(1)


if __name__ == "__main__":
    main()
