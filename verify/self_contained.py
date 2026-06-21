#!/usr/bin/env python3
"""Self-containment check (paper-impl principle: define before use).

A reader must never meet a load-bearing term they cannot resolve. Each registered key
term must be *introduced* (defined or glossed) at or before its first use in the body;
a use that precedes the term's definition is allowed ONLY if it carries a forward
\\ref to where the term is defined, so the reader can get there. (Example this was
written for: "the editorial gate (Gate~A)" appeared in a Section-3.1 remark while
Gate~A is not defined until Section~3.3.)

This is a structural PROXY: it checks that a forward use is *signposted* (a \\ref to the
definition section is present in the same paragraph), not that the gloss is good --- the
quality of the introduction is an editorial (Gate~A) judgement. The abstract is exempt
(a summary may name what the body later defines). Carve-outs in
claims/selfcontained_carveouts.tsv.

Registry maps each term to the \\label of the section/definition that introduces it.
Deterministic; reads tex/paper.tex; loud-fails on an unsignposted forward use.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PAPER = REPO / "tex" / "paper.tex"
CARVEOUTS = REPO / "claims" / "selfcontained_carveouts.tsv"

# term (as it appears in the source) -> \label of the section/definition that defines it.
REGISTRY = [
    ("Gate~A", "sec:mechanics"),
    ("Gate~B", "sec:mechanics"),
    ("Gate~C", "sec:mechanics"),
    ("Gate~S", "sec:mechanics"),
]


def carved():
    s = set()
    if CARVEOUTS.exists():
        for ln in CARVEOUTS.read_text().splitlines():
            if ln.startswith("CARVE-"):
                s.add(ln.split("\t")[1])
    return s


def paragraph_bounds(lines, i):
    """[start, end) of the blank-line-delimited paragraph containing line i."""
    start = i
    while start > 0 and lines[start - 1].strip():
        start -= 1
    end = i
    while end < len(lines) and lines[end].strip():
        end += 1
    return start, end


def main():
    lines = PAPER.read_text().splitlines()
    carves = carved()

    # abstract region (exempt)
    ab0 = ab1 = None
    for i, ln in enumerate(lines):
        if "\\begin{abstract}" in ln:
            ab0 = i
        if "\\end{abstract}" in ln:
            ab1 = i
    in_abstract = (lambda i: ab0 is not None and ab1 is not None and ab0 <= i <= ab1)

    bad = []
    checked = 0
    for term, label in REGISTRY:
        def_line = next((i for i, ln in enumerate(lines)
                         if f"\\label{{{label}}}" in ln), None)
        if def_line is None:
            bad.append(f"{term}: definition label '{label}' not found")
            continue
        first_use = next((i for i, ln in enumerate(lines)
                          if term in ln and not in_abstract(i)), None)
        if first_use is None:
            continue  # never used in body
        checked += 1
        if first_use >= def_line:
            continue  # defined at/before first use -- fine
        # forward use: require a \ref to the definition section in the same paragraph
        s, e = paragraph_bounds(lines, first_use)
        signposted = any(f"\\ref{{{label}}}" in lines[k] for k in range(s, e))
        if signposted or term in carves:
            continue
        bad.append(f"{term}: first used at line {first_use+1} but defined at "
                   f"\\label{{{label}}} (line {def_line+1}) with no forward \\ref to it")

    ok = not bad
    print("=== Self-containment check (is every key term introduced before use?) ===")
    print(f"  {checked} registered terms checked; {checked - len(bad)} introduced before use "
          f"or signposted")
    for b in bad:
        print("  [FAIL]", b)
    print(f"\nSelf-containment: {'PASS' if ok else 'FAIL'} ({len(bad)} forward use(s) unsignposted)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
