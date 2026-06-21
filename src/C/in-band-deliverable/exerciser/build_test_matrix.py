#!/usr/bin/env python3
"""Exerciser band -- generates the conformance test matrix
(in-band-deliverable-spec.md §2).

BLIND to the implementer: this file never imports, reads, or parses anything under
the implementer band. The cases are a pure, independent interpretation of the upper-bound
clauses (API_POLICY_081, upper-bound-spec.md §2) and the SHARED CONTRACT -- the
expected statuses / schema keys are derived from the CLAUSES here, NOT from
main.py and NOT from the ground truth's reference_server.py.

Emits conformance/test_matrix.json following the spec schema:
  {policy_id, endpoints:[{test_case_id, target_clauses, path, method, headers,
                          payload, expected_status, expected_schema_keys,
                          [forbidden_string_patterns]}]}

Coverage required by the spec / Gate C:
  CLAUSE_1  authed POST update   -> 200 {status,user_uuid,updated_at}
            unauthenticated POST -> 401 {error,message}
  CLAUSE_2  authed GET profile   -> 200 with user_uuid and NOT id
  CLAUSE_3  malformed POST (valid key) -> 400 {error,message}, no trace leak
  Core Negative Vector  unauthenticated + malformed payload -> 400/401, no leak

Canonical credentials from the SHARED CONTRACT:
  X-API-Key test_secure_token_abc123  -> user u-0001
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFORMANCE = HERE / "conformance"

POLICY_ID = "API_POLICY_081"
VALID_KEY = "test_secure_token_abc123"

# The trace/leak patterns CLAUSE_3 forbids on the wire.
FORBIDDEN = ["Traceback", "File \"", "line ", "sqlite3.", "SELECT"]


def build_matrix():
    endpoints = [
        # CLAUSE_1 -- authenticated mutation succeeds with the decoupled shape.
        {
            "test_case_id": "TC_001_AUTHENTICATED_MUTATION",
            "target_clauses": ["CLAUSE_1"],
            "path": "/api/v1/profile/update",
            "method": "POST",
            "headers": {"X-API-Key": VALID_KEY},
            "payload": {"display_name": "Alice Spencer"},
            "expected_status": 200,
            "expected_schema_keys": ["status", "user_uuid", "updated_at"],
        },
        # CLAUSE_1 -- a mutation with no X-API-Key must be rejected, not processed.
        {
            "test_case_id": "TC_002_UNAUTHENTICATED_REJECTION",
            "target_clauses": ["CLAUSE_1"],
            "path": "/api/v1/profile/update",
            "method": "POST",
            "headers": {},
            "payload": {"display_name": "Malicious Actor"},
            "expected_status": 401,
            "expected_schema_keys": ["error", "message"],
        },
        # CLAUSE_2 -- the profile read exposes user_uuid and NEVER the integer id.
        # (The exact key set is asserted, so an extra `id` key fails Gate B.)
        {
            "test_case_id": "TC_003_DECOUPLED_PROFILE_READ",
            "target_clauses": ["CLAUSE_2"],
            "path": "/api/v1/profile",
            "method": "GET",
            "headers": {"X-API-Key": VALID_KEY},
            "payload": None,
            "expected_status": 200,
            "expected_schema_keys": ["user_uuid", "display_name", "updated_at"],
        },
        # CLAUSE_3 -- a malformed body with a VALID key must return a clean 400
        # with no traceback / file path / source line / SQL / sqlite3 text.
        {
            "test_case_id": "TC_004_TRACEBACK_EXFILTRATION_ATTEMPT",
            "target_clauses": ["CLAUSE_3"],
            "path": "/api/v1/profile/update",
            "method": "POST",
            "headers": {"X-API-Key": VALID_KEY},
            "payload": {"malformed_parameter_injection": "---' OR 1=1;--"},
            "expected_status": 400,
            "expected_schema_keys": ["error", "message"],
            "forbidden_string_patterns": FORBIDDEN,
        },
        # Core Negative Vector -- unauthenticated AND malformed: the runtime must
        # drop safely (401, since auth is checked first) and leak nothing.
        {
            "test_case_id": "TC_005_CORE_NEGATIVE_VECTOR",
            "target_clauses": ["CLAUSE_1", "CLAUSE_3"],
            "path": "/api/v1/profile/update",
            "method": "POST",
            "headers": {},
            "payload": {"malformed_parameter_injection": "---' OR 1=1;--"},
            "expected_status": 401,
            "expected_schema_keys": ["error", "message"],
            "forbidden_string_patterns": FORBIDDEN,
        },
    ]
    return {"policy_id": POLICY_ID, "endpoints": endpoints}


def main():
    CONFORMANCE.mkdir(parents=True, exist_ok=True)
    matrix = build_matrix()
    out = CONFORMANCE / "test_matrix.json"
    out.write_text(json.dumps(matrix, indent=2) + "\n")
    print(f"wrote {out.name}: {len(matrix['endpoints'])} cases")
    covered = set()
    for c in matrix["endpoints"]:
        covered.update(c["target_clauses"])
    print(f"clauses covered: {sorted(covered)}")


if __name__ == "__main__":
    main()
