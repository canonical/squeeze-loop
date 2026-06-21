#!/usr/bin/env python3
"""Exerciser's Band -- generates the Validation Matrix (in-band-deliverable-spec §2).

Blind to the implementer: this reads ONLY the read-only warehouse and the Metric
Handbook clause ids; it never imports or reads anything under the implementer
band. Its expected values are an INDEPENDENT interpretation of the handbook,
computed here (not hand-typed), so they can collide with the implementer's output
in the sandbox.

For each metric it emits exerciser/tests/validation_matrix.<METRIC_ID>.json with
`positives` (correct values per quarter) and `negatives` (a named mutation per
obligation clause, with a window chosen to actually contain that clause's edge
case so the negative is non-vacuous).
"""

import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT_A = HERE.parents[1]                       # src/A
TESTS = HERE / "tests"

QUARTERS = {
    "2025_Q1": ("2025-01-01T00:00:00Z", "2025-04-01T00:00:00Z"),
    "2025_Q2": ("2025-04-01T00:00:00Z", "2025-07-01T00:00:00Z"),
    "2025_Q3": ("2025-07-01T00:00:00Z", "2025-10-01T00:00:00Z"),
    "2025_Q4": ("2025-10-01T00:00:00Z", "2026-01-01T00:00:00Z"),
}


def find_db():
    for p in (Path("/opt/squeeze/shared/base_warehouse.db"),
              ROOT_A / "ground-truth" / "shared" / "base_warehouse.db"):
        if p.exists():
            return p
    sys.exit("error: base_warehouse.db not found")


def _net_revenue(conn, s, e):
    c = conn.execute(
        "SELECT COALESCE(SUM(CASE WHEN event_type='purchase' THEN amount_cents END),0)"
        "     - COALESCE(SUM(CASE WHEN event_type='refund'   THEN amount_cents END),0)"
        "  FROM events WHERE ts>=? AND ts<?", (s, e)).fetchone()[0]
    return round(c / 100.0, 2)


def _active_users(conn, s, e):
    return int(conn.execute(
        "SELECT COUNT(DISTINCT user_id) FROM events WHERE ts>=? AND ts<?",
        (s, e)).fetchone()[0])


def _quarter_has_refunds(conn, s, e):
    return _scalar(conn, "SELECT COUNT(*) FROM events WHERE event_type='refund' AND ts>=? AND ts<?", (s, e)) > 0


def _quarter_has_repeat_user(conn, s, e):
    return _scalar(conn,
        "SELECT COUNT(*) FROM (SELECT user_id FROM events WHERE ts>=? AND ts<? "
        "GROUP BY user_id HAVING COUNT(*)>1)", (s, e)) > 0


def _quarter_has_deleted_active(conn, s, e):
    # a user active in-window whose row carries a deleted_ts (survivorship case)
    return _scalar(conn,
        "SELECT COUNT(DISTINCT e.user_id) FROM events e JOIN users u ON e.user_id=u.user_id "
        "WHERE u.deleted_ts IS NOT NULL AND e.ts>=? AND e.ts<?", (s, e)) > 0


def _scalar(conn, sql, args):
    return conn.execute(sql, args).fetchone()[0]


def _first_quarter(conn, predicate):
    for q, (s, e) in QUARTERS.items():
        if predicate(conn, s, e):
            return q, s, e
    return None


