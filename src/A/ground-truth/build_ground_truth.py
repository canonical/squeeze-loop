#!/usr/bin/env python3
"""Build the three Low-Level Sources of Truth (spec §2) into ./shared/:

  base_warehouse.db    Storage Plane   -- raw event log (root:root 0444 deployed)
  history_ledger.json  Invariant Plane -- baseline numbers, recomputed from the DB
  history_ledger.sig   SHA-256 of the ledger, in sha256sum(1) format

Idempotent and deterministic: re-running reproduces an identical ledger and sig.
Run `verify_ground_truth.py` afterwards, and `provision.sh` (as root) to deploy.
"""

import hashlib
import sqlite3
import sys
from pathlib import Path

import metrics
import seed_data

HERE = Path(__file__).resolve().parent
SHARED = HERE / "shared"
DB = SHARED / "base_warehouse.db"
LEDGER = SHARED / "history_ledger.json"
SIG = SHARED / "history_ledger.sig"
SCHEMA = HERE / "schema.sql"


def _force_unlink(path):
    """Remove an artifact even if a prior build left it mode 0444."""
    if path.exists():
        path.chmod(0o644)
        path.unlink()


def build_db():
    _force_unlink(DB)
    conn = sqlite3.connect(DB)
    try:
        conn.executescript(SCHEMA.read_text())
        users, events = seed_data.generate()
        conn.executemany(
            "INSERT INTO users(user_id,signup_ts,deleted_ts,home_region) "
            "VALUES (?,?,?,?)", users)
        conn.executemany(
            "INSERT INTO events(event_id,ts,user_id,event_type,amount_cents,region) "
            "VALUES (?,?,?,?,?,?)", events)
        conn.commit()
    finally:
        conn.close()
    return len(users), len(events)


def build_ledger():
    conn = metrics.connect_ro(DB)          # read the DB exactly as consumers will
    try:
        m = metrics.compute_all(conn)
    finally:
        conn.close()
    data = metrics.serialize(m)
    _force_unlink(LEDGER)
    LEDGER.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    _force_unlink(SIG)
    SIG.write_text(f"{digest}  history_ledger.json\n")
    return m, digest


def harden():
    """Best-effort local read-only (true root:root 0444 happens in provision.sh)."""
    for p in (DB, LEDGER, SIG):
        try:
            p.chmod(0o444)
        except OSError:
            pass


def main():
    SHARED.mkdir(parents=True, exist_ok=True)
    nu, ne = build_db()
    m, digest = build_ledger()
    harden()
    print(f"[storage]   base_warehouse.db   : {nu} users, {ne} events")
    print(f"[invariant] history_ledger.json : {len(m)} certified metrics")
    print(f"[invariant] sha256              : {digest}")
    print(f"[compute]   sqlite engine       : {sqlite3.sqlite_version} "
          f"(pin this version in the LXC image; see README)")
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
