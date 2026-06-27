# 12-1900-paper-spec-16 — paper-impl loop, circle 16: real-bug study wired to SWE-bench-Lite

STATUS: DONE (wired against real data; execution pending external infra)
The four synthetic studies hit a near-zero natural error rate. The only route to
a real nonzero defect population is real bugs --- SWE-bench. Honest scope: a full
SWE-bench run needs per-repository Docker environments to execute the gold tests,
which this setup does not provide; fabricating results would be the cardinal sin.
So this circle wires the study to REAL data and stops at the execution boundary.

## E-item — eval/swebench/
- fetch_instances.py: pulls real SWE-bench-Lite instances via the HuggingFace
  datasets-server REST API -> instances.json. Fetched 15 real GitHub bugs (every
  one a true defect with held-out failing tests) -- 35 FAIL_TO_PASS tests total
  across 2 repositories (the first Lite slice). This IS the nonzero defect
  population the synthetic studies lacked (0/24 buggy there).
- run_protocol.py: maps the squeeze onto SWE-bench (held-out FAIL/PASS tests =
  lower bound; implementer patches the issue tests-unseen; independent exerciser
  writes tests issue-only; Gate B = apply patch, FAIL_TO_PASS must flip).
  RUNNABLE here: acquire + characterize the real defects (2 steps). PENDING:
  patch generation and, crucially, executing patches against each repo's gold
  tests (3 steps) -- needs SWE-bench's per-repo Docker harness. Emits status.json
  + tex/macros/swebench.tex.

## W-item — manuscript
- §sec:eval new paragraph "Toward a real-bug study" (\ResSwe* macros): 15 real
  instances / 35 held-out failing tests vs the synthetic 0 bugs; the squeeze<->
  SWE-bench mapping; 2 steps run, 3 pending the Docker harness; wired and ready,
  effect size awaits that infrastructure. Cites jimenez2023swebench.
- Ledger CLM-062.

## Gates
- Gate B: build green (19 pp), all cites/refs/macros resolve, no bibtex warnings.
- Evidence: instances.json (real fetched data) + status.json committed;
  run_protocol.py recomputes.

## Integrity note
Real data fetched, protocol wired, execution boundary stated plainly. No effect
size is claimed; the route is operationalized, not faked. This is the honest
terminus of the in-environment evaluation: a real-bug study ready to execute on
SWE-bench's Docker harness.

## Open questions
1. Execute on the SWE-bench Docker harness (external infra) for the actual H1/H2
   effect size -- the genuine remaining work, now wired against real instances.
