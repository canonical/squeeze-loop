# Use Case C -- skill accumulation (end-to-end)

Implements docs/skill-accumulation-design.md on C. The server starts blending every
subtle clause; when a conformance check catches a blend it consolidates (K) a skill
("honor this clause") and stops blending. Skill enriches over the blended families
(no_id_leak, clean_error, state_machine, idempotency, pagination); caught-blends fall.
Run: `python3 src/C/skill/skill_loop.py`; test: `test_skill_enriches.py`.
Result (seed 6000): skill 0->5 (learned cycles 4,4,6,7,13); blends 1.4 -> 0.
Rule 1, reset-from-scratch, deterministic. Programmatic learner, not a live LLM.
