# Reference policy (B's ground truth)

**Definition.** The certified decider `reference_policy.decide(customer, orders, messages)`
that executes the refund policy's rules in priority order — legal escalation always wins,
then duplicate-refund, new-account high-value guard, fraud guard, nominal-distress refund,
else escalate-ambiguous — and returns the canonical verdict (REIMBURSE | DENY | ESCALATE).
B's instance of the [ground truth](../../../../docs/glossary/ground-truth.md): the runnable
answer key every archived case and every implementer decision is measured against.

Every certified case verdict is **recomputed** by this function at build time, never
hand-typed, and the archive is pinned by a signature so no past decision can change
silently.

## Sources

- `src/B/ground-truth/reference_policy.py` — `decide(...)`; decision constants; the legal
  keyword list; `MAX_REFUND_THRESHOLD_USD`.
- `src/B/ground-truth/README.md` — the priority-ordered rules; the certified archive +
  `ledger.sig`.

## See also

- [refund-policy](refund-policy.md) — the soft policy this decider executes.
- [legal-escalation-trigger](legal-escalation-trigger.md) — rule 1 (legal always wins) is
  exactly what the carved skill must defer to.
- [ground-truth](../../../../docs/glossary/ground-truth.md) — the shared oracle concept.
