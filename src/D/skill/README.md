# Use Case D -- skill accumulation (end-to-end)

Implements docs/skill-accumulation-design.md on D, where the SKILL is tactics. The
prover starts knowing no tactic; on a wall it acquires the catalog tactic the
exercise needs (lia, then nia) -- a BOUNDED conceptual leap. Tiers are real Rocq
verdicts cached by `precompute_tiers.py` (81 lia, 3 nia, 16 wall), so the loop/test
are deterministic and kernel-free.

The honest D signature: the catalog cannot crack everything. A residual WALL
(16/100: exponentials, amgm-style inequalities) needs a real conceptual leap -- a
manual lemma / induction -- which the design DEFERS. So solvable-misses fall to 0
as tactics are learned, but the not-found rate floors at the wall, NOT zero. That
floor is the frontier where the deferred conceptual-leap mechanism would act.

Run: `python3 src/D/skill/precompute_tiers.py` (once, needs Rocq) then
`python3 src/D/skill/skill_loop.py`; test: `test_skill_enriches.py`.
Result (seed 7000): skill 0->2 (lia@1, nia@8); solvable-miss 0.2 -> 0; wall 16/100.
