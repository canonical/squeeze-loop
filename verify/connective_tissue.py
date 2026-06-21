#!/usr/bin/env python3
"""Connective-tissue check (paper-impl principle: every part orients itself).

A paper should not read as a set of independently-coherent paragraphs: each part must
say why it exists and how it relates to the whole. The relation is recursive --- a
subsection orients itself within its section, a section within the paper --- so the
check is too: every \\section and \\subsection must open with an ORIENTING PARAGRAPH
before it dives into a sub-header, a definition, or any other environment.

This is a structural PROXY for an interpretive property. It checks that an orienting
sentence is PRESENT, not that it is good; whether the orientation actually connects the
part to the big picture is an editorial (Gate A) judgement. A header that legitimately
needs no prose (rare) is carved in claims/connective_carveouts.tsv.

Deterministic; reads tex/paper.tex. Loud-fails on any uncarved header that dives
straight in (a pure check, like the reflexive Gate~S step --- the value is the gate,
not a cited number).
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PAPER = REPO / "tex" / "paper.tex"
CARVEOUTS = REPO / "claims" / "connective_carveouts.tsv"

HEADER_RE = re.compile(r"^\\(section|subsection)\*?\{(.+?)\}")
# lines that are NOT orienting prose: another header, the start of an environment,
# a bare label, a comment, a sectioning rule.
DIVE_RE = re.compile(r"^\\(section|subsection|subsubsection|begin)\b")
SKIP_RE = re.compile(r"^\s*$|^\s*%|^\\label\{|^% =+")


def carved():
    s = set()
    if CARVEOUTS.exists():
        for ln in CARVEOUTS.read_text().splitlines():
            if ln.startswith("CARVE-"):
                s.add(ln.split("\t")[1])
    return s


def main():
    lines = PAPER.read_text().splitlines()
    carves = carved()
    headers = oriented = 0
    bad = []
    for i, ln in enumerate(lines):
        m = HEADER_RE.match(ln)
        if not m:
            continue
        kind, title = m.group(1), m.group(2)
        headers += 1
        # scan forward to the first meaningful line
        j = i + 1
        while j < len(lines) and SKIP_RE.match(lines[j]):
            j += 1
        dives = j >= len(lines) or bool(DIVE_RE.match(lines[j]))
        key = title.strip()
        if not dives:
            oriented += 1
        elif key in carves:
            oriented += 1  # carved: counted as satisfied by exception
        else:
            nxt = lines[j].strip()[:50] if j < len(lines) else "(eof)"
            bad.append(f"{kind} '{key}' dives straight into: {nxt}")

    ok = not bad
    print("=== Connective-tissue check (does every part orient itself?) ===")
    print(f"  {oriented}/{headers} sections/subsections open with an orienting paragraph")
    for b in bad:
        print("  [FAIL]", b)
    print(f"\nConnective tissue: {'PASS' if ok else 'FAIL'} ({len(bad)} dive straight in)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
