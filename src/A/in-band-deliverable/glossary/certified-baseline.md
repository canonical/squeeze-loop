# Certified baseline (A's ground-truth invariant)

**Definition.** A cryptographically signed ledger of byte-deterministically recomputed
baseline metrics for past quarters that any new query **must not shift by a single byte**
— the *total-additivity* invariant. A's instance of the
[ground truth](../../../../docs/glossary/ground-truth.md), enforced as a standing
invariant after every work item.

It is the executable floor: a new metric query is admissible only if the historical
numbers it recomputes match the signed ledger exactly. A drift of one byte trips the
regression (Gate B), so a change cannot silently rewrite history.

## Sources

- `src/A/ground-truth/shared/history_ledger.json` (+ `.sig`) — the signed baseline.
- `src/A/ground-truth/metrics.py` — the deterministic computation.
- `src/A/ground-truth/README.md` (§2) — the total-additivity rule.

## See also

- [metric-handbook](metric-handbook.md) — the soft ceiling this floor is checked against.
- [ground-truth](../../../../docs/glossary/ground-truth.md) ·
  [gates](../../../../docs/glossary/gates.md) — the shared oracle / standing-invariant concepts.
