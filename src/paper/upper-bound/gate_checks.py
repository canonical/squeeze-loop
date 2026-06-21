#!/usr/bin/env python3
"""Upper bound (gates A & C) for the manuscript.

Gate A (editorial plan): forward motion goes through approved per-circle plans;
the spec (paper-impl.md) and its per-circle spec docs exist.
Gate C (coverage map): the claim ledger covers the manuscript -- the CITE/RESULT
row counts equal the reflexive macros, so the ledger and the paper's own reflexive
section agree (no claim is unledgered, no ledgered count is stale).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import _paperlib as L


def main():
    g = L.Gate()

    # Gate A: the binding spec + the editorial plan trail exist
    specs = list((L.REPO / "docs").glob("*-paper-spec-*.md"))
    g.check("Gate A: paper-impl spec present", (L.REPO / "paper-impl.md").exists())
    g.check("Gate A: per-circle plans exist (editorial trail)", len(specs) > 0,
            f"{len(specs)} spec docs")

    # Gate C: ledger <-> reflexive macros reconcile
    n_cite = len(L.ledger_rows("CITE"))
    n_res = len(L.ledger_rows("RESULT"))
    g.check("Gate C: CITE rows == ResReflexCiteRows",
            str(n_cite) == L.reflex_macro("ResReflexCiteRows"),
            f"ledger={n_cite} macro={L.reflex_macro('ResReflexCiteRows')}")
    g.check("Gate C: RESULT rows == ResReflexResultRows",
            str(n_res) == L.reflex_macro("ResReflexResultRows"),
            f"ledger={n_res} macro={L.reflex_macro('ResReflexResultRows')}")

    print("GATES OK" if g.ok else "GATES FAILED")
    sys.exit(0 if g.ok else 1)


if __name__ == "__main__":
    main()
