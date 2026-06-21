# Difficulty ladder (level-up-D)

The richness of Use Case D comes from the richness of its upper bound: a *ladder*
of theorems of increasing mathematical depth, not one easy exercise. This is the
implementation of `level-up-D.md`.

Each rung ships a reference proof (`*_good.v`) and a FALSE mutation (`*_mut.v`),
graded against the real Rocq kernel by `../ladder_runner.py`:

| Rung | Tier | Theorem | Verdict |
|------|------|---------|---------|
| `trivial_*`  | trivial   | `n + 0 = n`              | PASS (proved, axiom-clean, mutation caught) |
| `easy_*`     | easy      | `n + m = m + n`         | PASS |
| `medium_*`   | medium    | `(n+m)+p = n+(m+p)`     | PASS |
| `hard_*`     | hard      | `n * m = m * n`         | PASS |
| `veryhard_*` | very_hard | `n <= 2 ^ n`            | OPEN (proof Admitted; the axiom audit catches it) |

PASS = the proof type-checks, `Print Assumptions` is clean, and the false mutation
is rejected by `coqc`. OPEN = the rung is beyond the certified witness; the
reference proof is left `Admitted` and the audit reports it rather than letting a
vacuous proof through — the gate stays honest at the boundary.

Run: `python3 ../ladder_runner.py` (writes `../../evidence/ladder_results.json`).
The numbers are real kernel verdicts; with Rocq absent the runner SKIPs (exit 3),
never fabricating a verdict. The ladder is the scaffold for a future live-prover
run, where the implementer error rate is expected to rise from trivial to very hard.
