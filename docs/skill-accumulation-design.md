# Design — skill accumulation: how the squeeze forces new-concept creation

> Design note, not yet implemented. It records the mechanism and the operating
> rules so they are not lost amid the U_self / strange-loop additions. It advances
> two U_self (`paper_upper_bound.md`) clauses directly: **O1** (a live self-model the
> loop consults to act) and **O4** (categories the loop generates and re-applies).
> It is also the step that turns the current *fixed-actor* diversity apparatus into a
> *learning* one — the missing piece behind the "per-model error gradient" left as
> future work in `10-cycles-after-level-up.md` and the OPN claim CLM-073.

## The mechanism

The squeeze forces new-concept creation because a designated agent, held between an
authority it cannot exceed and a ground truth it cannot alter with no role-crossing
escape, must **invent a new distinction to resolve the impasse**. We make that
operational: the agent **reflects on what happened and stores the result as a
skill** — a persistent, accumulating store the agent reads on later tasks and
writes to when it learns. The skill store IS the live self-model (O1); each stored
distinction is a generated category (O4); progress across tasks is the trial the
fixed actor could not produce.

## Rule 1 — only the deciding agent accumulates a skill (use case B)

In each squeeze, **only the agent that takes the decision** (the implementer / the
bot) reflects and saves a skill. The other actors — the exerciser, the
policy/answer-key, the gates — stay **fixed**.

*Why:* if every actor improved together, the differential the squeeze exists to
expose would not move, and the effect would be invisible. Keeping the exerciser and
the authority fixed is what makes the deciding agent's progress *measurable* — and
is where the "beauty" of the squeeze shows: the constrained agent is forced to
create the right concept to stay in-band, against an independent oracle that does
not drift to meet it.

## Rule 2 — the ledger must be progressive; change it if a wall is hit (use case D)

The exercise ledger must be **graded finely enough that the agent keeps making
progress**. If the exercises jump too far, the agent **hits a wall and stops
progressing** — and the experiment learns nothing past that point.

Operating rule: **do not hesitate to change the exercises (the ledger contents)
when a wall is hit** — re-grade, interpolate, or swap exercises so the next rung is
within reach of the agent's current skill. The ledger is mutable run-state in
service of keeping the agent in its zone of progress.

*Deferred — the conceptual leap.* When an agent is genuinely blocked (no
interpolation helps), the principled move is a **conceptual leap**: inject a new
capability the way one would add a math course on the blocking topic — a discrete
expansion of what the agent can do, not just an easier exercise. We name it here
but **do not implement it now**; for now, regrade/swap exercises (above).

## Gate S — skill ↔ upper-bound consistency (the carve-out)

Only the deciding agent learns (Rule 1), and it learns only from its own caught errors
— so its skills over-generalize and it cannot audit them (it shares their blind spot).
Therefore a consolidated skill enters the store only after **Gate S**, run by the
*paper / monitor loop* (a disjoint evidence base: the use case's upper bound + its
executable oracle), per `paper-monitoring-sub-skill.md` and the generic skill
`config/skills/sl-monitoring-sl/`.

Gate S (`verify/skill_consistency.py`) differential-tests each learned signal against
the use case's executable oracle — a base input vs base+signal. If the signal **changes
the oracle's verdict** it is a decision **trigger**, so a skill that treats it as noise
contradicts the upper bound and needs a **carve-out**: a narrowing exception that
defers to the oracle's mandated action on that signal. Carve-outs are recorded in
`claims/skill_carveouts.tsv`; the gate **loud-fails** if any trigger-contradiction has
no recorded carve-out. The monitor judges from the oracle only, never the deciding
agent's rationale (author separation). Implemented for **all four** use cases, each
with the check appropriate to its skill kind: B "ignore-signal" → trigger test
(oracle `reference_policy.decide`); A "use-certified-reading" → fork test (warehouse
intended vs naive); C "honor-clause" → membership in the conformance oracle; D
"use-tactic" → discharge in the kernel-verified `d_tactic_tiers.json`. **The criterion
discriminates**: only B needed a carve-out — its `legal` signal is a trigger
(REIMBURSE → ESCALATE), so the skill must defer to the upper bound (ESCALATE), not
merely "follow policy." A/C/D's skills all *defer to* their oracle and pass clean.

## Reset protocol (re-running the complete bench)

The skills are accumulated run-state. To re-run the complete benchmark, **drop the
created skills and start from the current situation** (the committed exercises /
ledger). The exercises and graders are the fixed substrate; only the learned skill
store is reset. This keeps a fresh bench reproducible while letting a live run
accumulate.

## What this changes (when built)

- A per-deciding-agent **skill store** artifact (read before a task, written after),
  consulted to act — discharging O1 and making O5's persistence a real updating
  self-model rather than a counter.
- A **skill/category log** (the existing `claims/category_ledger.tsv` is its static
  ancestor) recording each distinction the agent generated and where it re-applied
  it — O4 as accumulating evidence.
- A **mutable, progressive exercise ledger** with a wall-detector that triggers a
  regrade/swap (and, later, a conceptual leap).
- A **reset** that drops the skill store for a clean re-run.

## Scope / honesty

This is the live-agent step. It needs a real model in the deciding role (not the
fixed weak prover/bot/server of the current diversity pools). Until it is built and
run, the per-model gradient stays OPN (CLM-073 / the U_self Tier-1 path); this
document is the plan, not a result.
