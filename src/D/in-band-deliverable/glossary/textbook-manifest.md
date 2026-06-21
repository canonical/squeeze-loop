# Textbook manifest (D's upper bound)

**Definition.** The token-parsable normative spec that fixes the exact theorem statement,
the scope, the enumerated obligation clauses, the core negative vector (the target false
mutation), and the NOT-claims the prover may not breach. D's instance of the
[upper bound](../../../../docs/glossary/upper-bound.md).

D is a transcription instance ([Archetype A](../../../../docs/glossary/archetype.md)): the
manifest is an *external* written statement of what is to be proved, and the task is to
discharge it faithfully — the prover may not redefine the theorem to make it easier.

## Sources

- `src/D/upper-bound/textbook_manifest.md` — the artifact (`EX_ROCQ_074` block, clauses).
- `src/D/upper-bound/manifest.py` — parser + validator.
- `src/D/upper-bound/README.md` — specification.

## See also

- [rocq-kernel](rocq-kernel.md) — the executable oracle that decides whether the statement
  is proved.
- [upper-bound](../../../../docs/glossary/upper-bound.md) ·
  [archetype](../../../../docs/glossary/archetype.md) — the shared concepts this instantiates.
