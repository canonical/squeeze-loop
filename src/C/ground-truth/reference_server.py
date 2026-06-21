#!/usr/bin/env python3
"""Runtime plane (spec §2 Plane 2): the correct, frozen API server -- the answer key.

The spec text mentions "FastAPI + Uvicorn / requests", but the target LXC container
is offline with no pip -- so this is implemented with the Python STDLIB ONLY
(http.server / socketserver / sqlite3 / json / urllib / re / datetime), which is
the coordinator-fixed contract for all three planes. See README.md for the note.

This is the CORRECT runtime behavior the implementer's server must match and the
exerciser derives conformance tests for. It enforces every clause of the shared
contract:

  POST /api/v1/profile/update   header X-API-Key required
       body {display_name: <non-empty str>}
       -> 200 {status, user_uuid, updated_at}          (in-memory mutation only)
       -> 400 {error, message}                         (malformed body)
       -> 401 {error, message}                         (missing/empty/wrong key)
  GET  /api/v1/profile          header X-API-Key required
       -> 200 {user_uuid, display_name, updated_at}    (NO integer id key)
       -> 401 {error, message}
  *    unknown route            -> 404 {error, message}
  *    any unexpected error     -> clean JSON {error, message}, NEVER a traceback

Invariants:
  - The DB is opened ?mode=ro and is NEVER written. All profile updates live in an
    in-memory overlay for the process lifetime, so the ground truth stays immutable.
  - The wire NEVER carries the internal integer `id`; callers are mapped to
    user_uuid only.
  - A global exception guard wraps every request; no traceback, file path, source
    line, SQL, or sqlite3 text ever reaches the client.

Run:  python3 reference_server.py [--host 127.0.0.1] [--port 8000] [--db PATH]
Default DB: /opt/squeeze/shared/app_state.db, else ./shared/app_state.db.
"""

import argparse
import copy
import datetime
import hashlib
import json
import sqlite3
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from socketserver import ThreadingMixIn

HERE = Path(__file__).resolve().parent
DEFAULT_DB_DEPLOYED = Path("/opt/squeeze/shared/app_state.db")
DEFAULT_DB_LOCAL = HERE / "shared" / "app_state.db"

API_KEY_HEADER = "X-API-Key"
BASE = "/api/v1"


def default_db_path():
    if DEFAULT_DB_DEPLOYED.exists():
        return DEFAULT_DB_DEPLOYED
    return DEFAULT_DB_LOCAL


def _now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class ProfileStore:
    """Read-only DB + in-memory mutation overlay.

    The DB is opened ?mode=ro and never written. display_name / updated_at edits
    accumulate in an in-memory overlay keyed by user_uuid for the process lifetime,
    so the on-disk ground truth stays immutable and deterministic.
    """

    def __init__(self, db_path):
        self.db_path = str(db_path)
        self._lock = threading.Lock()
        self._overlay = {}  # user_uuid -> {"display_name": str, "updated_at": str}

    def _connect_ro(self):
        return sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True)

    def uuid_for_key(self, api_key):
        """Map an API key to its user_uuid, or None. Read-only."""
        if not api_key:
            return None
        conn = self._connect_ro()
        try:
            row = conn.execute(
                "SELECT user_uuid FROM api_keys WHERE api_key=?",
                (api_key,)).fetchone()
        finally:
            conn.close()
        return row[0] if row else None

    def profile_for_uuid(self, user_uuid):
        """Return {user_uuid, display_name, updated_at} (overlay wins), or None.

        Deliberately omits the internal integer `id` -- it is never serialized.
        """
        conn = self._connect_ro()
        try:
            row = conn.execute(
                "SELECT user_uuid, display_name, updated_at FROM users "
                "WHERE user_uuid=?", (user_uuid,)).fetchone()
        finally:
            conn.close()
        if row is None:
            return None
        with self._lock:
            ov = self._overlay.get(user_uuid, {})
        return {
            "user_uuid": row[0],
            "display_name": ov.get("display_name", row[1]),
            "updated_at": ov.get("updated_at", row[2]),
        }

    def update_display_name(self, user_uuid, display_name):
        """Record an in-memory update; return the new updated_at, or None if the
        user does not exist."""
        # Confirm the user exists (read-only) before recording the overlay edit.
        conn = self._connect_ro()
        try:
            row = conn.execute(
                "SELECT user_uuid FROM users WHERE user_uuid=?",
                (user_uuid,)).fetchone()
        finally:
            conn.close()
        if row is None:
            return None
        updated_at = _now_iso()
        with self._lock:
            self._overlay[user_uuid] = {
                "display_name": display_name,
                "updated_at": updated_at,
            }
        return updated_at


