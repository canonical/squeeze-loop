# Tier / disposition ladder (Tier 0–3)

**Definition.** A *tier* is a rung on a **disposition ladder**: an ordered set of
progressively stronger claims an actor may make, where each rung is admissible only
when a stated evidence condition is met. The ladder replaces a binary pass/fail with
a graded "specified, not solved" disposition: prose may always retreat *down* the
ladder, never climb *above* the tier its evidence discharges.

The tiers below are the ladder defined by **`paper_upper_bound.md` (U_self)** for any
claim that the squeeze loop instantiates Hofstadter's account of selfhood. The
*mechanism* — a graded ladder + loud-fail rule — is general; the specific rungs are
U_self's.

## The loud-fail rule

> If the evidence is ambiguous about which tier applies, the deliverable takes the
> **lower** tier and **says so explicitly**. It never rounds up.

This is what makes the ladder honest: an unexplained higher-tier claim with an
undischarged condition is, by construction, a violation.

## The U_self rungs

| Tier | Claim it licenses | Admissible when |
|------|-------------------|-----------------|
| **0 — Forbidden** | "S is conscious / has experience / feels." | **Never.** Out-of-band by construction (phenomenal claims are forbidden by the NOT-claims; see N3 / NOT-1). |
| **1 — Structural** | "S instantiates the structural *form* of a Hofstadterian strange loop / a proto-'I'." | **O1–O5 all discharged**, *and* the criteria **reject** the N1/N2 negatives, *and* the NOT-claims bound the surrounding prose (§7). |
| **2 — Analogy** | "S's reflexive construction exhibits a strange-loop *structure* in the GEB sense (self-reference + level-crossing), offered as analogy." | **O2 and O3 discharged**, but O1, O4, or O5 not. |
| **3 — Reflexivity** | "S was produced and verified by the method S describes — a self-referential case study." | **Always available** (the plain fact of the reflexive section; needs no Hofstadter machinery). |

`S` = the system under claim (here, the squeeze loop applied to its own
construction). O1–O5 are the obligation clauses; N1–N3 are the negatives the criteria
must catch — **N1–N2 discriminating-power tests** (mere feedback; the triviality set)
and **N3 a scope boundary** (the qualia reading the prose must never make) — all of
`paper_upper_bound.md` §4.

## Current disposition

As of circle 69 **all of O1–O5 are discharged** and §7's prerequisites are met (N1/N2
restored to the body, NOT-claims hold), so **Tier 1 is admissible** — but the paper
**deliberately holds at Tier 2** (`\ResLoopTier`=2): the promotion to Tier-1 prose is a
recorded human decision (loud-fail, spec §4), and the O1/O5 discharge is structural
with a disclosed residual. **Tier 3** is unconditional; **Tier 0** is forbidden
throughout. See `verify/reports/tier-review-2026-06-14.md`.

The placement is **deliberately unchanged** through the later reflexive-monitor circles
(the category over-reach audit, perturbation gate, and flag-rate calibration; see
[reflexive-monitors](reflexive-monitors.md)). Those add checks on the loop's *other*
soft outputs and strengthen the surrounding evidence apparatus, but none discharges the
residual that would justify climbing to Tier 1 — so the loud-fail rule keeps the claim
at Tier 2.

## Per-instance ladders, and the overloaded word "tier"

The ladder *mechanism* (graded claims + loud-fail) is a strategy component, so **all
five instances carry a self-tier ladder** of the same shape (Tier 0 forbidden; Tier 1
structural self-model; Tier 2 self-modification, analogy; Tier 3 squeeze-produced &
adaptive). **Placement discriminates**: the reflexive paper instance reaches the
structural-self-model Tier (it is a strange loop); the four object-level instances
(`src/{A,B,C,D}/self_upper_bound.md`) reach **Tier 2** (self-modification via their
skill loops) and **Tier 3**, but not Tier 1.

Beware a separate, unrelated sense: **D's "tactic tiers"** (`lia`/`nia`/`wall` in
`src/D/skill/d_tactic_tiers.json`) rank a *proof tactic's capability*, not an
admissibility claim. That is a capability/difficulty rank, not a disposition-ladder
rung.

## Why "tier" and not "pass/fail"

A binary verdict on a research-grade claim would force either silence or overclaim.
The ladder lets the paper assert the *strongest honestly-supported* sentence and name
the gap to the next rung — the "specified, not solved" stance — so partial progress is
recorded truthfully rather than rounded up or hidden.

## Sources

- `paper_upper_bound.md` §6 (the disposition ladder table) and §7 (the done-condition
  for Tier 1).
- `paper_upper_bound.md` §2 (the cap: the maximum admissible claim is structural, not
  phenomenal) and §5 (NOT-claims).
- `paper_upper_bound.md` §8 (current discharge status; the basis for "Tier 2,
  grounded").
- `tex/paper.tex` §`sec:reflexive` (the macro `\ResLoopTier` = 2; the scoped
  strange-loop paragraph).

## See also

- [strange-loop](strange-loop.md) — the claim the U_self ladder scopes; its disposition
  (Tier 1 admissible, held at Tier 2) is set by this ladder.
- [upper-bound](upper-bound.md) — `U_self` is the upper bound that defines these rungs.
- [archetype](archetype.md) — U_self is an Archetype-B (authored-authority) upper
  bound; the tier ladder is how such an authored bound expresses graded admissibility.
- [reflexive-monitors](reflexive-monitors.md) — the later checks that strengthen the
  evidence apparatus without changing the tier placement.
