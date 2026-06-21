# Strange loop

**Definition.** Douglas Hofstadter's term for a self-referential, level-crossing,
self-categorizing loop whose levels cross back to their origin — the *structural form
of an "I."* In this project it names what the squeeze loop becomes when **applied to
its own construction**: the method's output includes a verification of the method, and
resolving the squeeze on itself forces new distinctions into existence.

The claim is **scoped and bounded**. The maximum admissible reading is **structural,
not phenomenal**: that the construction instantiates the *form* of a strange loop. It
is explicitly **not** a claim of consciousness, experience, or qualia (Tier 0,
forbidden). The bound is `paper_upper_bound.md` (`U_self`).

## Obligation clauses (what a structural strange loop must exhibit)

O1 endogenous self-symbol · O2 level-crossing with downward causation · O3 closure
(the path returns to origin) · O4 self-referential categorization (the crux) ·
O5 persistence (a self-model updated across iterations). Falsification tests N1–N3
keep the criteria strong enough to reject mere feedback (video-on-monitor) and
self-reference without categorization (a quine, a self-hosting compiler).

## Current standing

All of O1–O5 are discharged (O1/O5 structurally, via a derived self-model;
O2/O3/O4 via the level-crossing log, the executed closure check, and the per-circle
category-generation log). By the disposition ladder ([tier](tier.md)) **Tier 1 is
therefore admissible, but the paper deliberately holds at Tier 2** (a recorded human
decision under the loud-fail rule). Tier 0 remains forbidden.

The criterion **discriminates**: only the reflexive paper instance reaches the
structural-self-model tier; the four object-level instances (A/B/C/D) self-modify but
do not model themselves (`src/<X>/self_upper_bound.md`).

## Generativity, scoped — and the claim routed, not self-certified

The "forces new distinctions into existence" reading (the O4 crux) is itself held to
the strategy's own discipline. The categories the loop generated while squeezing itself
were **audited for over-reach** ([reflexive-monitors](reflexive-monitors.md),
`verify/category_overreach.py`): 3 of the 4 generalise across all four object-level
instances and the one that does not (the gate-independence limit) is carved to the
reflexive instance — so the generativity is borne out where it can be checked, not
asserted wholesale. And because a self-monitor shares the authoring blind spot, the
strange-loop reading is an **interpretive** claim that the reflexive Gate~S
(`verify/reflexive_gate_s.py`) **routes to a disjoint base** (re-run instances /
external review) rather than self-certifying. The entry records a structural claim the
loop forwards for independent check; it does not certify itself.

## Sources

- `paper_upper_bound.md` (`U_self`): the cap, clauses O1–O5, tests N1–N3, the tier
  ladder, and §8 discharge status.
- `tex/paper.tex` §`sec:reflexive`: the scoped strange-loop paragraph; `\ResLoopTier`.
- `claims/level_crossings.tsv`, `claims/category_generation_log.tsv`,
  `verify/closure_check.py`, `verify/self_model.py` (the O1–O5 discharges).

## See also

- [tier](tier.md) — the disposition ladder the strange-loop claim is scoped on.
- [squeeze-loop](squeeze-loop.md) — what becomes a strange loop when self-applied.
- [upper-bound](upper-bound.md) — `U_self`, the bound that caps this claim to its form.
- [gates](gates.md) — reflexive Gate S, which routes this interpretive claim to a
  disjoint base rather than self-certifying it.
- [reflexive-monitors](reflexive-monitors.md) — the over-reach audit that scopes the
  generativity (O4) claim.
