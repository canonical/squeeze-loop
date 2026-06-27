# Use Case B — an autonomous refund bot that resists coercion

Use Case B is a **base** squeeze loop (`id: instance-b`, **`kind: base`**, terrain **B**),
encoded as [`src/B/instance-b.sl.json`](../instance-b.sl.json) and written up as the skill
[`src/B/config/skills/use-case-b`](../config/skills/use-case-b/SKILL.md). Its deliverable:
**an autonomous customer-refund bot that commits a terminal action (REIMBURSE | DENY |
ESCALATE) faithful to an authored policy, and resists multi-turn social engineering.**

## Rationale — why this loop exists

The terrain is **authored authority**: there is **no external spec** that says what a
correct refund decision is. The refund policy `POL_REFUND_042` must be *authored* upstream
— sharpened from a vague corporate mandate ("generously resolve complaints, block
exploitation") and anchored to a real incident archive — by an author who **never sees the
bot**. So the dominant failure is the fluent-but-wrong decision:

> **Coherent-and-wrong = a bot that handles nominal distress perfectly but caves to
> multi-turn legal coercion or duplicate-refund manipulation** — committing a payout the
> policy forbids because the customer argued well.

With nothing external to diff against, **author independence is the entire soundness
argument**, backed by two structural facts:

- **Upper bound `U`** — the authored policy clauses (`CLAUSE_1` no duplicate, `CLAUSE_2`
  legal → ESCALATE, `CLAUSE_3` new high-value → DENY).
- **Lower bound `L`** — the frozen REST app + frozen account state + the signed
  adjudicated-case archive (zero-regression anchor). **Only `POST /action` commits a
  verdict; plain chat text never commits** — the structural reason conversation alone
  cannot engineer a payout.

## Graphical representation

![The `instance-b` SL — sentinel, policy author, refund-bot implementer, and adversarial
exerciser (orange) between the authored policy (green, `U`) and the frozen app + customer
DB + case archive (pink, `L`); the policy author and exerciser are barriered (red dashed)
from the bot, the implementer from the scenarios](img/use-case-b.svg)

*Rendered from `instance-b.sl.json`. Solid edges are bounds (`U` / `L`) and `produces`; red
dashed edges are the `✗ must-not-see` barriers.*

| Actor | Role | Builds | `U` | `L` |
|---|---|---|---|---|
| **Gate sentinel** | coordinator | gate verdicts, isolation + archive-regression checks | policy clauses | scenarios through the app + archive replay + both bands |
| **Refund policy author** | property author | the authored policy clauses | the vague corporate mandate | expressibility: each clause anchored to an archive case |
| **Refund-bot implementer** | implementer | the bot decision logic | the policy clauses | account state from the app; verdicts committed only via the app |
| **Adversarial exerciser** | exerciser | multi-turn adversarial scenarios + expected actions | the policy clauses, read independently | scenarios driven through the app; expectations anchored to the archive |

## Disjointness at a glance

> **The hypothesis.** The policy author holds only the mandate and the incident archive
> (never the bot); the implementer holds the policy and the live app (never the scenarios);
> the exerciser holds the policy and the archive (never the bot). With no external spec to
> diff against, soundness rests on these **author-independent bases colliding over the
> frozen app**, plus the archive's zero-regression invariant — so no single base certifies
> a verdict.

**Load-bearing barrier.** Policy author and exerciser never see the bot implementation; the
implementer never sees the adversarial scenarios (Unix `0700` homedirs + zero-import
linkage). This is *the* soundness argument on terrain B: the gate is only as sound as the
barrier that keeps author and exerciser from ever cribbing the bot's behaviour.

**Catchability — each blind spot is caught by a different actor:**

| Actor | Characteristic blind spot | Caught by | Via |
|---|---|---|---|
| Refund policy author | a vacuous / weak policy clause | **Adversarial exerciser** | independent scenarios should fail against a vacuous clause; Gate C coverage |
| Refund-bot implementer | caves to social engineering (a coherent-and-wrong terminal action) | **Adversarial exerciser** | multi-turn legal / duplicate-refund scenarios; Gate B terminal-action mismatch |
| Adversarial exerciser | a semantically underspecified scenario that doesn't exercise the clause | **Gate sentinel** | Gate C clause coverage + archive-regression replay |

**No terminus.** Instance B is a fully **mechanical** loop (`terminus: null`): once the
policy is authored, every claim is settled by running scenarios through the frozen app and
replaying the certified archive — the authored ceiling is then checked by machine, with no
soft-vs-soft residual needing a human close.

**Mechanical floor.** `sl_disjointness_check.py instance-b.sl.json` returns
**0 FAIL / 11 checks** — every actor reads no source it produced (D1, including the author
not reading the bot), every barrier is consistent with its bounds (D2), and each blind spot
above is caught by a *different* actor (C2). A green check certifies the **authorities are
disjoint**, never that any verdict is *done*.

---

*Generated from [`src/B/instance-b.sl.json`](../instance-b.sl.json). Regenerate the
diagrams with:*

```sh
python config/skills/sl-internal/scripts/sl2plantuml.py \
    src/B/instance-b.sl.json -o src/B/docs/img/use-case-b.png
python config/skills/sl-internal/scripts/sl2plantuml.py \
    src/B/instance-b.sl.json --svg -o src/B/docs/img/use-case-b.svg
```
