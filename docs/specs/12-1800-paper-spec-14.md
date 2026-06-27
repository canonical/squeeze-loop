# 12-1800-paper-spec-14 — paper-impl loop, circle 14: weaker-model self-preference (still not surfaced)

STATUS: DONE
Attempt to surface the self-preference effect by lowering the implementer's
capability (a weaker model), raising the natural error rate.

## E-item — eval/pilot3/
- 5 tasks, two of them ones weak models classically trip on (roman_to_int with
  subtractive notation; is_leap_year with the 100/400 rule), plus bankers_round,
  title_case, second_largest.
- self-author = a WEAKER model (haiku) writing impl + its own tests; two
  independent exercisers per task, spec only: indep_weak (same weak model,
  capability-controlled) and indep_strong (strong model, confirms catchability).
  15 subagents total. score.py execs each weak self-impl, decides buggy vs the
  oracle on probes, counts catches per condition. cases/*.json committed.

## Result (faithful; THIRD inconclusive)
0/5 weak self-authored implementations were buggy --- even haiku implemented all
five textbook tasks correctly (including Roman numerals and leap years) --- so the
self-preference escape again could not be observed.

## Reading
Three pilots (visibility barrier-off; self-authorship; weaker-model
self-authorship) all failed to surface the effect at pilot scale. This is not
evidence of absence: capable models simply do not err on small, well-trodden
tasks, and we declined to search task space for one that induces a bug (the
cherry-pick the strategy forbids). The deterministic mechanism is clear
(§sec:synthesis); the real-agent effect resists a quick pilot. Surfacing it needs
the powered study: novel/compositional tasks with a measured nonzero implementer
error rate, multiple model families, repetitions.

## W-item — manuscript
- §sec:eval pilot paragraph extended with pilot-3 (\ResPilotThree* macros): the
  weaker-model attempt, 0/5 buggy, and the "honest state of the evidence" framing.
- Ledger CLM-060.

## Gates
- Gate B: build green (18 pp), all cites/refs/macros resolve, no bibtex warnings.
- Evidence: eval/pilot3/cases/*.json committed; score.py recomputes.

## Integrity note
Three consecutive honest non-results reported as-is. Stopping here rather than
fishing for a bug-inducing task IS the disciplined choice the paper is about.

## Open questions for the next circle
1. The powered study (calibrated non-textbook tasks, cross-model, repetitions) ---
   genuinely beyond a quick pilot; the real remaining work.
