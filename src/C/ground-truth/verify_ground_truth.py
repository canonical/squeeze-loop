#!/usr/bin/env python3
"""Self-check of the ground truth -- the executable lower bound (spec §2/§4).

Exits nonzero on any failure, printing a Gate-B-style report:

  1. LINT         base_schema.json passes the document-plane linter
  2. RECOMPUTE    ty0_baseline hash matches a freshly recomputed reflection
                  (the "every signature recomputes" invariant, §4)
  3. READ-ONLY    app_state.db opened ?mode=ro rejects an INSERT (§2 Plane 2)
  4. PERMISSIONS  artifacts are 0444 (warn-only off-container, where we aren't root)
  5. ENDPOINTS    boot reference_server.py on a free port and check the canonical
                  behaviors of the shared contract (no traceback leaks, no integer
                  id on the wire). Then tear the server down.
"""

import json
import socket
import sqlite3
import stat
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

import build_ground_truth as bgt
import linter
import reflection

HERE = Path(__file__).resolve().parent
SHARED = HERE / "shared"
DB = SHARED / "app_state.db"
BASE_SCHEMA = SHARED / "base_schema.json"
TY0 = SHARED / "ty0_baseline.json"

API_KEY = "test_secure_token_abc123"
# Substrings that must NEVER appear in an error body (no internal leakage).
LEAK_MARKERS = ["Traceback", 'File "', "line ", "sqlite3.", "SELECT"]


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))
    return ok


def _free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _request(method, url, payload=None, headers=None):
    """Return (status, body_dict, raw_text). HTTPError is mapped to its code."""
    data = None
    hdrs = dict(headers or {})
    if payload is not None:
        data = payload if isinstance(payload, bytes) else json.dumps(payload).encode("utf-8")
        hdrs.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            raw = r.read().decode("utf-8")
            return r.status, _maybe_json(raw), raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8")
        return e.code, _maybe_json(raw), raw


def _maybe_json(raw):
    try:
        return json.loads(raw)
    except ValueError:
        return None


def check_endpoints():
    """Boot reference_server.py on a free port and exercise the contract."""
    import reference_server
    port = _free_port()
    base = f"http://127.0.0.1:{port}/api/v1"
    httpd = reference_server.make_server("127.0.0.1", port, str(DB))
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    time.sleep(0.2)
    try:
        ok = True

        # authed POST update -> 200 {status, user_uuid, updated_at}
        st, body, _ = _request("POST", f"{base}/profile/update",
                               {"display_name": "Ada L."},
                               {"X-API-Key": API_KEY})
        ok &= check("  authed POST update -> 200",
                    st == 200 and isinstance(body, dict)
                    and set(body.keys()) == {"status", "user_uuid", "updated_at"}
                    and body.get("user_uuid") == "u-0001",
                    f"status={st} keys={sorted(body.keys()) if isinstance(body, dict) else body}")

        # unauthenticated POST -> 401 {error, message}
        st, body, _ = _request("POST", f"{base}/profile/update",
                               {"display_name": "x"})
        ok &= check("  unauthenticated POST -> 401",
                    st == 401 and isinstance(body, dict)
                    and set(body.keys()) == {"error", "message"},
                    f"status={st}")

        # wrong key -> 401
        st, body, _ = _request("POST", f"{base}/profile/update",
                               {"display_name": "x"}, {"X-API-Key": "wrong"})
        ok &= check("  wrong-key POST -> 401",
                    st == 401 and isinstance(body, dict)
                    and set(body.keys()) == {"error", "message"},
                    f"status={st}")

        # malformed POST (valid key, junk body) -> 400 with NO leak
        st, body, raw = _request("POST", f"{base}/profile/update",
                                 b"{not json at all}", {"X-API-Key": API_KEY})
        leaked = [m for m in LEAK_MARKERS if m in raw]
        ok &= check("  malformed POST -> 400 (no leak)",
                    st == 400 and isinstance(body, dict)
                    and set(body.keys()) == {"error", "message"}
                    and not leaked,
                    f"status={st} leaked={leaked}")

        # missing display_name -> 400
        st, body, raw = _request("POST", f"{base}/profile/update",
                                 {"name": "x"}, {"X-API-Key": API_KEY})
        ok &= check("  missing display_name -> 400",
                    st == 400 and set(body.keys()) == {"error", "message"},
                    f"status={st}")

        # GET profile authed -> 200 with user_uuid and NO 'id' key
        st, body, _ = _request("GET", f"{base}/profile", None, {"X-API-Key": API_KEY})
        ok &= check("  authed GET profile -> 200 (no id key)",
                    st == 200 and isinstance(body, dict)
                    and "id" not in body
                    and set(body.keys()) == {"user_uuid", "display_name", "updated_at"}
                    and body.get("user_uuid") == "u-0001"
                    # the in-memory mutation above must be reflected
                    and body.get("display_name") == "Ada L.",
                    f"status={st} keys={sorted(body.keys()) if isinstance(body, dict) else body}")

        # unauthenticated GET -> 401
        st, body, _ = _request("GET", f"{base}/profile")
        ok &= check("  unauthenticated GET -> 401",
                    st == 401 and set(body.keys()) == {"error", "message"},
                    f"status={st}")

        # unknown route -> 404
        st, body, _ = _request("GET", f"{base}/nope", None, {"X-API-Key": API_KEY})
        ok &= check("  unknown route -> 404",
                    st == 404 and set(body.keys()) == {"error", "message"},
                    f"status={st}")

        return ok
    finally:
        httpd.shutdown()
        httpd.server_close()


