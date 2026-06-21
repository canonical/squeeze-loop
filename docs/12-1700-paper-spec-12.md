# 12-1700-paper-spec-12 — paper-impl loop, circle 12: execute the protocol harness (real-agent pilot)

STATUS: DONE
Execute the comparative half of the evaluation protocol with REAL LLM agents
(subagents), not the deterministic instances --- a small, honest pilot of H2.

## E-item — eval/pilot/
- `tasks.py`: 4 single-argument tasks (net, median, running_max_count,
  dedup_count_ci), each with a spec, a correct reference impl (oracle), and a
  seeded coherent-and-wrong impl.
- 8 exerciser subagents (4 tasks x 2 conditions) authored test cases
  {input, expected} into `cases/<task>.<config>.json`:
  - barrier-on: the agent saw ONLY the spec.
  - barrier-off: the agent also saw the (buggy) implementation, neutral framing.
- `score.py`: a config CATCHES a task iff some case is discriminating
  (correct != wrong) AND spec-correct (expected == correct) --- exactly a test
  the seeded bug fails. Emits results.json + tex/macros/pilot.tex.

## Result (reported faithfully; this is a NULL / nuanced finding)
barrier-on caught 4/4; barrier-off ALSO caught 4/4; 100% of cases spec-correct
in both. **The barrier made no measurable difference**: shown the buggy code,
the model still computed expectations from the spec and caught the bug rather
than anchoring to the implementation.

Interpretation (in the paper, §sec:eval "Pilot execution"):
- This tempers the deterministic ablation (barrier-off modelled as FULL anchoring
  -> 0 detection): mere code visibility did not induce anchoring for this model
  on easy tasks.
- The strategy's value is a GUARANTEE (the barrier removes the possibility of
  anchoring by construction), not a claim that agents always anchor; the pilot
  bounds how often the possibility is realized for one model, not whether the
  guarantee is worth having.
- Underpowered: n=4 tasks, 1 rep, 1 model family, unambiguous specs, and a
  deliberately WEAK barrier-off (visibility, not self-authorship). A stronger
  self-preference condition (same agent writes impl + tests) and a powered,
  cross-model study remain H1-H2 proper.

## W-item — manuscript
- §sec:eval: new "Pilot execution" paragraph reporting on/off = 4/4 and the
  no-difference finding, with the guarantee-vs-hope framing and the caveats
  (\ResPilot* macros).
- §sec:synthesis: the barrier-off=0 sentence annotated as the deterministic
  full-anchoring extreme, pointing to the pilot.
- Ledger CLM-058 (RESULT bound to eval/pilot/).

## Gates
- Gate B: build green (18 pp), all cites/refs/macros resolve, no bibtex warnings.
- Evidence: cases/*.json committed (raw agent-authored data); score.py
  recomputes results.json + pilot.tex deterministically from them.

## Integrity note
The honest outcome (no difference) is reported, not buried or spun --- reporting
a fabricated or cherry-picked difference would be the coherent-and-wrong failure
the paper is about. The cases files are committed so the result is auditable.

## Open questions for the next circle
1. A STRONGER barrier-off (self-authorship / self-preference) condition --- the
   agent that wrote the buggy code then tests it --- to probe whether the effect
   appears when authorship, not just visibility, is shared.
2. A powered, cross-model study (the genuine H1-H2).
