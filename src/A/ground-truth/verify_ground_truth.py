#!/usr/bin/env python3
"""Self-check of the ground truth -- the executable lower bound.

Exits nonzero on any failure, printing a Gate-B-style report:

  1. SIGNATURE    sha256(history_ledger.json) == history_ledger.sig
  2. RECOMPUTE    re-running the metric queries against base_warehouse.db
                  reproduces history_ledger.json byte-for-byte (Total Additivity)
  3. READ-ONLY    the warehouse opened mode=ro rejects writes (spec §2 Step 1)
  4. PERMISSIONS  artifacts are 0444 (warn-only off-container, where we aren't root)
"""

import difflib
import hashlib
import sqlite3
import stat
import sys
from pathlib import Path

import metrics

HERE = Path(__file__).resolve().parent
SHARED = HERE / "shared"
DB = SHARED / "base_warehouse.db"
LEDGER = SHARED / "history_ledger.json"
SIG = SHARED / "history_ledger.sig"


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))
    return ok


def main():
    missing = [p.name for p in (DB, LEDGER, SIG) if not p.exists()]
    if missing:
        print(f"ground truth not built (missing {', '.join(missing)}); "
              f"run build_ground_truth.py")
        return 2

    ok = True
    ledger_bytes = LEDGER.read_bytes()

    # 1. signature
    digest = hashlib.sha256(ledger_bytes).hexdigest()
    sig_field = SIG.read_text().split()[0]
    ok &= check("signature", digest == sig_field,
                f"{digest[:12]}... vs {sig_field[:12]}...")

    # 2. recompute == ledger (every number recomputes; total additivity)
    conn = metrics.connect_ro(DB)
    try:
        recomputed = metrics.serialize(metrics.compute_all(conn))
    finally:
        conn.close()
    same = recomputed == ledger_bytes
    ok &= check("recompute==ledger", same)
    if not same:
        diff = difflib.unified_diff(
            ledger_bytes.decode().splitlines(),
            recomputed.decode().splitlines(),
            "history_ledger.json", "recomputed", lineterm="")
        for line in list(diff)[:24]:
            print("    " + line)

    # 3. read-only enforcement at the engine level
    ro = metrics.connect_ro(DB)
    try:
        ro.execute("INSERT INTO events(ts,user_id,event_type,amount_cents,region) "
                   "VALUES ('2099-01-01T00:00:00Z',1,'login',0,'UTC')")
        ro.commit()
        ro_ok = False
    except sqlite3.OperationalError:
        ro_ok = True
    finally:
        ro.close()
    ok &= check("read-only warehouse", ro_ok, "engine rejects writes")

    # 4. permissions (warn-only: 0444 is enforced by provision.sh as root)
    perms = {p.name: stat.S_IMODE(p.stat().st_mode) for p in (DB, LEDGER, SIG)}
    if all(m == 0o444 for m in perms.values()):
        check("permissions 0444", True)
    else:
        print("[WARN] not all artifacts are 0444 (expected only after root deploy): "
              + ", ".join(f"{k}={oct(v)}" for k, v in perms.items()))

    print("VERIFY OK" if ok else "VERIFY FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
