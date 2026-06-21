# No-blend check (C's disjointness rule)

**Definition.** The rule — and its executable enforcement — that the two evaluation paths,
the [document-plane](document-plane.md) and the [runtime-plane](runtime-plane.md), may not
pollute or compensate for one another: a compliant schema cannot excuse a runtime failure,
and a clean-running route cannot excuse an out-of-date contract. The planes are verified
*separately* and must **agree**; neither vouches for the other.

This is what makes C its own [archetype](../../../../docs/glossary/archetype.md): the new
risk is not improvisation (A) or being fooled (B) but **conflation** — passing the easy
plane's check and inheriting the hard plane's claim. The no-blend check is C's load-bearing
gate, the same no-blend guard the paper's [Gate C](../../../../docs/glossary/gates.md)
generalises.

## Sources

- `src/C/ground-truth-spec.md` §3 (the No-Blend invariant engine).
- `src/C/in-band-deliverable/runner/execute_squeeze.py` — the cross-plane verification.
- `src/C/in-band-deliverable/evidence/coherent_wrong_server.py` — the negative control
  (internally coherent but clause-violating servers are caught).

## See also

- [document-plane](document-plane.md) · [runtime-plane](runtime-plane.md) — the two
  surfaces it keeps disjoint.
- [gates](../../../../docs/glossary/gates.md) — Gate C's no-blend guard, generalised.