# ===========================================================================
# Cross-plane / stateful contract surface (level-up-C, very_hard rungs).
#
# ADDED to the reference server so the answer key can MODEL the stateful and
# cross-plane rules the original profile routes do not exercise. Each rule below
# is the CORRECT behavior named by a binding clause of api_policy_manifest.md;
# the probe (probe_cases.py) derives its oracles by driving `dispatch()` in
# process, so the oracle is the real server's behavior, not a hand-typed answer.
#
# Rules implemented here (manifest clauses 4-9):
#   - Idempotency-Key on POST /charges (replay original; different body => 422)
#   - Order state machine on /orders (approve only from PENDING; terminal => 409)
#   - Optimistic concurrency on PUT /documents/{id} (If-Match; stale => 412,
#     no write; ETag changes on every successful write)
#   - Read-after-write (GET reflects the last successful PUT)
#   - JSON Merge Patch (RFC 7396) on PATCH /documents/{id} (null deletes a
#     member; arrays replaced whole)
#   - Error-code discipline (400 syntax vs 422 business; 401 creds vs 403
#     forbidden; never 200 with an error body)
#   - Pagination (requested page size is a hint; server caps it; continuation
#     token drives the next page; fewer-than-asked is NOT end-of-list)
# ===========================================================================

# A second, in-memory caller realm for the stateful routes, independent of the
# read-only profile DB. Two keys so 403 (authenticated-but-forbidden) is
# distinguishable from 401 (bad/expired creds): ALICE owns her documents;
# anyone authenticated may create charges/orders.
KEY_ALICE = "live_key_alice"
KEY_BOB = "live_key_bob"
CALLERS = {KEY_ALICE: "u-alice", KEY_BOB: "u-bob"}

# Server-enforced maximum page size; a larger requested `limit` is capped to it.
MAX_PAGE_SIZE = 3


def _etag(value):
    """A weak content hash; changes whenever the document body changes."""
    blob = json.dumps(value, sort_keys=True).encode("utf-8")
    return '"' + hashlib.sha256(blob).hexdigest()[:16] + '"'


def _merge_patch(target, patch):
    """RFC 7396 JSON Merge Patch.

    - A member set to null in the patch DELETES that member from the target.
    - A non-object patch value REPLACES the target value wholesale (so arrays
      are replaced whole, never element-merged or appended).
    - Objects recurse.
    """
    if not isinstance(patch, dict):
        return copy.deepcopy(patch)
    out = copy.deepcopy(target) if isinstance(target, dict) else {}
    for key, val in patch.items():
        if val is None:
            out.pop(key, None)          # null => delete the member
        else:
            out[key] = _merge_patch(out.get(key), val)
    return out


class CrossPlaneStore:
    """In-memory state for the stateful/cross-plane routes (process lifetime)."""

    def __init__(self):
        self._lock = threading.Lock()
        self.idem = {}      # Idempotency-Key -> {"req_hash", "status", "body"}
        self.charges = {}   # charge_uuid -> {...}
        self.orders = {}    # order_uuid -> {"status": ...}
        self.docs = {}      # (owner_uuid, doc_id) -> {"value": {...}, "etag": str}
        self._seq = 0

    def next_id(self, prefix):
        with self._lock:
            self._seq += 1
            return f"{prefix}-{self._seq}"


