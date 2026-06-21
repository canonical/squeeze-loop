# Contract-richness ladder (level-up-C)

The richness of Use Case C comes from the richness of its upper bound: the size of
the contract and the number of clauses where the document plane and the runtime
plane can silently diverge (blending). This implements `level-up-C.md`.

`ladder.py` models each rung as pure handlers `h(state, req) -> (status, body)`: a
CORRECT server and FORK servers that pass the happy path but blend a plane.
`../ladder_runner.py` runs conformance cases (derived from the contract) against
each; a fork is **caught** when at least one case fails against it.

| Tier | Clause | Forks |
|------|--------|-------|
| trivial | GET 200 + documented field | missing-field |
| easy | auth on mutation | skips-auth |
| medium | no id leak; clean errors | leaks-id; traceback |
| hard | order state machine | allows-illegal-transition |
| very_hard | cross-plane consistency under state | stale-read-after-write; idempotency-ignored |

Run: `python3 ../ladder_runner.py` (writes `../../evidence/ladder_results.json`).
Current result: 5/5 rungs -- the correct server is conformant on every case and all
7 blended forks are caught. The hard/very-hard rungs use STATEFUL SEQUENCES, where
the doc-plane/runtime-plane divergence only surfaces across calls. The ladder is the
scaffold for a live-server run, where the blend rate is expected to rise from
trivial to very hard.
