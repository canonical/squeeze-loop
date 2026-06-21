# 12-5400-paper-spec-58 — paper-impl loop, circle 58: honest scoping of the demonstrations (review2 #6 + minors)

STATUS: APPROVED
Fifth review2 circle: Figure 2 (#6) and two minor points (analytics scale; refund
planted-not-searched seeds), plus a synthesis coupling-wording softening (#6).

## Changes (tex/paper.tex)
1. (#6) fig:coupling caption: label it an \emph{Illustration} (not a measured
   comparison); say the barrier-off row is the deterministic full-anchoring MODEL
   (detection zero by construction), not measured coupling; "weakly coupled" -> "low
   coupling".
2. (#6) sec:synthesis prose: "stayed weakly coupled to the implementation" -> "showed
   low overlap with the implementation" (the consistent-with-not-establishing caveat
   lives in the eval bullet, circle 57).
3. (minor) sec:caseD: after the warehouse-scale sentence, add ", a deliberately
   minimal demonstration rather than a benchmark".
4. (minor) sec:caseE: after the refund detection sentence, add that these are
   planted clause violations, NOT adversarially searched inputs -- we report
   catching the defects we seeded and did not search for a manipulation that slips
   past the external lockpoint; that red-team search is future work.

## Gates
- Gate B: build green; figures stay macro-bound; no new cite/number/macro/CLM; refs
  resolve; previously-SUPPORTED text byte-stable outside the four hunks.
- Gate C: ledger unchanged (CITE 46 + RESULT 28); reflexive macros reconcile;
  reflexive re-run byte-identical.

## Note
Safe direction: weakens the rhetorical force of Figure 2 and the coupling/detection
demonstrations, and states explicitly that the 4/4-style results are
detections-of-planted-seeds, not survivors of an adversarial search. No empirical
claim strengthened.
