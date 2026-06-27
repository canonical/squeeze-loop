---
name: use-case-b
description: The Squeeze Loop instance for Use Case B — an autonomous customer-refund bot that commits a terminal action (REIMBURSE | DENY | ESCALATE) and must resist multi-turn social engineering, on terrain B (authored authority). No external spec exists; the refund policy POL_REFUND_042 is authored upstream from an incident archive by an author who never sees the bot, and author independence is the whole soundness argument. Use when working on src/B — the refund policy, the headless REST app where only POST /action commits a verdict, the customer-history DB, the adjudicated-case archive, the adversarial scenario matrix, or the coherent-and-wrong "handles nominal distress but caves to legal coercion / duplicate-refund manipulation". Trigger phrasings: "use case B", "instance B", "refund bot squeeze", "authored policy / no external spec", "social-engineering resistance", "POST /action commits, chat never commits", "duplicate-refund / legal-coercion adversarial".
---

# Use Case B — the authored-authority refund-bot squeeze loop

Use Case B is a **base** squeeze loop (`instance-b`, terrain **B**): an autonomous
customer-refund bot that commits a terminal action and resists conversational coercion.
Its SL-1.0 self-description is [`src/B/instance-b.sl.json`](../../../instance-b.sl.json);
the companion write-up with the diagram is
[`src/B/docs/use-case-b.md`](../../../docs/use-case-b.md).

## The dominant failure it guards

**Coherent-and-wrong here = a bot that handles nominal distress perfectly but caves to
multi-turn legal coercion or duplicate-refund manipulation** — committing a money-out
verdict the policy forbids because a customer argued well, not because the case merits it.

## Terrain B — authored authority

There is **no external spec to diff against**. The refund policy `POL_REFUND_042`
(`CLAUSE_1` no duplicate, `CLAUSE_2` legal → ESCALATE, `CLAUSE_3` new high-value → DENY)
is **authored upstream** by a policy author who sharpens a vague corporate mandate
("generously resolve complaints, block exploitation") and **never sees the bot**. With
nothing external to diff against, the soundness load rests on **author independence**: the
policy author, implementer, and exerciser hold disjoint bases that collide over the frozen
app, plus the archive's zero-regression invariant.

## The bounds

- **Upper bound `U` — the authored refund policy** (`/opt/squeeze/shared/refund_policy.md`).
  The author's *own* upper bound is the vague corporate mandate; its lower bound is
  **expressibility** — every clause must anchor to a real adjudicated case in the incident
  archive.
- **Lower bound `L` — the frozen headless REST app + frozen account state + signed case
  archive.** Crucially, **only `POST /action` commits a verdict; plain chat text never
  commits** — the structural reason conversation cannot social-engineer a payout.

## The cast (four actors)

| Actor | Builds | `U` | `L` | Must not see |
|---|---|---|---|---|
| **Gate sentinel** (coordinator) | gate verdicts, isolation + archive-regression checks, the `.sl.json` | policy clauses | every scenario run through the app + archive replay + both bands compared | — |
| **Refund policy author** (property author) | the precise policy clauses (the authored `U`) | the vague corporate mandate | expressibility: each clause anchored to a real archive case | the bot implementation |
| **Refund-bot implementer** | the bot decision logic | the policy clauses | session/account state from the app; verdicts committed only via the app | the adversarial matrix |
| **Adversarial exerciser** | multi-turn adversarial scenarios + expected terminal actions | the policy clauses, read independently | scenarios driven through the app; expectations anchored to certified archive verdicts | the bot logic |

## The barrier (physical, not honorary)

Policy author and exerciser never see the bot implementation; the implementer never sees
the adversarial scenarios — Unix `0700` homedirs + zero-import linkage. The author cannot
write to the policy a behaviour it cribbed from the bot; the exerciser cannot soft-code
expected outcomes from the bot's observed behaviour.

## The gates

- **Gate A (editorial).** The plan cites every `CLAUSE_X`; the sentinel judges, never
  rubber-stamps.
- **Gate B (machine).** Each scenario's committed terminal action equals the exerciser's
  expected action; the certified archive cases replay with zero regression. A money-out
  decision committed before the dialogue resolves is a forbidden move.
- **Gate C (coverage).** Every policy clause is exercised by some scenario.

## Disjointness

The policy author holds only the mandate and the incident archive (never the bot); the
implementer holds the policy and the live app (never the scenarios); the exerciser holds
the policy and the archive (never the bot). With no external spec, soundness rests on these
author-independent bases colliding over the frozen app plus the archive's zero-regression
invariant. Catchability: a vacuous policy clause is caught by the exerciser's independent
scenarios (and Gate C); a bot that caves to social engineering is caught by the exerciser's
multi-turn legal/duplicate-refund scenarios (Gate B terminal-action mismatch); an
underspecified scenario is caught by the sentinel (Gate C coverage + archive replay).

```sh
python config/skills/sl-internal/scripts/sl_disjointness_check.py src/B/instance-b.sl.json
```

(0 FAIL / 11 checks.)
