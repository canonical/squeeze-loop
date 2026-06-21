# 12-1630-paper-spec-11 — paper-impl loop, circle 11: operationalize the evaluation protocol

STATUS: DONE
User decision (AskUserQuestion): "Build the harness." Turn §sec:eval from prose +
TODOs into a runnable config-matrix experiment driver that runs the deterministic
subset and stubs the model-dependent parts with their prerequisites --- no
fabricated numbers (fabricating an effect size would be the coherent-and-wrong
failure the paper warns against).

## E-item — `verify/eval_protocol.py`
A config-matrix harness over the three executable instances:
- CONFIGS: squeeze (barrier on) and barrier-off are RUNNABLE today; the
  shared-context / self-refine / debate baselines are PENDING, each listing its
  prerequisites (LLM agent pipeline, matched-difficulty task suite).
- HYPOTHESES: H2 is MEASURED (barrier-on 100% vs barrier-off 0% seeded-defect
  detection over 13 seeded defects across the 3 instances, plus the coupling
  numbers, all read from the instances); H1/H3/H4 are PENDING with prerequisites.
- Emits `eval/results.json` (status manifest) + `tex/macros/eval.tex`
  (\ResEvalHypTotal=4, \ResEvalHypMeasured=1, \ResEvalHypPending=3,
  \ResEvalConfigsRunnable=2, \ResEvalConfigsPending=3).
Wire-in point documented: replace a PENDING config's runner with a real
LLM-agent pipeline + task suite and its status flips to MEASURED.

## W-item — manuscript
- §sec:eval: new "Protocol status" paragraph (via \ResEval* macros) stating the
  protocol is operationalized; H2 discharged on the three instances; H1/H3/H4 and
  the baseline configs are explicit stubs reporting prerequisites, not fabricated
  results. Section heading TODO -> "comparative runs pending model access"; the
  intro TODO -> "execute the comparative runs once model access and a compute
  budget are available".
- Ledger CLM-057 (RESULT bound to the harness).

## L-item
None. No new external source.

## Gates
- Gate B: build green (18 pp), all cites/refs/macros resolve, no bibtex warnings.
- Evidence: eval_protocol.py runs and reports; numbers read from the instances.

## Honest status
The controlled, cross-model, matched-difficulty study is now operationalized but
NOT executed: it needs real model access, a task suite, a compute budget, and
statistics. The harness makes that boundary explicit and machine-checked.

## Open questions for the next circle
1. Execute the comparative runs (needs model access + budget + task suite) ---
   the genuine remaining gap.
