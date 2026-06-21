"""Upper-bound-driven gate primitives (spec §3): how the manifest drives the
gates. These are the structural checks `gate_sentinel.py` runs; they read the
ceiling and refuse a non-policy-centric manifest or a test matrix that does not
account for every obligation clause.

Gate A — Structural Plan Integrity: the property author must keep the manifest
          strictly policy-centric (WHAT, never HOW). The compilation track is
          blocked if the file injects code fragments, schema JSON, SQL/DDL, or
          web-framework implementation syntax.
Gate C — Structural Coverage Map: the exerciser's test_matrix.json must map a
          unique, non-trivial request assertion to every CLAUSE_n. A clause with
          no covering case fails the entire build, even if the OpenAPI schema and
          the live server are internally coherent (the "coherent-and-wrong" trap
          — a quietly dropped CLAUSE_2 user_uuid rule).

test_matrix.json schema (written by the exerciser):
    [
      {"name": "...", "clauses": ["CLAUSE_1"], "check": "<non-empty>", ...},
      {"name": "...", "clause":  "CLAUSE_2",   "check": "<non-empty>", ...}
    ]
A case covers a clause only if it names the clause AND carries a non-empty
`check` (a generic/sweeping case with no concrete assertion does not count).
"""

from __future__ import annotations

from dataclasses import dataclass

import handbook as hb


# Forbidden markers (spec §3 Gate A): code fragments, schema JSON, SQL/DDL, and
# web-framework implementation syntax. Presence of any => not policy-centric.
# These describe HOW; a manifest may only describe WHAT.
_FORBIDDEN = [
    ("```", "fenced code block"),
    ("def ", "Python function definition"),
    ("import ", "Python import"),
    ("class ", "Python class definition"),
    ("SELECT ", "SQL query"),
    ("CREATE TABLE", "DB schema (DDL)"),
    ("INSERT INTO", "SQL DML"),
    ("@app.", "web framework route decorator"),
    ("@router.", "web framework route decorator"),
    ("\"type\":", "schema JSON fragment"),
    ("\"properties\":", "schema JSON fragment"),
    ("\"required\":", "schema JSON fragment"),
]

# Heuristic: a JSON object block heavy with quoted keys / braces is schema JSON,
# not normative English. Counts braces across the document.
_JSON_BRACE_THRESHOLD = 6


@dataclass(frozen=True)
class GateResult:
    ok: bool
    gate: str
    subject: str            # manifest id, or "<file>" for the file-level Gate A check
    missing: list[str]      # clause ids not covered (Gate C) / forbidden hits (Gate A)
    detail: str = ""

    def __bool__(self) -> bool:
        return self.ok


def gate_a_policy_centric(text: str, subject: str = "<api_policy_manifest.md>") -> GateResult:
    """Fail if the manifest text contains code, schema JSON, SQL/DDL, or web
    framework implementation syntax — enforcing 'what, never how' (spec §3 Gate A).

    Markers are searched case-insensitively. A brace-heavy body (a likely inline
    JSON schema block) is also rejected even if no individual key marker hit."""
    low = text.lower()
    hits = sorted({label for marker, label in _FORBIDDEN if marker.lower() in low})

    # Brace-heavy => embedded JSON schema. Normative English carries few braces.
    if text.count("{") >= _JSON_BRACE_THRESHOLD and "{-heavy JSON block" not in hits:
        hits.append("{-heavy JSON block")
        hits = sorted(set(hits))

    ok = not hits
    return GateResult(ok, "A", subject, hits,
                      "policy-centric (no code/schema/impl syntax)"
                      if ok else f"non-policy-centric: contains {hits}")


def _clauses_in_case(c: dict) -> list[str]:
    if "clauses" in c:
        return list(c["clauses"])
    if "clause" in c:
        return [c["clause"]]
    return []


def gate_c_coverage(manifest: hb.Manifest, target_clauses_seen: list[dict]) -> GateResult:
    """Every CLAUSE_n of `manifest` must be covered by a non-trivial test case.
    Returns the missing set (empty => Gate C passes)."""
    covered: set[str] = set()
    for c in target_clauses_seen:
        if not isinstance(c, dict):
            continue
        if not str(c.get("check", "")).strip():     # trivial / no concrete assertion
            continue
        covered.update(_clauses_in_case(c))
    missing = [cid for cid in manifest.clause_ids if cid not in covered]
    ok = not missing
    return GateResult(ok, "C", manifest.manifest_id, missing,
                      "every clause has a targeted request assertion"
                      if ok else f"uncovered {missing}")


if __name__ == "__main__":
    manifests = hb.parse()
    m = hb.by_id(manifests, "API_POLICY_081")

    # Gate A on the real manifest (should pass) and on an injected snippet.
    from pathlib import Path
    real = Path(__file__).resolve().parent / "api_policy_manifest.md"
    print("Gate A real :", gate_a_policy_centric(real.read_text()))
    print("Gate A inject:", gate_a_policy_centric(
        "CLAUSE_1: auth\n```python\n@app.post('/x')\ndef h(): ...\n```", "<malicious>"))

    good_matrix = [
        {"name": "unauth POST -> 401",   "clause": "CLAUSE_1", "check": "no X-API-Key -> 401"},
        {"name": "GET exposes user_uuid","clause": "CLAUSE_2", "check": "200 body has user_uuid, no id"},
        {"name": "malformed -> clean 400","clause": "CLAUSE_3", "check": "bad body -> 400, no traceback"},
    ]
    bad_matrix = [
        {"name": "smoke", "check": "server boots"},               # maps to nothing
        {"name": "auth", "clause": "CLAUSE_1", "check": ""},      # trivial
    ]
    print("Gate C good:", gate_c_coverage(m, good_matrix))
    print("Gate C bad :", gate_c_coverage(m, bad_matrix))
