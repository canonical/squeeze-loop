#!/usr/bin/env python3
"""Self-check of the Upper Bound — the author's expressibility-from-below proof.

Exits nonzero on any failure:

  1. STRUCTURE     api_policy_manifest.md parses and passes the schema (spec §2).
  2. GATE A        the published manifest stays strictly policy-centric — no code,
                   schema JSON, SQL/DDL, or web-framework syntax (spec §3 Gate A).
  3. GROUNDING     the HTTP contract elements the clauses / negative vector name
                   actually EXIST in the real document-plane contract
                   ../ground-truth/base_schema.json: the `X-API-Key` header
                   security scheme, the mutation route POST /api/v1/profile/update,
                   the public `user_uuid` field, and the 400 / 401 error shapes.
                   So the ceiling is dischargeable, not a wish.
  4. GATE WIRING   gate_c_coverage accepts a complete clause set and rejects an
                   incomplete one (the trap defense, spec §3 Gate C).

The grounding step is the upper-bound analogue of the ground truth's "every
behavior is exercised against the real contract": a normative claim no live route
could ever satisfy is rejected here, not discovered downstream.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import gate_checks as gc
import handbook as hb

HERE = Path(__file__).resolve().parent
GT = HERE.parent / "ground-truth"
SCHEMA_CANDIDATES = [
    Path("/opt/squeeze/shared/base_schema.json"),
    GT / "base_schema.json",
]

# The mutation route the clauses / negative vector target.
MUTATION_ROUTE = "/api/v1/profile/update"


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))
    return ok


def _schema_obj():
    for p in SCHEMA_CANDIDATES:
        if p.exists():
            return p, json.loads(p.read_text(encoding="utf-8"))
    return None, None


def _collect_status_codes(schema: dict) -> set[str]:
    codes: set[str] = set()
    for route in schema.get("paths", {}).values():
        for method in route.values():
            if isinstance(method, dict):
                codes.update(method.get("responses", {}).keys())
    return codes


def _security_header_names(schema: dict) -> set[str]:
    names: set[str] = set()
    for s in schema.get("components", {}).get("securitySchemes", {}).values():
        if isinstance(s, dict) and s.get("in") == "header" and s.get("name"):
            names.add(s["name"])
    return names


def _schema_blob(schema: dict) -> str:
    return json.dumps(schema)


def main():
    ok = True

    # 1. structure
    try:
        manifests = hb.parse()
        check("structure", True, f"{len(manifests)} manifest(s): "
              + ", ".join(m.manifest_id for m in manifests))
    except hb.HandbookError as e:
        check("structure", False, str(e))
        print("VALIDATE FAILED")
        return 1

    # 2. Gate A — policy-centric (no code/schema/impl syntax)
    manifest_text = (HERE / "api_policy_manifest.md").read_text(encoding="utf-8")
    ga = gc.gate_a_policy_centric(manifest_text)
    ok &= check("gate A policy-centric", bool(ga), ga.detail)

    # 3. grounding against the document-plane contract
    schema_path, schema = _schema_obj()
    if schema is None:
        print("[WARN] ground-truth base_schema.json not found; skipping grounding "
              f"(looked in: {', '.join(str(p) for p in SCHEMA_CANDIDATES)})")
    else:
        codes = _collect_status_codes(schema)
        headers = _security_header_names(schema)
        blob = _schema_blob(schema)
        routes = set(schema.get("paths", {}).keys())

        for m in manifests:
            clause_blob = " ".join(m.clauses.values())
            nv_blob = (m.negative_vector.target_exploit + " "
                       + m.negative_vector.expected_defense)

            grounding = {
                # clause concept -> (named in manifest, present in real contract)
                "X-API-Key header security": (
                    "X-API-Key" in clause_blob,
                    "X-API-Key" in headers),
                "user_uuid public field (not internal id)": (
                    "user_uuid" in clause_blob,
                    "user_uuid" in blob and "internal" in clause_blob.lower()),
                "400 Bad Request on validation failure": (
                    "400" in clause_blob,
                    "400" in codes),
                "401 Unauthorized defense": (
                    "401" in nv_blob,
                    "401" in codes),
                "mutation route (POST profile update)": (
                    "POST" in clause_blob or "modification route" in nv_blob,
                    MUTATION_ROUTE in routes
                    and "post" in schema["paths"][MUTATION_ROUTE]),
            }
            for concept, (mentioned, grounded) in grounding.items():
                g_ok = mentioned and grounded
                ok &= check(f"{m.manifest_id} grounding: {concept}", g_ok,
                            "named in manifest and present in base_schema.json"
                            if g_ok else
                            f"mentioned={mentioned}, contract_present={grounded}")

    # 4. gate wiring (Gate C accepts complete, rejects incomplete)
    for m in manifests:
        complete = [{"clause": c, "check": "x"} for c in m.clause_ids]
        incomplete = complete[:-1]                       # drop the last clause
        c_ok = gc.gate_c_coverage(m, complete)
        c_bad = gc.gate_c_coverage(m, incomplete)
        wired = bool(c_ok) and not c_bad.ok and c_bad.missing == [m.clause_ids[-1]]
        ok &= check(f"{m.manifest_id} gate wiring", wired,
                    "Gate C accepts complete clause set, rejects incomplete")

    print("VALIDATE OK" if ok else "VALIDATE FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
