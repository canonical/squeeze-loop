# `sl-monitoring-sl` — a squeeze loop that monitors a squeeze loop

This skill is the one member of the `sl-*` family that is itself an **SL instance**:
it ships a machine-checkable SL-1.0 self-description,
[`monitor-loop.sl.json`](../config/skills/sl-monitoring-sl/monitor-loop.sl.json)
(`id: monitor-loop`, `kind: monitor`, terrain **B**). The other `sl-*` skills are
*about* squeeze loops but are not encoded instances — `sl-internal` is the theory
and the SL-1.0 schema, `sl-builder` is a build methodology, `sl-auditor` is an audit
methodology with no five-actor cast — so they carry no `.sl.json` and have no diagram
to show.

## Rationale — why this loop exists

Every squeeze loop accumulates **skills**: soft, learned heuristics that a deciding
actor consolidates to avoid repeating a class of caught error. A skill is not the
spec and not the oracle — it is an actor's compressed memory of its own failures, and
that makes it dangerous in two ways:

1. **It is learned from one signal.** The deciding actor only ever consolidates
   skills from the errors *it was caught making*, so its skills over-generalize in
   the one direction that signal points.
2. **Its producer cannot audit it.** The same blind spot that produced an
   over-general skill prevents the producer from seeing the over-generalization. An
   actor checking its own skill is exactly the self-judging the squeeze forbids.

So a consolidated skill can be **coherent-and-wrong**: it reads as sound advice and is
right on most inputs, yet on some reachable input it prescribes an action the upper
bound overrides. The dominant failures this loop guards are therefore (a) an
**over-generalized skill** — right on the common case, silently wrong on a governed
exception — and (b) a **mis-calibrated monitor** that either rubber-stamps (flags
nothing) or saturates (flags everything).

The fix is to apply the disjointness principle **to skills**: a skill is in-band only
if it is a reading the bounds do not refute on any reachable input, and — because the
skill's producer shares the skill's blind spot — that check must be performed by a
**different actor whose evidence base is the base loop's `U` and `L`**, never the
deciding actor's own reasoning. The monitor is itself a squeeze: its upper bound *is*
the base loop's `U` (the spec the skill must not contradict), its lower bound *is* the
base loop's `L` (the executable oracle, used as a differential-testing comparator), and
its forbidden move is reading the producer's rationale. Gate S returns one of three
verdicts — **PASS**, **CARVE-OUT** (a narrowing exception cited to the clause of `U` it
defers to), or **REJECT** (loud-fail).

The barrier is made physical by **running the observed base loop as a sub-agent**: its
reasoning and oracle runs live and die in the sub-agent's context, and only its *soft
outputs* (the consolidated skill) cross back. The monitor literally cannot read the
rationale, so it cannot judge against it — the sub-agent boundary *is* the barrier.

## Graphical representation

![The `monitor-loop` SL — actors (orange), upper-bound material (green), executable
oracle (pink), artifacts (grey), must-not-see rationale (red), human terminus
(lavender)](img/monitor-loop.svg)

*Rendered from `monitor-loop.sl.json` with
`config/skills/sl-internal/scripts/sl2plantuml.py … --svg`. Solid edges are bounds
(`U` / `L`) and `produces`; red dashed edges are the `✗ must-not-see` barriers; blue
edges are the catchability ("catches") relation.*

The four actors:

| Actor | Role | Builds | Upper bound `U` | Lower bound `L` |
|---|---|---|---|---|
| **Monitor-loop coordinator** | coordinator | the Gate S handshake, verdict ledger, flag-rate calibration, and this `.sl.json` | base loop's `U` | base `L` + the emitted verdicts |
| **Skill monitor (Gate S)** | monitor | the per-skill verdict (trigger test / validity test) | base loop's `U` | base loop's `L` (differential comparator) |
| **Bridge → observed base loop** | sub_loop | the base loop collapsed to one row; returns only its soft outputs | *(the base loop's own bounds)* | *(the base loop's machine verdict, returned)* |
| **External / human reviewer** | human_terminus | the terminal judgment that closes the coordinator's editorial soft side | base loop's `U` | **none** — soft-vs-soft faithfulness has no hard refuter |

## Disjointness at a glance

> **The hypothesis.** The monitor holds the base loop's `U` and `L` — a *disjoint*
> evidence base from the deciding actor, which holds only "what I was caught doing." The
> carve-out that repairs an over-general skill can only be derived by the actor holding
> `U` and `L`, never by the skill's producer. The base loop runs as a sub-agent so its
> rationale is **physically absent** from the monitor's context — the `must_not_see` on
> `producer_rationale` is real, not honorary. The coordinator's editorial judgment is the
> one soft-side hole, and it is closed by *disjoint authority* at the human-reviewer
> terminus, not mechanically.

**Load-bearing barrier.** The monitor and coordinator never see the producer's
rationale (it never leaves the sub-agent); they judge the skill **only** against the
base loop's `U` and `L`. This is the no-blend rule pushed down one level: a soft
*skill* may never silently stand in for the soft-but-authoritative *upper bound*.

**Catchability — each blind spot is caught by a different actor:**

| Actor | Characteristic blind spot | Caught by | Via |
|---|---|---|---|
| Base loop (`sub_base`) | emits a coherent-and-wrong skill — over-generalized, right on the common case, silently wrong on a governed exception | **Skill monitor** | the trigger test (perturb the ignored signal, watch `L`'s verdict move) or validity test |
| Skill monitor | mis-calibration — rubber-stamping (flags nothing) or saturating (flags everything) | **Coordinator** | flag-rate calibration: a healthy monitor *discriminates*, leaving defer-to-oracle skills untouched and flagging only over-reaching ignore-signal skills |
| Coordinator | its own un-squeezed editorial judgment of whether a carve-out is faithful to the base loop's `U` | **Human reviewer** | external / human review — the terminus that closes the soft side |

**The terminus is honest.** The chain closes at a *human / external* reviewer, by
disjoint authority rather than by a machine — because the faithfulness of a carve-out to
`U` is soft-vs-soft and has no executable refuter. The human-terminus row therefore
carries **no** lower bound; that absence is the point. A claim that the automation alone
closed the soft side would itself be the coherent-and-wrong failure this loop exists to
catch.

**Mechanical floor.** `sl_disjointness_check.py monitor-loop.sl.json` returns
**0 FAIL / 13 checks** — every actor reads no source it produced (D1), every barrier is
consistent with its bounds (D2), the human terminus correctly carries no executable `L`
(D8), and each blind spot above is caught by a *different* actor (C2). The one
informational note (the human terminus declares no blind spot of its own) is expected:
the terminus is the irreducible base, so nothing inside the loop squeezes it. A green
check certifies the **authorities are disjoint** — never that any skill verdict is
*done*; that lives in the Gate S evidence, not the registry.

---

*Generated from [`config/skills/sl-monitoring-sl/monitor-loop.sl.json`](../config/skills/sl-monitoring-sl/monitor-loop.sl.json).
Regenerate the diagram with:*

```sh
python config/skills/sl-internal/scripts/sl2plantuml.py \
    config/skills/sl-monitoring-sl/monitor-loop.sl.json --svg -o docs/img/monitor-loop.svg
```
