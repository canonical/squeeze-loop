# Use Case A — evidence verification (paper lower bound) — 2026-06-12

The executable instance `src/A/` is the lower bound for the paper's
Section~\ref{sec:caseD}. This report re-derives every number the manuscript cites
for it, the verifier role for the evidence plane.

## Artifact

`src/A/evidence/measure_squeeze.py` runs the full stack and emits
`src/A/evidence/results.json` (+ `tex/macros/results.tex`). Determinism: the
harness was run twice; `results.json` was **byte-identical** across runs.

## Re-derived measures (results.json)

| key | value | meaning |
|---|---|---|
| metrics | 2 | METRIC_001 (net revenue), METRIC_002 (active users) |
| clauses | 5 | obligation clauses across the two metrics |
| positive_cells | 8 | 2 metrics × 4 quarters |
| three_way_agreements | 8 | cells where implementer == exerciser == certified ledger |
| seeded_defects | 5 | clause-violating mutations (the negatives) |
| defects_caught | 5 | mutations that diverged (100%) |
| coherent_wrong_caught | true | gross-vs-net implementer rejected at Gate B |
| isolation_ok | true | no import/path linkage between the two bands |
| additivity_stable | true | ledger+sig byte-identical across a rebuild |
| ledger_sha256 | 323cbd5e… | certified-baseline signature |
| warehouse_users / events | 50 / 291 | the data plane |
| certified_ledger_metrics | 24 | entries in history_ledger.json |

All component self-checks returned ok: `ground_truth_verify_ok`,
`upper_bound_validate_ok`, `squeeze_ok`, plus the negative control.

## Manuscript consistency

`tex/macros/results.tex` (the only place these numbers enter the PDF) was
checked against `results.json`: `\ResWorkedSeededDefects=5`,
`\ResWorkedDefectsCaught=5`, `\ResWorkedThreeWayAgree=8`,
`\ResWorkedPositiveCells=8` — all consistent. No Use-Case-A number is hand-typed.

## Verdict

SUPPORTED. The claims in §\ref{sec:caseD} (CLM-039..043) are re-derived from a
deterministic, re-runnable artifact.

## Ablation — physical barrier on vs off (circle 3, H2)

Added to the harness: for each of the 5 seeded coherent-and-wrong implementers,
does the exerciser catch it? It depends on the exerciser's oracle.

| configuration | exerciser's oracle | seeded defects caught |
|---|---|---|
| barrier ON | the handbook (upper bound) | 5/5 |
| barrier OFF | the implementation it has seen | 0/5 |

Barrier-off collapses the exerciser to judging *observed* rather than *intended*
behaviour — the no-independent-oracle regime of the test-oracle problem
(`barr2015oracle`), the workflow-level form of the self-evaluation effects in §2.2.
Deterministic; results.json byte-identical on re-run. This is the **extreme** of
barrier-off (full anchoring) on **one** instance — it demonstrates the mechanism,
not an effect size; the matched-difficulty, partial-coupling study is future work.

## Honest scope (carried into the manuscript)

This is a constructed existence demonstration on one small terrain, deterministic
and **without a baseline configuration** — it shows feasibility and that an
independent exerciser catches a coherent-and-wrong implementer, not that the
strategy beats an alternative. The comparative evaluation (H1–H4) remains future
work (§\ref{sec:eval}). The mutation-testing analogy is cited as the *origin* of
the concepts; `jia2011analysis` is a SECONDARY (paywalled) read pending a
full-text upgrade for camera-ready.
