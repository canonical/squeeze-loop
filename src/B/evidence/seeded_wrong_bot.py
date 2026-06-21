#!/usr/bin/env python3
"""A parametrized seeded coherent-and-wrong refund bot for the evidence harness.

It reuses the real implementer's interface and multi-turn commit discipline, but
NEUTERS exactly one policy clause, selected by the SKIP_CLAUSE environment
variable (CLAUSE_1 | CLAUSE_2 | CLAUSE_3). The result is internally consistent
and fluent, yet wrong on precisely one obligation -- so the scenario that targets
that clause must diverge, proving the clause is load-bearing (the squeeze-loop
analogue of a single mutation that the suite must kill).
"""

import os
import sys
from pathlib import Path

# Reuse the real implementer (sentinel-side tooling may; the implementer band
# itself remains import-isolated from the exerciser band).
IMPL = Path(__file__).resolve().parents[1] / "in-band-deliverable" / "implementer" / "src"
sys.path.insert(0, str(IMPL))
import refund_bot_logic as _impl  # noqa: E402

SKIP = os.environ.get("SKIP_CLAUSE", "")


def _decide(customer, messages):
    """The real priority policy, with the SKIP_CLAUSE clause removed."""
    blob = " ".join(m or "" for m in messages).lower()
    if SKIP != "CLAUSE_2" and any(kw in blob for kw in _impl.LEGAL_KEYWORDS):
        return "ESCALATE"
    orders = customer.get("orders", [])
    target = _impl._target_order(orders, messages)
    if SKIP != "CLAUSE_1" and target is not None and target.get("status") == "REFUNDED":
        return "DENY"
    if (SKIP != "CLAUSE_3"
            and customer.get("registration_age_hours", 0) < 48
            and target is not None
            and target.get("value_usd", 0) >= _impl.MAX_REFUND_THRESHOLD_USD):
        return "DENY"
    if customer.get("fraud_flag") == 1 or customer.get("return_velocity", 0.0) >= 0.80:
        return "DENY"
    if target is not None and target.get("status") == "IN_TRANSIT":
        return "REIMBURSE"
    return "ESCALATE"


# Patch the real module's decision rule; reuse its commit discipline + interface.
_impl._decide = _decide
process_customer_turn = _impl.process_customer_turn
