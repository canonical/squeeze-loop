# Use Case C — evidence verification (paper third terrain) — 2026-06-12

The third executable instance `src/C/` (Archetype C, split planes: API Contract
Guard) is the lower bound for §\ref{sec:caseF}. This report re-derives its numbers.

## Artifact
`src/C/evidence/measure_squeeze.py` drives the real split-plane squeeze (the
in-band runner boots the implementer's stdlib HTTP server, runs the conformance
matrix, lints the contract, and checks the TY0 baseline) and emits
`src/C/evidence/results.json` (+ `tex/macros/results_c.tex`).
`seeded_wrong_server.py` is the parametrized coherent-and-wrong server.

## Re-derived measures (results.json)

| key | value | meaning |
|---|---|---|
| clauses | 3 | obligation clauses in API_POLICY_081 |
| test_cases | 5 | conformance cases (runtime plane) |
| legacy_routes | 2 | TY0 baseline route signatures |
| squeeze_ok | true | good run: ISOLATION + Gate C + Gate B + doc-plane + TY0 |
| document_plane_ok / ty0_ok / isolation_ok | true | sub-checks |
| seeded_defects | 4 | per-clause servers (skip-auth, leak-id, leak-trace) + combined control |
| ablation_barrier_on_caught | 4 | exerciser oracle = schema/manifest → all caught |
| ablation_barrier_off_caught | 0 | exerciser oracle = implementation → none caught |
| detection_rate_pct | 100 | barrier-on detection |

## Cross-terrain consistency
Seeded coherent-and-wrong detection now measured on all three archetypes:
A 5/5, B 4/4, C 4/4 with the barrier on; 0 with it off. The central claim holds on
every archetype. The C negative control: a server leaking the internal integer
`id` is rejected at Gate B (`key-set mismatch ... got [..., 'id', ...]`).

## Ran under LXC (no internet)
`src/C/run_in_lxc.sh` executed the full split-plane squeeze inside unprivileged
container `ucC` (loopback-only): the runtime server bound 127.0.0.1:8000 on the
container loopback, SQUEEZE OK offline, negative control rejected. See
`lxc-usage.md`.

## Honest scope
Constructed instance, deterministic, no matched-difficulty baseline.
`atlidakis2019restler` cited as the spec-derived-testing framing (read FULL);
per its record, RESTler's oracle is unexpected status codes / 500s.
