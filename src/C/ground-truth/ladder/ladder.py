"""Difficulty ladder for Use Case C (level-up-C.md): contract surface + cross-plane
consistency.

The richness of the experiment comes from the richness of the upper bound. For C
that richness is the breadth/subtlety of the contract and the number of clauses
where the document plane (the OpenAPI contract) and the runtime plane (the live
server) can silently diverge -- the "blending" failure. Each rung is a contract
clause of rising richness with a CORRECT server and FORK servers that pass the
happy path but blend a plane. A fork is CAUGHT when a conformance case derived from
the contract fails against it.

Servers are modeled as pure handlers `h(state, req) -> (status, body_dict)` (the
runtime plane), deterministic and stateful within a case -- the same checks a live
http.server would face, without ports. Conformance cases are sequences of requests
plus a predicate over the responses (the contract clause).
"""
TOKEN = "test_secure_token_abc123"


def req(method, path, headers=None, body=None):
    return {"method": method, "path": path, "headers": headers or {}, "body": body}


# ===========================================================================
# R1 trivial -- GET returns 200 with a documented field
def r1_correct(s, q):
    if q["method"] == "GET" and q["path"] == "/ping":
        return 200, {"status": "ok"}
    return 404, {"error": "not_found"}

def r1_missing_field(s, q):
    return (200, {}) if q["path"] == "/ping" else (404, {"error": "not_found"})


# R2 easy -- auth required on a mutation
def r2_correct(s, q):
    if q["headers"].get("X-API-Key") == TOKEN:
        return 200, {"status": "updated"}
    return 401, {"error": "unauthorized", "message": "missing or invalid key"}

def r2_skips_auth(s, q):
    return 200, {"status": "updated"}                       # runtime skips the check


# R3 medium -- no internal-id leak; clean typed errors (no traceback)
def r3_correct(s, q):
    if q["method"] == "GET" and q["path"] == "/profile":
        return 200, {"user_uuid": "u-1", "display_name": "Alice"}
    if q["body"] == "MALFORMED":
        return 400, {"error": "bad_request", "message": "invalid body"}
    return 200, {"user_uuid": "u-1", "display_name": "Alice"}

def r3_leaks_id(s, q):
    if q["method"] == "GET" and q["path"] == "/profile":
        return 200, {"id": 42, "user_uuid": "u-1", "display_name": "Alice"}  # leaks integer id
    return 400, {"error": "bad_request", "message": "invalid body"}

def r3_traceback(s, q):
    if q["body"] == "MALFORMED":
        return 500, {"error": "Traceback (most recent call last): File main.py line 42, KeyError"}
    return 200, {"user_uuid": "u-1", "display_name": "Alice"}


# R4 hard -- order state machine (create -> approve/cancel; approve-after-cancel illegal)
def r4_correct(s, q):
    st = s.get("status")
    if q["path"] == "/order/create":
        s["status"] = "draft"; return 201, {"status": "draft"}
    if q["path"] == "/order/approve":
        if st == "cancelled":
            return 409, {"error": "illegal_transition"}
        s["status"] = "approved"; return 200, {"status": "approved"}
    if q["path"] == "/order/cancel":
        s["status"] = "cancelled"; return 200, {"status": "cancelled"}
    return 404, {"error": "not_found"}

def r4_allows_illegal(s, q):
    if q["path"] == "/order/create":
        return 201, {"status": "draft"}
    if q["path"] == "/order/approve":
        return 200, {"status": "approved"}                 # never rejects (no state machine)
    if q["path"] == "/order/cancel":
        return 200, {"status": "cancelled"}
    return 404, {"error": "not_found"}


# R5 very hard -- cross-plane consistency under state (read-after-write; idempotency)
def r5_correct(s, q):
    if q["path"] == "/profile/update":
        s["name"] = q["body"]; return 200, {"status": "ok"}
    if q["path"] == "/profile":
        return 200, {"user_uuid": "u-1", "display_name": s.get("name", "Alice")}
    if q["path"] == "/order/create":
        idem = s.setdefault("idem", {}); k = q["headers"].get("Idempotency-Key")
        if k in idem:
            return 200, {"uuid": idem[k]}
        uuid = f"ord-{len(idem) + 1}"; idem[k] = uuid; return 201, {"uuid": uuid}
    return 404, {"error": "not_found"}

