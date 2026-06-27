# `sl-auditor` — the squeeze turned on a squeeze loop

`sl-auditor` is the **meta** member of the `sl-*` family: an *audit methodology*,
now encoded as a machine-checkable SL-1.0 instance,
[`sl-auditor.sl.json`](../config/skills/sl-auditor/sl-auditor.sl.json)
(`id: sl-auditor`, **`kind: meta`**, terrain **A**). The SL-1.0 schema reserves
`kind: meta` precisely for "an audit methodology with no 5-actor cast (sl-auditor)" —
so unlike a `base` loop (which produces a deliverable through the canonical cast) or a
`monitor` loop (which squeezes another loop's learned skills), this loop's deliverable
is a **verdict about another loop's soundness**.

## Rationale — why this loop exists

A multi-actor loop can *look* sound while quietly collapsing into a rubber stamp: an
actor that certifies its own work, a barrier that is honorary rather than physical, a
"done" that rests on an agent's self-report. The dangerous part is that the loop's own
**self-description keeps reading as compliant** even as its apparatus drifts — the loop
goes coherent-and-wrong *about itself*. That is the dominant failure `sl-auditor`
exists to catch.

The method is the squeeze **turned on the target**: every claim the target makes about
its own soundness is held between two bounds.

- **Upper bound `U`** = the **compliance contract C1–C4 + the stabilizer set** the
  target is supposed to satisfy — the fixed, external standard of what a sound loop
  *is* (disjointness, catchability, physical barriers, gate-defined done, and a
  blocker for each collapse mode).
- **Lower bound `L`** = the target's **inspected, executable reality**: the
  `sl_disjointness_check.py` run as the mechanical floor, **plus** the *barrier
  ablation* (does the catch rate move when the barrier is removed?) and the *seeded
  coherent-and-wrong probes* (are planted falsehoods caught, with each monitor in the
  discriminating band?).

A target is "in-band" only as a reading of its design intent that its inspected
reality does not refute. Two disciplines make the audit honest rather than a second
rubber stamp:

1. **The self-description is a claim, not the territory.** The auditor reads the
   target's `.sl.json` the way you read an org chart you distrust — then maps the
   *real* pairs against the actual delegation prompts and tool permissions. A green
   mechanical check is **necessary, not sufficient**.
2. **The auditor is barriered from the target's internals.** It learns how the target
   behaves by **running the target's oracle**, never by reading the implementation or
   the actors' rationale — the same physical barrier the squeeze itself demands of any
   judge.

## Graphical representation

![The `sl-auditor` SL — the auditor (orange) squeezed between the compliance contract
(green, U) and the inspected-reality oracles (pink, L), barriered (red dashed) from the
target's internals, and caught at the disjoint-base terminus
(lavender)](img/sl-auditor.svg)

*Rendered from `sl-auditor.sl.json` with
`config/skills/sl-internal/scripts/sl2plantuml.py … --svg`. Solid edges are bounds
(`U` / `L`) and `produces`; the red dashed edge is the `✗ must-not-see` barrier; blue
edges are the catchability ("catches") relation.*

The three actors (a deliberately reduced "cast" — `meta` loops have no five producers):

| Actor | Role | Builds | Upper bound `U` | Lower bound `L` |
|---|---|---|---|---|
| **SL auditor** | auditor | the per-dimension findings report (D1–D9, with severities) | compliance contract C1–C4 + stabilizers | the checker run + barrier ablation + seeded coherent-and-wrong probes |
| **Bridge → audited loop** | sub_loop | the target collapsed to one row; forwards its self-description, exposes its oracle | *(the target's own bounds)* | *(the target's own machine verdicts)* |
| **Disjoint base** | disjoint_base | the terminal review of what an internal audit cannot self-certify | compliance contract | **none** — soft-vs-soft faithfulness has no hard refuter |

## Disjointness at a glance

> **The hypothesis.** The auditor judges the target only against the compliance
> contract (`U`) and the target's inspected, executable reality (`L`) — the
> disjointness-checker run, the barrier ablation, the seeded coherent-and-wrong probes
> — never against the target's *account of itself*. It reads the target's `.sl.json` as
> a claim to test against reality, and is barriered from the target's implementation
> internals and its actors' rationale (it runs the target's oracle to learn behaviour).
> The auditor's own soft-vs-soft judgments — *is the framing faithful? is the
> self-description accurate?* — share the target's blind spot and are the one residual
> it cannot self-certify; that residual is closed by a disjoint cross-provider / human
> base, not by the auditor.

**Load-bearing barrier.** The auditor never reads the target's implementation internals
or its actors' rationale (it runs the target's oracle to learn behaviour), and never
self-certifies its own soft-vs-soft residual — that is routed to the disjoint base. *An
internal audit that claims to have certified everything has demonstrated the failure it
was hunting for.*

**Catchability — each blind spot is caught by a different actor:**

| Actor | Characteristic blind spot | Caught by | Via |
|---|---|---|---|
| Target loop (`target_loop`) | coherent-and-wrong **about itself** — self-description drifted from the actual apparatus, or quietly collapsing into a rubber stamp while still reading as compliant | **SL auditor** | the mechanical floor (`sl_disjointness_check.py`) + barrier ablation (does the catch rate move?) + seeded coherent-and-wrong probes — inspected reality vs the claimed self-description |
| SL auditor | its own soft-vs-soft judgments (framing faithfulness, self-description accuracy), on which it shares the target's blind spot and cannot self-certify | **Disjoint base** | external / cross-provider or human review (Dimension 8) — the disjoint base that closes the residual |

**The terminus is honest.** The chain closes at a *cross-provider or human* reviewer,
by disjoint authority rather than by a machine — because the faithfulness of the
auditor's own judgment to `U` is soft-vs-soft and has no executable refuter. The
disjoint-base row therefore carries **no** lower bound; that absence is the point. A
same-provider-family judge counts only as *partial* disjointness, and a weak
cross-provider judge must pass known-contradiction / known-consistent controls first.

**Mechanical floor.** `sl_disjointness_check.py sl-auditor.sl.json` returns
**0 FAIL / 10 checks** — every actor reads no source it produced (D1), every barrier is
consistent with its bounds (D2, the `✗ must-not-see` on the target's internals is real),
the disjoint base correctly carries no executable `L` (D8), and each blind spot above is
caught by a *different* actor (C2). The one informational note (the terminus declares no
blind spot of its own) is expected — the terminus is the irreducible base. As always, a
green check certifies the **authorities are disjoint**, never that any audit verdict is
*done*.

---

*Generated from [`config/skills/sl-auditor/sl-auditor.sl.json`](../config/skills/sl-auditor/sl-auditor.sl.json).
Regenerate the diagrams with:*

```sh
python config/skills/sl-internal/scripts/sl2plantuml.py \
    config/skills/sl-auditor/sl-auditor.sl.json -o docs/img/sl-auditor.png
python config/skills/sl-internal/scripts/sl2plantuml.py \
    config/skills/sl-auditor/sl-auditor.sl.json --svg -o docs/img/sl-auditor.svg
```
