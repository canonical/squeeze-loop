# Reflexive monitors (over-reach audit / perturbation gate / flag-rate calibration)

**Definition.** A *reflexive monitor* is a deterministic check that applies the
[Gate S](gates.md) move — the disjointness principle — to one of the **paper loop's
own soft outputs** *other than* its claim ledger. Where [reflexive Gate S](gates.md)
routes the paper's *claims*, these monitors audit the paper's *generated categories*,
its *citation/result anchors*, and *the monitors themselves*. Together with reflexive
Gate S they are the executable realization of `self-improve.md` (the lessons the paper
loop learned monitoring the object-level loops, turned back on itself).

| Monitor | Soft output audited | What it checks | Loud-fails on |
|---------|--------------------|----------------|---------------|
| **Category over-reach audit** | the four categories the loop *generated* while squeezing itself | For each (category, instance) an **objective artifact marker** tests whether the category generalises across the four object-level instances A/B/C/D. A category holding on all four **generalises**; a strict subset **over-reaches** and must be **carved**. | an **uncarved** over-reach (a category asserted generally that holds on a strict subset). |
| **Perturbation gate** | citation anchors (CITE) and sampling results (RESULT) | Anti-cherry-pick: a **comparative/strong citation** must trace to a `read:FULL` record (re-opened beyond the abstract); a **sampling result** must **vary across seeds** (≥2 distinct outcomes per seeded cycles). | a strong claim resting on a **non-FULL** record, or a sampling result that **does not vary** across seeds. |
| **Flag-rate calibration** | the monitors' own flag-rates, per circle | A healthy monitor **discriminates** — flags a *strict, nonempty* subset (0 < flagged < total): not zero (a rubber stamp), not all (saturation). Tracked **longitudinally** in an append-only history whose newest row is **anchored** to a live recomputation. | a **permanent rubber-stamp** or **saturated** plane; a **stale anchor** (history drifted from live); a **zero external-catch** count. |

## Why they form one family

All three are the **squeeze pattern pushed onto the paper's own non-claim outputs**, on
the same logic as Gate S: a producer shares its output's blind spot, so a soft output
(a learned skill, *or* a generated category, *or* a claim that rests on one passage)
needs a **disjoint** check holding the upper bound and an executable lower bound. The
honest limit Gate S cannot dodge is inherited verbatim — each monitor is a **forcing
function to route to a disjoint base** (the executable instances + external review),
never a substitute. The flag-rate monitor watches the watchers, so the apparatus does
not silently decay into a rubber stamp.

Each runs as a step in the **reflexive squeeze** (`execute_squeeze.py` STEPS) and emits
recomputed macros, so the numbers the manuscript cites are re-derived, never typed.

## Status

- **Category over-reach audit** — `verify/category_overreach.py` (circle 73). 3 of the
  4 generated categories generalise across all four instances; the gate-independence
  limit over-reaches (reflexive-only) and is carved in `claims/category_carveouts.tsv`.
- **Perturbation gate** — `verify/perturbation.py` (circle 77). 3/3 strong citations
  survive a full-text re-open; 4/4 instances vary across seeds. Realizes
  `self-improve.md` lesson #3 (differential testing over a pool, not a single anchor).
- **Flag-rate calibration** — `verify/flag_rate.py` + `claims/flag_rate_history.tsv`
  (circles 75–76). 3/3 monitoring planes discriminate; tracked across the recorded
  circles with the newest row anchored to a live recomputation. Realizes lesson #7.

## Sources

- `verify/category_overreach.py`, `claims/category_carveouts.tsv` — the over-reach audit.
- `verify/perturbation.py`, `tex/macros/perturb.tex` — the perturbation gate.
- `verify/flag_rate.py`, `claims/flag_rate_history.tsv`, `tex/macros/calibration.tex` —
  the calibration monitor and its trajectory.
- `tex/paper.tex` §`sec:reflexive` — where all three are reported (macro-bound figures).
- `self-improve.md` — the design rationale (lessons #3, #4, #7) and the honest limits.

## See also

- [gates](gates.md) — Gate S and **reflexive Gate S**, the same move on *skills* and on
  the paper's *claims*; these monitors extend it to the paper's other soft outputs.
- [squeeze-loop](squeeze-loop.md) — the pattern these monitors recursively apply.
- [strange-loop](strange-loop.md) — the loop carving categories it then audits on itself.
- [upper-bound](upper-bound.md) · [ground-truth](ground-truth.md) — the bounds each
  monitor holds its audited output between.
- [connective-tissue](connective-tissue.md) — a sibling reflexive-squeeze check (proxy +
  editorial), on the paper's prose *structure* rather than its claims.
