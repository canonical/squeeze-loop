# 12-2630-paper-spec-29 — paper-impl loop, circle 29: launch review1 response cycle + first fix

STATUS: DONE
Launches the review-response sub-loop (review1.md) and executes its first,
highest-priority self-contained fix.

## Deliverables this circle
1. level-up-test-plan.md (root) — plan to level up executable instances A/B/C so
   the strategy's effect becomes *measured*, not just mechanism-demonstrated:
   difficulty calibration to a nonzero natural error rate, partial-coupling
   barrier-off curve (de-tautologizes the headline), coupling baselines +
   embeddings, cost ledger, and the review's benchmark routes (SWE-bench Verified,
   SWT-Bench, tau-bench, AgentDojo/CaMeL, metamorphic + property-based testing).
2. docs/12-2600-review1-response-plan.md — full triage of every review item to a
   disposition (DONE / FIX / STUDY / DECIDE / DECLINE) and a circle sequencing.
3. The first fix (A1 below).

## A1 — Figure 1 caption internal inconsistency (FIXED)
The caption read "Gates~A--B are machine-checked acceptance" but Gate A is the
coordinator's EDITORIAL judgment (sec:mechanics, and the figure body itself:
"GATE A coordinator EDITORIAL approval"). The reviewer flagged the irony: the
reflexive section reports catching exactly this self-inconsistency class, yet this
one survived.
- Caption corrected: "Gate~A is the coordinator's editorial approval of the plan
  (judgment, not machine output); Gate~B is machine-checked acceptance; Gate~C is
  the coherent-and-wrong / no-blend coverage guard."
- Recorded as defect D8 in verify/manuscript_defects.tsv (evidence plane, F6
  self-inconsistency, FIXED) with the honest note that it was caught by EXTERNAL
  review, NOT by the internal gates.
- Reflexive limitation prose updated: now "in at least two instances, by external
  challenge" -- the environment claim AND the peer-review caption catch, framed as
  "the failure class the strategy targets, found by the one party with true
  context independence." Strengthens the paper's own thesis honestly.

## Effect on numbers
- manuscript_defects.tsv: 7 -> 8 rows (4 literature, 4 evidence).
- tex/macros/reflexive.tex regenerated: ResReflexDefects 7->8, ResReflexDefectsEvid
  3->4 (lit unchanged 4); ResReflexSpecDocs -> 28 (this circle). Others unchanged.
- The reflexive example list ("a figure crediting the wrong source, ...") still
  lists 3 of the 4 evidence defects under the "they included" sample hedge; the
  4th (the caption) is described in the limitation sentence.

## Why not more this circle
The review is large; per the methodology, circles are taken one at a time. The
remaining items are queued in the response plan: mechanical quick-wins, the formal
core (C1/C2 strengthening), the redundancy cut (-15-20%), the framing demotion of
the headline, the literature additions (read-before-cite, batched), and the
methodology/level-up study. Four items need a user decision (Figure 2 fate,
re-adding an appendix for the artifact, abstract \ref-vs-hardcode, author-block
deanonymization).

## Strange-loop fixed point
spec-29 counted in ResReflexSpecDocs: trail written first, harness regenerated,
committed together.

## Gates
- Gate B: build green (18 pp), all cites/refs/macros resolve, no bibtex warnings.
- Determinism: reflexive harness re-run byte-identical.
- Ledger: no claims/ledger.tsv change (D8 is a manuscript-defect record, not a
  CITE/RESULT claim).
