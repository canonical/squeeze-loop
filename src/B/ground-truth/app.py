#!/usr/bin/env python3
"""Compute Plane (spec §2 Step 3): the frozen, headless REST platform.

The spec text says "FastAPI/Flask", but the LXC container is offline with no pip
-- so this is implemented with the Python STDLIB ONLY (http.server / socketserver
/ sqlite3 / json / hashlib / threading), which is the coordinator-fixed contract
for all three planes. See README.md for the adaptation note.

This app is a deterministic PLATFORM, not a decider. It serves customer data,
logs chat, and RECORDS the decision the caller commits. It NEVER decides and
NEVER writes to the database (the DB is opened ?mode=ro). The correct decision
for any case is defined by reference_policy.decide(), which lives in the Invariant
Plane, not here.

Contract (base path /api/session):
  POST /api/session/start            {case_id, customer_id}
       -> 200 {session_token, customer:{...orders:[...]}}    | 404 unknown customer
  POST /api/session/chat             {session_token, message}
       -> 200 {ack:true}                                     | 404 bad token
  POST /api/session/action           {session_token, decision}
       -> 200 {committed:true, decision}                     | 400 bad decision
                                                             | 404 bad token
                                                             | 409 already committed
  GET  /api/session/state/{token}
       -> 200 {session_token, customer_id, customer:{...orders:[...]},
               turns:[...], committed_action: <d|null>}

Sessions are in-memory; tokens are derived deterministically from
(case_id, customer_id, session ordinal) via sha256 so a given call sequence
yields reproducible tokens.

Run:  python3 app.py [--host 127.0.0.1] [--port 8000] [--db PATH]
Default DB: ./shared/customer_history.db (or /opt/squeeze/shared/customer_history.db
if the local one is absent), opened read-only.
"""

import argparse
import hashlib
import json
import sqlite3
import sys
import threading
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from socketserver import ThreadingMixIn
from http.server import HTTPServer

HERE = Path(__file__).resolve().parent
DEFAULT_DB_LOCAL = HERE / "shared" / "customer_history.db"
DEFAULT_DB_DEPLOYED = Path("/opt/squeeze/shared/customer_history.db")

VALID_DECISIONS = ("REIMBURSE", "DENY", "ESCALATE")
BASE = "/api/session"


def default_db_path():
    if DEFAULT_DB_LOCAL.exists():
        return DEFAULT_DB_LOCAL
    return DEFAULT_DB_DEPLOYED


class SessionStore:
    """Thread-safe in-memory session registry. The DB is the only persistent
    state and it is read-only; everything here lives for the process lifetime."""

    def __init__(self, db_path):
        self.db_path = str(db_path)
        self._lock = threading.Lock()
        self._sessions = {}      # token -> session dict
        self._counter = 0        # monotonic, for deterministic token derivation

    def _connect_ro(self):
        return sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True)

    def load_customer(self, customer_id):
        """Return the customer payload dict, or None if unknown. Read-only."""
        conn = self._connect_ro()
        try:
            row = conn.execute(
                "SELECT customer_id, registration_age_hours, lifetime_orders, "
                "return_velocity, fraud_flag FROM customers WHERE customer_id=?",
                (customer_id,)).fetchone()
            if row is None:
                return None
            orders = conn.execute(
                "SELECT order_id, value_usd, status FROM orders "
                "WHERE customer_id=? ORDER BY order_id", (customer_id,)).fetchall()
        finally:
            conn.close()
        return {
            "customer_id": row[0],
            "registration_age_hours": row[1],
            "lifetime_orders": row[2],
            "return_velocity": row[3],
            "fraud_flag": row[4],
            "orders": [
                {"order_id": o[0], "value_usd": o[1], "status": o[2]}
                for o in orders
            ],
        }

    def start(self, case_id, customer_id):
        customer = self.load_customer(customer_id)
        if customer is None:
            return None
        with self._lock:
            self._counter += 1
            seed = f"{case_id}|{customer_id}|{self._counter}".encode("utf-8")
            token = hashlib.sha256(seed).hexdigest()
            self._sessions[token] = {
                "session_token": token,
                "case_id": case_id,
                "customer_id": customer_id,
                "customer": customer,
                "turns": [],
                "committed_action": None,
            }
        return token, customer

    def chat(self, token, message):
        with self._lock:
            sess = self._sessions.get(token)
            if sess is None:
                return False
            sess["turns"].append(message)
            return True

    def action(self, token, decision):
        """Return ('ok'|'bad_token'|'conflict')."""
        with self._lock:
            sess = self._sessions.get(token)
            if sess is None:
                return "bad_token"
            if sess["committed_action"] is not None:
                return "conflict"          # first commit wins (the Lockpoint)
            sess["committed_action"] = decision
            return "ok"

    def state(self, token):
        with self._lock:
            sess = self._sessions.get(token)
            if sess is None:
                return None
            return {
                "session_token": sess["session_token"],
                "customer_id": sess["customer_id"],
                "customer": sess["customer"],
                "turns": list(sess["turns"]),
                "committed_action": sess["committed_action"],
            }


