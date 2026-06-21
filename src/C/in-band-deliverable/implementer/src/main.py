#!/usr/bin/env python3
"""Implementer band -- the live HTTP server (in-band-deliverable-spec.md §1).

A stdlib-only `http.server` implementation of the Profile API contract, derived
INDEPENDENTLY from the upper-bound clauses (API_POLICY_081) and the canonical
document-plane contract base_schema.json. It is BLIND to the exerciser's test
matrix: nothing here imports, reads, or parses the exerciser band.

Contract (base path /api/v1, served on 127.0.0.1:8000):

  POST /api/v1/profile/update   X-API-Key auth; body {"display_name": <non-empty str>}
      200 {status, user_uuid, updated_at}      success (in-memory mutation only)
      400 {error, message}                     malformed body (clean, no leak)
      401 {error, message}                     missing / empty / wrong key
  GET  /api/v1/profile          X-API-Key auth
      200 {user_uuid, display_name, updated_at}  (NEVER the internal integer id)
      401 {error, message}                     missing / empty / wrong key
  any other route                              404 {error, message}
  any unhandled internal error                 clean 400 {error, message}, never a trace

Design notes mapped to the clauses:
  CLAUSE_1  mutations require a non-empty, correct X-API-Key (else 401).
  CLAUSE_2  responses expose user_uuid only; the integer id is scrubbed at the
            boundary -- it is never selected onto the wire.
  CLAUSE_3  every failure returns a hand-written constant {error,message}; a global
            try/except around request handling converts ANY unexpected exception to
            a constant clean 400 -- no traceback / file path / source line / SQL /
            sqlite3 text can ever reach the client.

Storage: app_state.db is opened ?mode=ro at boot and snapshotted into memory.
Profile updates mutate the in-memory overlay only; the file is never written.

CLI:  python3 main.py --port 8000 --db <path>

Stdlib only: http.server, socketserver, sqlite3, json, datetime, urllib, argparse.
"""

import argparse
import datetime
import json
import sqlite3
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from socketserver import ThreadingMixIn
from http.server import HTTPServer

API_KEY_HEADER = "X-API-Key"

# Constant, hand-written error bodies. They are NEVER derived from an exception,
# so no runtime detail (traceback, path, source line, SQL, sqlite3 text) can leak.
ERR_BAD_REQUEST = {"error": "bad_request",
                   "message": "The request body is malformed or missing required fields."}
ERR_UNAUTHORIZED = {"error": "unauthorized",
                    "message": "A valid X-API-Key header is required."}
ERR_NOT_FOUND = {"error": "not_found", "message": "The requested resource does not exist."}


# --------------------------------------------------------------------------- #
# In-memory store loaded from the read-only DB.
# --------------------------------------------------------------------------- #
class Store:
    """Snapshot of the read-only DB plus an in-memory overlay for mutations.

    The DB file is opened ?mode=ro and never written. `users` maps
    user_uuid -> {user_uuid, display_name, updated_at}; the internal integer
    `id` is intentionally dropped here so it can never be serialized.
    `api_keys` maps api_key -> user_uuid.
    """

    def __init__(self, db_path):
        self.users = {}
        self.api_keys = {}
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        try:
            for row in conn.execute(
                    "SELECT user_uuid, display_name, updated_at FROM users"):
                uuid, display_name, updated_at = row
                # NB: the integer id is deliberately NOT selected -> cannot leak.
                self.users[uuid] = {
                    "user_uuid": uuid,
                    "display_name": display_name,
                    "updated_at": updated_at,
                }
            for row in conn.execute("SELECT api_key, user_uuid FROM api_keys"):
                self.api_keys[row[0]] = row[1]
        finally:
            conn.close()

    def resolve_key(self, api_key):
        """Return the user_uuid for a non-empty, configured key, else None."""
        if not api_key:
            return None
        return self.api_keys.get(api_key)

    def get_profile(self, user_uuid):
        return self.users.get(user_uuid)

    def update_display_name(self, user_uuid, display_name):
        """In-memory mutation only; returns the updated record. Never writes disk."""
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        rec = self.users[user_uuid]
        rec["display_name"] = display_name
        rec["updated_at"] = now
        return rec


