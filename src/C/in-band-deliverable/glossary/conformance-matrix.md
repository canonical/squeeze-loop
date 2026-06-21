# Conformance matrix (C's blind test cases)

**Definition.** A JSON artifact mapping each obligation clause to a concrete request
assertion — expected status, response keys, forbidden patterns (e.g. `Traceback`, `SELECT`)
— authored by an exerciser **from the schema alone**, without reading the implementer's
code, then run against the live [runtime-plane](runtime-plane.md). C's instance of the
independent evidence base that defends the [no-blend-check](no-blend-check.md).

It includes the **core negative vector**: an unauthenticated, malformed request to a
mutation route that must be met with a safe 400/401 and zero framework leaks — the probe for
the hidden split-plane mismatch.

## Sources

- `src/C/in-band-deliverable/exerciser/conformance/test_matrix.json` — the cases (clauses +
  core negative vector; forbidden-pattern lists).
- `src/C/in-band-deliverable/exerciser/build_test_matrix.py` — derives expectations from the
  clauses alone.
- `src/C/upper-bound/api_policy_manifest.md` §3 — the core negative vector.

## See also

- [no-blend-check](no-blend-check.md) — what these independently-authored cases enforce.
- [runtime-plane](runtime-plane.md) — what they are run against.
- [squeeze-loop](../../../../docs/glossary/squeeze-loop.md) — C2 catchability via a disjoint
  evidence base.
