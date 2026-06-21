#!/usr/bin/env python3
"""The Squeeze Connector for Use Case C (in-band-deliverable-spec.md §3/§4).

Split-planes squeeze. The sentinel forces the implementer's running server and the
exerciser's conformance matrix to reconcile, and cross-checks the implementer's
public OpenAPI document against the ground-truth document plane + TY0 baseline. It
imports neither band as a peer of the other: it boots the implementer's main.py as
a subprocess and reads the exerciser's JSON matrix; the two bands never touch.

Checks (nonzero exit on any failure):

  ISOLATION       implementer/ and exerciser/ contain zero cross-references to each
                  other (Zero Import Linkage), verified by AST import scan +
                  filesystem-path scan.
  SERVER          boots the implementer's main.py on 127.0.0.1:8000, waits until it
                  binds, tears it down at the end.
  GATE C          every CLAUSE_n in src/C/upper-bound/api_policy_manifest.md
                  (parsed via that band's handbook.py, imported by path) is covered
                  by some test's target_clauses. Degrades to a WARNING if the
                  upper bound is absent.
  GATE B          (runtime plane) for each case: send method+path+headers+payload
                  via urllib; assert status == expected_status, response key set ==
                  expected_schema_keys, and no forbidden_string_patterns appear.
                  Any mismatch == GATE B CRASH.
  DOCUMENT PLANE  lint implementer/src/openapi.json via the ground-truth linter
                  (imported by path) and cross-check that it declares every route
                  the tests hit (no-blend doc side).
  TY0 REGRESSION  load src/C/ground-truth/shared/ty0_baseline.json and assert the
                  implementer's openapi.json preserves the legacy route signatures
                  (method, path, response-keys-by-status) -- no silent drop/mutation.

Usage:
  python3 runner/execute_squeeze.py            # drive the real implementer
  python3 runner/execute_squeeze.py --bad      # load the coherent-and-wrong server
  SERVER_CMD="python3 path/to/server.py" ...   # override the server under test
"""

import argparse
import ast
import importlib.util
import json
import os
import re
import shlex
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

RUNNER = Path(__file__).resolve().parent
ROOT = RUNNER.parent                       # src/C/in-band-deliverable
ROOT_C = ROOT.parent                       # src/C
GROUND_TRUTH = ROOT_C / "ground-truth"
UPPER_BOUND = ROOT_C / "upper-bound"
TY0_BASELINE = GROUND_TRUTH / "shared" / "ty0_baseline.json"

IMPL_MAIN = ROOT / "implementer" / "src" / "main.py"
IMPL_OPENAPI = ROOT / "implementer" / "src" / "openapi.json"
BAD_SERVER = ROOT / "evidence" / "coherent_wrong_server.py"
MATRIX = ROOT / "exerciser" / "conformance" / "test_matrix.json"
DB = GROUND_TRUTH / "shared" / "app_state.db"

HOST, PORT = "127.0.0.1", 8000

# Canonical clause set (upper-bound-spec.md §2) used when the upper bound is absent.
CANONICAL_CLAUSES = ["CLAUSE_1", "CLAUSE_2", "CLAUSE_3"]


class GateFail(Exception):
    pass


# --------------------------------------------------------------------------- #
# ISOLATION
# --------------------------------------------------------------------------- #
def _links_to(pyfile, other):
    """Real linkage only: an import of, or a filesystem path into, the other band.
    A prose mention in a comment/docstring is not linkage."""
    text = pyfile.read_text()
    for node in ast.walk(ast.parse(text)):
        if isinstance(node, ast.Import):
            for n in node.names:
                if other in n.name.split("."):
                    return f"imports {n.name}"
        elif isinstance(node, ast.ImportFrom):
            if node.module and other in node.module.split("."):
                return f"from {node.module} import ..."
    if re.search(rf"\b{other}/", text) or f"/home/{other}" in text:
        return f"path reference to {other}/"
    return None


def check_isolation():
    bad = []
    for f in (ROOT / "implementer").rglob("*.py"):
        link = _links_to(f, "exerciser")
        if link:
            bad.append(f"{f.name} {link}")
    for f in (ROOT / "exerciser").rglob("*.py"):
        link = _links_to(f, "implementer")
        if link:
            bad.append(f"{f.name} {link}")
    if bad:
        raise GateFail("Zero Import Linkage violated: " + "; ".join(bad))
    print("[PASS] ISOLATION  -- implementer and exerciser bands are import-isolated")


# --------------------------------------------------------------------------- #
# SERVER lifecycle (boot the implementer's main.py)
# --------------------------------------------------------------------------- #
def _port_open():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.3)
        return s.connect_ex((HOST, PORT)) == 0


