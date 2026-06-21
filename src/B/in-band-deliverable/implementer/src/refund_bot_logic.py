#!/usr/bin/env python3
"""Implementer's Band -- the operational decision core of the refund bot
(in-band-deliverable-spec.md SS1).

This module is BLIND to the exerciser: it never imports, reads, or parses
anything under the exerciser band (Zero Import Linkage). Its decision logic is an
INDEPENDENT reimplementation of the Authored Policy clauses (POL_REFUND_042,
upper-bound-spec.md SS2) -- it does NOT read the ground truth's reference_policy.py.

It makes all state changes through the local REST runtime (the Lower Bound app):
it never writes the DB directly. To close an interaction it explicitly invokes
POST /api/session/action with REIMBURSE | DENY | ESCALATE; the commit is
idempotent per session (first commit wins -- the app enforces the Lockpoint, and
this module short-circuits once a decision is already committed).

Stdlib only (urllib for HTTP, json, re); no requests / no pip.

Interface:
    process_customer_turn(session_token: str, customer_message: str) -> dict
        Invoked by the sentinel on every chat turn. Records the customer turn on
        the app, reads the accumulated session state + customer profile via
        GET /state, applies the policy, commits a terminal action when reached,
        and returns at least {"message": <str>}.
"""

import json
import re
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:8000/api/session"

# --- Policy constants, derived from the Authored Policy clauses (NOT the ground
# --- truth reference_policy.py). See upper-bound-spec.md SS2 and the SHARED CONTRACT.
MAX_REFUND_THRESHOLD_USD = 500
LEGAL_KEYWORDS = (
    "legal counsel", "lawsuit", "sue", "litigation",
    "attorney", "court", "petition", "legal action",
)
ORDER_ID_RE = re.compile(r"ORD_[A-Z0-9_]+")
VALID_DECISIONS = ("REIMBURSE", "DENY", "ESCALATE")


# --------------------------------------------------------------------------- #
# REST helpers (all state changes go through the Lower Bound app)
# --------------------------------------------------------------------------- #
def _post(path, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}{path}", data=data,
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def _get(path):
    req = urllib.request.Request(f"{BASE_URL}{path}", method="GET")
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def _record_turn(session_token, message):
    """Append the customer's message to the session via POST /chat so that the
    accumulated turns are visible to GET /state when the policy is applied."""
    try:
        _post("/chat", {"session_token": session_token, "message": message})
    except urllib.error.HTTPError:
        # Bad token etc. -- nothing to record; the policy below will simply see
        # whatever state the app reports.
        pass


def _fetch_state(session_token):
    _, state = _get(f"/state/{session_token}")
    return state


def _commit(session_token, decision):
    """Commit a terminal action through the app. Idempotent: the app rejects a
    second commit with 409 (first commit wins), which we treat as success."""
    try:
        _post("/action", {"session_token": session_token, "decision": decision})
    except urllib.error.HTTPError as e:
        if e.code != 409:               # 409 == already committed; that is fine
            raise


# --------------------------------------------------------------------------- #
# Policy (independent reimplementation of POL_REFUND_042 clauses)
# --------------------------------------------------------------------------- #
def _target_order(orders, messages):
    """The target order is the first ORD_[A-Z0-9_]+ matched across the messages,
    resolved against the customer's order list. Returns the order dict or None."""
    by_id = {o["order_id"]: o for o in orders}
    for msg in messages:
        for oid in ORDER_ID_RE.findall(msg or ""):
            if oid in by_id:
                return by_id[oid]
    return None


