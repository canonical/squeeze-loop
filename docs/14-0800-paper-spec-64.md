# 14-0800-paper-spec-64 — paper-impl loop, circle 64: refresh U_self §8 (discharge status)

STATUS: APPROVED
Circle C of 14-0649-plan.md. Refresh the discharge-status section of the upper-bound
document now that O2 (circle 62) and O3 (circle 63) are discharged. The §8 table was
frozen "as of circle 32" with stale counts and O2/O3 marked CANDIDATE.

## Changes
1. paper_upper_bound.md §8: heading "as of circle 32" -> "as of circle 64";
   - O2 row: CANDIDATE -> DISCHARGED (claims/level_crossings.tsv, 3 chains, CLM-077;
     canonical endogenous chain; ResLoopLevelCrossings=3).
   - O3 row: CANDIDATE -> DISCHARGED (verify/closure_check.py executes the traversal
     each circle: fixed point + re-entry; fig:closure; CLM-078; ResLoopClosure=2).
   - O4 row: CANDIDATE -> LOGGED (partial) (claims/category_ledger.tsv, 4 categories,
     CLM-072; ResLoopCategories=4) -- Tier-1-strength O4 still pending.
   - O1/O5 rows: still PARTIAL; refresh counts (circle 32 -> 64; SpecDocs -> 64,
     ResultRows 19/23 -> 30, defects 7->8).
   - "Admissible tier now": Tier 2 now FULLY GROUNDED (ladder = O2+O3 discharged,
     O1/O4/O5 not); Tier 1 still NOT in-band (needs O1, O4, O5); Tier 0 forbidden.
   - "Path to Tier 1": items 2 (O2 log) and 3 (O3 closure) DONE; items 1 (O1/O5 live
     self-model) and 4 (O4 strong) remain.
2. verify/strange_loop.py docstring: update the tier line to "O2/O3 discharged;
   O1/O5 partial; O4 logged-not-Tier-1-strong" (docstring only; no output change).
3. claims/ledger.tsv CLM-073 (OPN, tier status): note O2/O3 now discharged; Tier 1
   pending O1, O4, O5 (was "O1 + O4"). OPN row -> CITE/RESULT counts unchanged.

## Gates
- Gate B: build green; no new \cite/macro/CLM; manuscript claims unchanged (this is
  the upper-bound doc + a docstring + an OPN-row wording fix); previously-SUPPORTED
  text byte-stable.
- Gate C: ledger CITE 46 + RESULT 30 unchanged == regenerated reflexive macros
  (ResReflexSpecDocs 63->64 for this spec doc); strange_loop/reflexive/closure re-run
  byte-identical.

## Note
No tier change: the paper still claims Tier 2 (now on a discharged, not "reaching",
basis). Tier 0 and the NOT-claims are untouched. Completes 14-0649-plan.md.
