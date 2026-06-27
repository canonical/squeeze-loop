# 12-1830-paper-spec-15 — paper-impl loop, circle 15: the powered study (null, decisively)

STATUS: DONE
Run a pre-committed, more powered version of the H1/H2 comparison and report it
faithfully.

## Design (pre-committed; not tuned to results)
eval/study/: 8 harder, compositional single-arg tasks (merge_intervals,
spreadsheet_col, expand_ranges, is_balanced, int_to_roman ENCODING,
dedup_adjacent, compress_rle, most_common) with correct oracles + edge probes.
Three model tiers (haiku/sonnet/opus) each self-authored an implementation + its
own tests; one independent opus exerciser per task (spec only). 32 subagents.
score.py execs each impl, decides buggy vs oracle, and for buggy impls compares
self-tests vs independent-tests catches with a paired McNemar exact test.

## Result (faithful; NULL, decisively)
24 implementations, 0 buggy (haiku 0 / sonnet 0 / opus 0). Even the weakest tier
solved every harder task. The barrier comparison was vacuous (McNemar p=1.000,
0 discordant pairs).

## The lesson
The obstacle is NOT low power in N --- it is a near-zero per-implementation error
rate. Current models reliably implement small, well-specified single functions
correctly, so no sample size surfaces a self-authored bug for the barrier to
catch. Across four attempts (pilots 1-3 + this study) ~50 implementations yielded
0 natural bugs. Measuring the barrier's marginal value empirically therefore
needs either a domain where capable models genuinely err (real repository bugs,
SWE-bench-style; or ambiguous research-scale specs) or a seeded-defect design ---
which is exactly the deterministic route (§sec:synthesis) where the mechanism is
already demonstrated.

## W-item — manuscript
- §sec:eval new paragraph "Powered attempt, and why it too is null" (\ResStudy*
  macros): 24 impls, 0 buggy, vacuous comparison, the near-zero-error-rate
  diagnosis, and the redirect to real-world-bug or seeded designs. Cites
  jimenez2023swebench.
- Ledger CLM-061.

## Gates
- Gate B: build green (19 pp), all cites/refs/macros resolve, no bibtex warnings.
- Evidence: eval/study/cases/*.json committed (32 raw agent artifacts); score.py
  recomputes results.json + study.tex.

## Integrity note
Four consecutive honest non-results, reported as-is, with a pre-committed task
suite. The disciplined conclusion --- natural-bug-based measurement is infeasible
on this task class, so the deterministic/seeded route is the right evidence ---
is the strategy applied to its own evaluation.

## Open questions
1. A real-world-bug study (SWE-bench-style) or seeded-defect study at scale ---
   the only routes left to an empirical effect size. Genuinely large external work.
