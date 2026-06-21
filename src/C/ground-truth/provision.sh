#!/usr/bin/env bash
# Deploy the Low-Level Sources of Truth into the LXC container (spec §1 + §2 + §4).
# Run as root INSIDE the container, after `python3 build_ground_truth.py`.
# Idempotent: safe to re-run.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
SRC="$ROOT/shared"
DEST="/opt/squeeze/shared"
DEST_APP="/opt/squeeze/runtime_app"

if [ "$(id -u)" -ne 0 ]; then
    echo "error: must run as root (chown root:root + system directories)" >&2
    exit 1
fi
for f in app_state.db base_schema.json ty0_baseline.json; do
    [ -f "$SRC/$f" ] || { echo "error: $SRC/$f missing; run build_ground_truth.py first" >&2; exit 1; }
done
[ -f "$ROOT/reference_server.py" ] || { echo "error: $ROOT/reference_server.py missing" >&2; exit 1; }
[ -f "$ROOT/run_server.sh" ] || { echo "error: $ROOT/run_server.sh missing" >&2; exit 1; }

# Shared, read-only ground-truth plane. db + schema + ty0 are universally read-only
# (0444), root-owned, so neither implementer nor exerciser can mutate the data, the
# contract, or the Item Zero baseline.
install -d -m 0755 -o root -g root /opt/squeeze "$DEST" "$DEST_APP"
install -m 0444 -o root -g root "$SRC/app_state.db"      "$DEST/app_state.db"
install -m 0444 -o root -g root "$SRC/base_schema.json"  "$DEST/base_schema.json"
install -m 0444 -o root -g root "$SRC/ty0_baseline.json" "$DEST/ty0_baseline.json"

# Runtime plane: the frozen API server + its launcher (read-only; the service user
# only executes them). run_server.sh is 0555 so it can be invoked.
install -m 0444 -o root -g root "$ROOT/reference_server.py" "$DEST_APP/reference_server.py"
install -m 0555 -o root -g root "$ROOT/run_server.sh"       "$DEST_APP/run_server.sh"

# Re-verify the TY0 baseline hash at the deployed location.
( cd "$DEST" && python3 - <<'PY'
import hashlib, json, sqlite3, sys
ty0 = json.load(open("ty0_baseline.json"))
schema = json.load(open("base_schema.json"))
sigs = []
for path, ops in schema.get("paths", {}).items():
    for method, op in ops.items():
        if method.lower() not in ("get","post","put","patch","delete","head","options"):
            continue
        responses = {s: sorted(r.get("schema",{}).get("properties",{}).keys())
                     for s, r in op.get("responses",{}).items()}
        sigs.append({"method": method.upper(), "path": path, "responses": responses})
sigs.sort(key=lambda s: (s["path"], s["method"]))
conn = sqlite3.connect("file:app_state.db?mode=ro", uri=True)
tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
cols = {t: [r[1] for r in conn.execute(f"PRAGMA table_info({t})")] for t in tables}
conn.close()
snap = {"routes": sigs, "db_columns": cols}
fresh = hashlib.sha256(json.dumps(snap, sort_keys=True, separators=(",",":")).encode()).hexdigest()
print("ty0 baseline OK" if fresh == ty0.get("hash") else "ty0 baseline MISMATCH")
sys.exit(0 if fresh == ty0.get("hash") else 1)
PY
)

echo "deployed ground truth -> $DEST (root:root, 0444)"
echo "deployed runtime app  -> $DEST_APP/reference_server.py (0444), run_server.sh (0555)"
echo "note: the isolated POSIX users (sentinel/implementer/exerciser) and their"
echo "      0700 home directories are provisioned by the orchestrator layer (spec §1),"
echo "      not by this script, which owns only the §2 sources-of-truth + runtime plane."