class Handler(BaseHTTPRequestHandler):
    server_version = "RefundPlatform/1.0"
    protocol_version = "HTTP/1.1"

    # --- helpers ----------------------------------------------------------
    def _send(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length) if length else b""
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    def log_message(self, *args):  # silence default stderr access log
        pass

    # --- routing ----------------------------------------------------------
    def do_POST(self):
        store = self.server.store
        try:
            if self.path == f"{BASE}/start":
                body = self._read_json()
                cid = body.get("customer_id")
                case_id = body.get("case_id")
                if not cid or not case_id:
                    return self._send(400, {"error": "case_id and customer_id required"})
                result = store.start(case_id, cid)
                if result is None:
                    return self._send(404, {"error": f"unknown customer {cid}"})
                token, customer = result
                return self._send(200, {"session_token": token, "customer": customer})

            if self.path == f"{BASE}/chat":
                body = self._read_json()
                token = body.get("session_token")
                message = body.get("message", "")
                if not store.chat(token, message):
                    return self._send(404, {"error": "unknown session_token"})
                return self._send(200, {"ack": True})

            if self.path == f"{BASE}/action":
                body = self._read_json()
                token = body.get("session_token")
                decision = body.get("decision")
                if decision not in VALID_DECISIONS:
                    return self._send(400, {"error": f"decision must be one of {VALID_DECISIONS}"})
                outcome = store.action(token, decision)
                if outcome == "bad_token":
                    return self._send(404, {"error": "unknown session_token"})
                if outcome == "conflict":
                    return self._send(409, {"error": "session already committed"})
                return self._send(200, {"committed": True, "decision": decision})

            return self._send(404, {"error": "no such endpoint"})
        except (json.JSONDecodeError, ValueError):
            self._send(400, {"error": "invalid JSON body"})

    def do_GET(self):
        store = self.server.store
        prefix = f"{BASE}/state/"
        if self.path.startswith(prefix):
            token = self.path[len(prefix):]
            st = store.state(token)
            if st is None:
                return self._send(404, {"error": "unknown session_token"})
            return self._send(200, st)
        return self._send(404, {"error": "no such endpoint"})


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def make_server(host, port, db_path):
    httpd = ThreadingHTTPServer((host, port), Handler)
    httpd.store = SessionStore(db_path)
    return httpd


def main(argv=None):
    parser = argparse.ArgumentParser(description="Frozen refund-platform REST app")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--db", default=str(default_db_path()))
    args = parser.parse_args(argv)

    if not Path(args.db).exists():
        print(f"error: DB not found: {args.db} (run build_ground_truth.py)", file=sys.stderr)
        return 2

    httpd = make_server(args.host, args.port, args.db)
    print(f"refund platform listening on http://{args.host}:{args.port}{BASE} "
          f"(db={args.db}, read-only)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