def build_metric_001(conn):
    positives = []
    for q, (s, e) in QUARTERS.items():
        positives.append({
            "test_case_id": f"TC_M001_{q}_STANDARD_RUN",
            "description": f"Net revenue over the clean UTC window {q}.",
            "window": {"start": s, "end": e},
            "target_clauses": ["CLAUSE_1", "CLAUSE_2", "CLAUSE_3"],
            "expected_output": {"value": _net_revenue(conn, s, e)},
        })

    negatives = []
    # CLAUSE_2: a quarter with refunds, so "sum all, no type filter" inflates.
    qref = _first_quarter(conn, _quarter_has_refunds)
    if qref:
        q, s, e = qref
        negatives.append({
            "test_case_id": "TC_M001_NO_TYPE_FILTER",
            "description": "Summing all amounts without an event_type filter adds refunds instead of subtracting them.",
            "window": {"start": s, "end": e},
            "target_clauses": ["CLAUSE_2"],
            "mutation": "NO_TYPE_FILTER",
            "expected_fault": {"site": "event_type_filter_block", "reason": "DIVERGENT_VALUE_ERROR"},
        })
        negatives.append({
            "test_case_id": "TC_M001_OMIT_REFUND_SUBTRACTION",
            "description": "Reporting gross purchase revenue without subtracting refunds over-reports the figure.",
            "window": {"start": s, "end": e},
            "target_clauses": ["CLAUSE_3"],
            "mutation": "OMIT_REFUND_SUBTRACTION",
            "expected_fault": {"site": "refund_subtraction_block", "reason": "DIVERGENT_VALUE_ERROR"},
        })
    # CLAUSE_1: Q2 carries the quarter-boundary witnesses; a local-tz shift moves them.
    s, e = QUARTERS["2025_Q2"]
    negatives.append({
        "test_case_id": "TC_M001_LOCAL_TZ_SHIFT",
        "description": "Binning by a local (-8h) offset instead of UTC moves boundary events into the wrong quarter.",
        "window": {"start": s, "end": e},
        "target_clauses": ["CLAUSE_1"],
        "mutation": "LOCAL_TZ_SHIFT",
        "expected_fault": {"site": "utc_window_block", "reason": "DIVERGENT_VALUE_ERROR"},
    })
    return {"metric_id": "METRIC_001", "positives": positives, "negatives": negatives}


def build_metric_002(conn):
    positives = []
    for q, (s, e) in QUARTERS.items():
        positives.append({
            "test_case_id": f"TC_M002_{q}_STANDARD_RUN",
            "description": f"Distinct active users over the clean UTC window {q}.",
            "window": {"start": s, "end": e},
            "target_clauses": ["CLAUSE_1", "CLAUSE_2"],
            "expected_output": {"value": _active_users(conn, s, e)},
        })

    negatives = []
    # CLAUSE_1: a quarter where some user has >1 event, so COUNT(*) != COUNT(DISTINCT).
    qrep = _first_quarter(conn, _quarter_has_repeat_user)
    if qrep:
        q, s, e = qrep
        negatives.append({
            "test_case_id": "TC_M002_DEDUP_AT_ROW_LEVEL",
            "description": "Counting raw event rows instead of distinct user_id over-reports activity.",
            "window": {"start": s, "end": e},
            "target_clauses": ["CLAUSE_1"],
            "mutation": "DEDUP_AT_ROW_LEVEL",
            "expected_fault": {"site": "user_id_dedup_block", "reason": "DIVERGENT_VALUE_ERROR"},
        })
    # CLAUSE_2: a quarter with a deleted-but-active user, so the deleted-join drops them.
    qdel = _first_quarter(conn, _quarter_has_deleted_active)
    if qdel:
        q, s, e = qdel
        negatives.append({
            "test_case_id": "TC_M002_JOIN_EXCLUDE_DELETED",
            "description": "Inner-joining users on deleted_ts IS NULL drops deleted-but-previously-active users (survivorship bias).",
            "window": {"start": s, "end": e},
            "target_clauses": ["CLAUSE_2"],
            "mutation": "JOIN_EXCLUDE_DELETED",
            "expected_fault": {"site": "survivorship_filter_block", "reason": "DIVERGENT_VALUE_ERROR"},
        })
    return {"metric_id": "METRIC_002", "positives": positives, "negatives": negatives}


def main():
    TESTS.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(f"file:{find_db()}?mode=ro", uri=True)
    try:
        matrices = [build_metric_001(conn), build_metric_002(conn)]
    finally:
        conn.close()

    for matrix in matrices:
        mid = matrix["metric_id"]
        out = TESTS / f"validation_matrix.{mid}.json"
        out.write_text(json.dumps(matrix, indent=2, sort_keys=True) + "\n")
        # Honour the spec's canonical filename for the first metric.
        if mid == "METRIC_001":
            (TESTS / "validation_matrix.json").write_text(
                json.dumps(matrix, indent=2, sort_keys=True) + "\n")
        print(f"wrote {out.name}: {len(matrix['positives'])} positives, "
              f"{len(matrix['negatives'])} negatives")


if __name__ == "__main__":
    main()
