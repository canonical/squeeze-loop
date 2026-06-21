# Tier-1 review — U_self (paper_upper_bound.md §7), 2026-06-14 (circle 69)

Reviews whether the Tier-1 sentence is in-band, per the §7 done-condition, after
circles 62–68 discharged O1–O5. Loud-fail: any unmet condition holds the paper at the
highest surviving tier.

## §7 conditions

1. **O1–O5 each discharged and logged against the document.** YES.
   - O1, O5 — `claims/self_model.json` + `verify/self_model_check.py` (CLM-080), structural.
   - O2 — `claims/level_crossings.tsv` (CLM-077).
   - O3 — `verify/closure_check.py` (CLM-078).
   - O4 — `claims/category_generation_log.tsv` + `verify/category_log_measures.py` (CLM-079).
   - All marked DISCHARGED in §8.

2. **The criteria reject every N1/N2 negative at the named clause.** YES.
   Restored to the body in circle 65 (`sec:reflexive`): video feedback rejected at
   O1 (no self-denotation) + O4 (no categorization); the triviality set (thermostat,
   quine, self-hosting compiler) rejected at O4/O5 (reproduction/processing is not a
   perceived, re-categorized self-model). N3 (qualia) is a scope boundary, not a test.

3. **Every consciousness-adjacent sentence checked against NOT-1…NOT-4.** YES — all
   structural-only:
   - Abstract: "structural *form* of a strange loop … scoped to that form, never to
     experience."
   - Contribution (vii): "structural *form* of an ‘I’, never experience."
   - `sec:reflexive`: "structural *form* of an ‘I’ … *not* experience or consciousness."
   - Conclusion: "the form of an ‘I’ and nothing more … no consciousness, no qualia."
   None asserts qualia (NOT-1), Hofstadter endorsement (NOT-2), sufficiency (NOT-3),
   or primacy (NOT-4).

4. **No sentence at Tier 0.** YES — no "is conscious / has experience / feels."

## Verdict

All four §7 conditions hold ⇒ **Tier 1 is admissible.**

## Decision: HOLD at Tier 2

The paper **does not** promote to a Tier-1 sentence at this time. Reasons, recorded:

- **Loud-fail + spec §4:** the move to Tier-1 prose is a *deliberate, recorded human
  decision*, never an automatic consequence of green checks.
- **Structural residual:** the O1/O5 discharge is *structural* (a derived self-model
  consulted with priority-consistent read→act and a behaviour-changing redirect). It
  does not establish that the model *caused* circle selection rather than converging
  with the build plan — disclosed, not hidden.
- **Strategic:** an external review (review2) judged the strange-loop framing a
  credibility risk and asked to compress it; promoting to Tier 1 cuts against that.

`ResLoopTier` stays **2**; CLM-073 remains OPN and records this disposition. The
Tier-1 option is available to the authors as a deliberate future decision.
