#!/usr/bin/env python3
"""In-band exerciser (the verifier): re-derive each ledgered claim from the source
or the artifact -- NOT from the writer's prose.

This is the paper-verifier-agent's job, structurally: for every CITE row the cited
key must have a reading record (the claim traces to a read source); for every
RESULT row the bound artifact path must exist on disk (the claim traces to a
re-runnable artifact). A claim that cannot be traced to ground truth is a defect.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import _paperlib as L


def main():
    g = L.Gate()
    rec = L.record_keys()

    # CITE rows -> a reading record exists for the bound source
    cite_bad = [clm for clm, key, _ in L.ledger_rows("CITE") if key not in rec]
    g.check(f"every CITE claim traces to a reading record ({len(L.ledger_rows('CITE'))} rows)",
            not cite_bad, f"untraceable: {cite_bad}")

    # RESULT rows -> the bound artifact exists. The binding's first token is a
    # path, optionally with a '#field' anchor into it (e.g.
    # src/A/evidence/results.json#defects_caught) -- strip the anchor.
    res_bad = []
    for clm, binding, _ in L.ledger_rows("RESULT"):
        path = binding.split("#", 1)[0]
        if not (L.REPO / path).exists():
            res_bad.append((clm, path))
    g.check(f"every RESULT claim traces to an artifact on disk ({len(L.ledger_rows('RESULT'))} rows)",
            not res_bad, f"missing: {res_bad}")

    print("CLAIMS OK" if g.ok else "CLAIMS FAILED")
    sys.exit(0 if g.ok else 1)


if __name__ == "__main__":
    main()
