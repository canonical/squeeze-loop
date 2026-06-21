# review1 response cycle — triage and roadmap

Source: review1.md (external review, 2026-06-12). Every item mapped to a
disposition: DONE (this circle 29), FIX (queued, self-contained), STUDY (needs
the level-up work, see level-up-test-plan.md), DECIDE (needs the user), or
DECLINE (with reason). This launches the review-response sub-loop; circles are
taken one at a time and committed individually, as in the polish sweep.

## A. Correctness / internal consistency (highest priority)
- **A1 [DONE c29]** Figure 1 caption said "Gates A-B are machine-checked
  acceptance" while Gate A is editorial. Fixed the caption; recorded as defect D8
  (caught by EXTERNAL review, not the internal gates); reflexive limitation now
  reports the peer-review catch honestly (ResReflexDefects 7->8).
- **A2 [FIX]** C1 is weaker than the prose: pi_i != pi_j is satisfied by trivially
  different lower bounds while a blind spot is shared, and Table 1's implementer
  and exerciser both derive their upper bound from the same spec. State the
  stronger intended condition (non-nested / non-dominated evidence bases) and tie
  C2's "characteristic failure" to the seeded-defect families. (Formal-core circle.)
- **A3 [FIX]** "intersection ... is the correct deliverable" presumes a unique
  correct answer; for generative tasks say "contained in the acceptable set."
- **A4 [FIX]** Stabilizers 1/2/3/13 restate Table 1 / C3 / C4 / Archetype B's gate;
  fold those four into the compliance conditions, keep 4-12. (Also a redundancy item.)

## B. Headline framing (high priority)
- **B1 [STUDY+FIX]** Barrier-off = full anchoring, so 0% is partly by construction.
  Prose half [FIX]: demote the 100/0 line to a *mechanism demonstration* in the
  abstract/conclusion and let the design conditions + honest pilot nulls lead.
  Measurement half [STUDY]: the partial-coupling leakage curve in
  level-up-test-plan.md replaces the tautological two points.
- **B2 [FIX]** Promote the honest-null pilot findings (models test against spec
  even when shown code; near-zero error rate) out of §7 into the abstract/intro —
  the review calls them the most informative empirical content.

