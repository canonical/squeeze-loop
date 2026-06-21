#!/usr/bin/env python3
"""Editorial-gate freshness check (paper-impl principle: a standing, disjoint Gate A).

The framing residual that machine gates cannot verify -- whether the paper's soft framing is
FAITHFUL to its evidence (a soft-truth vs soft-truth judgment with no executable lower bound)
-- is, by the paper's own thesis, catchable only by DISJOINT AUTHORITY: an editorial judge who
is not the author (Archetype B). This gate does NOT perform that judgment (that would be the
author grading itself). It ENFORCES that a disjoint judgment was performed and is CURRENT:

  - claims/editorial_review.md must exist and record:
        paper-sha256: <sha256 of tex/paper.tex at review time>
        judge: <model id or person>
        disjoint-from-author: <how the judge is disjoint from the author>
        verdict: ACCEPT | ACCEPT-WITH-FIXES | REJECT
  - the recorded sha must match the CURRENT tex/paper.tex (else the review is STALE: the paper
    changed since it was judged -- re-run the disjoint pass).
  - the verdict must be ACCEPT or ACCEPT-WITH-FIXES.

R3 warns that a same-provider-family judge shares the author's blind spot; the gate therefore
also REPORTS the disjointness quality and recommends cross-provider or human review as the
gold standard (it does not fail on same-family, but records the limitation honestly).

Deterministic; loud-fails. The sha is over tex/paper.tex only (macros live elsewhere), so
recompiling or regenerating numbers does not stale the review -- only editing the manuscript
prose does, which is exactly when re-judgment is wanted.
"""
import hashlib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PAPER = REPO / "tex" / "paper.tex"
REVIEW = REPO / "claims" / "editorial_review.md"
XPROVIDER = REPO / "claims" / "cross_provider_review.md"
OK_VERDICTS = {"ACCEPT", "ACCEPT-WITH-FIXES"}


def field(text, name):
    m = re.search(rf"(?mi)^\s*{re.escape(name)}\s*:\s*(.+?)\s*$", text)
    return m.group(1).strip() if m else None


def main():
    print("=== Editorial gate (standing disjoint Gate A: is a current review on file?) ===")
    if not REVIEW.exists():
        print(f"  [FAIL] no disjoint editorial review at {REVIEW.relative_to(REPO)}")
        print("  Run a disjoint editorial pass (cross-provider/human ideal) and record it.")
        print("\nEditorial gate: FAIL (no review)")
        return 1

    rt = REVIEW.read_text()
    recorded = field(rt, "paper-sha256")
    judge = field(rt, "judge")
    disjoint = field(rt, "disjoint-from-author")
    verdict = (field(rt, "verdict") or "").upper()
    current = hashlib.sha256(PAPER.read_bytes()).hexdigest()

    fails = []
    if not recorded:
        fails.append("review records no paper-sha256")
    elif recorded != current:
        fails.append(f"STALE review: recorded sha {recorded[:12]} != current {current[:12]} "
                     "(paper changed since it was judged -- re-run the disjoint pass)")
    if verdict not in OK_VERDICTS:
        fails.append(f"verdict is {verdict or '(missing)'} -- not in {sorted(OK_VERDICTS)}")

    print(f"  judge: {judge or '(unrecorded)'}")
    print(f"  disjoint-from-author: {disjoint or '(unrecorded)'}")
    print(f"  verdict: {verdict or '(missing)'}")
    print(f"  paper sha: current {current[:12]}; reviewed {(recorded or '-')[:12]}")
    if disjoint and "cross-provider" not in disjoint.lower() and "human" not in disjoint.lower():
        print("  [note] operative judge is not cross-provider/human; R3 shows same-family judges "
              "share the author's blind spot -- treat as PARTIAL disjointness.")
    # cross-provider axis (gold standard): report, do not gate on the weak local model.
    if XPROVIDER.exists():
        xt = XPROVIDER.read_text()
        xprov = field(xt, "cross-provider")
        xauth = field(xt, "authoritative")
        xmodel = field(xt, "model")
        print(f"  cross-provider axis: model {xmodel or '?'} -- cross-provider={xprov or '?'}, "
              f"authoritative={xauth or '?'}")
        if (xauth or "").lower() != "true":
            print("  [note] cross-provider check ran but is NON-AUTHORITATIVE (the available judge "
                  "is truly disjoint but too weak / not cross-provider). GOLD STANDARD pending a "
                  "CAPABLE cross-provider judge: set OPENAI_API_KEY + CROSS_MODEL and run "
                  "verify/cross_provider_review.py. (Capability and disjointness trade off -- R3.)")
    else:
        print("  [note] no cross-provider review on file; the gold-standard disjoint judge "
              "(capable + cross-provider) is pending -- run verify/cross_provider_review.py.")
    for f in fails:
        print("  [FAIL]", f)
    ok = not fails
    print(f"\nEditorial gate: {'PASS' if ok else 'FAIL'} "
          f"({'current disjoint review on file' if ok else 'review missing/stale/negative'})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
