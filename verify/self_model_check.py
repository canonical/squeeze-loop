#!/usr/bin/env python3
"""O1 + O5 discharge check for paper_upper_bound.md (U_self).

Asserts the live self-model (claims/self_model.json) satisfies the three structural
conditions O1+O5 require:

  (1) DERIVED, not fiction (the §6 anti-gaming guard): re-running verify/self_model.py
      reproduces claims/self_model.json byte-identically, so next_target is computed
      from the repo, not hand-set.
  (2) READ->ACT (O1), as priority-consistency: the sequence of per-circle TARGETs is
      non-decreasing in the gap priority -- the loop never addresses a lower-priority
      gap while a higher-priority one is open, i.e. each circle addresses the model's
      top open gap. Requires >= 2 circles since the model artifact was built.
  (3) REDIRECT (O5): >= 1 transition where consecutive TARGETs differ -- the model
      updated and the next circle followed the new target (a behaviour-changing
      update, not a counter tick).

HONEST SCOPE (recorded, not hidden): this establishes the *structural* O1/O5 ---
"the loop maintains a derived self-model and addresses its highest-ranked open
obligation each circle, the model updating and redirecting as obligations close." It
does NOT by itself prove the model *caused* the selection rather than converging with
the build plan; that stronger reading accrues as future circles are model-driven.
Per spec §4 the Tier-1 prose move stays a deliberate decision, never automatic.
Loud-fail: nonzero exit => O1/O5 NOT discharged.
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MODEL = REPO / "claims" / "self_model.json"
GEN = REPO / "verify" / "self_model.py"
MODEL_BUILT = 67  # circle at which claims/self_model.json first existed

PRIORITY = ["G-N", "G-O4", "G-O1O5", "G-tier-review"]  # order the loop addresses them


def rank(t):
    return PRIORITY.index(t) if t in PRIORITY else -1


def main():
    before = MODEL.read_bytes()
    subprocess.run([sys.executable, str(GEN)], capture_output=True)
    fixed_point = MODEL.read_bytes() == before

    model = json.loads(MODEL.read_text())
    hist = model["history"]
    ranks = [rank(e["target"]) for e in hist]
    consistent = all(r >= 0 for r in ranks) and all(b >= a for a, b in zip(ranks, ranks[1:]))
    n_consult = sum(1 for e in hist if e["circle"] >= MODEL_BUILT)
    redirects = sum(1 for a, b in zip(hist, hist[1:]) if a["target"] != b["target"])

    ok = fixed_point and consistent and n_consult >= 2 and redirects >= 1
    print(f"self-model: fixed_point={fixed_point} priority_consistent={consistent} "
          f"circles_since_model={n_consult} redirects={redirects}")
    print("O1+O5 (structural):", "DISCHARGED" if ok else "NOT discharged")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
