#!/usr/bin/env python3
"""Negative control -- a deliberately COHERENT-AND-WRONG Profile API server.

It honours the surface contract (same routes, same X-API-Key auth on the happy
path, stdlib http.server) and is internally consistent, but it VIOLATES the
upper-bound clauses in two ways the runner must catch:

  * CLAUSE_3 violation: on a malformed POST body it lets the JSON/validation
    exception propagate and writes the raw Python traceback into the response
    body -- exactly the "Traceback Exfiltration Injection" the Core Negative
    Vector probes for. (Gate B trips on the forbidden_string_patterns.)
  * CLAUSE_2 violation: GET /api/v1/profile returns the internal integer `id`
    alongside user_uuid -- a leaked storage primary key. (Gate B trips because
    the response key set no longer equals the documented schema keys.)

The runner can load it with `--bad` (or SERVER_CMD=) to demonstrate that GATE B
rejects a plausible-but-wrong server rather than rubber-stamping it.

Stdlib only.  CLI:  python3 coherent_wrong_server.py --port 8000 --db <path>
"""

import argparse
import datetime
import json
import sqlite3
import sys
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from socketserver import ThreadingMixIn

API_KEY_HEADER = "X-API-Key"
ERR_UNAUTHORIZED = {"error": "unauthorized",
                    "message": "A valid X-API-Key header is required."}
ERR_NOT_FOUND = {"error": "not_found", "message": "The requested resource does not exist."}


class Store:
    def __init__(self, db_path):
        self.users = {}
        self.api_keys = {}
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        try:
            # WRONG (CLAUSE_2): the internal integer id is loaded and kept.
            for row in conn.execute(
                    "SELECT id, user_uuid, display_name, updated_at FROM users"):
                self.users[row[1]] = {
                    "id": row[0],
                    "user_uuid": row[1],
                    "display_name": row[2],
                    "updated_at": row[3],
                }
            for row in conn.execute("SELECT api_key, user_uuid FROM api_keys"):
                self.api_keys[row[0]] = row[1]
        finally:
            conn.close()

    def resolve_key(self, api_key):
        if not api_key:
            return None
        return self.api_keys.get(api_key)


class Handler(BaseHTTPRequestHandler):
    store = None

    def log_message(self, fmt, *args):
        return

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, status, text):
        body = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _auth(self):
        return self.store.resolve_key(self.headers.get(API_KEY_HEADER))

    def do_GET(self):
        path = self.path.split("?", 1)[0].rstrip("/") or "/"
        if path == "/api/v1/profile":
            uuid = self._auth()
            if uuid is None:
                return self._send_json(401, ERR_UNAUTHORIZED)
            rec = self.store.users[uuid]
            # WRONG (CLAUSE_2): leaks the integer id key.
            return self._send_json(200, {
                "id": rec["id"],
                "user_uuid": rec["user_uuid"],
                "display_name": rec["display_name"],
                "updated_at": rec["updated_at"],
            })
        return self._send_json(404, ERR_NOT_FOUND)

    def do_POST(self):
        path = self.path.split("?", 1)[0].rstrip("/") or "/"
        if path != "/api/v1/profile/update":
            return self._send_json(404, ERR_NOT_FOUND)
        uuid = self._auth()
        if uuid is None:
            return self._send_json(401, ERR_UNAUTHORIZED)
        # WRONG (CLAUSE_3): no guard -- a malformed body raises and the raw
        # traceback is written to the client.
        try:
            n = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(n) if n > 0 else b""
            body = json.loads(raw.decode("utf-8"))
            display_name = body["display_name"]
            if not isinstance(display_name, str) or not display_name.strip():
                raise ValueError("display_name must be a non-empty string")
            now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            return self._send_json(200, {
                "status": "ok", "user_uuid": uuid, "updated_at": now})
        except Exception:  # noqa: BLE001 -- the bug: leak the trace on the wire.
            return self._send_text(500, traceback.format_exc())


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--db", default=str(
        Path(__file__).resolve().parents[2] / "ground-truth" / "shared" / "app_state.db"))
    args = ap.parse_args(argv)
    if not Path(args.db).exists():
        sys.exit(f"error: database not found: {args.db}")
    Handler.store = Store(args.db)
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"coherent-wrong server on http://{args.host}:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
