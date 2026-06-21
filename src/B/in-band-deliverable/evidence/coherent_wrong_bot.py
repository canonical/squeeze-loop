#!/usr/bin/env python3
"""Negative control -- a deliberately COHERENT-AND-WRONG refund bot.

It honours the interface contract perfectly (same process_customer_turn signature,
records the turn, reads /state, commits through POST /action -- never the DB) and
is internally consistent, but it IGNORES the policy clauses: it always REIMBURSE,
so it fails the legal-threat rule (CLAUSE_2), the duplicate-refund rule
(CLAUSE_1), the new-account high-value rule (CLAUSE_3) and the fraud guard.

The runner can load this instead of the real implementer (--bad) to demonstrate
that GATE B catches a plausible-but-wrong bot rather than rubber-stamping it.

Stdlib only.
"""

import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:8000/api/session"

VALID_DECISIONS = ("REIMBURSE", "DENY", "ESCALATE")


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


def _commit(session_token, decision):
    try:
        _post("/action", {"session_token": session_token, "decision": decision})
    except urllib.error.HTTPError as e:
        if e.code != 409:
            raise


def process_customer_turn(session_token: str, customer_message: str) -> dict:
    is_finalize = customer_message == ""

    # Record the turn (well-behaved on the surface)...
    if not is_finalize:
        try:
            _post("/chat", {"session_token": session_token, "message": customer_message})
        except urllib.error.HTTPError:
            pass

    _, state = _get(f"/state/{session_token}")
    already = state.get("committed_action")
    if already in VALID_DECISIONS:
        return {"message": "Already handled.", "decision": already, "committed": True}

    # ...but always approve at finalization, regardless of legal threats, fraud,
    # or duplicates. This is internally consistent yet ignores every clause, so
    # GATE B must reject it on the legal-threat / fraud / duplicate scenarios.
    if is_finalize:
        _commit(session_token, "REIMBURSE")
        return {"message": "Your refund has been approved!",
                "decision": "REIMBURSE", "committed": True}
    return {"message": "Sure, one moment.", "decision": "REIMBURSE", "committed": False}
