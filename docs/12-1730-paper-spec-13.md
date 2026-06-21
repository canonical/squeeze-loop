# 12-1730-paper-spec-13 — paper-impl loop, circle 13: stronger barrier-off (self-authorship)

STATUS: DONE
Run the stronger barrier-off the previous circle flagged: true SELF-AUTHORSHIP
(self-preference), where one agent writes both the implementation and its own
tests, vs an independent spec-only exerciser testing the same implementation.

## E-item — eval/pilot2/
- tasks.py: 4 single-arg tasks with a tempting misreading (bankers_round,
  second_largest, title_case, is_sorted_strict) + correct oracle + discriminating
  probes. No seeded bug --- the bug, if any, is the agent's own.
- 4 self-author subagents wrote {impl, own tests}; 4 independent subagents wrote
  spec-only tests. score.py execs the self-authored impl, decides if it is buggy
  vs the oracle on the probes, and asks whether each config has a spec-correct
  test the impl fails. Emits results.json + tex/macros/pilot2.tex.

## Result (reported faithfully; INCONCLUSIVE)
0/4 self-authored implementations were buggy --- the model wrote correct code on
all four subtle tasks (e.g. title_case avoided str.title(); is_sorted_strict used
strict <). With no self-authored bug, the self-preference escape could not be
observed: nothing for the agent's own tests, or an independent exerciser, to miss.
This is inconclusive, NOT evidence of absence.

Why inconclusive, and what a real measurement needs: tasks calibrated to a
nonzero implementer error rate, weaker models, or a far larger sample. Reported
rather than searching for a task on which the effect appears --- that would be the
cherry-pick the strategy forbids.

## W-item — manuscript
- §sec:eval "Pilot execution": pilot-1's closing reworded (it had named the
  self-preference condition as future; it is now done), plus a new paragraph
  reporting pilot-2's inconclusive result (\ResPilotTwo* macros) with the
  not-evidence-of-absence + no-cherry-pick framing.
- Ledger CLM-059 (RESULT bound to eval/pilot2/).

## Gates
- Gate B: build green (18 pp), all cites/refs/macros resolve, no bibtex warnings.
- Evidence: eval/pilot2/cases/*.json committed (raw agent-authored impls+tests);
  score.py recomputes results.json + pilot2.tex.

## Integrity note
Two consecutive honest non-results (pilot-1 no-difference; pilot-2 inconclusive)
are reported as-is. The mechanism is demonstrated deterministically
(§sec:synthesis); the real-agent effect size is not measurable on small/easy
tasks with a strong model. Demonstrating that discipline reflexively --- not
spinning a null into a finding --- is itself on-thesis.

## Code-execution caveat
score.py execs agent-generated implementations (tiny pure functions); flagged in
the script. A hardened version would run them in the LXC sandbox.

## Open questions for the next circle
1. Calibrated-difficulty tasks (nonzero natural error rate) and/or weaker models
   to actually observe the self-preference escape --- a powered study.
