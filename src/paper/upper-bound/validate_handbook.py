#!/usr/bin/env python3
"""Upper bound (literature plane): the read peer-reviewed sources.

The normative ceiling for the manuscript's claims is the literature, under the
rule that each cited source is downloaded, read, and recorded BEFORE it may be
cited. This validates that rule structurally -- the reflexive analogue of
src/A/upper-bound/validate_handbook.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import _paperlib as L


def main():
    g = L.Gate()
    cited, bib, rec = L.cite_keys(), L.bib_keys(), L.record_keys()

    g.check(f"every \\cite has a references.bib entry ({len(cited)} cited)",
            not (cited - bib), f"missing: {sorted(cited - bib)}")
    g.check("every \\cite has a reading record (read before cited)",
            not (cited - rec), f"missing: {sorted(cited - rec)}")

    # uncited bib entries are tolerated but reported (baudin_acsl is the known one)
    orphans = sorted(bib - cited)
    if orphans:
        g.skip("uncited bib entries (intentional orphans)", ", ".join(orphans))

    print("VALIDATE OK" if g.ok else "VALIDATE FAILED")
    sys.exit(0 if g.ok else 1)


if __name__ == "__main__":
    main()
