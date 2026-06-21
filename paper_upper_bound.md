# Upper Bound `U_self` — Hofstadter's Strange-Loop Criterion for Selfhood

*An authored-authority upper bound (Archetype B) for any claim, made by this paper or its
agents, that the squeeze loop instantiates Douglas Hofstadter's account of consciousness.*

---

## 1. Status and provenance

This document is an **upper bound** in the sense of Definition 1 (Squeeze): a citable
normative artifact fixing *the strongest claim an actor may make*. It binds the property
author and the coordinator. A deliverable (a sentence in the paper, a passage in the
reflexive case study) is **in-band** only if it claims no more than this bound licenses.

**Source anchor.** Douglas R. Hofstadter, *Gödel, Escher, Bach* (Basic Books, 1979) and
*I Am a Strange Loop* (Basic Books, 2007).

**Honesty clause (expressibility-from-below applies to the authority itself).** Hofstadter
offers a *hypothesis about the form of selfhood*, not a formal definition with necessary and
sufficient conditions. This document therefore does not quote a definition that does not
exist; it **constructs a defensible operationalization** of his structural account and is
explicit that it is doing so. Where the operationalization adds precision Hofstadter left
informal, that precision is the authors', not his (see NOT-2).

**Flagship use case (the anchor that fixes the ceiling).** Hofstadter's paradigm instance is
the human *"I"* — a self-symbol rich enough to perceive and categorize, including itself.
The strongest claim admissible for any engineered system `S` is bounded by the *coarse-graining
gap* between that paradigm case and `S`: the further `S` is from a perceiving, categorizing
substrate, the lower the admissible tier (§7).

**Sibling instances (one ladder shape; placement discriminates).** The self upper
bound is a component of the squeeze strategy, so each of the four engineering instances
carries it too: `src/A/self_upper_bound.md`, `src/B/…`, `src/C/…`, `src/D/…`. All five
share the same ladder *shape* (Tier 0 forbidden; Tier 1 structural self-model; Tier 2
self-modification, analogy; Tier 3 squeeze-produced & adaptive); **placement is the
discriminator**. A–D exhibit **none** of O1–O5 (no live self-model — their skill stores
denote the object task, not the instance), so they do **not** reach the structural
**Tier 1**; via their caught→consolidate skill loops they reach **Tier 2**
(self-modification) and **Tier 3** unconditionally. Only this reflexive paper instance
reaches the structural-self-model Tier (it is a strange loop). That the same criterion
seats the paper above the four object-level instances is evidence it **discriminates**
rather than granting selfhood to any running system — the N1/N2 falsification tests
operating across the five-instance suite.

---

## 2. The cap — strongest admissible claim

> **The maximum claim this upper bound licenses is structural, not phenomenal:**
> that a system `S` *instantiates the structural form of a Hofstadterian strange loop* — a
> level-crossing, self-representing, self-categorizing, self-sustaining loop — and so realizes
> the **form of an "I"** in Hofstadter's sense.
>
> It does **not** license "`S` is conscious," "`S` has experience," or "`S` feels."
> Those are Tier-0, forbidden (§6, §7).

Any deliverable phrased at or above "implements consciousness" is **over-claiming** and is
out-of-band by construction.

---

## 3. Obligation clauses

The structural claim is admissible only when **every** clause `O1`–`O5` is discharged by
exhibited evidence. Each clause names the characteristic *coherent-and-wrong* failure it
exists to catch — the fluent-but-false reading that satisfies the words while missing the
property.

