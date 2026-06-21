# Refund policy (B's upper bound)

**Definition.** The authored, English-only policy spec (`POL_REFUND_042`) declaring the
obligation clauses and their paired decision tokens (REIMBURSE / DENY / ESCALATE),
anchored to a core negative vector (already-refunded order + legal threat → ESCALATE). B's
instance of the [upper bound](../../../../docs/glossary/upper-bound.md).

B is [Archetype B](../../../../docs/glossary/archetype.md): **no external authority exists**
for "what is the correct refund decision," so the policy is *authored upstream* and anchored
to a flagship use case. Because there is no external spec to diff against, the soundness
argument rests on author independence (the exerciser never sees the bot's code), not on an
outside reference.

## Sources

- `src/B/upper-bound/refund_policy.md` — `POL_REFUND_042`, the clauses and decision tokens.
- `src/B/upper-bound/README.md` — structure; how Gate A / Gate C use it.

## See also

- [reference-policy](reference-policy.md) — the executable answer key for this policy.
- [upper-bound](../../../../docs/glossary/upper-bound.md) ·
  [archetype](../../../../docs/glossary/archetype.md) — the shared concepts this instantiates.
