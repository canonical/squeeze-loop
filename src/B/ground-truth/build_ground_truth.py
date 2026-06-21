#!/usr/bin/env python3
"""Build the Low-Level Sources of Truth (spec §2) into ./shared/:

  customer_history.db          Storage Plane   -- frozen customer/order state (0444)
  archive_ledger/case_NNN_input.json           -- certified case inputs
  archive_ledger/case_NNN_verdict.json         -- verdicts, recomputed by the
                                                  reference policy (never hand-typed)
  archive_ledger/ledger.sig    Invariant Plane -- SHA-256 over a deterministic
                                                  sha256sum-style manifest of the
                                                  sorted archive case files

Idempotent and deterministic: re-running reproduces identical archive files and
sig byte-for-byte. Run `verify_ground_truth.py` afterwards, and `provision.sh`
(as root) to deploy.
"""

import hashlib
import sqlite3
import sys
from pathlib import Path

import reference_policy
import seed_data

HERE = Path(__file__).resolve().parent
SHARED = HERE / "shared"
DB = SHARED / "customer_history.db"
ARCHIVE = SHARED / "archive_ledger"
SIG = ARCHIVE / "ledger.sig"
SCHEMA = HERE / "schema.sql"

# Certified regression cases (spec §2 Step 2). Verdicts are NOT listed here --
# they are computed by reference_policy.decide() at build time, so the answer key
# can never drift from the certified policy. (case_num, customer_id, [turns])
CASES = [
    (1, "CUST_GOOD",
     ["my order ORD_GOOD never arrived",
      "I checked with neighbors, please refund"]),
    (2, "CUST_LEGAL",
     ["I want a manual credit now",
      "if not I am filing with my legal counsel"]),
    (3, "CUST_NEW",
     ["refund my order ORD_HIGH immediately"]),
    (4, "CUST_DUP",
     ["please refund ORD_REFUNDED again"]),
    (5, "CUST_FRAUD",
     ["refund my order ORD_FRAUD"]),
    (6, "CUST_DUP",
     ["I will sue you",
      "refund ORD_REFUNDED"]),
]


def _force_unlink(path):
    """Remove an artifact even if a prior build left it mode 0444."""
    if path.exists():
        path.chmod(0o644)
        path.unlink()


def _dumps(obj):
    """Byte-stable JSON: sorted keys, 2-space indent, trailing newline.

    json.dumps with sort_keys + fixed separators is deterministic across runs and
    Python versions for these plain (str/int/list[str]) structures.
    """
    import json
    return (json.dumps(obj, sort_keys=True, indent=2) + "\n").encode("utf-8")


def build_db():
    _force_unlink(DB)
    conn = sqlite3.connect(DB)
    try:
        conn.executescript(SCHEMA.read_text())
        customers, orders = seed_data.generate()
        conn.executemany(
            "INSERT INTO customers(customer_id,registration_age_hours,"
            "lifetime_orders,return_velocity,fraud_flag) VALUES (?,?,?,?,?)",
            customers)
        conn.executemany(
            "INSERT INTO orders(order_id,customer_id,value_usd,status) "
            "VALUES (?,?,?,?)", orders)
        conn.commit()
    finally:
        conn.close()
    return len(customers), len(orders)


def _customer_view(conn, customer_id):
    """Read the customer row + their orders from the DB (read-only at build)."""
    crow = conn.execute(
        "SELECT customer_id, registration_age_hours, lifetime_orders, "
        "return_velocity, fraud_flag FROM customers WHERE customer_id=?",
        (customer_id,)).fetchone()
    customer = {
        "customer_id": crow[0],
        "registration_age_hours": crow[1],
        "lifetime_orders": crow[2],
        "return_velocity": crow[3],
        "fraud_flag": crow[4],
    }
    orows = conn.execute(
        "SELECT order_id, value_usd, status FROM orders WHERE customer_id=?",
        (customer_id,)).fetchall()
    orders = {o[0]: {"value_usd": o[1], "status": o[2]} for o in orows}
    return customer, orders


def build_archive():
    """Write case input/verdict files; verdicts are computed by the policy."""
    # Clear any prior archive contents to stay idempotent.
    if ARCHIVE.exists():
        for p in sorted(ARCHIVE.iterdir()):
            _force_unlink(p)
    ARCHIVE.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    verdicts = []
    try:
        for num, customer_id, turns in CASES:
            case_id = f"case_{num:03d}"
            customer, orders = _customer_view(conn, customer_id)
            decision = reference_policy.decide(customer, orders, turns)

            inp = {"case_id": case_id, "customer_id": customer_id, "turns": turns}
            ver = {"case_id": case_id, "decision": decision}

            ip = ARCHIVE / f"{case_id}_input.json"
            vp = ARCHIVE / f"{case_id}_verdict.json"
            _force_unlink(ip)
            _force_unlink(vp)
            ip.write_bytes(_dumps(inp))
            vp.write_bytes(_dumps(ver))
            verdicts.append((case_id, decision))
    finally:
        conn.close()
    return verdicts


def archive_manifest():
    """sha256sum-style manifest over the sorted archive case files (sig excluded).
    Returns the manifest bytes; this is what ledger.sig signs."""
    lines = []
    for p in sorted(ARCHIVE.iterdir()):
        if p.name == SIG.name:
            continue
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        lines.append(f"{digest}  {p.name}")
    return ("\n".join(lines) + "\n").encode("utf-8")


def build_sig():
    manifest = archive_manifest()
    digest = hashlib.sha256(manifest).hexdigest()
    _force_unlink(SIG)
    SIG.write_text(f"{digest}  archive_ledger\n")
    return digest


def harden():
    """Best-effort local read-only (true root:root 0444 happens in provision.sh)."""
    targets = [DB, SIG]
    if ARCHIVE.exists():
        targets += [p for p in ARCHIVE.iterdir() if p.name != SIG.name]
    for p in targets:
        try:
            p.chmod(0o444)
        except OSError:
            pass


def main():
    SHARED.mkdir(parents=True, exist_ok=True)
    nc, no = build_db()
    verdicts = build_archive()
    digest = build_sig()
    harden()
    print(f"[storage]   customer_history.db : {nc} customers, {no} orders")
    print(f"[invariant] archive_ledger      : {len(verdicts)} certified cases")
    for case_id, decision in verdicts:
        print(f"              {case_id} -> {decision}")
    print(f"[invariant] ledger.sig sha256   : {digest}")
    print(f"[compute]   sqlite engine       : {sqlite3.sqlite_version} "
          f"(pin this version in the LXC image; see README)")
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
