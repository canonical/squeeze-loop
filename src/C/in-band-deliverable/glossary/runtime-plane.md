# Runtime plane (what the service does)

**Definition.** A live HTTP server whose actual behaviour — status codes, response keys,
error messages — is tested independently against the [document-plane](document-plane.md)
schema. One of C's two semantic surfaces: what the construct *actually is*. It must never
leak tracebacks and must expose only public UUIDs, never internal integer ids.

The runtime plane carries its own executable ground truth (the running process inspected
over the network), distinct from the document's linter. The dominant failure of
[Archetype C](../../../../docs/glossary/archetype.md) is *blending* — letting the runtime's
behaviour be vouched for by a compliant schema, or vice versa.

## Sources

- `src/C/ground-truth/reference_server.py` — the frozen answer-key server.
- `src/C/in-band-deliverable/implementer/src/main.py` — the agent's runtime code under
  squeeze.
- `src/C/ground-truth-spec.md` §2 (Plane 2).

## See also

- [document-plane](document-plane.md) — the contract it must conform to.
- [no-blend-check](no-blend-check.md) — the rule keeping the two verdicts disjoint.
- [conformance-matrix](conformance-matrix.md) — the cases run against this server.
