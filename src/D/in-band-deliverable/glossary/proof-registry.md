# Proof registry (D's invariant trunk)

**Definition.** A certified trunk of previously verified exercise `.v` files, pinned by a
deterministic SHA-256 signature (`registry.sig`), so that any changed byte in any registered
proof invalidates the trunk digest and Gate B's regression detects it. D's instance of the
standing invariant on the [ground truth](../../../../docs/glossary/ground-truth.md).

It is the analogue of A's certified baseline and B's archive ledger: a new proof is
admissible only if the whole certified trunk still verifies byte-for-byte, so progress
cannot silently break an earlier result.

## Sources

- `src/D/ground-truth/registry.py` — `compute_manifest()`, `write_signature()`,
  `verify_signature()`.
- `src/D/ground-truth/shared/proof_registry/` — the trunk of certified `.v` files.
- `src/D/ground-truth/README.md` §2 (invariant plane).

## See also

- [rocq-kernel](rocq-kernel.md) — the oracle that re-checks the trunk.
- [ground-truth](../../../../docs/glossary/ground-truth.md) ·
  [gates](../../../../docs/glossary/gates.md) — the standing-invariant / Gate B concepts.