## C. Missing references (needs read-before-cite — these are STUDY, not quick)
Every add requires a reading record first (the paper's own rule), so these are
batched into a literature circle, in review-priority order:
- **C1 [FIX-lit]** AI Control (Greenblatt et al. ICML 2024) — closest framework
  where evidence flow is the design object; must engage in §2.3/§2.6.
- **C2 [FIX-lit]** MAST (Cemri et al. 2025) — empirical multi-agent failure
  taxonomy; the motivation §1 argues from first principles.
- **C3 [FIX-lit]** SWT-Bench (Mündler et al. NeurIPS 2024) + SWE-bench Verified —
  the exerciser role on real bugs; weakens the §7 infra excuse. Ties to
  level-up Stage 2.
- **C4 [FIX-lit]** CodeT (ICLR 2023), AlphaCode (Science 2022) — dual
  execution-agreement, nearest ancestor of implementer/exerciser agreement.
- **C5 [FIX-lit]** EvalPlus (NeurIPS 2023) — weak suites pass wrong code; the
  abstract's "tests tuned to the implementation" currently uncited.
- **C6 [FIX-lit]** tau-bench (Yao et al. ICLR 2025) + tau2-bench — Case E's exact
  setting; ties to level-up B.
- **C7 [FIX-lit]** AgentDojo (NeurIPS 2024) + CaMeL (2025) — Case E's action
  lockpoint; cite with perez2022/greshake2023.
- **C8 [FIX-lit]** Newer judge work: Wataoka et al., Xu et al. 2024 (Pride and
  Prejudice), Ye et al. 2024 survey — extend §2.2 past the 2023-24 wave.
- **C9 [FIX-lit]** Classics: Parnas 1972 (information hiding -> C3 ancestor);
  metamorphic testing (Chen 1998 / Segura 2016) — REQUIRED for Archetype B;
  property-based testing (Claessen & Hughes 2000); vacuity/coverage in model
  checking (Beer 2001; Chockler-Kupferman-Vardi) -> Gate C ancestor.
- **C10 [FIX-lit]** Small cites: IV&V (NASA handbook / Boehm 1984); golden-master
  / characterization testing (Feathers 2004) for "total additivity".
- **C11 [FIX]** Update preprint keys to venue versions: huang2023cannot -> ICLR
  2024; sharma2023sycophancy -> ICLR 2024; panickssery2024llm -> NeurIPS 2024;
  du2023debate -> ICML 2024. (Metadata only, no re-read.)

## D. Redundancy (target -15-20% length)
- **D1 [FIX]** Disjointness restated ~5x (abstract, intro item 2, Remark 1, §3.3,
  conclusion) — keep one full statement, cross-reference the rest.
- **D2 [FIX]** Barrier-on/off result restated 8+ times — keep abstract + Fig 2 +
  synthesis; cut the per-case-study and Limitations repeats.
- **D3 [FIX]** Scope caveat closes all three case studies near-verbatim + recurs
  in Limitations — state once in the §4 preamble.
- **D4 [FIX]** Merge Tables 2 and 3 (three duplicated rows) or strip Table 3 to
  measurements only.
- **D5 [DECIDE]** Figure 2 plots y in {0,100} only — review says it adds nothing
  over the Table 3 row. Counter: the partial-coupling curve (B1) gives it real
  content. Decide after Stage 0 of the level-up: drop the figure, or replace with
  the curve. (Recommend: keep, fill with the curve.)
- **D6 [FIX]** Fold stabilizers 1/2/3/13 into the compliance conditions (= A4).

## E. Methodology additions (STUDY — see level-up-test-plan.md)
- **E1** Partial-coupling barrier-off curve (de-tautologize the headline).
- **E2** Coupling baseline + embedding estimator.
- **E3** Cost ledger (H4 data) + report/optional-mark the probe role.
- **E4** Run SWE-bench Verified + SWT-Bench (Stage 2).

## F. Show the artifact
- **F1 [FIX]** Display one instantiated squeeze table + a delegation-prompt excerpt
  (contribution (ii) is described but never shown). NOTE: appendices were removed
  in circle 10; this re-adds a small appendix — confirm that is wanted.

## G. Mechanical / reviewability
- **G1 [DECIDE]** `\ref{item:laststab}` in the abstract breaks standalone abstract
  extraction / arXiv metadata; review says hardcode "thirteen". This REVERSES
  circle 26 (which made it drift-proof). Trade-off: extraction-robustness vs
  drift-proofing. RECOMMEND: hardcode in the abstract only (extraction-facing),
  keep \ref in the body. User to confirm.
- **G2 [DECIDE]** Author-block GitHub URL deanonymizes if the venue is
  double-blind. Depends on target venue — user to confirm.
- **G3 [FIX]** Ship macros/ with the submission OR inline final numbers, so the
  paper does not compile to blanks without macros/. (Reviewer saw all blanks.)
- **G4 [FIX]** Convert the ASCII `verbatim` pipeline to a real figure (tikz).
- **G5 [FIX]** Remove the unused `extract` environment (dead code).

## H. Prose
- **H1 [FIX]** Abstract is ~a page; halve it (overlaps B1/B2/D1).
- **H2 [FIX]** Split the worst em-dash-chained sentences (pairs with the
  de-duplication).

## Sequencing of circles
1. c29 (this): A1 + launch (triage + level-up plan). DONE.
2. Quick-win circle: G5, G4, C11, G3 (mechanical, no decisions).
3. Formal-core circle: A2, A3.
4. Redundancy circle(s): D1-D4, D6/A4, H1-H2 (the -15-20%).
5. Framing circle: B1-prose, B2.
6. Literature circles: C1-C10 (read-before-cite, batched by theme).
7. Methodology/level-up: E1-E4 per level-up-test-plan.md (Stages 0-3).
8. Decisions to surface to the user: D5, F1, G1, G2.