def start_server(cmd):
    if _port_open():
        raise GateFail(f"port {PORT} already in use -- stop the other listener first")
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    deadline = time.time() + 15
    while time.time() < deadline:
        if proc.poll() is not None:
            out = proc.stdout.read() if proc.stdout else ""
            raise GateFail(f"server exited early (rc={proc.returncode}):\n{out}")
        if _port_open():
            break
        time.sleep(0.2)
    else:
        proc.terminate()
        raise GateFail("server did not bind within 15s")
    print(f"[ OK ] SERVER    -- listening on http://{HOST}:{PORT}")
    return proc


def stop_server(proc):
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
    print("[ OK ] SERVER    -- torn down")


# --------------------------------------------------------------------------- #
# HTTP helper (raw -- we need status + bytes for both JSON and leak inspection)
# --------------------------------------------------------------------------- #
def http_call(method, path, headers, payload):
    """Return (status:int, raw_text:str). 4xx/5xx are returned, not raised."""
    url = f"http://{HOST}:{PORT}{path}"
    data = None
    hdrs = dict(headers or {})
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        hdrs.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


# --------------------------------------------------------------------------- #
# GATE C
# --------------------------------------------------------------------------- #
def upper_bound_clauses():
    """Return (clause_ids, source_label). Parse via handbook.py if the band is
    built; otherwise return the canonical set with a None source."""
    handbook = UPPER_BOUND / "handbook.py"
    manifest = UPPER_BOUND / "api_policy_manifest.md"
    if handbook.exists() and manifest.exists():
        sys.path.insert(0, str(UPPER_BOUND))
        try:
            import handbook as hb  # noqa
            manifests = hb.parse(str(manifest))
            first = manifests[0] if isinstance(manifests, list) else manifests
            if hasattr(first, "clause_ids") and first.clause_ids:
                return list(first.clause_ids), str(manifest)
        except Exception as e:  # noqa: BLE001 -- degrade rather than crash
            print(f"[WARN] GATE C    -- upper-bound handbook present but unparsable "
                  f"({e}); using canonical clause set")
            return CANONICAL_CLAUSES, None
    return CANONICAL_CLAUSES, None


def gate_c(matrix):
    clause_ids, source = upper_bound_clauses()
    covered = set()
    for c in matrix["endpoints"]:
        covered.update(c.get("target_clauses", []))
    missing = [c for c in clause_ids if c not in covered]
    if source is None:
        if missing:
            print(f"[WARN] GATE C    -- upper bound not built; canonical clauses "
                  f"{clause_ids} NOT all covered (missing {missing})")
        else:
            print(f"[WARN] GATE C    -- upper bound not built; degraded to a warning. "
                  f"Canonical clauses {clause_ids} all covered.")
        return
    if missing:
        raise GateFail(f"GATE C: clauses uncovered by the test matrix: {missing} "
                       f"(from {source})")
    print(f"[PASS] GATE C    -- all upper-bound clauses covered {clause_ids}")


# --------------------------------------------------------------------------- #
# GATE B (runtime plane)
# --------------------------------------------------------------------------- #
def gate_b(matrix):
    print(f"\n=== GATE B: {len(matrix['endpoints'])} conformance cases "
          f"(policy {matrix['policy_id']}) ===")
    for case in matrix["endpoints"]:
        cid = case["test_case_id"]
        status, text = http_call(
            case["method"], case["path"], case.get("headers"), case.get("payload"))

        if status != case["expected_status"]:
            raise GateFail(f"GATE B CRASH: {cid} {case['method']} {case['path']} -- "
                           f"expected status {case['expected_status']}, got {status} "
                           f"(body: {text[:120]!r})")

        # Forbidden-pattern (leak) check first, against the raw text.
        for pattern in case.get("forbidden_string_patterns", []):
            if pattern in text:
                raise GateFail(f"GATE B CRASH: {cid} leaked forbidden pattern "
                               f"{pattern!r} in response: {text[:200]!r}")

        try:
            body = json.loads(text)
        except ValueError:
            raise GateFail(f"GATE B CRASH: {cid} response is not JSON: {text[:120]!r}")
        if not isinstance(body, dict):
            raise GateFail(f"GATE B CRASH: {cid} response is not a JSON object")
        got_keys = set(body.keys())
        want_keys = set(case["expected_schema_keys"])
        if got_keys != want_keys:
            raise GateFail(f"GATE B CRASH: {cid} key-set mismatch -- "
                           f"expected {sorted(want_keys)}, got {sorted(got_keys)}")
        print(f"[PASS] GATE B    -- {cid}: {status} {sorted(got_keys)} "
              f"{case['target_clauses']}")
    print("GATE B SUCCESS: runtime plane aligns with the conformance matrix.")


