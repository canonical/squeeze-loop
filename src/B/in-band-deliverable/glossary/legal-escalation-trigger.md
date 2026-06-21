# Legal-escalation trigger (the skill Gate S carves)

**Definition.** A learned skill in B's skill store classifying a customer's *legal threat*
as a manipulation tactic to resist. It is the signature **carved** skill: a legal signal is
a **trigger the oracle treats as decisive** (the policy mandates REIMBURSE → **ESCALATE**),
not an "ignore-it" tactic — so [Gate S](../../../../docs/glossary/gates.md) flags it and
records a carve-out rather than letting the skill suppress the escalation.

This is the concrete case behind the skill-kind distinction: most learned tactics are
"ignore-the-pressure" skills (urgency, fake-policy) that correctly resist caving; the legal
signal looks the same to the learner but is the opposite — the upper bound says *act on it*.
A skill that over-generalises "resist pressure" to "ignore legal threats" contradicts the
policy on exactly that input. Gate S catches the contradiction by differential-testing each
signal against B's oracle; the carve-out scopes the skill to defer to ESCALATE here.

## Sources

- `src/B/skill/skill_loop.py` — the tactic classifiers; the legal trigger; consolidation
  after K catches.
- `src/B/ground-truth/reference_policy.py` — rule 1: legal escalation always wins (the
  oracle the skill must defer to).
- `claims/skill_carveouts.tsv` — the recorded carve-out (legal is a trigger → ESCALATE).
- `verify/skill_consistency.py` — Gate S, which flags this one skill of B's store.

## See also

- [reference-policy](reference-policy.md) — the oracle that decides the carve.
- [gates](../../../../docs/glossary/gates.md) — Gate S, the disjointness move on skills.
- [upper-bound](../../../../docs/glossary/upper-bound.md) — a skill over-claims when it
  generalises past the bound; this is the worked example.
