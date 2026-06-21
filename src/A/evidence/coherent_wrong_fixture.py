#!/usr/bin/env python3
"""Seeded coherent-and-wrong implementer -- a permanent fixture for the evidence
harness (the paper's seeded-defect measurement).

It is a well-formed, internally consistent program that returns a clean number
for every metric, but it violates METRIC_001 CLAUSE_3: it reports GROSS purchase
revenue and omits the refund subtraction. METRIC_002 is computed correctly. The
squeeze must reject it at Gate B (the independent exerciser expected net revenue).
This is the coherent-and-wrong failure the whole strategy exists to exclude.
"""

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / "ground-truth" / "shared" / "base_warehouse.db"

ap = argparse.ArgumentParser()
ap.add_argument("--metric")
ap.add_argument("--start")
ap.add_argument("--end")
a = ap.parse_args()

conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
if a.metric == "METRIC_001":
    cents = conn.execute(
        "SELECT COALESCE(SUM(amount_cents),0) FROM events "
        "WHERE event_type='purchase' AND ts>=? AND ts<?", (a.start, a.end)).fetchone()[0]
    value = round(cents / 100.0, 2)          # BUG: gross, not net (omits refunds)
elif a.metric == "METRIC_002":
    value = int(conn.execute(
        "SELECT COUNT(DISTINCT user_id) FROM events WHERE ts>=? AND ts<?",
        (a.start, a.end)).fetchone()[0])
else:
    raise SystemExit(2)

print(json.dumps({
    "metric_id": a.metric, "value": value,
    "execution_utc_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
}))
