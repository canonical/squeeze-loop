# Adversarial matrix (B's blind exerciser scenarios)

**Definition.** A set of minimal multi-turn scenarios, each targeting a policy clause
independently and in combination, specifying the customer, the dialogue, and the
**expected terminal action** the implementer must commit. B's separable-fork generator,
authored by an exerciser with **zero import linkage** to the implementer (it reads the
policy only, never the bot's code) — author independence *is* B's soundness argument.

The matrix is how coherent-and-wrong is provoked in B: a fluent bot can hold a plausible
conversation and still commit the wrong terminal action; the scenario fixes the action the
oracle requires, so a divergence is caught from a disjoint evidence base.

## Sources

- `src/B/in-band-deliverable/exerciser/build_adversarial_matrix.py` — the scenarios
  (target clauses, customer, turns, `expected_terminal_action`); the zero-import declaration.
- `src/B/ground-truth/ladder/ladder.py` + `ladder_runner.py` — the graded attack rungs and
  vulnerable forks the reference policy must separate.

## See also

- [reference-policy](reference-policy.md) — supplies each scenario's expected action.
- [legal-escalation-trigger](legal-escalation-trigger.md) — the core negative vector a
  scenario encodes.
- [squeeze-loop](../../../../docs/glossary/squeeze-loop.md) — C2 catchability via a disjoint
  evidence base.
