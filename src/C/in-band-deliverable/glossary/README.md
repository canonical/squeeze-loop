# Glossary — Use Case C (API contract guard, split planes)

Concepts this instance generates and uses, each anchored to one meaning grounded in its
artifacts (see [glossary](glossary.md) for why a generative loop needs this). For the
shared, cross-instance vocabulary (squeeze-loop, upper-bound, ground-truth, gates,
archetype, …) see the paper's glossary at `../../../../docs/glossary/`.

## Entries

- [glossary](glossary.md) — the role of a glossary in a generative loop (the shared
  meta-entry; identical across instances).
- [document-plane](document-plane.md) — what the contract *promises* (the OpenAPI schema).
- [runtime-plane](runtime-plane.md) — what the service *does* (the live server).
- [no-blend-check](no-blend-check.md) — the disjointness rule that keeps one plane from
  vouching for the other; what makes C its own archetype.
- [conformance-matrix](conformance-matrix.md) — clause→assertion cases derived from the
  schema alone and run against the live server.
