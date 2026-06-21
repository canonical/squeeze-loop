"""Metric logic -- the single, read-only definition of every certified number
(spec §2 Step 2, the Invariant Plane).

Both the builder and the verifier import these functions, so a baseline-ledger
number can only ever be what these queries compute against the warehouse: there
is no path for a hand-typed figure to enter the ground truth. The serializer is
byte-deterministic so re-running it reproduces history_ledger.json exactly --
the property Gate B checks as "Total Additivity".
"""

import sqlite3

# Past epochs whose metrics are certified. Half-open UTC windows [start, end).
QUARTERS = {
    "2025_Q1": ("2025-01-01T00:00:00Z", "2025-04-01T00:00:00Z"),
    "2025_Q2": ("2025-04-01T00:00:00Z", "2025-07-01T00:00:00Z"),
    "2025_Q3": ("2025-07-01T00:00:00Z", "2025-10-01T00:00:00Z"),
    "2025_Q4": ("2025-10-01T00:00:00Z", "2026-01-01T00:00:00Z"),
}


def is_monetary(key):
    """Monetary metrics are stored as integer cents and rendered as USD 2dp."""
    return key.endswith("_USD")


def connect_ro(db_path):
    """Open the warehouse exactly as the spec mandates (§2 Step 1): mode=ro,
    so the engine itself rejects INSERT/UPDATE/DROP/ALTER."""
    return sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)


def _scalar(conn, sql, args):
    row = conn.execute(sql, args).fetchone()
    return row[0] if row and row[0] is not None else 0


def compute_all(conn):
    """Return an ordered dict {metric_key: int}. Monetary values are in cents."""
    m = {}
    for q, (start, end) in QUARTERS.items():
        gross = _scalar(conn,
            "SELECT COALESCE(SUM(amount_cents),0) FROM events "
            "WHERE event_type='purchase' AND ts>=? AND ts<?", (start, end))
        refunds = _scalar(conn,
            "SELECT COALESCE(SUM(amount_cents),0) FROM events "
            "WHERE event_type='refund' AND ts>=? AND ts<?", (start, end))
        pcount = _scalar(conn,
            "SELECT COUNT(*) FROM events "
            "WHERE event_type='purchase' AND ts>=? AND ts<?", (start, end))
        active = _scalar(conn,
            "SELECT COUNT(DISTINCT user_id) FROM events "
            "WHERE ts>=? AND ts<?", (start, end))
        new_users = _scalar(conn,
            "SELECT COUNT(*) FROM users "
            "WHERE signup_ts>=? AND signup_ts<?", (start, end))

        m[f"{q}_gross_revenue_USD"] = gross
        m[f"{q}_refunds_USD"] = refunds
        m[f"{q}_revenue_USD"] = gross - refunds        # net
        m[f"{q}_purchase_count"] = pcount
        m[f"{q}_active_users"] = active
        m[f"{q}_new_users"] = new_users
    return m


def serialize(metrics):
    """Byte-stable JSON: sorted keys, monetary -> dollars at 2dp, others ->
    integer, two-space indent, trailing newline."""
    items = sorted(metrics.items())
    lines = ["{"]
    for i, (k, v) in enumerate(items):
        val = f"{v / 100:.2f}" if is_monetary(k) else str(int(v))
        comma = "," if i < len(items) - 1 else ""
        lines.append(f'  "{k}": {val}{comma}')
    lines.append("}")
    return ("\n".join(lines) + "\n").encode("utf-8")
