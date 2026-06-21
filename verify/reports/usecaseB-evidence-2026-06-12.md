# Use Case B — evidence verification (paper second terrain) — 2026-06-12

The second executable instance `src/B/` (Archetype B, authored authority: refund
bot) is the lower bound for §\ref{sec:caseE}. This report re-derives the numbers
the manuscript cites for it.

## Artifact
`src/B/evidence/measure_squeeze.py` drives the real squeeze (the in-band runner
starts/stops the ground-truth REST app) and emits `src/B/evidence/results.json`
(+ `tex/macros/results_b.tex`). `seeded_wrong_bot.py` is the parametrized
coherent-and-wrong bot.

## Re-derived measures (results.json)

| key | value | meaning |
|---|---|---|
| clauses | 3 | obligation clauses in POL_REFUND_042 |
| scenarios | 5 | adversarial multi-turn scenarios |
| archive_cases | 6 | adjudicated regression cases |
| squeeze_ok | true | good bot: ISOLATION + Gate C + Gate B all pass |
| archive_regression_ok | true | replaying the archive: no decision flips |
| seeded_defects | 4 | one bot per clause + an always-refund bot |
| ablation_barrier_on_caught | 4 | exerciser oracle = policy → all caught |
| ablation_barrier_off_caught | 0 | exerciser oracle = implementation → none caught |
| detection_rate_pct | 100 | barrier-on detection rate |
| ground_truth_verify_ok / upper_bound_validate_ok | true | component self-checks |

## Cross-terrain consistency
The measures mirror Use Case A (§\ref{sec:caseD}): seeded coherent-and-wrong
detection 4/4 (B) and 5/5 (A) with the barrier on, 0 with it off. The central
claim — an independent exerciser holding only the upper bound catches a
coherent-and-wrong implementer — holds on both terrains. The negative control: a
bot ignoring the legal-threat clause is rejected at Gate B
(`expected ESCALATE, implementer committed REIMBURSE`).

## Ran under LXC (no internet)
`src/B/run_in_lxc.sh` executed the full B use case inside unprivileged LXC
container `ucB` with a loopback-only network namespace: ground truth built &
verified, upper bound validated, `SQUEEZE OK`, and the negative control rejected —
all offline (TCP+DNS blocked; the REST app served only on 127.0.0.1 inside the
container). See `lxc-usage.md`.

## Honest scope
Constructed instance, deterministic, no matched-difficulty baseline; generalisation
across terrains in kind (n=2), not the controlled comparison of §\ref{sec:eval}.
`perez2022ignore`/`greshake2023injection` are cited as the threat framing, read
FULL at abstract+HTML level.