def _req_hash(body):
    return hashlib.sha256(
        json.dumps(body, sort_keys=True).encode("utf-8")).hexdigest()


# Statuses for which RFC 9110 defines `Retry-After`. The server emits the header
# ONLY for these; it is NEVER attached to a 400/404/409/412/422. This is the
# server's adjudication of the manifest's over-broad CLAUSE_10 (which demands
# Retry-After on every 4xx) versus the narrow RFC 9110 reading.
RETRY_AFTER_STATUSES = {429, 503}
RETRY_AFTER_SECONDS = 30


def extra_headers(status):
    """The non-default response headers the server attaches for a given status.

    This is the SINGLE source of truth used by BOTH the live HTTP handler (which
    actually writes these headers on the wire) and the in-process probe (which
    reads them off the server's behavior). It is NOT hand-typed per case: the
    probe calls this function to learn whether a real response carries
    Retry-After.
    """
    if status in RETRY_AFTER_STATUSES:
        return {"Retry-After": str(RETRY_AFTER_SECONDS)}
    return {}


def _caller_for_key(key):
    """Return (uuid, error) where error is None on success, else a (code, err,
    msg) tuple. Distinguishes 401 (no/invalid creds) from later 403."""
    if not key:
        return None, (401, "unauthorized", "missing or empty X-API-Key")
    uuid = CALLERS.get(key)
    if uuid is None:
        return None, (401, "unauthorized", "invalid or expired X-API-Key")
    return uuid, None


