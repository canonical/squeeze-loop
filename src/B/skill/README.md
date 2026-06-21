# Use Case B -- skill accumulation (end-to-end)

Implements `docs/skill-accumulation-design.md` on B and tests that the skill
ENRICHES across cycles. The deciding agent (the refund bot) starts with an empty
skill store; each time the independent exerciser catches it caving to a
manipulation tactic, it records the catch and, after consolidating (learning rate
K), writes a skill ("this tactic is manipulation -> follow policy, do not cave").
It then reads the skill and stops caving to that tactic. The skill grows and the
error rate falls.

Design rules honoured:
- **Rule 1**: only the DECIDING agent learns; the exerciser and the policy
  (`reference_policy.decide`) stay fixed -- the fixed oracle is what forces the
  concept. (If everyone learned, the differential would vanish.)
- **Reset**: a run starts from scratch (empty skill); re-run, or delete
  `skill_store.json`, to redo from the current discussions/policy.

Run / test:
```
python3 src/B/skill/skill_loop.py            # 100 cycles from scratch -> results + skill store
python3 src/B/skill/test_skill_enriches.py   # asserts the skill enriches across cycles
```

Result (seed 9000, 100 cycles, sample 4, K=5): skill enriches 0 -> 8 tactics
(consolidated at cycles 4,7,9,12,13,14,16,22), error rate falls 2.9/4 (first 10
cycles) -> 0 (last 10). The test's causality check confirms the skill is what
reduced the error: replaying the late-window chats against an EMPTY skill remakes
29 errors the trained skill avoids.

Artifacts (recomputable, seeded): `skill_enrichment_results.json` (the per-cycle
enrichment curve), `skill_store.json` (the final learned concepts).

HONEST SCOPE: the deciding agent is a programmatic learner (it extracts the lesson
from being caught), NOT a live LLM. The skill-store / enrichment-policy / Rule-1 /
consolidation / reset machinery is real and tested; putting a live model in the
deciding role is the remaining step (the paper's per-model gradient stays OPN).
