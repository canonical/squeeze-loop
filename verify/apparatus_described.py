#!/usr/bin/env python3
"""Apparatus-vs-description check (paper-impl principle: the manuscript must describe its own gates).

Circle 122's editorial pass found a new escaped class: the manuscript had gone
coherent-and-wrong about its OWN apparatus -- it described a 4-member reflexive-monitor family
while three more gates had been wired in (circles 119-121). This is CODE-vs-PROSE drift, which
neither claim_consistency.py (prose-vs-prose) nor editorial_gate.py (prose-vs-evidence) covers.

This gate closes it, against claims/apparatus_manifest.tsv:
  1. Every script wired into the squeeze (execute_squeeze.py STEPS) is classified in the
     manifest -- a NEW gate forces a described/internal decision; drift cannot enter silently.
  2. Every `described` script is \\code-referenced in tex/paper.tex and exists on disk -- a
     described gate missing from the manuscript is drift (hard fail).
  3. Every verify/*.py the manuscript \\code-references exists on disk and is in the manifest --
     a dangling or unclassified reference fails.

Deterministic; loud-fails. Reads execute_squeeze.py, tex/paper.tex, and the manifest. It is a
PROXY: it checks the gate is NAMED in the paper, not that the description is accurate -- the
latter is the standing disjoint Gate A (editorial_gate.py).
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PAPER = REPO / "tex" / "paper.tex"
MANIFEST = REPO / "claims" / "apparatus_manifest.tsv"
STEPS_SRC = REPO / "src" / "paper" / "in-band-deliverable" / "runner" / "execute_squeeze.py"
VERIFY = REPO / "verify"


def steps_scripts():
    """Filenames of .py scripts wired into the execute_squeeze STEPS list."""
    txt = STEPS_SRC.read_text()
    # the STEPS entries reference scripts as string literals "<name>.py"
    return set(re.findall(r'"([a-z0-9_]+\.py)"', txt))


def paper_refs():
    """verify/*.py scripts \\code-referenced in the manuscript.

    Normalises the captured path: \\_ -> _, and strips typographic break hints
    (\\allowbreak, \\-, \\,) and whitespace, so a line-break hint inside the path
    (e.g. \\code{verify/\\allowbreak eval\\_protocol.py}) still extracts the logical
    script name. The gate checks the script is NAMED, not how it is typeset.
    """
    refs = set()
    for m in re.findall(r"\\code\{verify/([^}]+?)\.py\}", PAPER.read_text()):
        name = m.replace("\\_", "_")
        for hint in ("\\allowbreak", "\\-", "\\,", " "):
            name = name.replace(hint, "")
        refs.add(name + ".py")
    return refs


def manifest():
    described, internal = {}, {}
    for ln in MANIFEST.read_text().splitlines():
        if not ln.strip() or ln.startswith("#"):
            continue
        f = ln.split("\t")
        if len(f) < 2:
            continue
        (described if f[1] == "described" else internal)[f[0]] = f[2] if len(f) > 2 else ""
    return described, internal


def main():
    steps = steps_scripts()
    refs = paper_refs()
    described, internal = manifest()
    known = set(described) | set(internal)
    fails = []

    # 1. every STEPS script classified
    for s in sorted(steps - known):
        fails.append(f"STEPS script not classified in apparatus_manifest.tsv: {s} "
                     "(new gate? mark it described or internal)")

    # 2. every described script is in the paper and on disk
    for s in sorted(described):
        if not (VERIFY / s).exists():
            fails.append(f"manifest 'described' script missing on disk: verify/{s}")
        if s not in refs:
            fails.append(f"DRIFT: verify/{s} is 'described' but the manuscript does not "
                         f"\\code-reference it ({described[s]})")

    # 3. every paper reference exists and is classified
    for s in sorted(refs):
        if not (VERIFY / s).exists():
            fails.append(f"manuscript references a missing script: verify/{s}")
        if s not in known:
            fails.append(f"manuscript references verify/{s} but it is not in apparatus_manifest.tsv")

    ok = not fails
    print("=== Apparatus-vs-description check (does the paper describe its own gates?) ===")
    print(f"  STEPS scripts: {len(steps)}; manifest: {len(described)} described, "
          f"{len(internal)} internal; manuscript references: {len(refs)}")
    for f in fails:
        print("  [FAIL]", f)
    print(f"\nApparatus described: {'PASS' if ok else 'FAIL'} "
          f"({len(fails)} drift(s); proxy for NAMED, not for accurate -- accuracy is Gate A)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
