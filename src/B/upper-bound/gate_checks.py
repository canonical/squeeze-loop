"""Upper-bound-driven gate primitives (spec §3): how the handbook drives the
gates. These are the structural checks `gate_sentinel.py` runs; they read the
ceiling and refuse a non-policy-centric handbook or a test matrix that does not
account for every obligation clause.

Gate A — Structural Content Integrity: the property author must keep the handbook
          strictly policy-centric (WHAT, never HOW). The compilation track is
          blocked if the file injects code fragments, database schema
          assumptions, or direct prompting / injection syntax.
Gate C — Structural Coverage Map: the exerciser's validation_matrix.json must map
          a unique, non-trivial validation case to every CLAUSE_n. A clause with
          no covering case fails the entire build, even if all dialogue flows ran
          cleanly (the trap defense — a quietly dropped CLAUSE_2 escalation rule).

validation_matrix.json schema (written by the exerciser):
    [
      {"name": "...", "clauses": ["CLAUSE_1"], "check": "<non-empty>", ...},
      {"name": "...", "clause":  "CLAUSE_2",   "check": "<non-empty>", ...}
    ]
A case covers a clause only if it names the clause AND carries a non-empty
`check` (a generic/sweeping case with no concrete check does not count).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import handbook as hb


# Forbidden markers (spec §3 Gate A): code fragments, DB schema assumptions, and
# direct prompt / injection syntax. Presence of any => not policy-centric.
_FORBIDDEN = [
    ("```", "fenced code block"),
    ("SELECT ", "SQL query"),
    ("CREATE TABLE", "DB schema (DDL)"),
    ("INSERT INTO", "SQL DML"),
    ("def ", "Python function definition"),
    ("import ", "Python import"),
    ("system prompt:", "prompt-injection syntax"),
    ("ignore previous instructions", "prompt-injection syntax"),
]


@dataclass(frozen=True)
class GateResult:
    ok: bool
    gate: str
    subject: str            # policy id, or "<file>" for the file-level Gate A check
    missing: list[str]      # clause ids not covered (Gate C) / forbidden hits (Gate A)
    detail: str = ""

    def __bool__(self) -> bool:
        return self.ok


def gate_a_policy_centric(text: str, subject: str = "<refund_policy.md>") -> GateResult:
    """Fail if the policy text contains code, DB schema, or prompt/injection
    syntax — enforcing 'what, never how' (spec §3 Gate A).

    Markers are searched case-insensitively, ignoring HTML comments (the
    handbook's authoring notes are not part of the published normative body, but
    we still forbid the dangerous markers everywhere to be conservative)."""
    low = text.lower()
    hits = sorted({label for marker, label in _FORBIDDEN if marker.lower() in low})
    ok = not hits
    return GateResult(ok, "A", subject, hits,
                      "policy-centric (no code/schema/prompt syntax)"
                      if ok else f"non-policy-centric: contains {hits}")


def _clauses_in_case(c: dict) -> list[str]:
    if "clauses" in c:
        return list(c["clauses"])
    if "clause" in c:
        return [c["clause"]]
    return []


def gate_c_coverage(policy: hb.Policy, validation_matrix: list[dict]) -> GateResult:
    """Every CLAUSE_n of `policy` must be covered by a non-trivial validation case.
    Returns the missing set (empty => Gate C passes)."""
    covered: set[str] = set()
    for c in validation_matrix:
        if not isinstance(c, dict):
            continue
        if not str(c.get("check", "")).strip():     # trivial / no concrete check
            continue
        covered.update(_clauses_in_case(c))
    missing = [cid for cid in policy.clause_ids if cid not in covered]
    ok = not missing
    return GateResult(ok, "C", policy.policy_id, missing,
                      "every clause has a targeted validation case"
                      if ok else f"uncovered {missing}")


if __name__ == "__main__":
    policies = hb.parse()
    p = hb.by_id(policies, "POL_REFUND_042")

    # Gate A on the real handbook (should pass) and on an injected snippet.
    from pathlib import Path
    real = Path(__file__).resolve().parent / "refund_policy.md"
    print("Gate A real :", gate_a_policy_centric(real.read_text()))
    print("Gate A inject:", gate_a_policy_centric(
        "CLAUSE_1: run\n```sql\nSELECT * FROM orders;\n```", "<malicious>"))

    good_matrix = [
        {"name": "already-refunded blocked", "clause": "CLAUSE_1", "check": "status REFUNDED -> not REIMBURSE"},
        {"name": "legal threat escalates",   "clause": "CLAUSE_2", "check": "lawsuit -> ESCALATE"},
        {"name": "new high-value denied",    "clause": "CLAUSE_3", "check": "age<48 & value>=500 -> DENY"},
    ]
    bad_matrix = [
        {"name": "smoke", "check": "runs"},                       # maps to nothing
        {"name": "refunded", "clause": "CLAUSE_1", "check": ""},  # trivial
    ]
    print("Gate C good:", gate_c_coverage(p, good_matrix))
    print("Gate C bad :", gate_c_coverage(p, bad_matrix))
