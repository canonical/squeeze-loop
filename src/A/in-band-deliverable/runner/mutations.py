"""Mutation catalog (sentinel-side) for negative test cases.

Each entry is a deliberately clause-violating variant computation. A negative
test passes when the mutated value DIVERGES from the deliverable's correct value
over the same window -- proving the obligation clause is load-bearing (the
"proves WITH the clause, fails WITHOUT it" payoff). A mutation that never
diverges would mean the clause is vacuous, which the runner reports as a failure.

These live with the runner, not with either band: the implementer is blind to
them (it must not know how it is tested) and the exerciser only *names* a
mutation and predicts its fault site -- it does not execute one.
"""

from datetime import datetime, timedelta, timezone


def _scalar(conn, sql, args):
    return conn.execute(sql, args).fetchone()[0]


def _shift(ts, hours):
    dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return (dt + timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")


# --- METRIC_001 (Net Revenue) mutations -------------------------------------

def m_no_type_filter(conn, start, end):
    """CLAUSE_2 violation: sum ALL amounts with no event_type filter, so refunds
    are added instead of subtracted (gross + refunds)."""
    cents = _scalar(conn,
        "SELECT COALESCE(SUM(amount_cents),0) FROM events WHERE ts>=? AND ts<?",
        (start, end))
    return round(cents / 100.0, 2)


def m_omit_refund_subtraction(conn, start, end):
    """CLAUSE_3 violation: report gross purchase revenue, never subtracting refunds."""
    cents = _scalar(conn,
        "SELECT COALESCE(SUM(amount_cents),0) FROM events "
        "WHERE event_type='purchase' AND ts>=? AND ts<?", (start, end))
    return round(cents / 100.0, 2)


def m_local_tz_shift(conn, start, end):
    """CLAUSE_1 violation: bin by a local offset (US/Pacific, -8h) instead of UTC,
    so events near the quarter boundary fall in the wrong window."""
    s, e = _shift(start, -8), _shift(end, -8)
    cents = _scalar(conn,
        "SELECT COALESCE(SUM(CASE WHEN event_type='purchase' THEN amount_cents END),0)"
        "     - COALESCE(SUM(CASE WHEN event_type='refund'   THEN amount_cents END),0)"
        "  FROM events WHERE ts>=? AND ts<?", (s, e))
    return round(cents / 100.0, 2)


# --- METRIC_002 (Active Users) mutations ------------------------------------

def m_dedup_at_row_level(conn, start, end):
    """CLAUSE_1 violation: count raw event rows instead of DISTINCT user_id."""
    return int(_scalar(conn,
        "SELECT COUNT(*) FROM events WHERE ts>=? AND ts<?", (start, end)))


def m_join_exclude_deleted(conn, start, end):
    """CLAUSE_2 violation: inner-join users on deleted_ts IS NULL, dropping
    deleted-but-previously-active users (survivorship bias)."""
    return int(_scalar(conn,
        "SELECT COUNT(DISTINCT e.user_id) FROM events e "
        "JOIN users u ON e.user_id=u.user_id "
        "WHERE u.deleted_ts IS NULL AND e.ts>=? AND e.ts<?", (start, end)))


CATALOG = {
    "NO_TYPE_FILTER": m_no_type_filter,
    "OMIT_REFUND_SUBTRACTION": m_omit_refund_subtraction,
    "LOCAL_TZ_SHIFT": m_local_tz_shift,
    "DEDUP_AT_ROW_LEVEL": m_dedup_at_row_level,
    "JOIN_EXCLUDE_DELETED": m_join_exclude_deleted,
}


def apply(name, conn, start, end):
    if name not in CATALOG:
        raise KeyError(f"unknown mutation {name!r}")
    return CATALOG[name](conn, start, end)