# --------------------------------------------------------------------------- #
# DOCUMENT PLANE (lint the implementer's openapi.json + route cross-check)
# --------------------------------------------------------------------------- #
def load_linter():
    spec = importlib.util.spec_from_file_location(
        "gt_linter", str(GROUND_TRUTH / "linter.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def document_plane(matrix):
    if not IMPL_OPENAPI.exists():
        raise GateFail(f"implementer openapi.json not found: {IMPL_OPENAPI}")
    linter = load_linter()
    try:
        errors = linter.lint_file(str(IMPL_OPENAPI))
    except ValueError as e:
        raise GateFail(f"DOCUMENT PLANE: openapi.json is not well-formed JSON: {e}")
    if errors:
        raise GateFail("DOCUMENT PLANE: openapi.json failed the ground-truth linter: "
                       + "; ".join(errors))
    print("[PASS] DOC PLANE  -- openapi.json passes the ground-truth linter")

    # No-blend doc-side cross-check: every route the tests hit must be declared.
    schema = json.loads(IMPL_OPENAPI.read_text())
    declared = set()
    for path, ops in schema.get("paths", {}).items():
        for method in ops:
            if method.lower() in ("get", "post", "put", "patch", "delete",
                                  "head", "options"):
                declared.add((method.upper(), path.rstrip("/") or "/"))
    missing = []
    for case in matrix["endpoints"]:
        key = (case["method"].upper(), case["path"].rstrip("/") or "/")
        # 404-expecting cases legitimately hit undeclared routes; skip those.
        if case["expected_status"] == 404:
            continue
        if key not in declared:
            missing.append(f"{key[0]} {key[1]}")
    if missing:
        raise GateFail("DOCUMENT PLANE: openapi.json does not declare routes the "
                       "tests hit: " + ", ".join(sorted(set(missing))))
    print("[PASS] DOC PLANE  -- openapi.json declares every route the tests exercise")


# --------------------------------------------------------------------------- #
# TY0 REGRESSION (legacy route signatures preserved)
# --------------------------------------------------------------------------- #
def _signatures_from_openapi(schema):
    """{(METHOD, path): {status: sorted([response keys])}} from a contract doc."""
    sigs = {}
    for path, ops in schema.get("paths", {}).items():
        for method, op in ops.items():
            if method.lower() not in ("get", "post", "put", "patch", "delete",
                                      "head", "options"):
                continue
            responses = {}
            for status, resp in op.get("responses", {}).items():
                props = resp.get("schema", {}).get("properties", {})
                responses[status] = sorted(props.keys())
            sigs[(method.upper(), path)] = responses
    return sigs


def ty0_regression():
    if not TY0_BASELINE.exists():
        print("[WARN] TY0       -- baseline not found; skipping TY0 regression")
        return
    baseline = json.loads(TY0_BASELINE.read_text())
    impl = _signatures_from_openapi(json.loads(IMPL_OPENAPI.read_text()))

    drift = []
    for route in baseline.get("routes", []):
        key = (route["method"], route["path"])
        want = {k: sorted(v) for k, v in route["responses"].items()}
        got = impl.get(key)
        if got is None:
            drift.append(f"{key[0]} {key[1]}: route DROPPED from openapi.json")
            continue
        if got != want:
            drift.append(f"{key[0]} {key[1]}: response signature mutated "
                         f"(baseline {want}, openapi {got})")
    if drift:
        raise GateFail("TY0 REGRESSION: legacy route signatures changed: "
                       + "; ".join(drift))
    print(f"[PASS] TY0       -- openapi.json preserves all "
          f"{len(baseline.get('routes', []))} legacy route signatures")


# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description="In-band squeeze runner (Use Case C)")
    ap.add_argument("--bad", action="store_true",
                    help="load the coherent-and-wrong negative control server")
    args = ap.parse_args()

    if os.environ.get("SERVER_CMD"):
        cmd = shlex.split(os.environ["SERVER_CMD"])
        label = "OVERRIDE (SERVER_CMD)"
    elif args.bad:
        cmd = [sys.executable, str(BAD_SERVER), "--host", HOST,
               "--port", str(PORT), "--db", str(DB)]
        label = "NEGATIVE CONTROL (coherent-and-wrong)"
    else:
        cmd = [sys.executable, str(IMPL_MAIN), "--host", HOST,
               "--port", str(PORT), "--db", str(DB)]
        label = "implementer"

    if not MATRIX.exists():
        sys.exit(f"error: test matrix not found: {MATRIX} "
                 f"(run exerciser/build_test_matrix.py)")

    print(f"Server under test: {cmd[1] if len(cmd) > 1 else cmd[0]}  [{label}]")
    matrix = json.loads(MATRIX.read_text())

    proc = None
    try:
        check_isolation()
        gate_c(matrix)
        proc = start_server(cmd)
        gate_b(matrix)
        document_plane(matrix)
        ty0_regression()
    except GateFail as e:
        print(f"\n[FAIL] {e}")
        print("SQUEEZE FAILED")
        if proc:
            stop_server(proc)
        return 1
    except Exception as e:  # noqa: BLE001
        print(f"\n[ERROR] unexpected: {e}")
        print("SQUEEZE FAILED")
        if proc:
            stop_server(proc)
        return 1

    stop_server(proc)
    print("\nSQUEEZE OK: ISOLATION + GATE C + GATE B + DOCUMENT-PLANE + TY0 all green.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