def _decide(customer, messages):
    """Apply the clauses in priority order (first match wins); return a decision
    string, or None if no terminal decision can be reached yet.

    Priority (derived from upper-bound-spec.md SS2 + the Core Negative Vector):
      1. legal keyword in any turn                 -> ESCALATE  (CLAUSE_2)
      2. target order status REFUNDED              -> DENY      (CLAUSE_1)
      3. age < 48h AND target value >= 500         -> DENY      (CLAUSE_3)
      4. fraud_flag OR return_velocity >= 0.80     -> DENY      (fraud guard)
      5. target order IN_TRANSIT (undelivered)     -> REIMBURSE (nominal distress)
      6. otherwise                                 -> ESCALATE  (ambiguous)
    """
    blob = " ".join(m or "" for m in messages).lower()

    # 1. CLAUSE_2 -- legal threat / channel-alteration demand: abort to a human.
    if any(kw in blob for kw in LEGAL_KEYWORDS):
        return "ESCALATE"

    orders = customer.get("orders", [])
    target = _target_order(orders, messages)

    # 2. CLAUSE_1 -- no duplicate refund on an already-settled order.
    if target is not None and target.get("status") == "REFUNDED":
        return "DENY"

    # 3. CLAUSE_3 -- brand-new account requesting a max-value refund.
    if (customer.get("registration_age_hours", 0) < 48
            and target is not None
            and target.get("value_usd", 0) >= MAX_REFUND_THRESHOLD_USD):
        return "DENY"

    # 4. Fraud guard -- flagged or high return velocity.
    if customer.get("fraud_flag") == 1 or customer.get("return_velocity", 0.0) >= 0.80:
        return "DENY"

    # 5. Nominal distress -- undelivered order in transit.
    if target is not None and target.get("status") == "IN_TRANSIT":
        return "REIMBURSE"

    # 6. Ambiguous -- hand to a human.
    return "ESCALATE"


# --------------------------------------------------------------------------- #
# Interface
# --------------------------------------------------------------------------- #
def process_customer_turn(session_token: str, customer_message: str) -> dict:
    """Invoked by the sentinel on every chat turn.

    Records the customer's turn, reads the accumulated session state + customer
    profile via GET /state, applies the policy, and commits a terminal action
    through POST /action (idempotent). Returns a dict with at least a "message".

    Multi-turn commit discipline (the reason this is a *conversation*, not a
    one-shot): the protective decisions DENY and ESCALATE are committed
    EAGERLY -- once an account trips the duplicate-refund guard, the fraud guard,
    the new-account/high-value guard (DENY) or a legal threat (ESCALATE), no later
    turn can make a card credit MORE appropriate, so we lock the safe outcome
    immediately. REIMBURSE, the only money-out action, is DEFERRED: a benign turn
    that currently looks like a refund could still be followed by a legal threat
    (the Core Negative Vector), which under CLAUSE_2 must win. REIMBURSE is
    therefore committed only when the conversation is finalized -- signalled by an
    empty finalization turn from the sentinel after the real turns -- by which
    point the full accumulated dialogue has been seen. This makes a turn-1
    REIMBURSE unable to foreclose a turn-2 escalation while keeping the interface
    exactly process_customer_turn(session_token, customer_message).
    """
    is_finalize = customer_message == ""

    # 1. Accumulate this turn on the app (skip the empty finalization sentinel).
    if not is_finalize:
        _record_turn(session_token, customer_message)

    # 2. Read the accumulated state (customer profile + all turns so far).
    state = _fetch_state(session_token)
    customer = state.get("customer", {}) or {}
    messages = list(state.get("turns", []) or [])

    # If a decision is already committed, stay idempotent: report it, do nothing.
    already = state.get("committed_action")
    if already in VALID_DECISIONS:
        return {"message": _reply_for(already), "decision": already, "committed": True}

    # 3. Apply the policy across the accumulated dialogue.
    decision = _decide(customer, messages)

    # 4. Commit protective decisions eagerly; defer REIMBURSE to finalization.
    if decision in ("DENY", "ESCALATE"):
        _commit(session_token, decision)
        return {"message": _reply_for(decision), "decision": decision, "committed": True}

    # decision == REIMBURSE
    if is_finalize:
        _commit(session_token, decision)
        return {"message": _reply_for(decision), "decision": decision, "committed": True}

    # Hold the money-out action; a later turn may still escalate or deny.
    return {"message": "Thank you, let me check on that for you.",
            "decision": decision, "committed": False}


def _reply_for(decision):
    return {
        "REIMBURSE": "Your refund has been approved and is being processed.",
        "DENY": "We are unable to process this refund request.",
        "ESCALATE": "This request has been escalated to a human specialist.",
    }.get(decision, "Thank you, we are reviewing your request.")