# --------------------------------------------------------------------------- #
# Request handler
# --------------------------------------------------------------------------- #
class Handler(BaseHTTPRequestHandler):
    store = None  # set on the server instance class before serving

    # Silence default stderr request logging (would otherwise be noisy).
    def log_message(self, fmt, *args):
        return

    # ---- low-level JSON response -------------------------------------------
    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    # ---- auth --------------------------------------------------------------
    def _authenticate(self):
        """Return user_uuid for a valid non-empty X-API-Key, else None (CLAUSE_1)."""
        key = self.headers.get(API_KEY_HEADER)
        return self.store.resolve_key(key)

    # ---- routing -----------------------------------------------------------
    def do_GET(self):
        self._dispatch("GET")

    def do_POST(self):
        self._dispatch("POST")

    def do_PUT(self):
        self._dispatch("PUT")

    def do_PATCH(self):
        self._dispatch("PATCH")

    def do_DELETE(self):
        self._dispatch("DELETE")

    def _dispatch(self, method):
        """Global exception guard: ANY unexpected error becomes a constant clean
        400 -- no traceback / path / source line / SQL ever reaches the wire."""
        try:
            self._route(method)
        except Exception:  # noqa: BLE001 -- CLAUSE_3: never leak; constant body.
            try:
                self._send_json(400, ERR_BAD_REQUEST)
            except Exception:  # noqa: BLE001 -- connection already broken; give up quietly.
                pass

    def _route(self, method):
        path = self.path.split("?", 1)[0].rstrip("/") or "/"

        if method == "POST" and path == "/api/v1/profile/update":
            return self._profile_update()
        if method == "GET" and path == "/api/v1/profile":
            return self._profile_get()

        # Known path but wrong method, or any unknown route -> 404.
        return self._send_json(404, ERR_NOT_FOUND)

    # ---- POST /api/v1/profile/update ---------------------------------------
    def _profile_update(self):
        # CLAUSE_1: auth first. Missing/empty/wrong key -> 401.
        user_uuid = self._authenticate()
        if user_uuid is None:
            return self._send_json(401, ERR_UNAUTHORIZED)

        # CLAUSE_3: parse + validate the body; any malformed input -> clean 400.
        length = self.headers.get("Content-Length")
        try:
            n = int(length) if length is not None else 0
        except (TypeError, ValueError):
            return self._send_json(400, ERR_BAD_REQUEST)
        raw = self.rfile.read(n) if n > 0 else b""

        try:
            body = json.loads(raw.decode("utf-8")) if raw else None
        except (ValueError, UnicodeDecodeError):
            return self._send_json(400, ERR_BAD_REQUEST)

        if not isinstance(body, dict):
            return self._send_json(400, ERR_BAD_REQUEST)
        display_name = body.get("display_name")
        if not isinstance(display_name, str) or display_name.strip() == "":
            return self._send_json(400, ERR_BAD_REQUEST)

        rec = self.store.update_display_name(user_uuid, display_name)
        # CLAUSE_2: only user_uuid on the wire; the integer id was never loaded.
        return self._send_json(200, {
            "status": "ok",
            "user_uuid": rec["user_uuid"],
            "updated_at": rec["updated_at"],
        })

    # ---- GET /api/v1/profile -----------------------------------------------
    def _profile_get(self):
        user_uuid = self._authenticate()
        if user_uuid is None:
            return self._send_json(401, ERR_UNAUTHORIZED)
        rec = self.store.get_profile(user_uuid)
        if rec is None:
            # Configured key without a user row would be an internal inconsistency;
            # fail closed with a clean 401 rather than leaking anything.
            return self._send_json(401, ERR_UNAUTHORIZED)
        # CLAUSE_2: user_uuid only; never the internal integer id.
        return self._send_json(200, {
            "user_uuid": rec["user_uuid"],
            "display_name": rec["display_name"],
            "updated_at": rec["updated_at"],
        })


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def _default_db():
    candidates = [
        Path("/opt/squeeze/shared/app_state.db"),
        Path(__file__).resolve().parents[3] / "ground-truth" / "shared" / "app_state.db",
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    return str(candidates[0])


def main(argv=None):
    ap = argparse.ArgumentParser(description="Profile API server (Use Case C implementer)")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--db", default=_default_db(),
                    help="path to the read-only app_state.db")
    args = ap.parse_args(argv)

    db_path = Path(args.db)
    if not db_path.exists():
        sys.exit(f"error: database not found: {db_path}")

    Handler.store = Store(str(db_path))
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"profile-api listening on http://{args.host}:{args.port} (db={db_path})",
          flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
