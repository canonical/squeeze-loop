#!/usr/bin/env python3
"""Implementer's Band -- the analytical engine (in-band-deliverable-spec §1).

Stateless and blind to how it is tested. It reads ONLY the read-only warehouse
and its own CLI/env arguments; it never imports, reads, or parses anything under
the exerciser band (Zero Import Linkage). It emits exactly one JSON object on
stdout -- no log prose.

Window convention: half-open [START_DATE, END_DATE) in UTC, matching the Metric
Handbook (CLAUSE_1: quarter boundaries evaluated strictly in UTC). For a quarter,
END_DATE is the next quarter's 00:00:00Z.
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path


def find_db():
    for p in (Path("/opt/squeeze/shared/base_warehouse.db"),
              Path(__file__).resolve().parents[3] / "ground-truth" / "shared" / "base_warehouse.db"):
        if p.exists():
            return p
    sys.exit("error: base_warehouse.db not found")


def compute(conn, metric_id, start, end):
    if metric_id == "METRIC_001":          # Quarterly Net Revenue (USD)
        cents = conn.execute(
            "SELECT COALESCE(SUM(CASE WHEN event_type='purchase' THEN amount_cents END),0)"
            "     - COALESCE(SUM(CASE WHEN event_type='refund'   THEN amount_cents END),0)"
            "  FROM events WHERE ts>=? AND ts<?", (start, end)).fetchone()[0]
        return round(cents / 100.0, 2)
    if metric_id == "METRIC_002":          # Quarterly Active Users
        return int(conn.execute(
            "SELECT COUNT(DISTINCT user_id) FROM events WHERE ts>=? AND ts<?",
            (start, end)).fetchone()[0])
    sys.exit(f"error: unknown metric {metric_id}")


def main():
    ap = argparse.ArgumentParser(description="In-band analytical engine")
    ap.add_argument("--metric", default=os.environ.get("METRIC_ID"))
    ap.add_argument("--start", default=os.environ.get("START_DATE", "2025-01-01T00:00:00Z"))
    ap.add_argument("--end", default=os.environ.get("END_DATE", "2026-01-01T00:00:00Z"))
    a = ap.parse_args()
    if not a.metric:
        sys.exit("error: --metric or METRIC_ID is required")

    conn = sqlite3.connect(f"file:{find_db()}?mode=ro", uri=True)
    try:
        value = compute(conn, a.metric, a.start, a.end)
    finally:
        conn.close()

    print(json.dumps({
        "metric_id": a.metric,
        "value": value,
        "window": {"start": a.start, "end": a.end},
        "execution_utc_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }))


if __name__ == "__main__":
    main()
