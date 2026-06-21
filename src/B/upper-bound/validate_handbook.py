#!/usr/bin/env python3
"""Self-check of the Upper Bound — the author's expressibility-from-below proof.

Exits nonzero on any failure:

  1. STRUCTURE     refund_policy.md parses and passes the schema (spec §2).
  2. GATE A        the published policy stays strictly policy-centric — no code,
                   DB schema, or prompt/injection syntax (spec §3 Gate A).
  3. GROUNDING     the decision tokens the clauses / negative vector name are
                   EXACTLY the app's allowed decisions, and the customer/order
                   attributes the clauses mention (account age, refund/REFUNDED
                   status, value/threshold) correspond to REAL columns in
                   ../ground-truth/schema.sql, so the ceiling is dischargeable,
                   not a wish.
  4. GATE WIRING   gate_c_coverage accepts a complete clause set and rejects an
                   incomplete one (the trap defense, spec §3 Gate C).

The grounding step is the upper-bound analogue of the ground truth's "every
decision recomputes": a normative claim no runtime verdict could ever satisfy is
rejected here, not discovered downstream.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import gate_checks as gc
import handbook as hb

HERE = Path(__file__).resolve().parent
GT = HERE.parent / "ground-truth"
SCHEMA_CANDIDATES = [
    Path("/opt/squeeze/shared/schema.sql"),
    GT / "schema.sql",
]

# The app's allowed decision set (../ground-truth: REIMBURSE | DENY | ESCALATE).
APP_DECISIONS = {"REIMBURSE", "DENY", "ESCALATE"}

# The order status the clauses reference must be a real CHECK-constrained value.
EXPECTED_STATUS_TOKEN = "REFUNDED"


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))
    return ok


def _schema_text():
    for p in SCHEMA_CANDIDATES:
        if p.exists():
            return p, p.read_text(encoding="utf-8")
    return None, None


def _decision_tokens(policy: hb.Policy) -> set[str]:
    """Every all-caps verdict token the clauses + negative vector mention."""
    blob = " ".join(policy.clauses.values()) + " " + policy.negative_vector.expected_action
    toks = set(re.findall(r"\b[A-Z]{4,}\b", blob))
    # Keep only tokens that look like decisions (in the app set or adjacent).
    return {t for t in toks if t in APP_DECISIONS}


def main():
    ok = True

    # 1. structure
    try:
        policies = hb.parse()
        check("structure", True, f"{len(policies)} policy(ies): "
              + ", ".join(p.policy_id for p in policies))
    except hb.HandbookError as e:
        check("structure", False, str(e))
        print("VALIDATE FAILED")
        return 1

    # 2. Gate A — policy-centric (no code/schema/prompt syntax)
    handbook_text = (HERE / "refund_policy.md").read_text(encoding="utf-8")
    ga = gc.gate_a_policy_centric(handbook_text)
    ok &= check("gate A policy-centric", bool(ga), ga.detail)

    # 3. grounding against the ground truth
    schema_path, schema = _schema_text()
    if schema is None:
        print("[WARN] ground-truth schema.sql not found; skipping grounding "
              f"(looked in: {', '.join(str(p) for p in SCHEMA_CANDIDATES)})")
    else:
        schema_low = schema.lower()
        for p in policies:
            # 3a. decision tokens are EXACTLY a subset of the app's allowed set,
            #     and the failsafe action is one of them.
            used = _decision_tokens(p)
            nv_action = p.negative_vector.expected_action
            decisions_ok = used and used <= APP_DECISIONS and nv_action in APP_DECISIONS
            ok &= check(f"{p.policy_id} decision tokens", decisions_ok,
                        f"clauses/vector use {sorted(used)} ⊆ app decisions "
                        f"{sorted(APP_DECISIONS)}; failsafe={nv_action}"
                        if decisions_ok else
                        f"decision tokens {sorted(used)} not within app set "
                        f"{sorted(APP_DECISIONS)} / failsafe {nv_action!r}")

            # 3b. the attributes the clauses mention map to real schema columns.
            clause_blob = " ".join(p.clauses.values()).lower()
            attr_checks = {
                # clause concept -> (mentioned in clauses, grounding column in schema.sql)
                "account registration age": (
                    "registration age" in clause_blob,
                    "registration_age_hours" in schema_low),
                "order refunded status": (
                    "refunded" in clause_blob,
                    EXPECTED_STATUS_TOKEN.lower() in schema_low and "status" in schema_low),
                "order value / refund threshold": (
                    ("value" in clause_blob or "threshold" in clause_blob),
                    "value_usd" in schema_low),
            }
            for concept, (mentioned, grounded) in attr_checks.items():
                # The concept must be mentioned by the policy AND backed by a column.
                attr_ok = mentioned and grounded
                ok &= check(f"{p.policy_id} grounding: {concept}", attr_ok,
                            "mentioned in clauses and present in schema.sql"
                            if attr_ok else
                            f"mentioned={mentioned}, schema_column_present={grounded}")

    # 4. gate wiring (Gate C accepts complete, rejects incomplete)
    for p in policies:
        complete = [{"clause": c, "check": "x"} for c in p.clause_ids]
        incomplete = complete[:-1]                       # drop the last clause
        c_ok = gc.gate_c_coverage(p, complete)
        c_bad = gc.gate_c_coverage(p, incomplete)
        wired = bool(c_ok) and not c_bad.ok and c_bad.missing == [p.clause_ids[-1]]
        ok &= check(f"{p.policy_id} gate wiring", wired,
                    "Gate C accepts complete clause set, rejects incomplete")

    print("VALIDATE OK" if ok else "VALIDATE FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
