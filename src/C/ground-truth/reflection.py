"""Item Zero (TY0) route-discovery reflection (spec §4).

This is the pinned reflection engine that BOTH build_ground_truth.py and
verify_ground_truth.py call, so the TY0 baseline can only ever be what this
function computes -- no hand-typed signature can enter the ground truth, and the
"every signature recomputes" invariant is enforced by construction.

`reflect()` logs the canonical signature of every listening route (method, path,
response-keys-by-status) plus the database column state, and `manifest_hash()`
computes the content hash over a deterministic manifest of that snapshot. A silent
structural or signature mutation on any route -- or a column change -- flips the
hash, which is exactly the regression the sentinel blocks on (spec §4).

The route signatures are derived from the canonical shared contract
(base_schema.json), so the TY0 snapshot is anchored to the document plane and the
runtime plane must align with it.
"""

import hashlib
import json
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE_SCHEMA = HERE / "base_schema.json"


def _route_signatures():
    """Canonical {method, path, responses:{status:[sorted response keys]}} list,
    derived from the document-plane contract. Sorted for determinism."""
    schema = json.loads(BASE_SCHEMA.read_text())
    sigs = []
    for path, ops in schema.get("paths", {}).items():
        for method, op in ops.items():
            if method.lower() not in (
                    "get", "post", "put", "patch", "delete", "head", "options"):
                continue
            responses = {}
            for status, resp in op.get("responses", {}).items():
                props = resp.get("schema", {}).get("properties", {})
                responses[status] = sorted(props.keys())
            sigs.append({
                "method": method.upper(),
                "path": path,
                "responses": responses,
            })
    sigs.sort(key=lambda s: (s["path"], s["method"]))
    return sigs


def _db_columns(db_path):
    """{table: [columns in declared order]} for the storage DB. Read-only."""
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        tables = [r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall()]
        cols = {}
        for t in tables:
            # PRAGMA table_info rows: (cid, name, type, notnull, dflt, pk)
            info = conn.execute(f"PRAGMA table_info({t})").fetchall()
            cols[t] = [row[1] for row in info]
    finally:
        conn.close()
    return cols


def reflect(db_path):
    """Return the TY0 snapshot dict (WITHOUT the 'hash' field)."""
    return {
        "routes": _route_signatures(),
        "db_columns": _db_columns(db_path),
    }


def manifest_hash(snapshot):
    """SHA-256 over a deterministic manifest of the snapshot (hash field excluded).

    Serializing with sort_keys + fixed separators makes the manifest canonical, so
    the same snapshot always yields the same digest across runs and Python versions.
    """
    payload = {k: v for k, v in snapshot.items() if k != "hash"}
    manifest = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(manifest).hexdigest()
