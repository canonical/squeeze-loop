#!/usr/bin/env python3
"""DEFECT-RESOLUTION probe for Use Case C (API Contract Guard, split planes).

REDESIGN (soft-truth-with-defects).
-----------------------------------
The previous version of this probe paired each scenario with a manifest that
PINNED exactly one answer, so a capable model just read the rule and complied:
no error surface. That defeats the experiment.

This version embeds the manifest's DELIBERATE CONTRADICTIONS (see
../upper-bound/api_policy_manifest.md, MANIFEST_ID API_POLICY_083). Every case's
`system` text quotes BOTH sides of a real, citable standards conflict
(RFC 7396 vs Zalando #123; RFC 9110's 404-MAY vs Google AIP-193's 403-MUST; an
over-broad Retry-After clause; "all client errors are 400" vs the 401/422 split;
"POST is never idempotent" vs the idempotency-key replay clause). A competent
reader can therefore land on a COHERENT-BUT-WRONG resolution. The contract prose
does not adjudicate the conflict — the executable reference server does. We
measure whether a model resolves each contradiction the way the SERVER does or
diverges to the other (coherent) authority.

ORACLE PROVENANCE
-----------------
Every oracle is derived by ACTUALLY EXECUTING the scenario against the frozen
reference server (reference_server.py) IN PROCESS via reference_server.dispatch()
(and reference_server.extra_headers() for the Retry-After point) — the same code
the live HTTP handler runs. No oracle below is hand-typed: build_cases() replays
the call sequence against a fresh CrossPlaneStore and reads the answer off the
real server's responses.

Each case's `options` always include the coherent-but-wrong resolution (the OTHER
side of the contradiction), distinct from the oracle.

Public API:  build_cases() -> list[dict]
Self-test:   python3 probe_cases.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import reference_server as R  # noqa: E402

AK = R.API_KEY_HEADER
ALICE = {AK: R.KEY_ALICE}
BOB = {AK: R.KEY_BOB}

REASON = "Reason briefly, then end with a line EXACTLY: ANSWER: <one option>"


# ---------------------------------------------------------------------------
# Contested-point contract slices. EACH quotes BOTH conflicting clauses so the
# model genuinely sees the contradiction and must resolve it. (Normative prose
# only, no code — self-contained for a model run.)
# ---------------------------------------------------------------------------

SYS_PATCH_NULL = (
    "API contract (binding, BUT self-contradictory on this point — you must "
    "resolve it).\n"
    "CLAUSE_8 (RFC 7396, JSON Merge Patch): on PATCH /api/v1/documents/{id}, a "
    "member whose patch value is null is given special meaning: it DELETES that "
    "member from the target resource (it is NOT stored as a literal null).\n"
    "CLAUSE_8G (Zalando RESTful API Guidelines, Rule #123, GOVERNANCE OVERRIDE): "
    "a field that is null and a field that is absent MUST be treated identically; "
    "null carries no mutating intent, so a null member NEVER deletes and NEVER "
    "mutates state.\n"
    "These two clauses directly contradict each other (delete vs ignore). Decide "
    "what the server actually does."
)

SYS_PATCH_ARRAY = (
    "API contract (binding). PATCH /api/v1/documents/{id} uses JSON Merge Patch "
    "(RFC 7396): a member whose patch value is an array REPLACES the existing "
    "array wholesale (it is never element-merged or appended)."
)

SYS_DISCLOSE = (
    "API contract (binding, BUT self-contradictory on this point — you must "
    "resolve it).\n"
    "CLAUSE_9 (RFC 9110 §15.5, MAY): to avoid disclosing a resource's existence "
    "to a party not entitled to know of it, the server MAY return 404 Not Found "
    "instead of 403 to an unauthorized caller; accordingly an authenticated "
    "caller lacking permission SHOULD receive 404 so existence is hidden.\n"
    "CLAUSE_9A (Google AIP-193 / AIP-211, MUST): a service MUST return 403 "
    "Forbidden (not 404, not 401) when an authenticated principal lacks "
    "permission on an existing target; existence is not hidden from an "
    "authenticated principal.\n"
    "These two clauses directly contradict each other (hide with 404 vs disclose "
    "with 403). Decide what the server actually does."
)

SYS_RETRY_AFTER = (
    "API contract (binding, BUT contains an over-broad clause — you must decide "
    "whether the server obeys it literally).\n"
    "CLAUSE_10: for retry-friendliness, EVERY client-error (4xx) response MUST "
    "include a Retry-After header advising when to retry.\n"
    "Background: RFC 9110 defines Retry-After only for 503 and 429; it has no "
    "defined meaning on a 400/404/409/412/422. Decide whether the server "
    "actually attaches Retry-After to the 4xx error in question."
)

SYS_ERR_TAXONOMY = (
    "API contract (binding, BUT self-contradictory on this point — you must "
    "resolve it).\n"
    "CLAUSE_11: for a uniform error surface, ALL client errors MUST return 400 "
    "Bad Request.\n"
    "CLAUSE_11A: validation failures (well-formed body, business-invalid) MUST "
    "return 422; authentication failures (missing/invalid/expired credentials) "
    "MUST return 401; 400 is reserved strictly for malformed request SYNTAX (an "
    "unparseable body).\n"
    "These two clauses directly contradict each other on every overlapping case. "
    "Decide what the server actually does."
)

SYS_POST_IDEM = (
    "API contract (binding, BUT self-contradictory on this point — you must "
    "resolve it).\n"
    "CLAUSE_12 (RFC 9110 §9.2.2, general principle): POST is NOT an idempotent "
    "method; repeating a POST is expected to create an additional resource each "
    "time.\n"
    "CLAUSE_12A (idempotency-key exception): POST /api/v1/charges REQUIRES an "
    "Idempotency-Key; a repeated POST carrying the SAME key and an equivalent "
    "body MUST NOT create a second resource — it replays the first response "
    "verbatim (same charge_uuid). A repeated key with a DIFFERENT body is "
    "rejected 422.\n"
    "These two clauses contradict for the keyed-duplicate case (create-again vs "
    "replay). Decide what the server actually does."
)

SYS_STATE_TERMINAL = (
    "API contract (binding, BUT self-contradictory on this point — you must "
    "resolve it).\n"
    "CLAUSE_5: an order is created PENDING; PENDING -> APPROVED or CANCELLED; "
    "APPROVED -> REFUNDED; CANCELLED and REFUNDED are TERMINAL. Any mutating "
    "action on a resource in a non-permitting state MUST be rejected 409 and "
    "leave state unchanged; it must NOT be a silent 200 no-op.\n"
    "CLAUSE_12 (general principle): mutating verbs SHOULD be idempotent where "
    "possible, so re-issuing an action that has already taken effect (e.g. "
    "refunding an already-REFUNDED order, cancelling an already-CANCELLED order) "
    "SHOULD return a 200 no-op rather than an error.\n"
    "These two readings contradict for the repeat-terminal-action case (409 vs "
    "200 no-op). Decide what the server actually does."
)

SYS_CONC = (
    "API contract (binding). Updating an existing document via PUT "
    "/api/v1/documents/{id} REQUIRES an If-Match validator holding the current "
    "ETag. A stale If-Match must be rejected 412 and the write MUST NOT be "
    "applied. Every successful write assigns a NEW ETag. A read immediately "
    "after a successful write must reflect the new value."
)

SYS_PAGE = (
    "API contract (binding). GET /api/v1/items: the requested page size is a "
    "HINT the server MAY cap at its own maximum. A page with fewer items than "
    "requested does NOT mean end-of-collection. End-of-collection is signalled "
    "ONLY by the absence of a continuation token (next_cursor)."
)


def _run(steps, store=None):
    """Replay a list of (method, path, headers, body) against a server (fresh if
    not supplied). Returns (responses, store)."""
    s = store if store is not None else R.CrossPlaneStore()
    out = []
    for method, path, headers, body in steps:
        out.append(R.dispatch(s, method, path, headers, body))
    return out, s


def build_cases():
    cases = []

    # =====================================================================
    # CONTESTED POINT 8 — MERGE-PATCH null  (RFC 7396 delete  vs  Zalando #123 ignore)
    # =====================================================================
    # 1. null member: server follows RFC 7396 => DELETED. Zalando side => UNCHANGED.
    s = R.CrossPlaneStore()
    R.dispatch(s, "PUT", "/api/v1/documents/d1", ALICE, {"title": "T", "subtitle": "S"})
    p = R.dispatch(s, "PATCH", "/api/v1/documents/d1", ALICE, {"subtitle": None})
    body = p[1]
    if "subtitle" not in body:
        oracle = "DELETED"
    elif body.get("subtitle") is None:
        oracle = "SET_NULL"
    else:
        oracle = "UNCHANGED"
    cases.append({
        "id": "C_patch_null_1", "instance": "C", "system": SYS_PATCH_NULL,
        "user": (
            "Document d1 is {\"title\": \"T\", \"subtitle\": \"S\"}. A PATCH "
            "/api/v1/documents/d1 with body {\"subtitle\": null} arrives. The two "
            "clauses conflict on what null means. Per this contract, what should "
            "this endpoint do to the subtitle member? Resolve the conflict as you "
            "judge best.\n"
            "Options: DELETED (subtitle removed), UNCHANGED (subtitle still 'S'), "
            "SET_NULL (stored as literal null). "
            + REASON),
        "options": ["DELETED", "UNCHANGED", "SET_NULL"],
        "oracle": oracle,
        "fork": "follows Zalando #123 (ignore null) instead of RFC 7396 (delete)",
    })

    # 2. Read-after-write confirming the delete: GET shows subtitle absent.
    g = R.dispatch(s, "GET", "/api/v1/documents/d1", ALICE, None)
    gbody = g[1]
    if "subtitle" not in gbody:
        oracle = "ABSENT"
    elif gbody.get("subtitle") is None:
        oracle = "NULL"
    else:
        oracle = "PRESENT_S"
    cases.append({
        "id": "C_patch_null_2", "instance": "C", "system": SYS_PATCH_NULL,
        "user": (
            "Continuing: after the PATCH {\"subtitle\": null} on d1, a client does "
            "GET /api/v1/documents/d1. The clauses conflict; decide how YOU would "
            "implement this endpoint and pick the matching option for what the read "
            "shows for subtitle.\n"
            "Options: ABSENT (no subtitle key at all), PRESENT_S (subtitle still "
            "'S'), NULL (subtitle present as null). "
            + REASON),
        "options": ["ABSENT", "PRESENT_S", "NULL"],
        "oracle": oracle,
        "fork": "Zalando-style ignore keeps subtitle='S' after a null patch",
    })

    # 3. (uncontested companion) array member REPLACED whole, not appended.
    s = R.CrossPlaneStore()
    R.dispatch(s, "PUT", "/api/v1/documents/d2", ALICE, {"tags": ["a", "b", "c"]})
    p = R.dispatch(s, "PATCH", "/api/v1/documents/d2", ALICE, {"tags": ["z"]})
    tags = p[1].get("tags")
    if tags == ["z"]:
        oracle = "REPLACED"
    elif tags in (["a", "b", "c", "z"], ["z", "a", "b", "c"]):
        oracle = "APPENDED"
    else:
        oracle = "OTHER"
    cases.append({
        "id": "C_patch_array_1", "instance": "C", "system": SYS_PATCH_ARRAY,
        "user": (
            "Document d2 is {\"tags\": [\"a\",\"b\",\"c\"]}. PATCH "
            "/api/v1/documents/d2 with body {\"tags\": [\"z\"]} arrives. Per this "
            "contract, what should this endpoint do to the tags value? Resolve as "
            "you judge best.\n"
            "Options: REPLACED (tags becomes [\"z\"]), APPENDED (tags becomes "
            "[\"a\",\"b\",\"c\",\"z\"]), MERGED (set union). " + REASON),
        "options": ["REPLACED", "APPENDED", "MERGED"],
        "oracle": oracle,
        "fork": "merge-patch appends/merges the array instead of replacing it",
    })

    # =====================================================================
    # CONTESTED POINT 9 — DISCLOSURE  (RFC 9110 404-hide  vs  AIP-193 403-MUST)
    # =====================================================================
    # 4. Authenticated-but-forbidden: server follows AIP-193 => 403. 404 = wrong.
    s = R.CrossPlaneStore()
    R.dispatch(s, "PUT", "/api/v1/documents/d3", ALICE, {"title": "alice-doc"})
    forbidden = R.dispatch(s, "PUT", "/api/v1/documents/d3", BOB, {"title": "bob-was-here"})
    oracle = {403: "ERROR_403", 404: "ERROR_404", 401: "ERROR_401"}.get(
        forbidden[0], str(forbidden[0]))
    cases.append({
        "id": "C_disclosure_1", "instance": "C", "system": SYS_DISCLOSE,
        "user": (
            "Document d3 is owned by Alice. Bob presents a VALID API key (he is "
            "authenticated) and sends PUT /api/v1/documents/d3 to overwrite it. "
            "Bob does not own d3. The two clauses conflict on which status to "
            "return. Per this contract, what should this endpoint do? Resolve the "
            "conflict as you judge best.\n"
            "Options: ERROR_403 (403 Forbidden), ERROR_404 (404 Not Found), "
            "ERROR_401 (401 Unauthorized). " + REASON),
        "options": ["ERROR_403", "ERROR_404", "ERROR_401"],
        "oracle": oracle,
        "fork": "follows RFC 9110 404-hide instead of AIP-193 403-MUST",
    })

    # 5. Same conflict, on a PATCH by the forbidden caller.
    s = R.CrossPlaneStore()
    R.dispatch(s, "PUT", "/api/v1/documents/d4", ALICE, {"title": "alice"})
    forbidden = R.dispatch(s, "PATCH", "/api/v1/documents/d4", BOB, {"title": "bob"})
    oracle = {403: "ERROR_403", 404: "ERROR_404", 401: "ERROR_401"}.get(
        forbidden[0], str(forbidden[0]))
    cases.append({
        "id": "C_disclosure_2", "instance": "C", "system": SYS_DISCLOSE,
        "user": (
            "Document d4 exists and is owned by Alice. Bob (authenticated, valid "
            "key, not the owner) sends PATCH /api/v1/documents/d4 with body "
            "{\"title\": \"bob\"}. The clauses conflict; decide how YOU would "
            "implement this endpoint and pick the matching option.\n"
            "Options: ERROR_404 (404 Not Found), ERROR_403 (403 Forbidden), "
            "ERROR_401 (401 Unauthorized). " + REASON),
        "options": ["ERROR_404", "ERROR_403", "ERROR_401"],
        "oracle": oracle,
        "fork": "follows RFC 9110 404-hide instead of AIP-193 403-MUST",
    })

    # =====================================================================
    # CONTESTED POINT 10 — Retry-After  (over-broad CLAUSE_10  vs  RFC 9110 narrow)
    # =====================================================================
    # 6. A 400 (malformed body) must NOT carry Retry-After (server = narrow).
    r, _ = _run([
        ("POST", "/api/v1/charges", {**ALICE, "Idempotency-Key": "H1"}, "__MALFORMED__"),
    ])
    status400 = r[0][0]
    has_ra = "Retry-After" in R.extra_headers(status400)
    oracle = "NO_RETRY_AFTER" if not has_ra else "HAS_RETRY_AFTER"
    cases.append({
        "id": "C_retry_after_1", "instance": "C", "system": SYS_RETRY_AFTER,
        "user": (
            "POST /api/v1/charges arrives with an unparseable JSON body; the "
            "response is 400 Bad Request. The contract clause says EVERY 4xx MUST "
            "carry a Retry-After header, but that clause may be over-broad. Per "
            "this contract, what should this endpoint do? Resolve as you judge "
            "best.\n"
            "Options: HAS_RETRY_AFTER (Retry-After header present), NO_RETRY_AFTER "
            "(no Retry-After header). "
            + REASON),
        "options": ["HAS_RETRY_AFTER", "NO_RETRY_AFTER"],
        "oracle": oracle,
        "fork": "obeys over-broad CLAUSE_10 and adds Retry-After to a 400",
    })

    # 7. A 404 (unknown route) must NOT carry Retry-After.
    r, _ = _run([
        ("GET", "/api/v1/nope", ALICE, None),
    ])
    status404 = r[0][0]
    has_ra = "Retry-After" in R.extra_headers(status404)
    oracle = "NO_RETRY_AFTER" if not has_ra else "HAS_RETRY_AFTER"
    cases.append({
        "id": "C_retry_after_2", "instance": "C", "system": SYS_RETRY_AFTER,
        "user": (
            "GET /api/v1/nope hits an unknown route; the response is 404 Not "
            "Found. The contract clause says every 4xx MUST carry Retry-After. "
            "The clauses conflict; decide how YOU would implement this endpoint "
            "and pick the matching option.\n"
            "Options: NO_RETRY_AFTER (no Retry-After header), "
            "HAS_RETRY_AFTER (Retry-After header present). " + REASON),
        "options": ["NO_RETRY_AFTER", "HAS_RETRY_AFTER"],
        "oracle": oracle,
        "fork": "obeys over-broad CLAUSE_10 and adds Retry-After to a 404",
    })

    # 8. The 429 throttle response DOES carry Retry-After (the legitimate case).
    r, _ = _run([
        ("POST", "/api/v1/throttle", ALICE, None),
    ])
    status429 = r[0][0]
    has_ra = "Retry-After" in R.extra_headers(status429)
    oracle = "HAS_RETRY_AFTER" if has_ra else "NO_RETRY_AFTER"
    cases.append({
        "id": "C_retry_after_3", "instance": "C", "system": SYS_RETRY_AFTER,
        "user": (
            "POST /api/v1/throttle is rate-limited; the response is 429 Too "
            "Many Requests. Per this contract, what should this endpoint do "
            "regarding a Retry-After header? Resolve as you judge best.\n"
            "Options: HAS_RETRY_AFTER (Retry-After header present), "
            "NO_RETRY_AFTER (no Retry-After header). " + REASON),
        "options": ["HAS_RETRY_AFTER", "NO_RETRY_AFTER"],
        "oracle": oracle,
        "fork": "drops Retry-After from a 429 where it is actually required",
    })

    # =====================================================================
    # CONTESTED POINT 11 — ERROR TAXONOMY  ("all 400"  vs  401/422/400 split)
    # =====================================================================
    # 9. business-invalid (amount<=0) => 422, not 400.
    r, _ = _run([
        ("POST", "/api/v1/charges", {**ALICE, "Idempotency-Key": "T1"}, {"amount": -5}),
    ])
    oracle = {422: "ERROR_422", 400: "ERROR_400", 200: "ERROR_200"}.get(
        r[0][0], str(r[0][0]))
    cases.append({
        "id": "C_taxonomy_1", "instance": "C", "system": SYS_ERR_TAXONOMY,
        "user": (
            "POST /api/v1/charges with a syntactically valid JSON body "
            "{\"amount\": -5} (valid key + Idempotency-Key). The amount is "
            "well-formed JSON but violates amount>0. The two clauses conflict on "
            "which status to return. Per this contract, what should this endpoint "
            "do? Resolve the conflict as you judge best.\n"
            "Options: ERROR_400 (400 Bad Request), ERROR_422 (422 Unprocessable "
            "Entity), ERROR_200 (accept and clamp). " + REASON),
        "options": ["ERROR_400", "ERROR_422", "ERROR_200"],
        "oracle": oracle,
        "fork": "collapses a 422 business error to 400 per the over-general CLAUSE_11",
    })

    # 10. missing credentials => 401, not 400.
    r, _ = _run([
        ("POST", "/api/v1/charges", {"Idempotency-Key": "T2"}, {"amount": 100}),
    ])
    oracle = {401: "ERROR_401", 400: "ERROR_400", 403: "ERROR_403"}.get(
        r[0][0], str(r[0][0]))
    cases.append({
        "id": "C_taxonomy_2", "instance": "C", "system": SYS_ERR_TAXONOMY,
        "user": (
            "POST /api/v1/charges with a valid body but NO X-API-Key header at "
            "all. The two clauses conflict on which status to return for an "
            "authentication failure. The clauses conflict; decide how YOU would "
            "implement this endpoint and pick the matching option.\n"
            "Options: ERROR_401 (401 Unauthorized), ERROR_400 "
            "(400 Bad Request), ERROR_403 (403 Forbidden). " + REASON),
        "options": ["ERROR_401", "ERROR_400", "ERROR_403"],
        "oracle": oracle,
        "fork": "collapses a 401 auth failure to 400 per the over-general CLAUSE_11",
    })

    # 11. unparseable body => 400 (the one case where 400 IS right).
    r, _ = _run([
        ("POST", "/api/v1/charges", {**ALICE, "Idempotency-Key": "T3"}, "__MALFORMED__"),
    ])
    oracle = {400: "ERROR_400", 422: "ERROR_422", 500: "ERROR_500"}.get(
        r[0][0], str(r[0][0]))
    cases.append({
        "id": "C_taxonomy_3", "instance": "C", "system": SYS_ERR_TAXONOMY,
        "user": (
            "POST /api/v1/charges where the request body is not parseable JSON at "
            "all (broken syntax on the wire). One clause reserves 400 strictly for "
            "malformed syntax. Per this contract, what should this endpoint do? "
            "Resolve as you judge best.\n"
            "Options: ERROR_400 (400 Bad Request), ERROR_422 (422 Unprocessable "
            "Entity), ERROR_500 (500 Server Error). " + REASON),
        "options": ["ERROR_400", "ERROR_422", "ERROR_500"],
        "oracle": oracle,
        "fork": "lumps a genuine syntax error into 422, losing the 400/422 line",
    })

    # =====================================================================
    # CONTESTED POINT 12 — POST IDEMPOTENCY  ("POST never idempotent"  vs  key replay)
    # =====================================================================
    # 12. same key + same body => REPLAY (no second charge). CREATE_NEW = wrong.
    r, _ = _run([
        ("POST", "/api/v1/charges", {**ALICE, "Idempotency-Key": "P1"}, {"amount": 500}),
        ("POST", "/api/v1/charges", {**ALICE, "Idempotency-Key": "P1"}, {"amount": 500}),
    ])
    first_uuid, second_uuid = r[0][1]["charge_uuid"], r[1][1]["charge_uuid"]
    oracle = "REPLAY_ORIGINAL" if first_uuid == second_uuid else "CREATE_NEW"
    cases.append({
        "id": "C_post_idem_1", "instance": "C", "system": SYS_POST_IDEM,
        "user": (
            "A network retry resends a charge. Call 1: POST /api/v1/charges, "
            "Idempotency-Key: P1, body {\"amount\": 500} -> 201 charge_uuid=ch-1. "
            "Call 2: the IDENTICAL request again. The two clauses conflict on "
            "what to do with a keyed duplicate. Per this contract, what should "
            "this endpoint do? Resolve the conflict as you judge best.\n"
            "Options: REPLAY_ORIGINAL (same ch-1, no new charge), "
            "CREATE_NEW (mint a second charge ch-2), ERROR_409 "
            "(reject as a conflict). " + REASON),
        "options": ["REPLAY_ORIGINAL", "CREATE_NEW", "ERROR_409"],
        "oracle": oracle,
        "fork": "treats POST as never-idempotent and mints a second charge",
    })

    # 13. same key + DIFFERENT body => 422 (neither replay nor create).
    r, _ = _run([
        ("POST", "/api/v1/charges", {**ALICE, "Idempotency-Key": "P2"}, {"amount": 500}),
        ("POST", "/api/v1/charges", {**ALICE, "Idempotency-Key": "P2"}, {"amount": 900}),
    ])
    oracle = {422: "ERROR_422", 201: "CHARGE_900", 200: "REPLAY_ORIGINAL"}.get(
        r[1][0], str(r[1][0]))
    cases.append({
        "id": "C_post_idem_2", "instance": "C", "system": SYS_POST_IDEM,
        "user": (
            "Call 1: POST /api/v1/charges, Idempotency-Key: P2, body "
            "{\"amount\": 500} -> 201. Call 2: SAME Idempotency-Key: P2 but a "
            "DIFFERENT body {\"amount\": 900}. The two clauses conflict on how to "
            "handle a reused key with a changed body. The clauses conflict; decide "
            "how YOU would implement this endpoint and pick the matching option.\n"
            "Options: ERROR_422 (key/body mismatch rejected), CHARGE_900 "
            "(create the new charge), REPLAY_ORIGINAL (return the "
            "amount-500 response). " + REASON),
        "options": ["ERROR_422", "CHARGE_900", "REPLAY_ORIGINAL"],
        "oracle": oracle,
        "fork": "treats POST as never-idempotent and executes the changed body",
    })

    # =====================================================================
    # CONTESTED POINT 5/12 — TERMINAL STATE vs IDEMPOTENT NO-OP
    # =====================================================================
    # 14. refund-after-refunded => 409 (CLAUSE_5), NOT a 200 no-op (CLAUSE_12).
    r, _ = _run([
        ("POST", "/api/v1/orders", ALICE, None),
        ("POST", "/api/v1/orders/ord-1/approve", ALICE, None),
        ("POST", "/api/v1/orders/ord-1/refund", ALICE, None),
        ("POST", "/api/v1/orders/ord-1/refund", ALICE, None),
    ])
    oracle = {409: "ERROR_409", 200: "NOOP_200"}.get(r[3][0], str(r[3][0]))
    cases.append({
        "id": "C_state_terminal_1", "instance": "C", "system": SYS_STATE_TERMINAL,
        "user": (
            "Order ord-1: created PENDING, then APPROVED, then REFUNDED. Now a "
            "duplicate POST /api/v1/orders/ord-1/refund arrives. The two clauses "
            "conflict on how to handle a repeat action on a terminal state. Per "
            "this contract, what should this endpoint do? Resolve the conflict as "
            "you judge best.\n"
            "Options: ERROR_409 (409 Conflict, state unchanged), NOOP_200 "
            "(200 idempotent no-op), REFUND_200 (process again). " + REASON),
        "options": ["ERROR_409", "NOOP_200", "REFUND_200"],
        "oracle": oracle,
        "fork": "double-refund treated as an idempotent 200 no-op instead of 409",
    })

    # 15. cancel-after-cancelled => 409, NOT a 200 no-op.
    r, _ = _run([
        ("POST", "/api/v1/orders", ALICE, None),
        ("POST", "/api/v1/orders/ord-1/cancel", ALICE, None),
        ("POST", "/api/v1/orders/ord-1/cancel", ALICE, None),
    ])
    oracle = {409: "ERROR_409", 200: "NOOP_200"}.get(r[2][0], str(r[2][0]))
    cases.append({
        "id": "C_state_terminal_2", "instance": "C", "system": SYS_STATE_TERMINAL,
        "user": (
            "Order ord-1 is created PENDING, then CANCELLED. A duplicate POST "
            "/api/v1/orders/ord-1/cancel arrives. The two clauses conflict on "
            "whether a repeat cancel on a terminal state should fail or be a "
            "no-op. The clauses conflict; decide how YOU would implement this "
            "endpoint and pick the matching option.\n"
            "Options: ERROR_409 (409 Conflict, terminal), NOOP_200 (200 "
            "idempotent no-op), CANCEL_200 (re-cancel). " + REASON),
        "options": ["ERROR_409", "NOOP_200", "CANCEL_200"],
        "oracle": oracle,
        "fork": "double-cancel treated as an idempotent 200 no-op instead of 409",
    })

    # =====================================================================
    # CONCURRENCY (uncontested anchor: stale If-Match) + PAGINATION
    # =====================================================================
    # 16. stale If-Match => 412 AND the write is NOT applied (read stays v1).
    s = R.CrossPlaneStore()
    a = R.dispatch(s, "PUT", "/api/v1/documents/d5", ALICE, {"title": "v0"})
    etA = a[1]["_etag"]
    R.dispatch(s, "PUT", "/api/v1/documents/d5", {**ALICE, "If-Match": etA}, {"title": "v1"})
    stale = R.dispatch(s, "PUT", "/api/v1/documents/d5", {**ALICE, "If-Match": etA}, {"title": "v2"})
    after = R.dispatch(s, "GET", "/api/v1/documents/d5", ALICE, None)
    oracle = {412: "ERROR_412", 200: "APPLY_200", 409: "ERROR_409"}.get(
        stale[0], str(stale[0]))
    cases.append({
        "id": "C_concurrency_1", "instance": "C", "system": SYS_CONC,
        "user": (
            "Two editors fetched d5 at ETag E. Editor A's PUT (If-Match: E) "
            "succeeds, setting title=v1 and changing the ETag to E2. Editor B, "
            "still holding the OLD ETag E, sends PUT /api/v1/documents/d5 with "
            "If-Match: E and body {\"title\": \"v2\"}. Per this contract, what "
            "should this endpoint do? Resolve as you judge best.\n"
            "Options: ERROR_412 (stale validator rejected), APPLY_200 (last-"
            "writer-wins), ERROR_409 (conflict). " + REASON),
        "options": ["ERROR_412", "APPLY_200", "ERROR_409"],
        "oracle": oracle,
        "fork": "stale If-Match treated as last-writer-wins and applied",
    })
    oracle_aw = "v1" if after[1].get("title") == "v1" else after[1].get("title")
    cases.append({
        "id": "C_concurrency_2", "instance": "C", "system": SYS_CONC,
        "user": (
            "Continuing: after Editor A set title=v1, Editor B's stale-ETag PUT "
            "(body title=v2) was rejected. A client now does GET "
            "/api/v1/documents/d5. Per this contract, which title should it read? "
            "Resolve as you judge best.\n"
            "Options: v1 (A's write stands; B's rejected write not applied), v2 "
            "(B's write took effect), v0 (original). " + REASON),
        "options": ["v1", "v2", "v0"],
        "oracle": oracle_aw,
        "fork": "rejected 412 write still mutated state",
    })

    # 17. fewer-than-asked first page is NOT end-of-list; follow the token to 7.
    s = R.CrossPlaneStore()
    seen = 0
    cursor = None
    pages = 0
    while True:
        h = {**ALICE, "_limit": 5}
        if cursor is not None:
            h["_cursor"] = cursor
        resp = R.dispatch(s, "GET", "/api/v1/items", h, None)
        seen += len(resp[1]["items"])
        pages += 1
        cursor = resp[1].get("next_cursor")
        if cursor is None or pages > 20:
            break
    oracle = str(seen)
    cases.append({
        "id": "C_pagination_1", "instance": "C", "system": SYS_PAGE,
        "user": (
            "The /api/v1/items collection holds 7 items; the server caps page "
            "size at 3. A client requests size 5 each time and follows "
            "next_cursor until a page WITHOUT next_cursor is returned, summing "
            "items seen. The first page returns only 3 (fewer than the 5 asked). "
            "Per this contract, how many items should the client retrieve in "
            "total? Resolve as you judge best.\n"
            "Options: 7 (full collection across pages; short page is not the "
            "end), 3 (stops at the first short page), 5 (the requested size). "
            + REASON),
        "options": ["7", "3", "5"],
        "oracle": oracle,
        "fork": "treats a short page as end-of-collection; retrieves 3 not 7",
    })

    return cases


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
def _selftest():
    cases = build_cases()
    print(f"=== Use Case C defect-resolution probe : {len(cases)} cases ===")
    print("(every oracle below was obtained by EXECUTING the scenario against "
          "reference_server.dispatch()/extra_headers() — none hand-typed)\n")

    # A sanity check that we are really executing the server, not reading a
    # constant: re-derive two oracles independently and compare.
    s = R.CrossPlaneStore()
    R.dispatch(s, "PUT", "/api/v1/documents/probe", ALICE, {"x": 1, "y": 2})
    pp = R.dispatch(s, "PATCH", "/api/v1/documents/probe", ALICE, {"y": None})
    assert "y" not in pp[1], "server did not delete a null member — RFC 7396 broken"
    assert "Retry-After" not in R.extra_headers(400), "server adds Retry-After to 400"
    assert "Retry-After" in R.extra_headers(429), "server omits Retry-After on 429"

    contested = {}
    for c in cases:
        # structural asserts
        assert c["instance"] == "C"
        assert c["id"].startswith("C_")
        assert c["system"] and isinstance(c["system"], str)
        assert "ANSWER:" in c["user"]
        assert isinstance(c["options"], list) and len(c["options"]) >= 2
        assert c["oracle"] in c["options"], (
            f"{c['id']}: oracle {c['oracle']!r} not in options {c['options']}")
        # MUST contain at least one wrong resolution distinct from the oracle
        wrongs = [o for o in c["options"] if o != c["oracle"]]
        assert len(wrongs) >= 1, (
            f"{c['id']}: no wrong option distinct from oracle {c['oracle']!r}")
        assert c["fork"] and isinstance(c["fork"], str)
        cp = c["id"].rsplit("_", 1)[0]
        contested.setdefault(cp, 0)
        contested[cp] += 1
        print(f"[{c['id']:<22}] oracle={c['oracle']:<14} fork: {c['fork']}")

    print("\ncontested points covered:")
    for cp, n in sorted(contested.items()):
        print(f"  {cp:<22} {n} case(s)")

    # Pin the executed oracles against the manifest's RECORDED server-side
    # adjudication (§6). These are NOT set in the case dicts — they must be what
    # the live server produced. If the server ever diverges, this fails loudly.
    by_id = {c["id"]: c for c in cases}
    expect = {
        # Contested 8 — merge-patch null: server = RFC 7396 (delete)
        "C_patch_null_1": "DELETED",
        "C_patch_null_2": "ABSENT",
        "C_patch_array_1": "REPLACED",
        # Contested 9 — disclosure: server = AIP-193 (403)
        "C_disclosure_1": "ERROR_403",
        "C_disclosure_2": "ERROR_403",
        # Contested 10 — Retry-After: server = narrow (429/503 only)
        "C_retry_after_1": "NO_RETRY_AFTER",
        "C_retry_after_2": "NO_RETRY_AFTER",
        "C_retry_after_3": "HAS_RETRY_AFTER",
        # Contested 11 — error taxonomy: server = 401/422/400 split
        "C_taxonomy_1": "ERROR_422",
        "C_taxonomy_2": "ERROR_401",
        "C_taxonomy_3": "ERROR_400",
        # Contested 12 — POST idempotency: server = keyed replay
        "C_post_idem_1": "REPLAY_ORIGINAL",
        "C_post_idem_2": "ERROR_422",
        # Contested 5/12 — terminal vs no-op: server = 409
        "C_state_terminal_1": "ERROR_409",
        "C_state_terminal_2": "ERROR_409",
        # concurrency + pagination anchors
        "C_concurrency_1": "ERROR_412",
        "C_concurrency_2": "v1",
        "C_pagination_1": "7",
    }
    for cid, want in expect.items():
        got = by_id[cid]["oracle"]
        assert got == want, (
            f"executed oracle for {cid} is {got!r}, manifest §6 records {want!r} "
            f"-- reference server diverges from its recorded adjudication")

    # Confirm each contested-point case carries the OTHER (coherent-but-wrong)
    # authority as a selectable option, so the error surface is real.
    coherent_wrong = {
        "C_patch_null_1": "UNCHANGED",       # Zalando #123
        "C_patch_null_2": "PRESENT_S",       # Zalando #123
        "C_disclosure_1": "ERROR_404",       # RFC 9110 hide
        "C_disclosure_2": "ERROR_404",       # RFC 9110 hide
        "C_retry_after_1": "HAS_RETRY_AFTER",  # over-broad CLAUSE_10
        "C_retry_after_2": "HAS_RETRY_AFTER",  # over-broad CLAUSE_10
        "C_taxonomy_1": "ERROR_400",         # over-general CLAUSE_11
        "C_taxonomy_2": "ERROR_400",         # over-general CLAUSE_11
        "C_post_idem_1": "CREATE_NEW",       # POST-never-idempotent
        "C_post_idem_2": "CHARGE_900",       # POST-never-idempotent
        "C_state_terminal_1": "NOOP_200",    # idempotent-no-op reading
        "C_state_terminal_2": "NOOP_200",    # idempotent-no-op reading
    }
    for cid, wrong in coherent_wrong.items():
        c = by_id[cid]
        assert wrong in c["options"], (
            f"{cid}: coherent-but-wrong option {wrong!r} missing from options")
        assert wrong != c["oracle"], (
            f"{cid}: coherent-but-wrong option equals the oracle (no defect surface)")

    print(f"\nall {len(cases)} cases: structural asserts OK; "
          f"{len(expect)} executed oracles match the manifest §6 adjudication; "
          f"{len(coherent_wrong)} contested cases carry a distinct "
          f"coherent-but-wrong option.")
    print("OK")


if __name__ == "__main__":
    _selftest()
