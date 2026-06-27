# 12-1430-paper-spec-7 — paper-impl loop, circle 7: third executable terrain (Use Case C)

STATUS: DONE
Bring `src/C` (Archetype C, split planes: API Contract Guard) into the paper as
the third executable instance, completing archetype coverage (A transcription,
B authored authority, C split planes).

## E-item — measure src/C, recomputably
- `src/C/evidence/measure_squeeze.py` (mirrors A/B harnesses) runs the full C
  squeeze and emits `src/C/evidence/results.json` + `tex/macros/results_c.tex`.
- `src/C/evidence/seeded_wrong_server.py`: a parametrized coherent-and-wrong API
  server (one clause violated per VIOLATE env: skip-auth / leak-id / leak-trace).

Measured: 3 clauses, 5 conformance cases, 2 legacy routes; good implementer
passes runtime + document-plane + TY0; seeded coherent-and-wrong detection 4/4
with the barrier on, 0/4 off.

## L-item — new question → bibliography
C's exerciser derives conformance tests from the OpenAPI document plane and runs
them against the live runtime plane to catch spec/runtime drift — the established
automated-REST-API-testing practice. Added and verified (read FULL):
`atlidakis2019restler` (RESTler, ICSE 2019). Cited in §\ref{sec:caseF}. CLM-052.
(Scoping note from the record: RESTler's oracle is unexpected HTTP status codes /
500s; it backs the spec-derived-testing-catches-drift claim, not the
undocumented-key check specifically.)

## W-item — manuscript
- New §\ref{sec:caseF} "A third terrain: split planes (Use Case C)": the
  document-plane + runtime-plane lower bound, the API-governance manifest upper
  bound, the schema-derived exerciser (cite RESTler), TY0 legacy-route guard, and
  the measures via \ResC* macros. States that all three archetypes now have an
  executable instance and that the central claim + barrier ablation hold on each.
- §\ref{sec:caseD} ("first of three") and §\ref{sec:caseE} closing reworded for
  three instances.
- Abstract + contribution (iii) + §6 ablation sentence updated to span all three
  terrains.
- Ledger CLM-052 (CITE), CLM-053 (RESULT bound to src/C/evidence/results.json).

## Ran under LXC (no internet)
`src/C/run_in_lxc.sh` ran the full split-plane squeeze inside unprivileged
container `ucC`, loopback-only: SQUEEZE OK offline, negative control rejected.

## Gates
- Gate B: build green (20 pp), all cites/refs/macros resolve, no bibtex warnings.
- Evidence: measure_squeeze.py exits MEASURE OK (4/4 on, 0/4 off); see
  verify/reports/usecaseC-evidence-2026-06-12.md.

## Honest scope
Constructed, deterministic instances, no matched-difficulty baseline;
generalisation across terrains in kind (now n=3, all archetypes), not the
controlled H1-H4 study (§\ref{sec:eval}).

## Open questions for the next circle
1. The controlled, cross-model, matched-difficulty study remains future.
2. The three executable terrains could be drawn together in the reflexive /
   discussion framing (the strategy demonstrated end-to-end on every archetype).
