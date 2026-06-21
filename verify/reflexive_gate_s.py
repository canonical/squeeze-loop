#!/usr/bin/env python3
"""Reflexive Gate S -- Gate S turned on the paper loop's OWN soft outputs (self-improve.md).

The paper loop is itself a squeeze loop, so its accumulated soft outputs -- the claims in
claims/ledger.tsv and the generated categories -- are subject to the same failure as a
use case's skills: an over-generalised, coherent-and-wrong claim. This monitor applies
the Gate S discipline reflexively, but under the honesty limit self-improve.md states:
a producer shares its output's blind spot, so this gate CANNOT self-certify interpretive
claims. It is a CLASSIFIER + COVERAGE/ROUTING auditor, not a self-judge.

Per claim it does three things:
  1. CLASSIFY by kind. CITE/RESULT are evidence-bound (defer-to-oracle): their disjoint
     check already exists (the verifier re-opens the source at its anchor; the
     determinism gate re-runs the artifact). OPN/DEFN and the framing/category claims are
     interpretive (the high-risk, ignore-signal analog).
  2. CHECK COVERAGE (deterministic, can hard-fail): every claim must have a non-empty
     binding (no bare claim), and every OPN claim must be marked open/hedged.
  3. ROUTE the interpretive/high-risk claims to a DISJOINT base -- the executable
     instances (re-run) and external review -- and report them. The gate does NOT pass
     them on its own authority; routing is the point (no self-certification).

LOUD-FAIL only on a coverage breach (a bare claim, or an unhedged OPN). Interpretive
claims are routed, never silently certified. Deterministic.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LEDGER = REPO / "claims" / "ledger.tsv"

# An interpretive (high-risk) claim asserts a generalisation/reading rather than
# deferring to a single source or artifact. Detect by type (OPN/DEFN/MATH) or content.
INTERPRETIVE_RE = re.compile(
    r"strange.?loop|categor|generativ|\btier\b|disjoint|hard.?truth|soft.?truth"
    r"|self.?model|self.?symbol|relevance|level.?crossing|closure", re.I)
HEDGE_RE = re.compile(r"hedg|conjecture|pending|not measured|deliberately|disclosed"
                      r"|future work|OPN|admissible|held", re.I)


def rows():
    for line in LEDGER.read_text().splitlines():
        if re.match(r"^CLM-\d", line):
            c = line.split("\t")
            yield {"id": c[0], "type": c[1], "section": c[2], "binding": c[3],
                   "status": c[4] if len(c) > 4 else ""}


def main():
    by_kind = {"evidence-bound": 0, "interpretive": 0}
    routed, fails = [], []
    for r in rows():
        if not r["binding"].strip():
            fails.append(f"{r['id']}: bare claim (empty binding)"); continue
        interpretive = r["type"] in ("OPN", "DEFN", "MATH") or bool(INTERPRETIVE_RE.search(r["binding"]))
        by_kind["interpretive" if interpretive else "evidence-bound"] += 1
        if r["type"] == "OPN" and not (r["status"] == "OPEN" or HEDGE_RE.search(r["binding"])):
            fails.append(f"{r['id']}: OPN claim not marked open/hedged")
        if interpretive:
            disjoint = ("re-run on the executable instances" if r["type"] == "RESULT"
                        else "external review" if r["type"] in ("CITE", "OPN", "DEFN", "MATH")
                        else "external review")
            routed.append((r["id"], r["type"], disjoint))

    print("=== Reflexive Gate S: the paper loop auditing its own claims ===")
    print(f"classified: {by_kind['evidence-bound']} evidence-bound (CITE/RESULT -- disjoint "
          f"check = existing verifier/determinism gate), {by_kind['interpretive']} interpretive")
    print(f"\nrouted to a DISJOINT base (NOT self-certified -- self-improve.md honesty limit): "
          f"{len(routed)} claim(s)")
    for cid, t, route in routed:
        print(f"  {cid:9} [{t}] -> {route}")
    if fails:
        print("\nCOVERAGE BREACHES (loud-fail):")
        for f in fails:
            print("  [FAIL]", f)
    ok = not fails
    print(f"\nReflexive Gate S: {'PASS' if ok else 'FAIL'} "
          f"(coverage {'complete' if ok else 'broken'}; "
          f"{len(routed)} interpretive claim(s) routed for disjoint review)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
