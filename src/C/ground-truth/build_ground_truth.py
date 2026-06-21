#!/usr/bin/env python3
"""Build the Low-Level Sources of Truth (spec §2/§4) into ./shared/:

  app_state.db        Storage     -- frozen users/api_keys state (0444, read-only)
  base_schema.json    Doc plane   -- canonical contract, re-serialized byte-stably
  ty0_baseline.json   Item Zero   -- route-reflection snapshot of the legacy trunk:
                                     canonical route signatures (method, path,
                                     response-keys-by-status) + db columns, plus a
                                     "hash" = SHA-256 over a deterministic manifest
                                     of that snapshot.

Idempotent and deterministic: re-running reproduces app_state.db, base_schema.json,
and ty0_baseline.json byte-for-byte. Run `verify_ground_truth.py` afterwards, and
`provision.sh` (as root) to deploy.
"""

import hashlib
import json
import sqlite3
import sys
from pathlib import Path

import reflection
import seed_data

HERE = Path(__file__).resolve().parent
SHARED = HERE / "shared"
DB = SHARED / "app_state.db"
SCHEMA = HERE / "schema.sql"
SRC_BASE_SCHEMA = HERE / "base_schema.json"
OUT_BASE_SCHEMA = SHARED / "base_schema.json"
TY0 = SHARED / "ty0_baseline.json"


def _force_unlink(path):
    """Remove an artifact even if a prior build left it mode 0444."""
    if path.exists():
        path.chmod(0o644)
        path.unlink()


def _dumps(obj):
    """Byte-stable JSON: sorted keys, 2-space indent, trailing newline."""
    return (json.dumps(obj, sort_keys=True, indent=2) + "\n").encode("utf-8")


def build_db():
    _force_unlink(DB)
    conn = sqlite3.connect(DB)
    try:
        conn.executescript(SCHEMA.read_text())
        users, api_keys = seed_data.generate()
        conn.executemany(
            "INSERT INTO users(id,user_uuid,display_name,updated_at) "
            "VALUES (?,?,?,?)", users)
        conn.executemany(
            "INSERT INTO api_keys(api_key,user_uuid) VALUES (?,?)", api_keys)
        conn.commit()
    finally:
        conn.close()
    return len(users), len(api_keys)


def build_base_schema():
    """Re-serialize the canonical contract byte-stably into shared/."""
    schema = json.loads(SRC_BASE_SCHEMA.read_text())
    _force_unlink(OUT_BASE_SCHEMA)
    OUT_BASE_SCHEMA.write_bytes(_dumps(schema))


def build_ty0():
    """TY0 route-reflection snapshot + content hash (spec §4)."""
    snapshot = reflection.reflect(DB)
    snapshot["hash"] = reflection.manifest_hash(snapshot)
    _force_unlink(TY0)
    TY0.write_bytes(_dumps(snapshot))
    return snapshot["hash"]


def harden():
    """Best-effort local read-only (true root:root 0444 happens in provision.sh)."""
    for p in (DB, OUT_BASE_SCHEMA, TY0):
        try:
            p.chmod(0o444)
        except OSError:
            pass


def main():
    SHARED.mkdir(parents=True, exist_ok=True)
    nu, nk = build_db()
    build_base_schema()
    digest = build_ty0()
    harden()
    print(f"[storage]  app_state.db      : {nu} users, {nk} api_keys")
    print(f"[document] base_schema.json  : canonical contract re-serialized")
    print(f"[item0]    ty0_baseline.json : route-reflection snapshot")
    print(f"[item0]    ty0 hash sha256   : {digest}")
    print(f"[compute]  sqlite engine     : {sqlite3.sqlite_version} "
          f"(pin this version in the LXC image; see README)")
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
