# Use Case A -- skill accumulation (end-to-end)

Implements docs/skill-accumulation-design.md on A. The analyst starts with an empty
skill and writes the OBVIOUS query; when the exerciser catches its value diverging
from the intended reading on the real warehouse, it consolidates (K) a skill for
that metric family and switches to the intended reading. Skill enriches over the
subtle families (net_rev, dau_grain, active_customer, survivorship); errors fall.
Run: `python3 src/A/skill/skill_loop.py`; test: `test_skill_enriches.py`.
Result (seed 8000): skill 0->4 (learned cycles 3,7,10,52); errors 1.0 -> 0.
Rule 1 (only the analyst learns), reset-from-scratch, deterministic. Programmatic
learner, not a live LLM (the honest gap).
