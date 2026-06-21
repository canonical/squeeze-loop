#!/usr/bin/env python3
"""Claim-consistency check (paper-impl principle: framing claims may not silently diverge).

The squeeze's other gates verify EVIDENCE-BOUND claims (CITE/RESULT). They do not verify
mutual consistency of INTERPRETIVE / framing claims across sections -- a soft-truth vs
soft-truth comparison with no executable lower bound. That residual is caught only by a
disjoint editorial pass (Gate A). This gate MECHANIZES the part of that residual that can be
mechanized: a growing ledger of framing invariants (claims/framing_invariants.tsv).

Two row kinds, matched against tex/paper.tex with LaTeX commands stripped and whitespace
collapsed (case-insensitive):
  BANNED <regex> <rationale>     -- a previously-caught coherent-and-wrong phrasing; FAIL if
                                    it reappears (regression guard).
  MAX <regex> <n> <rationale>    -- this pattern may match at most n times; FAIL if exceeded
                                    (superlative / ranking uniqueness).

This is a PROXY: it catches the RETURN of a known framing defect and the violation of a
registered uniqueness cap; it cannot catch a brand-new, unregistered framing defect (coverage
is the ceiling -- which is why editorial_gate.py keeps a standing disjoint Gate A).

Deterministic; loud-fails. Mirrors connective_tissue.py / self_contained.py in spirit.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PAPER = REPO / "tex" / "paper.tex"
INVARIANTS = REPO / "claims" / "framing_invariants.tsv"


def normalized_paper() -> str:
    """Strip LaTeX commands that fragment phrases (\\emph{x}->x, \\code{x}->x, \\ResX{}),
    drop comments, collapse whitespace, lowercase. Makes phrase patterns robust to markup."""
    txt = PAPER.read_text()
    txt = re.sub(r"(?m)^\s*%.*$", " ", txt)          # comment lines
    txt = re.sub(r"\\(emph|textbf|textit|code|texttt)\{([^{}]*)\}", r"\2", txt)
    txt = re.sub(r"\\Res[A-Za-z]+\{\}", " ", txt)    # gated number macros -> space
    txt = re.sub(r"\\[A-Za-z]+\b", " ", txt)          # any remaining control words
    txt = txt.replace("{", " ").replace("}", " ")
    txt = re.sub(r"\s+", " ", txt)
    return txt.lower()


def rows():
    banned, capped = [], []
    if not INVARIANTS.exists():
        return banned, capped
    for ln in INVARIANTS.read_text().splitlines():
        if not ln.strip() or ln.startswith("#"):
            continue
        f = ln.split("\t")
        if f[0] == "BANNED" and len(f) >= 2:
            banned.append((f[1], f[2] if len(f) > 2 else ""))
        elif f[0] == "MAX" and len(f) >= 3:
            capped.append((f[1], int(f[2]), f[3] if len(f) > 3 else ""))
    return banned, capped


def main():
    text = normalized_paper()
    banned, capped = rows()
    fails = []

    for pat, why in banned:
        if re.search(pat.lower(), text):
            fails.append(f"BANNED phrasing returned: /{pat}/ -- {why}")

    cap_lines = []
    for pat, n, why in capped:
        hits = re.findall(pat.lower(), text)
        cap_lines.append(f"  MAX /{pat[:48]}.../ = {len(hits)}/{n}")
        if len(hits) > n:
            fails.append(f"MAX exceeded ({len(hits)}>{n}): /{pat}/ -- {why}")

    ok = not fails
    print("=== Claim-consistency check (do framing claims stay mutually consistent?) ===")
    print(f"  {len(banned)} banned phrasings checked, {len(capped)} uniqueness caps checked")
    for c in cap_lines:
        print(c)
    for f in fails:
        print("  [FAIL]", f)
    print(f"\nClaim consistency: {'PASS' if ok else 'FAIL'} "
          f"({len(fails)} framing divergence(s); coverage is a floor, not a ceiling)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
