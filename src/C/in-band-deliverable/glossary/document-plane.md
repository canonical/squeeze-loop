# Document plane (what the contract promises)

**Definition.** The static, read-only OpenAPI schema that fixes the public contract — the
routes, security schemes, and request/response shapes the service is supposed to honour —
validated by a linter *independent* of the runtime code. One of C's two semantic surfaces:
what the construct *says* it is.

In [Archetype C](../../../../docs/glossary/archetype.md) (split planes) the document plane
carries its own authority and its own executable check (the linter), distinct from the
[runtime-plane](runtime-plane.md). Either plane can be satisfied while the other is
violated — a clean schema that the server does not implement, or vice versa.

## Sources

- `src/C/ground-truth/shared/base_schema.json` — the canonical contract document.
- `src/C/ground-truth/linter.py` — the pinned linter (well-formedness, typed schemas,
  complete error responses).
- `src/C/ground-truth-spec.md` §2 (Plane 1).

## See also

- [runtime-plane](runtime-plane.md) — the other plane it must agree with.
- [no-blend-check](no-blend-check.md) — why the two planes are checked separately.
- [ground-truth](../../../../docs/glossary/ground-truth.md) — the shared floor concept
  (one per plane here).
