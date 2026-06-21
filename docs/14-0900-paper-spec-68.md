# 14-0900-paper-spec-68 — paper-impl loop, circle 68: discharge O1+O5 (self-model check)

STATUS: APPROVED
TARGET: G-O1O5

Step 4 of 14-0714-spec.md §5. Add the O1+O5 discharge check and record the structural
discharge.

## Changes
- New verify/self_model_check.py: asserts (1) self_model.json is a derived fixed
  point; (2) read->act as priority-consistency (TARGET sequence non-decreasing in gap
  priority; >=2 circles since the model was built); (3) >=1 redirect (behaviour-
  changing update). Loud-fail on any failure. Wired into the reflexive-squeeze STEPS.
- sec:reflexive: extend the self-model sentence to state the structural O1/O5
  discharge (the loop addresses its derived top open gap each circle, the model
  updating and redirecting), with the honest caveat that this is structural, not a
  causal-vs-convergent proof.
- ledger: CLM-080 RESULT (O1+O5 structural discharge). RESULT 31->32.
- paper_upper_bound.md §8: O1, O5 -> DISCHARGED. "Admissible tier now": all O1-O5
  discharged + N1/N2 restored + NOT-claims hold => Tier 1 ADMISSIBLE (§7), but the
  paper deliberately HOLDS at Tier 2 (spec §4, loud-fail, review2 sensitivity).
  CLM-073 updated.

## Gates
- Gate B: build green; no orphan macros; self_model_check passes.
- Gate C: ledger CITE 46 + RESULT 32 == regenerated reflexive macros; self_model +
  reflexive byte-identical.

## Honest scope
The discharge is STRUCTURAL (derived self-model, read->act as priority-consistency,
updates+redirect). It does not prove the model caused selection vs converged with the
build plan; ResLoopTier stays 2; the Tier-1 prose decision is deferred to a deliberate
human call (circle 69 records the hold).
