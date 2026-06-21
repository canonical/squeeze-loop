#!/usr/bin/env python3
"""Self-check of the ground truth -- the executable lower bound.

Exits nonzero on any failure, printing a Gate-B-style report:

  1. SIGNATURE    ledger.sig matches a freshly computed manifest of the archive
  2. RECOMPUTE    replaying every archive case through reference_policy.decide()
                  reproduces its stored verdict (the "every decision recomputes"
                  invariant -- the analogue of Total Additivity)
  3. READ-ONLY    customer_history.db opened ?mode=ro rejects an INSERT
  4. PERMISSIONS  artifacts are 0444 (warn-only off-container, where we aren't root)
  5. ENDPOINTS    (optional) start app.py on a free port; /start returns the seeded
                  customer and a posted /action is reflected in /state
"""

import hashlib
import json
import socket
import sqlite3
import stat
import sys
import threading
import time
import urllib.request
from pathlib import Path

import build_ground_truth as bgt
import reference_policy

HERE = Path(__file__).resolve().parent
SHARED = HERE / "shared"
DB = SHARED / "customer_history.db"
ARCHIVE = SHARED / "archive_ledger"
SIG = ARCHIVE / "ledger.sig"


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))
    return ok


def _customer_view(conn, customer_id):
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


def _free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _post(url, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data,
                                 headers={"Content-Type": "application/json"},
                                 method="POST")
    with urllib.request.urlopen(req, timeout=5) as r:
        return r.status, json.loads(r.read().decode("utf-8"))


def _get(url):
    with urllib.request.urlopen(url, timeout=5) as r:
        return r.status, json.loads(r.read().decode("utf-8"))


def check_endpoints():
    """Start the app on a free port and exercise the four endpoints."""
    import app
    port = _free_port()
    base = f"http://127.0.0.1:{port}/api/session"
    httpd = app.make_server("127.0.0.1", port, str(DB))
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    time.sleep(0.2)
    try:
        # /start CUST_GOOD
        st, body = _post(f"{base}/start",
                         {"case_id": "VERIFY", "customer_id": "CUST_GOOD"})
        ok = st == 200 and body["customer"]["customer_id"] == "CUST_GOOD"
        ok &= any(o["order_id"] == "ORD_GOOD" for o in body["customer"]["orders"])
        token = body["session_token"]

        # unknown customer -> 404
        try:
            _post(f"{base}/start", {"case_id": "V", "customer_id": "NOPE"})
            ok = False
        except urllib.error.HTTPError as e:
            ok &= e.code == 404

        # /chat
        st, body = _post(f"{base}/chat",
                         {"session_token": token, "message": "ORD_GOOD never arrived"})
        ok &= st == 200 and body.get("ack") is True

        # /action REIMBURSE
        st, body = _post(f"{base}/action",
                         {"session_token": token, "decision": "REIMBURSE"})
        ok &= st == 200 and body.get("decision") == "REIMBURSE"

        # second commit -> 409
        try:
            _post(f"{base}/action", {"session_token": token, "decision": "DENY"})
            ok = False
        except urllib.error.HTTPError as e:
            ok &= e.code == 409

        # bad decision -> 400
        try:
            _post(f"{base}/action", {"session_token": token, "decision": "BOGUS"})
            ok = False
        except urllib.error.HTTPError as e:
            ok &= e.code == 400

        # /state reflects the committed action + the logged turn
        st, body = _get(f"{base}/state/{token}")
        ok &= st == 200 and body.get("committed_action") == "REIMBURSE"
        ok &= "ORD_GOOD never arrived" in body.get("turns", [])
        return ok
    finally:
        httpd.shutdown()
        httpd.server_close()


def main():
    if not DB.exists() or not SIG.exists() or not ARCHIVE.exists():
        print("ground truth not built; run build_ground_truth.py")
        return 2

    ok = True

    # 1. signature: ledger.sig matches a fresh manifest of the archive
    manifest = bgt.archive_manifest()
    fresh = hashlib.sha256(manifest).hexdigest()
    sig_field = SIG.read_text().split()[0]
    ok &= check("signature", fresh == sig_field,
                f"{fresh[:12]}... vs {sig_field[:12]}...")

    # 2. every decision recomputes: replay each case through reference_policy
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    try:
        case_files = sorted(ARCHIVE.glob("case_*_input.json"))
        all_match = True
        for ip in case_files:
            inp = json.loads(ip.read_text())
            vp = ARCHIVE / ip.name.replace("_input.json", "_verdict.json")
            stored = json.loads(vp.read_text())["decision"]
            customer, orders = _customer_view(conn, inp["customer_id"])
            recomputed = reference_policy.decide(customer, orders, inp["turns"])
            if recomputed != stored:
                all_match = False
                print(f"    {inp['case_id']}: stored={stored} recomputed={recomputed}")
        ok &= check("every-decision-recomputes", all_match,
                    f"{len(case_files)} cases")
    finally:
        conn.close()

    # 3. read-only enforcement at the engine level
    ro = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    try:
        ro.execute("INSERT INTO customers(customer_id,registration_age_hours,"
                   "lifetime_orders,return_velocity,fraud_flag) "
                   "VALUES ('HACK',1,0,0.0,0)")
        ro.commit()
        ro_ok = False
    except sqlite3.OperationalError:
        ro_ok = True
    finally:
        ro.close()
    ok &= check("read-only db", ro_ok, "engine rejects writes")

    # 4. permissions (warn-only off-container)
    perm_targets = [DB, SIG] + [p for p in ARCHIVE.iterdir() if p.name != SIG.name]
    perms = {p.name: stat.S_IMODE(p.stat().st_mode) for p in perm_targets}
    if all(m == 0o444 for m in perms.values()):
        check("permissions 0444", True)
    else:
        print("[WARN] not all artifacts are 0444 (expected only after root deploy): "
              + ", ".join(f"{k}={oct(v)}" for k, v in sorted(perms.items())))

    # 5. endpoint smoke test
    try:
        ep_ok = check_endpoints()
        ok &= check("endpoints (start/chat/action/state)", ep_ok)
    except Exception as e:  # noqa: BLE001 -- surface, don't crash the report
        ok = False
        check("endpoints (start/chat/action/state)", False, f"error: {e}")

    print("VERIFY OK" if ok else "VERIFY FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