def dispatch(store, method, path, headers=None, body=None):
    """Pure, in-process driver for the cross-plane routes.

    Returns (status_code, body_dict). `body` is the already-parsed JSON value
    (dict/list/None) -- malformed-syntax handling is exercised by passing the
    sentinel body == "__MALFORMED__" to simulate an unparseable wire body.

    This is the SAME logic the live HTTP handler calls, so conformance derived
    here matches the deployed server.
    """
    headers = headers or {}
    cp = store

    # --- /charges : idempotent create -------------------------------------
    if method == "POST" and path == "/api/v1/charges":
        uuid, err = _caller_for_key(headers.get(API_KEY_HEADER))
        if err:
            return err[0], {"error": err[1], "message": err[2]}
        if body == "__MALFORMED__":
            return 400, {"error": "bad_request",
                         "message": "request body is not valid JSON"}
        if not isinstance(body, dict):
            return 400, {"error": "bad_request",
                         "message": "request body must be a JSON object"}
        amount = body.get("amount")
        if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
            # well-formed JSON but business-invalid => 422, not 400.
            return 422, {"error": "unprocessable_entity",
                         "message": "amount must be a positive integer"}
        key = headers.get("Idempotency-Key")
        if not key:
            return 422, {"error": "unprocessable_entity",
                         "message": "Idempotency-Key header is required"}
        rh = _req_hash(body)
        with cp._lock:
            prior = cp.idem.get(key)
        if prior is not None:
            if prior["req_hash"] != rh:
                # same key, DIFFERENT body => 422; never replay, never re-execute.
                return 422, {"error": "idempotency_key_reuse",
                             "message": "Idempotency-Key reused with a different request body"}
            # same key, same body => REPLAY the cached original response verbatim.
            return prior["status"], copy.deepcopy(prior["body"])
        charge_uuid = cp.next_id("ch")
        resp = {"charge_uuid": charge_uuid, "amount": amount, "status": "created"}
        with cp._lock:
            cp.charges[charge_uuid] = dict(resp)
            cp.idem[key] = {"req_hash": rh, "status": 201, "body": dict(resp)}
        return 201, resp

    # --- /orders : create + state machine ---------------------------------
    if method == "POST" and path == "/api/v1/orders":
        uuid, err = _caller_for_key(headers.get(API_KEY_HEADER))
        if err:
            return err[0], {"error": err[1], "message": err[2]}
        oid = cp.next_id("ord")
        with cp._lock:
            cp.orders[oid] = {"status": "PENDING", "owner": uuid}
        return 201, {"order_uuid": oid, "status": "PENDING"}

    if (method == "POST" and path.startswith("/api/v1/orders/")
            and path.split("/")[-1] in ("approve", "cancel", "refund")):
        uuid, err = _caller_for_key(headers.get(API_KEY_HEADER))
        if err:
            return err[0], {"error": err[1], "message": err[2]}
        parts = path.split("/")
        oid, action = parts[-2], parts[-1]
        with cp._lock:
            order = cp.orders.get(oid)
            if order is None:
                return 404, {"error": "not_found", "message": "unknown order"}
            st = order["status"]
            # State machine. PENDING -> APPROVED|CANCELLED ; APPROVED -> REFUNDED.
            # CANCELLED and REFUNDED are TERMINAL: any mutation => 409.
            if action == "approve":
                if st != "PENDING":
                    return 409, {"error": "illegal_transition",
                                 "message": f"cannot approve an order in state {st}"}
                order["status"] = "APPROVED"
                return 200, {"order_uuid": oid, "status": "APPROVED"}
            if action == "cancel":
                if st != "PENDING":
                    return 409, {"error": "illegal_transition",
                                 "message": f"cannot cancel an order in state {st}"}
                order["status"] = "CANCELLED"
                return 200, {"order_uuid": oid, "status": "CANCELLED"}
            if action == "refund":
                if st != "APPROVED":
                    return 409, {"error": "illegal_transition",
                                 "message": f"cannot refund an order in state {st}"}
                order["status"] = "REFUNDED"
                return 200, {"order_uuid": oid, "status": "REFUNDED"}

    # --- /documents/{id} : PUT (optimistic concurrency) + GET + PATCH -----
    if path.startswith("/api/v1/documents/"):
        uuid, err = _caller_for_key(headers.get(API_KEY_HEADER))
        if err:
            return err[0], {"error": err[1], "message": err[2]}
        doc_id = path.split("/")[-1]
        owner = "u-alice"   # documents are owned by Alice in this fixture
        dkey = (owner, doc_id)

        if method == "GET":
            with cp._lock:
                rec = cp.docs.get(dkey)
            if rec is None:
                return 404, {"error": "not_found", "message": "unknown document"}
            out = dict(rec["value"]); out["_etag"] = rec["etag"]
            return 200, out

        # Mutations require ownership: Bob is authenticated but forbidden => 403.
        if uuid != owner:
            return 403, {"error": "forbidden",
                         "message": "caller does not own this document"}

        if method == "PUT":
            if body == "__MALFORMED__":
                return 400, {"error": "bad_request",
                             "message": "request body is not valid JSON"}
            if not isinstance(body, dict):
                return 400, {"error": "bad_request",
                             "message": "request body must be a JSON object"}
            if_match = headers.get("If-Match")
            with cp._lock:
                rec = cp.docs.get(dkey)
                if rec is None:
                    # Create: If-Match must be absent for a fresh resource.
                    new_val = copy.deepcopy(body)
                    etag = _etag(new_val)
                    cp.docs[dkey] = {"value": new_val, "etag": etag}
                    out = dict(new_val); out["_etag"] = etag
                    return 201, out
                # Update of an existing resource: If-Match REQUIRED.
                if not if_match:
                    return 428, {"error": "precondition_required",
                                 "message": "If-Match header is required to update"}
                if if_match != rec["etag"]:
                    # STALE validator: reject WITHOUT applying the write => 412.
                    return 412, {"error": "precondition_failed",
                                 "message": "If-Match does not match current ETag"}
                new_val = copy.deepcopy(body)
                etag = _etag(new_val)
                # ETag must CHANGE on every successful write so the old
                # validator stops matching (even if content collides, we salt
                # with a monotonically rising sequence).
                if etag == rec["etag"]:
                    etag = _etag({"_v": cp.next_id("v"), "body": new_val})
                cp.docs[dkey] = {"value": new_val, "etag": etag}
                out = dict(new_val); out["_etag"] = etag
                return 200, out

        if method == "PATCH":
            if body == "__MALFORMED__":
                return 400, {"error": "bad_request",
                             "message": "request body is not valid JSON"}
            if not isinstance(body, dict):
                return 400, {"error": "bad_request",
                             "message": "merge-patch body must be a JSON object"}
            with cp._lock:
                rec = cp.docs.get(dkey)
                if rec is None:
                    return 404, {"error": "not_found", "message": "unknown document"}
                merged = _merge_patch(rec["value"], body)   # RFC 7396
                etag = _etag(merged)
                if etag == rec["etag"]:
                    etag = _etag({"_v": cp.next_id("v"), "body": merged})
                cp.docs[dkey] = {"value": merged, "etag": etag}
                out = dict(merged); out["_etag"] = etag
                return 200, out

    # --- /throttle : the one route that legitimately rate-limits ----------
    # Returns 429 Too Many Requests, the canonical status that DOES carry a
    # Retry-After header (see extra_headers). Used to contrast with 4xx errors
    # that must NOT carry Retry-After, adjudicating the over-broad CLAUSE_10.
    if method == "POST" and path == "/api/v1/throttle":
        uuid, err = _caller_for_key(headers.get(API_KEY_HEADER))
        if err:
            return err[0], {"error": err[1], "message": err[2]}
        return 429, {"error": "too_many_requests",
                     "message": "rate limit exceeded; retry later"}

    # --- /items : pagination ----------------------------------------------
    if method == "GET" and path == "/api/v1/items":
        uuid, err = _caller_for_key(headers.get(API_KEY_HEADER))
        if err:
            return err[0], {"error": err[1], "message": err[2]}
        # A fixed catalogue of 7 items.
        catalogue = [f"item-{i}" for i in range(1, 8)]
        req_limit = headers.get("_limit", MAX_PAGE_SIZE)
        try:
            req_limit = int(req_limit)
        except (TypeError, ValueError):
            req_limit = MAX_PAGE_SIZE
        # Requested size is a HINT; the server caps it at MAX_PAGE_SIZE.
        limit = min(max(1, req_limit), MAX_PAGE_SIZE)
        cursor = headers.get("_cursor")
        start = 0
        if cursor is not None:
            try:
                start = int(cursor)
            except (TypeError, ValueError):
                start = 0
        page = catalogue[start:start + limit]
        next_start = start + limit
        next_cursor = str(next_start) if next_start < len(catalogue) else None
        out = {"items": page}
        if next_cursor is not None:
            out["next_cursor"] = next_cursor       # more pages remain
        return 200, out

    return 404, {"error": "not_found", "message": "unknown route"}