def r5_write_ignored(s, q):
    if q["path"] == "/profile/update":
        return 200, {"status": "ok"}                        # 200 but does NOT persist
    if q["path"] == "/profile":
        return 200, {"user_uuid": "u-1", "display_name": "Alice"}
    return r5_correct(s, q)

def r5_idem_ignored(s, q):
    if q["path"] == "/order/create":
        s["n"] = s.get("n", 0) + 1; return 201, {"uuid": f"ord-{s['n']}"}  # new each time
    return r5_correct(s, q)


def _last_status(resps): return resps[-1][0]
def _body(resps, i=-1): return resps[i][1]

RUNGS = [
    {"id": "API_L1", "tier": "trivial", "clause": "GET returns 200 with documented field",
     "correct": r1_correct,
     "forks": [{"name": "missing_field", "handler": r1_missing_field, "why": "drops the documented 'status' field"}],
     "cases": [{"name": "ping", "steps": [req("GET", "/ping")],
                "ok": lambda r: r[-1][0] == 200 and "status" in _body(r)}]},
    {"id": "API_L2", "tier": "easy", "clause": "auth required on mutation (401 without token)",
     "correct": r2_correct,
     "forks": [{"name": "skips_auth", "handler": r2_skips_auth, "why": "returns 200 with no token (runtime skips auth the docs claim)"}],
     "cases": [{"name": "authed", "steps": [req("POST", "/profile/update", {"X-API-Key": TOKEN}, {"display_name": "Bob"})],
                "ok": lambda r: r[-1][0] == 200},
               {"name": "unauthed", "steps": [req("POST", "/profile/update", {}, {"display_name": "X"})],
                "ok": lambda r: r[-1][0] == 401}]},
    {"id": "API_L3", "tier": "medium", "clause": "no internal-id leak; clean typed errors",
     "correct": r3_correct,
     "forks": [{"name": "leaks_id", "handler": r3_leaks_id, "why": "exposes the internal integer id on the wire"},
               {"name": "traceback", "handler": r3_traceback, "why": "leaks a raw traceback on a malformed body"}],
     "cases": [{"name": "no_id_leak", "steps": [req("GET", "/profile", {"X-API-Key": TOKEN})],
                "ok": lambda r: r[-1][0] == 200 and "id" not in _body(r) and "user_uuid" in _body(r)},
               {"name": "clean_error", "steps": [req("POST", "/profile/update", {"X-API-Key": TOKEN}, "MALFORMED")],
                "ok": lambda r: r[-1][0] == 400 and "traceback" not in str(_body(r)).lower()}]},
    {"id": "API_L4", "tier": "hard", "clause": "order state machine: approve-after-cancel is illegal",
     "correct": r4_correct,
     "forks": [{"name": "allows_illegal", "handler": r4_allows_illegal, "why": "permits approve after cancel (no state machine)"}],
     "cases": [{"name": "legal_path", "steps": [req("POST", "/order/create"), req("POST", "/order/approve")],
                "ok": lambda r: r[-1][0] == 200},
               {"name": "illegal_path", "steps": [req("POST", "/order/create"), req("POST", "/order/cancel"), req("POST", "/order/approve")],
                "ok": lambda r: r[-1][0] == 409}]},
    {"id": "API_L5", "tier": "very_hard", "clause": "cross-plane consistency under state (read-after-write; idempotency)",
     "correct": r5_correct,
     "forks": [{"name": "write_ignored", "handler": r5_write_ignored, "why": "update returns 200 but a later read is stale (docs say X, runtime does Y)"},
               {"name": "idem_ignored", "handler": r5_idem_ignored, "why": "duplicate create with same Idempotency-Key yields a new resource"}],
     "cases": [{"name": "read_after_write", "steps": [req("POST", "/profile/update", {"X-API-Key": TOKEN}, "Bob"), req("GET", "/profile", {"X-API-Key": TOKEN})],
                "ok": lambda r: _body(r).get("display_name") == "Bob"},
               {"name": "idempotency", "steps": [req("POST", "/order/create", {"Idempotency-Key": "K1"}), req("POST", "/order/create", {"Idempotency-Key": "K1"})],
                "ok": lambda r: _body(r, 0).get("uuid") == _body(r, 1).get("uuid")}]},
]
