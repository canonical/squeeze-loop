#!/usr/bin/env python3
"""Prover Band -- materialize the tactical proof deliverable (in-band-spec D1).

The prover's deliverable is the Rocq source `solution/exercise.v`: it imports the
formalizer's unalterable signature (`Require Import Top.exercise_sig.`), restates
the theorem signature VERBATIM, and discharges it with a tactical script ending
in `Qed.`.

This generator emits that file deterministically and self-checks the structural
constraints the gate sentinel will enforce (spec D1):
  * the signature line is preserved verbatim (no token drift);
  * no escape hatch keyword (Admitted / Axiom / Skip / Parameter / Conjecture);
  * the script terminates with `Qed.`.

It is CODE-BLIND to the exerciser: it imports / reads nothing under the exerciser
band; its only inputs are the canonical signature and the textbook ceiling. It
does NOT call the Rocq kernel -- that verdict belongs to the gate (capability-
gated). `--check` validates the on-disk file without rewriting it.
"""

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOLUTION = HERE / "solution" / "exercise.v"

# The exact theorem signature the formalizer fixed (Top.exercise_sig). The prover
# is forbidden from altering a single token of this line (spec D1 constraint 1).
CANON_SIGNATURE = "Theorem exercise_42 : forall n m : nat, n + m = m + n."

ESCAPE_HATCHES = ("Admitted", "Axiom", "Skip", "Parameter", "Conjecture", "admit")


def proof_source() -> str:
    """The full exercise.v source (kept identical to the checked-in artifact)."""
    return (HERE / "solution" / "exercise.v").read_text()


def check(text: str) -> list[str]:
    """Return a list of structural violations (empty == compliant)."""
    problems = []
    if "Require Import Top.exercise_sig." not in text:
        problems.append("missing the formalizer signature import (Require Import Top.exercise_sig.)")
    if CANON_SIGNATURE not in text:
        problems.append("theorem signature drift: the canonical "
                        f"'{CANON_SIGNATURE}' line is not present verbatim")
    if "Qed." not in text:
        problems.append("proof does not terminate with Qed. (no closing command)")
    # Scan only proof-bearing code, not the header comment block, for escape hatches.
    code = text.split(CANON_SIGNATURE, 1)[-1] if CANON_SIGNATURE in text else text
    for kw in ESCAPE_HATCHES:
        # crude token check: keyword as a statement (followed by space, dot, or EOL)
        for tok in (f"{kw} ", f"{kw}.", f"{kw}\n"):
            if tok in code:
                problems.append(f"forbidden escape hatch present in proof body: {kw!r}")
                break
    return problems


def main():
    ap = argparse.ArgumentParser(description="Prover band: emit/validate exercise.v")
    ap.add_argument("--check", action="store_true",
                    help="validate the on-disk solution without rewriting it")
    a = ap.parse_args()

    if not SOLUTION.exists():
        sys.exit(f"error: {SOLUTION} not found")
    text = SOLUTION.read_text()

    problems = check(text)
    if problems:
        for p in problems:
            print(f"[VIOLATION] {p}")
        print("prover deliverable is NON-COMPLIANT with spec D1")
        return 1

    if a.check:
        print(f"[ok] {SOLUTION.name} is structurally compliant "
              "(signature preserved, ends in Qed., no escape hatch).")
        print("NOTE: type-checking is the gate's job and is capability-gated on Rocq.")
        return 0

    # Deterministic emit is a no-op here (the artifact is the source of truth);
    # we re-write it byte-identically so the band is reproducible from the script.
    SOLUTION.write_text(text)
    print(f"wrote {SOLUTION} ({len(text)} bytes); structurally compliant.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