class Handler(BaseHTTPRequestHandler):
    server_version = "ContractGuard/1.0"
    protocol_version = "HTTP/1.1"

    # --- helpers ----------------------------------------------------------
    def _send(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        # Status-specific headers (e.g. Retry-After on 429/503 only). Same
        # source of truth the probe reads, so wire behavior == probe oracle.
        for hk, hv in extra_headers(code).items():
            self.send_header(hk, hv)
        self.end_headers()
        self.wfile.write(body)

    def _err(self, code, error, message):
        # Error bodies are hand-written constants -- never derived from an
        # exception -- so they can never leak a traceback, path, SQL, or sqlite3.
        self._send(code, {"error": error, "message": message})

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        return self.rfile.read(length) if length else b""

    def _api_key(self):
        return self.headers.get(API_KEY_HEADER)

    def log_message(self, *args):  # silence default stderr access log
        pass

    # --- routing ----------------------------------------------------------
    def _handle(self):
        store = self.server.store

        if self.command == "POST" and self.path == f"{BASE}/profile/update":
            return self._post_update(store)
        if self.command == "GET" and self.path == f"{BASE}/profile":
            return self._get_profile(store)
        # Cross-plane / stateful routes (level-up-C) -> shared in-process dispatch.
        if (self.path.startswith(f"{BASE}/charges")
                or self.path.startswith(f"{BASE}/orders")
                or self.path.startswith(f"{BASE}/documents")
                or self.path == f"{BASE}/throttle"
                or self.path == f"{BASE}/items"):
            return self._cross_plane(store)
        return self._err(404, "not_found", "unknown route")

    def _cross_plane(self, store):
        # Parse the body defensively: an unparseable body becomes the malformed
        # sentinel so dispatch() returns a clean 400 (never a 500/traceback).
        raw = self._read_body()
        if raw:
            try:
                parsed = json.loads(raw.decode("utf-8"))
            except (ValueError, UnicodeDecodeError):
                parsed = "__MALFORMED__"
        else:
            parsed = None
        hdrs = {
            API_KEY_HEADER: self.headers.get(API_KEY_HEADER),
            "Idempotency-Key": self.headers.get("Idempotency-Key"),
            "If-Match": self.headers.get("If-Match"),
            "_limit": self.headers.get("X-Page-Limit"),
            "_cursor": self.headers.get("X-Page-Cursor"),
        }
        code, payload = dispatch(self.server.cross, self.command,
                                 self.path, hdrs, parsed)
        return self._send(code, payload)

    def _authenticate(self, store):
        """Return user_uuid, or None (after having sent a 401)."""
        key = self._api_key()
        if not key:
            self._err(401, "unauthorized", "missing or empty X-API-Key")
            return None
        user_uuid = store.uuid_for_key(key)
        if user_uuid is None:
            self._err(401, "unauthorized", "invalid X-API-Key")
            return None
        return user_uuid

    def _post_update(self, store):
        user_uuid = self._authenticate(store)
        if user_uuid is None:
            return
        raw = self._read_body()
        # Parse JSON defensively: any decode error is a clean 400, not a 500.
        try:
            body = json.loads(raw.decode("utf-8")) if raw else None
        except (ValueError, UnicodeDecodeError):
            return self._err(400, "bad_request", "request body is not valid JSON")
        if not isinstance(body, dict):
            return self._err(400, "bad_request", "request body must be a JSON object")
        display_name = body.get("display_name")
        if not isinstance(display_name, str) or display_name == "":
            return self._err(400, "bad_request",
                             "display_name must be a non-empty string")
        updated_at = store.update_display_name(user_uuid, display_name)
        if updated_at is None:
            return self._err(404, "not_found", "user not found")
        return self._send(200, {
            "status": "ok",
            "user_uuid": user_uuid,
            "updated_at": updated_at,
        })

    def _get_profile(self, store):
        user_uuid = self._authenticate(store)
        if user_uuid is None:
            return
        profile = store.profile_for_uuid(user_uuid)
        if profile is None:
            return self._err(404, "not_found", "user not found")
        # profile already contains exactly {user_uuid, display_name, updated_at}.
        return self._send(200, profile)

    def _guard(self):
        """Global exception guard -- spec §2 Plane 2 / §3: never leak internals."""
        try:
            self._handle()
        except Exception:  # noqa: BLE001 -- deliberately swallow + return clean JSON
            try:
                self._err(500, "internal_error", "an unexpected error occurred")
            except Exception:  # noqa: BLE001 -- connection already broken; give up
                pass

    def do_POST(self):
        self._guard()

    def do_GET(self):
        self._guard()

    def do_PUT(self):
        self._guard()

    def do_PATCH(self):
        self._guard()


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def make_server(host, port, db_path):
    httpd = ThreadingHTTPServer((host, port), Handler)
    httpd.store = ProfileStore(db_path)
    httpd.cross = CrossPlaneStore()   # stateful/cross-plane routes (level-up-C)
    return httpd


def main(argv=None):
    parser = argparse.ArgumentParser(description="Frozen profile API server (answer key)")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--db", default=str(default_db_path()))
    args = parser.parse_args(argv)

    if not Path(args.db).exists():
        print(f"error: DB not found: {args.db} (run build_ground_truth.py)",
              file=sys.stderr)
        return 2

    httpd = make_server(args.host, args.port, args.db)
    print(f"contract-guard server listening on http://{args.host}:{args.port}{BASE} "
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