def main():
    if not DB.exists() or not BASE_SCHEMA.exists() or not TY0.exists():
        print("ground truth not built; run build_ground_truth.py")
        return 2

    ok = True

    # 1. linter passes on the canonical contract
    lint_errors = linter.lint_file(str(BASE_SCHEMA))
    ok &= check("base_schema.json lints clean", not lint_errors,
                f"{len(lint_errors)} problem(s)" if lint_errors else "")
    for e in lint_errors:
        print(f"    - {e}")

    # 2. TY0 hash recomputes (every signature recomputes)
    stored = json.loads(TY0.read_text())
    fresh_snapshot = reflection.reflect(DB)
    fresh = reflection.manifest_hash(fresh_snapshot)
    same_body = {k: v for k, v in stored.items() if k != "hash"} == fresh_snapshot
    ok &= check("ty0 hash recomputes", stored.get("hash") == fresh and same_body,
                f"{str(stored.get('hash'))[:12]}... vs {fresh[:12]}...")

    # 3. read-only enforcement at the engine level
    ro = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    try:
        ro.execute("INSERT INTO users(id,user_uuid,display_name,updated_at) "
                   "VALUES (99,'u-hack','Hacker','2025-01-01T00:00:00Z')")
        ro.commit()
        ro_ok = False
    except sqlite3.OperationalError:
        ro_ok = True
    finally:
        ro.close()
    ok &= check("read-only db", ro_ok, "engine rejects writes")

    # 4. permissions (warn-only off-container)
    perm_targets = [DB, BASE_SCHEMA, TY0]
    perms = {p.name: stat.S_IMODE(p.stat().st_mode) for p in perm_targets}
    if all(m == 0o444 for m in perms.values()):
        check("permissions 0444", True)
    else:
        print("[WARN] not all artifacts are 0444 (expected only after root deploy): "
              + ", ".join(f"{k}={oct(v)}" for k, v in sorted(perms.items())))

    # 5. endpoint smoke test (boot + tear down)
    try:
        ep_ok = check_endpoints()
        ok &= check("endpoints (split-plane runtime behaviors)", ep_ok)
    except Exception as e:  # noqa: BLE001 -- surface, don't crash the report
        ok = False
        check("endpoints (split-plane runtime behaviors)", False, f"error: {e}")

    print("VERIFY OK" if ok else "VERIFY FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
