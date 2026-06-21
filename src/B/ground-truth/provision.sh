#!/usr/bin/env bash
# Deploy the Low-Level Sources of Truth into the LXC container (spec §1 + §2).
# Run as root INSIDE the container, after `python3 build_ground_truth.py`.
# Idempotent: safe to re-run.
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)/shared"
APP="$(cd "$(dirname "$0")" && pwd)/app.py"
DEST="/opt/squeeze/shared"
DEST_ARCHIVE="$DEST/archive_ledger"
DEST_APP="/opt/squeeze/runtime_app"

if [ "$(id -u)" -ne 0 ]; then
    echo "error: must run as root (chown root:root + system directories)" >&2
    exit 1
fi
[ -f "$SRC/customer_history.db" ] || { echo "error: $SRC/customer_history.db missing; run build_ground_truth.py first" >&2; exit 1; }
[ -f "$SRC/archive_ledger/ledger.sig" ] || { echo "error: $SRC/archive_ledger/ledger.sig missing; run build_ground_truth.py first" >&2; exit 1; }
[ -f "$APP" ] || { echo "error: $APP missing" >&2; exit 1; }

# Shared, read-only ground-truth plane. The db + archive are universally read-only
# (0444), root-owned, so neither implementer nor exerciser can mutate the data or
# the adjudicated archive.
install -d -m 0755 -o root -g root /opt/squeeze "$DEST" "$DEST_ARCHIVE" "$DEST_APP"
install -m 0444 -o root -g root "$SRC/customer_history.db" "$DEST/customer_history.db"

# Archive ledger: every case file + the signature, all 0444.
for f in "$SRC"/archive_ledger/*; do
    install -m 0444 -o root -g root "$f" "$DEST_ARCHIVE/$(basename "$f")"
done

# Compute plane: the frozen REST app (read-only; the service user only executes it).
install -m 0444 -o root -g root "$APP" "$DEST_APP/app.py"

# Re-verify the archive signature at the deployed location.
( cd "$DEST" && python3 - <<'PY'
import hashlib, pathlib, sys
arc = pathlib.Path("archive_ledger")
sig = (arc / "ledger.sig").read_text().split()[0]
lines = []
for p in sorted(arc.iterdir()):
    if p.name == "ledger.sig":
        continue
    lines.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}")
manifest = ("\n".join(lines) + "\n").encode()
fresh = hashlib.sha256(manifest).hexdigest()
print("archive signature OK" if fresh == sig else "archive signature MISMATCH")
sys.exit(0 if fresh == sig else 1)
PY
)

echo "deployed ground truth -> $DEST (root:root, 0444)"
echo "deployed runtime app  -> $DEST_APP/app.py (root:root, 0444)"
echo "note: the isolated POSIX users (sentinel/implementer/exerciser) and their"
echo "      0700 home directories are provisioned by the orchestrator layer (spec §1),"
echo "      not by this script, which owns only the §2 sources-of-truth + §3 app plane."
