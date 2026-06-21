"""Upper-bound-driven gate primitives (spec §3): how the handbook drives the
gates. These are the structural checks `gate_sentinel.py` runs; they read the
ceiling and refuse plans/tests that do not account for every obligation clause.

Gate A — Plan Validation: the Coordinator's spec-N.md must explicitly cite every
          CLAUSE_X of the active metric, so no obligation is silently dropped.
Gate C — Coherent-and-Wrong Guard: the exerciser's assertions.json must contain a
          targeted, non-trivial test mapped to every CLAUSE_X. A clause with no
          covering assertion fails the build even if the SQL ran cleanly.

assertions.json schema (written by the exerciser):
    [
      {"name": "...", "clauses": ["CLAUSE_1"], "check": "<non-empty>", ...},
      {"name": "...", "clause":  "CLAUSE_2",   "check": "<non-empty>", ...}
    ]
An assertion covers a clause only if it names the clause AND carries a non-empty
`check` (a generic/sweeping assertion with no concrete check does not count).
"""

from __future__ import annotations

from dataclasses import dataclass

import handbook as hb


@dataclass(frozen=True)
class GateResult:
    ok: bool
    gate: str
    metric_id: str
    missing: list[str]      # clause ids not cited / not covered
    detail: str = ""

    def __bool__(self) -> bool:
        return self.ok


def _clauses_in_assertion(a: dict) -> list[str]:
    if "clauses" in a:
        return list(a["clauses"])
    if "clause" in a:
        return [a["clause"]]
    return []


def gate_a_plan(metric: hb.Metric, plan_text: str) -> GateResult:
    """Every CLAUSE_X of `metric` must appear verbatim in the plan text."""
    missing = [cid for cid in metric.clause_ids if cid not in plan_text]
    ok = not missing
    return GateResult(ok, "A", metric.metric_id, missing,
                      "all clauses cited" if ok else f"plan omits {missing}")


def gate_c_assertions(metric: hb.Metric, assertions: list[dict]) -> GateResult:
    """Every CLAUSE_X must be covered by a non-trivial assertion."""
    covered: set[str] = set()
    for a in assertions:
        if not isinstance(a, dict):
            continue
        if not str(a.get("check", "")).strip():     # trivial / no concrete check
            continue
        covered.update(_clauses_in_assertion(a))
    missing = [cid for cid in metric.clause_ids if cid not in covered]
    ok = not missing
    return GateResult(ok, "C", metric.metric_id, missing,
                      "every clause has a targeted test" if ok else f"uncovered {missing}")


if __name__ == "__main__":
    # Pilot: exercise both gates on METRIC_001 with a good and a bad input.
    metrics = hb.parse()
    m = hb.by_id(metrics, "METRIC_001")

    good_plan = "Plan: handle CLAUSE_1 (UTC), CLAUSE_2 (filter type), CLAUSE_3 (refunds)."
    bad_plan = "Plan: handle CLAUSE_1 and CLAUSE_2."  # drops CLAUSE_3
    print("Gate A good:", gate_a_plan(m, good_plan))
    print("Gate A bad :", gate_a_plan(m, bad_plan))

    good_assertions = [
        {"name": "q1 boundary", "clauses": ["CLAUSE_1"], "check": "Q1 == 1987.21"},
        {"name": "no logins", "clause": "CLAUSE_2", "check": "logins excluded"},
        {"name": "refunds subtracted", "clause": "CLAUSE_3", "check": "net < gross"},
    ]
    bad_assertions = [
        {"name": "smoke", "check": "runs"},                      # maps to nothing
        {"name": "boundary", "clauses": ["CLAUSE_1"], "check": ""},  # trivial
    ]
    print("Gate C good:", gate_c_assertions(m, good_assertions))
    print("Gate C bad :", gate_c_assertions(m, bad_assertions))
