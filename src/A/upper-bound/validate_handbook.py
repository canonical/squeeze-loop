#!/usr/bin/env python3
"""Self-check of the Upper Bound — the author's expressibility-from-below proof.

Exits nonzero on any failure:

  1. STRUCTURE     metric_handbook.md parses and passes the schema (spec §2).
  2. GROUNDING     every metric's Target Table and every column its formula
                   references actually exist in the ground-truth warehouse
                   (`events`/`users`), so the ceiling is dischargeable, not a wish.
  3. GATE WIRING   the Gate A / Gate C primitives accept a correct plan/test set
                   for each metric and reject one that drops a clause.

The grounding step is the upper-bound analogue of the ground truth's "every
number recomputes": a normative claim no query could ever satisfy is rejected
here, not discovered downstream.
"""

from __future__ import annotations

import re
import sqlite3
import sys
from pathlib import Path

import gate_checks as gc
import handbook as hb

HERE = Path(__file__).resolve().parent
DB_CANDIDATES = [
    Path("/opt/squeeze/shared/base_warehouse.db"),
    HERE.parent / "ground-truth" / "shared" / "base_warehouse.db",
]

# Tokens in a Normative Formula that are placeholders / keywords / literals,
# not warehouse columns.
_PLACEHOLDERS = {"quarter_start_utc", "quarter_end_utc", "quarter_start", "quarter_end"}
_SQL_WORDS = {"sum", "count", "distinct", "over", "where", "and", "or", "not", "null", "is"}
_LITERALS = {"purchase", "refund", "login"}
_TOKEN = re.compile(r"\b[a-z][a-z0-9_]*\b")


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))
    return ok


def _columns(conn, table):
    try:
        return {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
    except sqlite3.OperationalError:
        return None


def main():
    ok = True

    # 1. structure
    try:
        metrics = hb.parse()
        check("structure", True, f"{len(metrics)} metric(s): "
              + ", ".join(m.metric_id for m in metrics))
    except hb.HandbookError as e:
        check("structure", False, str(e))
        print("VALIDATE FAILED")
        return 1

    # 2. grounding against the ground-truth warehouse
    db = next((p for p in DB_CANDIDATES if p.exists()), None)
    if db is None:
        print("[WARN] ground-truth warehouse not found; skipping grounding "
              f"(looked in: {', '.join(str(p) for p in DB_CANDIDATES)})")
    else:
        conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        try:
            tables = {row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")}
            for m in metrics:
                if m.target_table not in tables:
                    ok &= check(f"{m.metric_id} target table", False,
                                f"`{m.target_table}` not in warehouse {sorted(tables)}")
                    continue
                cols = _columns(conn, m.target_table)
                refs = {t for t in _TOKEN.findall(m.formula)
                        if t not in _PLACEHOLDERS | _SQL_WORDS | _LITERALS | tables}
                # user_id may live in either events or users; allow cross-table id.
                known = set(cols)
                if "users" in tables:
                    known |= _columns(conn, "users") or set()
                phantom = sorted(r for r in refs if r not in known)
                ok &= check(f"{m.metric_id} grounding", not phantom,
                            f"table `{m.target_table}`, columns {sorted(refs)} present"
                            if not phantom else f"phantom columns {phantom}")
        finally:
            conn.close()

    # 3. gate wiring (positive + negative per metric)
    for m in metrics:
        plan_ok = gc.gate_a_plan(m, " ".join(m.clause_ids))
        plan_bad = gc.gate_a_plan(m, " ".join(m.clause_ids[:-1]))   # drop last clause
        asserts_ok = [{"clause": c, "check": "x"} for c in m.clause_ids]
        asserts_bad = asserts_ok[:-1]
        c_ok = gc.gate_c_assertions(m, asserts_ok)
        c_bad = gc.gate_c_assertions(m, asserts_bad)
        wired = bool(plan_ok) and not plan_bad.ok and bool(c_ok) and not c_bad.ok
        ok &= check(f"{m.metric_id} gate wiring", wired,
                    "Gate A & C accept complete, reject incomplete")

    print("VALIDATE OK" if ok else "VALIDATE FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
