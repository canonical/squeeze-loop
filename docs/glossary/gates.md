# Gates (A / B / C / S / reflexive S)

**Definition.** A *gate* is a checkpoint that decides whether an item is **done** —
by machine output or the coordinator's editorial judgment, **never by an actor's
self-report** (compliance condition C4). Each work item flows through the per-item
pipeline **Gate A → Gate B → Gate C**; **Gate S** is a later, recursive addition that
audits a loop's *accumulated skills*; **reflexive Gate S** turns that same audit on the
paper loop's *own* claims.

| Gate | What it checks | Kind | Catches |
|------|----------------|------|---------|
| **A** — editorial approval | The plan/property against the **upper bound**, before any source edit. The coordinator judges, amends, cuts, or sharpens (never a binary stamp); no edit happens from a `DRAFT`. | **Editorial** (human judgment, not machine output) | The aspirational/undischargeable claim; the rubber-stamp approval. |
| **B** — machine-checked acceptance | Positives pass; every negative **fails at the named site violating the named clause**; the **standing invariant** (e.g. total additivity / determinism re-run) is green after *every* item; each escape hatch is classified. | **Machine** | Broken implementations, vacuous negatives, silent regressions. |
| **C** — coverage / no-blend guard | Each obligation clause maps to a **specific passing check**, and the thing actually proved **is** the property intended. Machine-checked where external ground truth exists; defended by **author independence** where it does not. | **Machine** (or independence-defended) | **Coherent-and-wrong**; plane-**blending** (one plane's weak check standing in for the other's strong claim). |
| **S** — skill↔upper-bound consistency | A *monitor squeeze* audits a loop's **accumulated skills** against that loop's own upper bound + executable oracle, from a **disjoint evidence base** (not the deciding agent's rationale). Verdicts: PASS / CARVE-OUT / REJECT. The check is matched to the skill kind (trigger / fork / membership / discharge) and run over the level-up pools. | **Machine** (deterministic) | Over-generalised or spurious **learned skills** — a coherent-and-wrong *skill* that contradicts the upper bound on some input. |
| **reflexive S** — Gate S on the paper's own claims | Gate S turned on the paper loop's *own* soft outputs (`claims/ledger.tsv`). It **classifies** each claim (evidence-bound CITE/RESULT vs interpretive OPN/DEFN + framing), **checks coverage** (no bare claim; every OPN marked open/hedged), and **routes** the interpretive/high-risk claims to a *disjoint* base — re-run on the executable instances, or external review — rather than self-certifying them. | **Machine** (classifier/router; deterministic) | Bare or unhedged claims (hard-fail); and, by routing not stamping, the **self-judging** of the paper's own interpretive/over-general claims. |

## Scope and status of each

- **A, B, C** are the **per-item gates**, defined and used throughout the manuscript
  (`sec:mechanics`, `fig:pipeline`). They structure every work item.
- **S is now first-class** in the manuscript's gate vocabulary: **named and defined in
  `sec:mechanics`** (circle 71) as a gate on a *different cadence* — it fires when the
  loop *accumulates* a learned skill, not per work item — and named again at its
  deterministic demonstration in `sec:eval`. It is the **squeeze pattern applied
  recursively**: a squeeze monitoring a squeeze's own learned outputs (the no-blend rule
  + disjointness pushed down one level). Its runnable form is
  `verify/skill_consistency.py`; the generic pattern is `config/skills/sl-monitoring-sl/`
  and the design rationale is `paper-monitoring-sub-skill.md`.
- **Reflexive Gate S** applies S to the paper loop itself — because the paper loop *is*
  a squeeze loop, its own ledger claims can over-generalise like a use case's skills.
  Crucially it observes the honesty limit a producer cannot dodge (a self-monitor shares
  its own blind spot): it **routes** interpretive claims to a *disjoint* base (the
  executable instances + external review) and **never self-certifies** them. Runnable
  form: `verify/reflexive_gate_s.py` (a reflexive-squeeze step); rationale in
  `self-improve.md`. On the current ledger it classifies the claims (most evidence-bound,
  a handful interpretive), confirms coverage, and routes the interpretive ones for
  disjoint review. Reflexive Gate S audits the paper's *claims*; the same move on the
  paper's **other** soft outputs (generated categories, citation/result anchors, the
  monitors' own flag-rates) is the [reflexive-monitors](reflexive-monitors.md) family.

## A naming caution

"Gate A/B/C" is **overloaded across two contexts** (like [tier](tier.md)):

- the **per-item strategy gates** above (the generic pattern), and
- the **paper-impl meta-gates** for producing this paper, where the same letters carry
  adapted meanings (Gate A = editorial plan approval; Gate B = build green + every
  `\cite` has a reading record + orphan-claim scan; Gate C = re-derive every ledger
  claim from raw ground truth / ledger↔macro reconciliation in `gate_checks.py`).

They share the *spirit* (A editorial, B mechanical acceptance, C coverage/re-derivation)
but not the literal checks. Read the gate against its context.

## Sources

- `tex/paper.tex` §`sec:mechanics` + `fig:pipeline` (Gate A/B/C definitions and the
  per-item pipeline); §`sec:strategy` (C4, gate-defined done).
- `paper-impl.md` §4 (the paper-impl meta-gates A/B/C).
- `tex/paper.tex` §`sec:mechanics` (Gate S named + defined, circle 71) and §`sec:eval`
  (its deterministic demonstration, `\ResGateS…`); `verify/skill_consistency.py`,
  `paper-monitoring-sub-skill.md`, `config/skills/sl-monitoring-sl/` (its runnable form,
  design rationale, and generic pattern).
- `verify/reflexive_gate_s.py` + `self-improve.md` (reflexive Gate S: Gate S on the
  paper's own claims, routing-not-self-certifying).

## See also

- [squeeze-loop](squeeze-loop.md) — gates are how "done" is defined (C4).
- [upper-bound](upper-bound.md) · [ground-truth](ground-truth.md) — what A/C/S check against.
- [tier](tier.md) — another term overloaded across the strategy vs paper-impl contexts.
- [reflexive-monitors](reflexive-monitors.md) — Gate S's move applied to the paper's
  other soft outputs (categories, anchors, the monitors themselves).