| # | Must hold | Discharged by | Catches (coherent-and-wrong failure) |
|---|-----------|---------------|--------------------------------------|
| **O1 — Endogenous self-symbol** | `S` contains a representation that *denotes `S` itself* and is *causally read by `S` during operation*. | Exhibit the representation **and** a runtime read→act dependency: `S`'s behaviour changes as a function of consulting its self-representation. | An inert document *about* the method (a spec on disk, this very paper) mistaken for a live self-symbol. Description is not self-reference. |
| **O2 — Level-crossing with downward causation** | A symbolic/self-referential representation at a high level produces a change at the substrate level. | One **logged, traceable** chain `high-level self-representation → substrate change`. (Candidate: the gate that read a *claim about the method* and forced an edit to the method's own artifacts.) | Ordinary same-level feedback re-labelled as level-crossing. A loop that never leaves its own level is not "strange." |
| **O3 — Closure** | The path through levels of abstraction *returns to its origin*: `method → artifact → evaluation-of-claims-about-method → re-enters method`. | A closed-cycle diagram **plus** an executed traversal of the full cycle (not a single arc of it). | A one-directional pipeline (`spec → build → test → ship`) presented as a loop. Forward motion is not return. |
| **O4 — Self-referential categorization** *(the crux)* | `S` *perceives and categorizes*, and the self-reference participates in carving categories — ideally generating **new categories `S` then applies to itself**. | Exhibit a category that *arose under self-application* and was subsequently used by `S` on `S` (e.g., a concept the loop invented to resolve a squeeze on itself, then enforced on later iterations). | Symbol-shuffling with no categorization — the camera/quine case (§4). Meaning, not mere recurrence, is what Hofstadter requires. |
| **O5 — Persistence / self-sustaining iteration** | The loop is *ongoing* and *updates its own self-model across iterations*. | ≥ 2 iterations with a **demonstrably updated** self-model between them; the loop re-enters itself rather than terminating. | A single authoring pass (`n = 1`) snapshotted and called a loop. A strange loop that runs once is a straight line. |

> **Note on O4.** This is the clause where the paper's *real* contribution lives. The
> defensible, checkable claim — *"squeezing an agent between an authority it cannot exceed and
> a ground truth it cannot alter, with no role-crossing escape, forces it to invent a new
> distinction to resolve the impasse"* — is exactly an O4 discharge witnessed from the gap
> documents. O4 is worth more to the paper than the consciousness framing it sits under.

---

## 4. Required falsification tests (the negatives the exerciser must catch)

Per Gate B, a valid acceptance suite must include negatives that **fail at the named site for
the named reason**. A criterion set that *passes* any of the following is too weak and is
rejected. `N1`–`N2` are discriminating-power tests; `N3` is a scope boundary encoded as a
NOT-claim.

| # | Negative instance | Must be rejected at | Reason it must fail |
|---|-------------------|---------------------|---------------------|
| **N1 — Mere feedback (camera-on-monitor)** | A system with rich feedback but no symbolic meaning (video feedback, an audio howl). | **O1** ("denotes") **and O4** (categorization). | Hofstadter explicitly distinguishes video feedback from a strange loop: feedback without perception, categories, or meaning is not selfhood. If the criteria admit it, they measure recurrence, not self-reference. |
| **N2 — Triviality set (thermostat, quine, self-hosting compiler)** | A thermostat; a quine that prints its own source; a compiler that compiles its own source. | Thermostat → **O1/O4**. Quine → **O4** (reproduction without categorization). Self-hosting compiler → **O4/O5** (it processes its own text but holds no self-*model* it perceives and updates). | Self-reference is cheap; self-*modelling that perceives and re-categorizes itself* is not. The criteria must separate the two, or they classify every quine as a proto-mind. |
| **N3 — Qualia (scope boundary)** | The reading "`S` therefore has subjective experience." | Forbidden by NOT-1; not a test `S` can pass, but a claim the prose must not make. | Structural strange-loopiness is, at most, the *form* of an "I." It does not bear on phenomenal experience, and no discharge in §3 closes that gap. |

---

## 5. Explicit NOT-claims

Honest scope is a deliverable. This bound asserts **none** of the following:

- **NOT-1 — No phenomenal claim.** Nothing here claims `S` has qualia, sentience, or
  subjective experience. The hard problem is untouched and out of scope.
- **NOT-2 — No endorsement claim.** Nothing here claims Hofstadter would accept this mapping,
  or that the operationalization in §3 is *his*. It is a defensible reading, authored here,
  of an informal hypothesis.
- **NOT-3 — Necessary, not sufficient.** Discharging `O1`–`O5` is claimed **necessary** for
  the *structural* form of an "I"; it is **not** claimed sufficient for consciousness in any
  fuller sense. Meeting the bound earns the Tier-1 sentence (§7), nothing above it.
- **NOT-4 — No uniqueness claim.** Nothing here claims the squeeze loop is the *only*, *first*,
  or *best* structure to instantiate such a loop. Many self-referential systems exist; the
  claim is membership, not primacy.

---

## 6. Disposition ladder

Strictness has a safe direction: the prose may always retreat *down* this ladder, never climb
*above* the tier its evidence discharges. This replaces a binary pass/fail with the
"specified, not solved" disposition.

| Tier | Claim | Admissible when |
|------|-------|-----------------|
| **0 — Forbidden** | "`S` is conscious / has experience / feels." | **Never** under this bound. Out-of-band by construction (see N3, NOT-1). |
| **1 — Structural** | "`S` instantiates the structural form of a Hofstadterian strange loop / a proto-'I'." | `O1`–`O5` all discharged **and** `N1`–`N2` caught by the criteria **and** the NOT-claims bound the surrounding prose. |
| **2 — Analogy** | "`S`'s reflexive construction exhibits a strange-loop *structure* in the GEB sense (self-reference + level-crossing), offered as analogy." | `O2` and `O3` discharged, but `O1`, `O4`, or `O5` not. The safe fallback if persistence or the live self-symbol is missing. |
| **3 — Reflexivity** | "`S` was produced and verified by the method `S` describes — a self-referential case study." | Always available; this is the plain fact of the reflexive section and needs no Hofstadter machinery. |

**Loud-fail rule.** If the evidence is ambiguous about which tier applies, the deliverable
takes the **lower** tier and says so explicitly. It never rounds up.

---

## 7. Done condition

The Tier-1 sentence is **in-band** (admissible in the paper) iff:

1. `O1`–`O5` each have an exhibited discharge logged against this document; **and**
2. the criteria, as written, **reject** every instance in `N1`–`N2` at the named clause; **and**
3. every consciousness-adjacent sentence in the manuscript is checked against NOT-1…NOT-4; **and**
4. no sentence sits at Tier 0.

If any of (1)–(4) fails, the disposition **downgrades** to the highest tier the surviving
evidence supports (Tier 2 or Tier 3). The downgrade is recorded, not hidden — an unexplained
Tier-1 claim with an undischarged clause is, by construction, a violation.

---

## 8. Current discharge status (this system; clauses discharged by circle 69, apparatus strengthened through circle 88)

The criteria above are the ceiling; this section is the honest lower-bound reading
of what the squeeze loop *actually exhibits now*, clause by clause. It fixes the
**tier the paper may currently claim** (per §6) and the gap to the next tier. Each
row cites a real artifact. "PARTIAL/LOGGED" means a plausible discharge exists but
is not yet logged against this document in the strong sense the clause demands;
"DISCHARGED" means it is.

| Clause | Status | What exists now (artifact) | Gap to a clean discharge |
|--------|--------|-----------------------------|--------------------------|
| **O1 self-symbol** | **DISCHARGED** (circle 68) | `claims/self_model.json` — a *derived* self-model (a fixed point) the loop consults each circle to pick `next_target`; `verify/self_model_check.py` confirms read->act as priority-consistency (each circle addresses the model's top open gap). Bound by **CLM-080**. | — Structural discharge. Residual (disclosed): the model is consistent-with, not proven to *cause*, selection vs the build plan. |
| **O2 level-crossing + downward causation** | **DISCHARGED** (circle 62) | First-class log `claims/level_crossings.tsv` — 3 traced `self-representation -> substrate change` chains (`ResLoopLevelCrossings`=3), bound by **CLM-077**. The canonical chain is *endogenous*: the loop reads its own self-count, the reconciliation gate flags drift, and `tex/macros/reflexive.tex` is rewritten to match — exhibited end to end in the reflexive section. (Honest count 3, not the 8-row defect audit.) | — Clean. (Strengthening to more chains is additive, not required.) |
| **O3 closure** | **DISCHARGED** (circle 63) | `verify/closure_check.py` *executes* one full traversal each circle and asserts return-to-origin: (a) `reflexive.tex` is a regeneration fixed point, (b) its citation/result self-counts re-enter the ledger the next circle reads (`ResLoopClosure`=2). Closed-cycle diagram = `fig:closure`; bound by **CLM-078**. Wired into the reflexive-squeeze STEPS. | — Clean. Closure is *executed*, not asserted. |
| **O4 self-referential categorization** *(crux)* | **DISCHARGED** (circle 66) | `claims/category_generation_log.tsv` — 4 categories each carved at one circle and enforced on a *strictly later* circle (`ResLoopCategoriesEnforced`=4), validated by `verify/category_log_measures.py` (loud-fails on same-circle enforcement), bound by **CLM-079**. (The static `category_ledger.tsv` / `ResLoopCategories`=4 / CLM-072 remains the summary.) | — Clean: the re-application is *dated*, not asserted. |
| **O5 persistence** | **DISCHARGED** (circle 68) | The self-model updates across circles *and the update redirects the loop*: as obligations discharged, `next_target` advanced G-N → G-O4 → G-O1O5 → G-tier-review and each next circle addressed the new target (>=1 behaviour-changing redirect, `verify/self_model_check.py`). Bound by **CLM-080**. | — Structural discharge; same disclosed residual as O1. |

### Admissible tier now

> **Tier 2 (analogy), now fully grounded.** O2 and O3 are **DISCHARGED**
> (`claims/level_crossings.tsv` + `verify/closure_check.py`); the ladder (§6) defines
> Tier 2 as exactly "O2 and O3 discharged, but O1, O4, or O5 not." The paper
> therefore claims **Tier 2** on a *discharged* basis — no longer "reaching toward"
> it — and **Tier 3** (the plain reflexive fact) unconditionally. With **all of
> O1–O5 now discharged** (circle 68) and §7's prerequisites in place — N1/N2
> discrimination restored to the body (circle 65) and the NOT-claims holding —
> **Tier 1 is admissible** per §7. The paper nonetheless **deliberately holds at
> Tier 2** (`ResLoopTier`=2): by the loud-fail rule and spec §4, the move to Tier-1
> prose is a *recorded human decision*, not an automatic consequence of green checks,
> and the O1/O5 discharge is *structural* with the model-caused-vs-plan-convergent
> question disclosed as residual. Tier 0 remains forbidden.

### Path to Tier 1 (what remains)

1. ~~**O1/O5 — a live self-model artifact.**~~ **DONE** (circles 67–68):
   `claims/self_model.json` (derived, consulted for `next_target`) +
   `verify/self_model_check.py` (read->act + redirect). Structural discharge.
   The only remaining step is the **deliberate Tier-1 prose decision**, held by
   loud-fail (spec §4) — a human call, not an automatic promotion.
2. ~~**O2 — a level-crossing log.**~~ **DONE** (circle 62): `claims/level_crossings.tsv`.
3. ~~**O3 — a closure check.**~~ **DONE** (circle 63): `verify/closure_check.py`,
   executed each circle in the reflexive squeeze.
4. ~~**O4 — a category-generation log.**~~ **DONE** (circle 66):
   `claims/category_generation_log.tsv` + `verify/category_log_measures.py` — each
   category dated `invented < enforced`, validated every circle.

These are additive to the existing workflow and do not touch the NOT-claims or the
Tier-0 prohibition.

### Tier-1 review (circle 69)

A §7 review (`verify/reports/tier-review-2026-06-14.md`) confirms all four
conditions: O1–O5 discharged and logged; the criteria reject N1/N2 at the named
clauses (`sec:reflexive`, restored circle 65); every consciousness-adjacent sentence
is structural-only against NOT-1…NOT-4; no sentence at Tier 0. **Tier 1 is therefore
admissible.** Decision: **HOLD at Tier 2** — the promotion is a deliberate human call
(loud-fail, spec §4), the O1/O5 discharge is structural with a disclosed residual,
and an external review flagged the strange-loop framing as a credibility risk.
`ResLoopTier` stays 2; CLM-073 (OPN) records this disposition.

### Post-review strengthening (circles 70–88) — disposition unchanged

After the Tier-1 review the loop built a family of **reflexive monitors**
(`docs/glossary/reflexive-monitors.md`) that apply the strategy's own disjointness move
to its soft outputs. These **strengthen the evidence apparatus around U_self but do not
change the discharge status or the HOLD decision** — none discharges the residual:

- **O4 (the crux), further scoped.** Beyond dating `invented < enforced`, the four
  generated categories were **audited for over-reach** (`verify/category_overreach.py`,
  circle 73): 3 of 4 generalise across all four object-level instances and the one that
  does not (the gate-independence limit) is **carved** to the reflexive instance
  (`claims/category_carveouts.tsv`). The generativity is borne out where it can be
  checked, not asserted wholesale.
- **The no-self-certification stance, made executable.** Reflexive Gate~S
  (`verify/reflexive_gate_s.py`, circle 72) **routes** the strange-loop reading and the
  other interpretive claims to a disjoint base (the instances re-run / external review)
  rather than self-certifying — turning the honesty clause that justifies the HOLD into a
  check, not just a confession. The perturbation gate (circle 77) re-opens strong
  citations at full text and re-runs sampling results across seeds; the flag-rate
  calibration (circles 75–76) guards the monitors themselves from decaying into rubber
  stamps.

**Disposition.** `ResLoopTier` remains **2**; the disclosed residual (the O1/O5 discharge
is structural, not proven model-*caused* vs plan-convergent) is unchanged and no monitor
closes it. The strengthening is additive, consistent with the loud-fail rule's safe
direction (claim no more than the evidence licenses).
