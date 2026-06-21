"""Reference policy -- the certified "answer key" decider (spec §2 Step 2,
the Invariant Plane). This is the analogue of Example A's metrics.py: it is the
single source of truth for *correct behaviour*.

Both build_ground_truth.py and verify_ground_truth.py import decide(), so every
verdict in the archive ledger can only ever be what this function computes -- no
hand-typed decision can enter the ground truth. The implementer agent reimplements
this logic independently from the policy handbook (it is physically barred from
reading this file); the archive ledger is what its reimplementation is squeezed
against.

Decision constants are mirrored by the storage plane (value_usd in integer USD).
"""

import re

# --- Decision constants (spec contract) -------------------------------------
MAX_REFUND_THRESHOLD_USD = 500

LEGAL_KEYWORDS = [
    "legal counsel",
    "lawsuit",
    "sue",
    "litigation",
    "attorney",
    "lawyer",
    "lawyers",
    "court",
    "petition",
    "legal action",
]

# Regulator / statute invocations (CLAUSE_8). Distinct from LEGAL_KEYWORDS: these
# name a codified rule or statutory body rather than a litigation threat. ANY
# invocation -> ESCALATE for human review, whether or not the rule actually
# applies; the system must not itself rule on a regulation's applicability.
REGULATOR_KEYWORDS = [
    "ftc",
    "federal trade commission",
    "cooling-off",
    "cooling off",
    "consumer protection",
    "consumer rights act",
    "magnuson-moss",
    "magnuson moss",
    "regulation",
    "statute",
    "statutory",
    "gdpr",
    "ccpa",
    "ombudsman",
    "trading standards",
    "distance selling",
    "uniform commercial code",
    "ucc",
]

# Phrases that signal an externally-filed payment dispute / chargeback (CLAUSE_5).
DISPUTE_PHRASES = [
    "called my bank",
    "contacted my bank",
    "called the bank",
    "chargeback",
    "charge back",
    "dispute the charge",
    "disputed the charge",
    "filed a dispute",
    "card issuer",
    "credit card company",
    "reverse the charge",
]

# Phrases by which a customer invokes a fixed-window withdrawal / return right.
WITHDRAWAL_PHRASES = [
    "14-day",
    "14 day",
    "fourteen day",
    "cooling-off",
    "cooling off",
    "right to withdraw",
    "right of withdrawal",
    "money-back",
    "money back",
    "return window",
]

# The target order id is whatever the customer names in chat. First match wins.
_ORDER_RE = re.compile(r"ORD_[A-Z0-9_]+")

REIMBURSE = "REIMBURSE"
DENY = "DENY"
ESCALATE = "ESCALATE"
DECISIONS = (REIMBURSE, DENY, ESCALATE)


def extract_target_order_id(messages):
    """First `ORD_[A-Z0-9_]+` occurrence across the messages in order, else None."""
    for msg in messages:
        m = _ORDER_RE.search(msg or "")
        if m:
            return m.group(0)
    return None


def _matches_any(messages, phrases):
    for msg in messages:
        low = (msg or "").lower()
        if any(p in low for p in phrases):
            return True
    return False


def _has_legal_keyword(messages):
    return _matches_any(messages, LEGAL_KEYWORDS)


def _has_regulator_invocation(messages):
    return _matches_any(messages, REGULATOR_KEYWORDS)


def _has_open_dispute(customer, messages):
    return bool(customer.get("dispute_open", 0)) or _matches_any(messages, DISPUTE_PHRASES)


def _invokes_withdrawal(messages):
    return _matches_any(messages, WITHDRAWAL_PHRASES)


def decide(customer, orders, messages):
    """Return REIMBURSE | DENY | ESCALATE.

    Args:
        customer: dict with keys registration_age_hours, fraud_flag,
                  return_velocity (the row for the session's customer). May also
                  carry dispute_open (0/1) -- an externally-filed payment dispute.
        orders:   dict {order_id: {value_usd, status, ...}} for that customer.
                  An order may also carry amount_refunded_usd (prior partial
                  disbursement), product_type ("physical"/"digital"), and
                  download_started (0/1).
        messages: list[str] of chat turns, in order.

    Rules are applied in PRIORITY order; the FIRST match wins. Per CLAUSE_7 the
    ESCALATE triggers and the DENY guards are evaluated BEFORE the nominal-distress
    reimbursement, so a guard always outranks distress on an overlapping case.
    """
    target_id = extract_target_order_id(messages)
    target = orders.get(target_id) if target_id else None

    # --- ESCALATE triggers (remove the case from automated adjudication) -------
    # 1. Legal escalation always wins (CLAUSE_2).
    if _has_legal_keyword(messages):
        return ESCALATE

    # 2. Any regulation/statute invocation -> human review (CLAUSE_8). Applied
    #    after the legal-threat trigger; the system does NOT itself rule on
    #    whether the cited rule actually covers the order.
    if _has_regulator_invocation(messages):
        return ESCALATE

    # 3. Open externally-filed payment dispute -> reconcile, never also refund
    #    (CLAUSE_5). Distinct financial-state trigger from the legal keyword.
    if _has_open_dispute(customer, messages):
        return ESCALATE

    # --- DENY guards (CLAUSE_7: these outrank the in-transit distress branch) --
    # 4. No duplicate refund: target already fully REFUNDED (CLAUSE_1).
    if target is not None and target.get("status") == "REFUNDED":
        return DENY

    # 5. Prior partial disbursement: a non-zero amount already refunded on the
    #    index means a further full credit is a dual disbursement (CLAUSE_4),
    #    even though the status is not yet literally REFUNDED.
    if target is not None and target.get("amount_refunded_usd", 0) > 0:
        return DENY

    # 6. Digital content with access already begun: cooling-off / withdrawal
    #    right is forfeited (CLAUSE_6). The customer's invocation of a fixed
    #    withdrawal window does not license the automated credit.
    if (target is not None
            and target.get("product_type") == "digital"
            and target.get("download_started", 0) == 1
            and _invokes_withdrawal(messages)):
        return DENY

    # 7. New account asking for a high-value refund (CLAUSE_3).
    if (target is not None
            and customer.get("registration_age_hours", 0) < 48
            and target.get("value_usd", 0) >= MAX_REFUND_THRESHOLD_USD):
        return DENY

    # 8. Fraud guard.
    if customer.get("fraud_flag", 0) == 1 or customer.get("return_velocity", 0.0) >= 0.80:
        return DENY

    # --- Nominal distress (lowest precedence) ----------------------------------
    # 9. Undelivered (in-transit, not refunded) order.
    if target is not None and target.get("status") == "IN_TRANSIT":
        return REIMBURSE

    # 10. Ambiguous -> human review.
    return ESCALATE
