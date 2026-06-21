#!/usr/bin/env python3
"""A parametrized seeded coherent-and-wrong API server for the evidence harness.

Self-contained stdlib http.server implementing the Profile API contract correctly
EXCEPT for exactly one clause, selected by the VIOLATE environment variable:
  CLAUSE_1  skip the X-API-Key auth check (an unauthenticated mutation succeeds)
  CLAUSE_2  leak the internal integer `id` in the GET response
  CLAUSE_3  leak a raw traceback string in the 400 body on a malformed payload
Each is internally consistent and fluent; the split-plane squeeze must catch each
at Gate B (status / key-set / forbidden-pattern). CLI mirrors the implementer:
  python3 seeded_wrong_server.py --host 127.0.0.1 --port 8000 --db <path>
"""

import argparse
import json
import os
import sqlite3
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer

VIOLATE = os.environ.get("VIOLATE", "")
VALID_KEY = "test_secure_token_abc123"
LEAK = ('Traceback (most recent call last):\n  File "main.py", line 42, in do_POST\n'
        '    cur = conn.execute("SELECT * FROM users WHERE id=?")\n'
        'sqlite3.OperationalError: malformed input')


class Store:
    def __init__(self, db_path):
        self.users, self.keys = {}, {}
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        try:
            for i, u, d, t in conn.execute(
                    "SELECT id, user_uuid, display_name, updated_at FROM users"):
                rec = {"user_uuid": u, "display_name": d, "updated_at": t}
                if VIOLATE == "CLAUSE_2":
                    rec["id"] = i                      # WRONG: leak storage key
                self.users[u] = rec
            for k, u in conn.execute("SELECT api_key, user_uuid FROM api_keys"):
                self.keys[k] = u
        finally:
            conn.close()


def make_handler(store):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _json(self, status, payload):
            body = json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _auth(self):
            if VIOLATE == "CLAUSE_1":
                return "u-0001"                         # WRONG: skip auth
            key = self.headers.get("X-API-Key", "")
            return store.keys.get(key) if key else None

        def do_GET(self):
            if self.path != "/api/v1/profile":
                return self._json(404, {"error": "not_found", "message": "no such route"})
            uuid = self._auth()
            if not uuid:
                return self._json(401, {"error": "unauthorized", "message": "X-API-Key required"})
            rec = dict(store.users[uuid])
            keys = ["user_uuid", "display_name", "updated_at"] + (["id"] if VIOLATE == "CLAUSE_2" else [])
            return self._json(200, {k: rec[k] for k in keys})

        def do_POST(self):
            if self.path != "/api/v1/profile/update":
                return self._json(404, {"error": "not_found", "message": "no such route"})
            uuid = self._auth()
            if not uuid:
                return self._json(401, {"error": "unauthorized", "message": "X-API-Key required"})
            n = int(self.headers.get("Content-Length", 0) or 0)
            raw = self.rfile.read(n) if n else b""
            try:
                body = json.loads(raw)
                name = body["display_name"]
                if not isinstance(name, str) or not name.strip():
                    raise ValueError("display_name must be a non-empty string")
            except Exception:
                if VIOLATE == "CLAUSE_3":
                    return self._json(400, {"error": "bad_request", "message": LEAK})  # WRONG: leak
                return self._json(400, {"error": "bad_request", "message": "invalid payload"})
            store.users[uuid]["display_name"] = name
            store.users[uuid]["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            return self._json(200, {"status": "updated", "user_uuid": uuid,
                                    "updated_at": store.users[uuid]["updated_at"]})
    return H


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--db", required=True)
    a = ap.parse_args()
    store = Store(a.db)
    TCPServer.allow_reuse_address = True
    with TCPServer((a.host, a.port), make_handler(store)) as srv:
        srv.serve_forever()


if __name__ == "__main__":
    main()
