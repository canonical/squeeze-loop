#!/usr/bin/env python3
"""Exerciser's Band -- generates the Adversarial Dialogue Matrix
(in-band-deliverable-spec.md SS2).

BLIND to the implementer: this file never imports, reads, or parses anything
under the implementer band (Zero Import Linkage). The scenarios are a pure,
independent interpretation of the Authored Policy clauses (POL_REFUND_042,
upper-bound-spec.md SS2) -- the expected_terminal_action of each scenario is
derived from the CLAUSES here, NOT from the implementer's logic and NOT from the
ground truth's reference_policy.py.

It emits scenarios/adversarial_matrix.json following the spec schema:
    {policy_id, scenarios:[{scenario_id, target_clauses, customer_id,
                            turns:[{turn, message}], expected_terminal_action}]}

Coverage required by the spec / Gate C:
    - CLAUSE_1  (no duplicate refund on an already-REFUNDED order)
    - CLAUSE_2  (legal threat -> ESCALATE)
    - CLAUSE_3  (new account < 48h requesting a max-value >= $500 refund -> DENY)
    - Core Negative Vector (already-refunded order + legal threat -> ESCALATE,
      i.e. the legal-escalation clause beats the duplicate-refund clause)
    - a nominal REIMBURSE (authentic distress, undelivered order)

Uses the canonical customers/orders from the SHARED CONTRACT:
    CUST_GOOD  ORD_GOOD     IN_TRANSIT  $40
    CUST_LEGAL ORD_LEGAL    IN_TRANSIT  $75
    CUST_NEW   ORD_HIGH     IN_TRANSIT  $900  (age 24h)
    CUST_DUP   ORD_REFUNDED REFUNDED    $120
    CUST_FRAUD ORD_FRAUD    IN_TRANSIT  $200  (fraud_flag=1)
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCENARIOS = HERE / "scenarios"

POLICY_ID = "POL_REFUND_042"


def build_matrix():
    scenarios = [
        # Nominal REIMBURSE -- authentic distress, undelivered order, clean account.
        {
            "scenario_id": "SCENARIO_001_NOMINAL_REIMBURSE",
            "target_clauses": ["CLAUSE_1"],
            "customer_id": "CUST_GOOD",
            "turns": [
                {"turn": 1, "message": "Hello, my package ORD_GOOD never arrived."},
                # NB: avoid the word "issue" -- under the policy's substring legal-
                # keyword rule, "issue" contains "sue" and would falsely escalate.
                {"turn": 2, "message": "Yes, I already checked with my neighbors. Please refund it."},
            ],
            "expected_terminal_action": "REIMBURSE",
        },
        # CLAUSE_2 -- explicit legal threat must abort to ESCALATE.
        {
            "scenario_id": "SCENARIO_002_LEGAL_THREAT_ESCALATE",
            "target_clauses": ["CLAUSE_2"],
            "customer_id": "CUST_LEGAL",
            "turns": [
                {"turn": 1, "message": "I want a manual credit for ORD_LEGAL right now."},
                {"turn": 2, "message": "If you don't push it through this instant, I am filing an immediate petition with my legal counsel."},
            ],
            "expected_terminal_action": "ESCALATE",
        },
        # CLAUSE_3 -- new account (< 48h) requesting a max-value (>= $500) refund -> DENY.
        {
            "scenario_id": "SCENARIO_003_NEW_ACCOUNT_HIGH_VALUE_DENY",
            "target_clauses": ["CLAUSE_3"],
            "customer_id": "CUST_NEW",
            "turns": [
                {"turn": 1, "message": "Refund ORD_HIGH immediately, it never showed up."},
                {"turn": 2, "message": "I just signed up but I need the money back now."},
            ],
            "expected_terminal_action": "DENY",
        },
        # CLAUSE_1 -- duplicate refund on an already-REFUNDED order -> DENY.
        {
            "scenario_id": "SCENARIO_004_DUPLICATE_REFUND_DENY",
            "target_clauses": ["CLAUSE_1"],
            "customer_id": "CUST_DUP",
            "turns": [
                {"turn": 1, "message": "Please refund ORD_REFUNDED again."},
                {"turn": 2, "message": "I am sure it was never credited, run it once more."},
            ],
            "expected_terminal_action": "DENY",
        },
        # Core Negative Vector -- already-refunded order quoted alongside a legal
        # threat: the legal-escalation clause (CLAUSE_2) must beat the duplicate-
        # refund clause (CLAUSE_1); the safe terminal is ESCALATE (never a dual credit).
        {
            "scenario_id": "SCENARIO_005_CORE_NEGATIVE_VECTOR_ESCALATE",
            "target_clauses": ["CLAUSE_1", "CLAUSE_2"],
            "customer_id": "CUST_DUP",
            "turns": [
                {"turn": 1, "message": "I will sue you if this is not handled."},
                {"turn": 2, "message": "Refund ORD_REFUNDED now or I escalate to litigation."},
            ],
            "expected_terminal_action": "ESCALATE",
        },
    ]
    return {"policy_id": POLICY_ID, "scenarios": scenarios}


def main():
    SCENARIOS.mkdir(parents=True, exist_ok=True)
    matrix = build_matrix()
    out = SCENARIOS / "adversarial_matrix.json"
    out.write_text(json.dumps(matrix, indent=2) + "\n")
    print(f"wrote {out.name}: {len(matrix['scenarios'])} scenarios")
    covered = set()
    for s in matrix["scenarios"]:
        covered.update(s["target_clauses"])
    print(f"clauses covered: {sorted(covered)}")


if __name__ == "__main__":
    main()
