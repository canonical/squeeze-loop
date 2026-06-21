#!/usr/bin/env bash
# Deploy the Low-Level Sources of Truth into the LXC container (spec §1 + §2).
# Run as root INSIDE the container, after `python3 build_ground_truth.py`.
# Idempotent: safe to re-run.
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)/shared"
DEST="/opt/squeeze/shared"

if [ "$(id -u)" -ne 0 ]; then
    echo "error: must run as root (chown root:root + system directories)" >&2
    exit 1
fi
for f in base_warehouse.db history_ledger.json history_ledger.sig; do
    [ -f "$SRC/$f" ] || { echo "error: $SRC/$f missing; run build_ground_truth.py first" >&2; exit 1; }
done

# Shared, read-only ground-truth plane. The db is universally read-only (0444),
# root-owned, so neither implementer nor exerciser can mutate the data plane.
install -d -m 0755 -o root -g root /opt/squeeze "$DEST"
install -m 0444 -o root -g root "$SRC/base_warehouse.db"   "$DEST/base_warehouse.db"
install -m 0444 -o root -g root "$SRC/history_ledger.json" "$DEST/history_ledger.json"
install -m 0444 -o root -g root "$SRC/history_ledger.sig"  "$DEST/history_ledger.sig"

# Re-verify the signature at the deployed location.
( cd "$DEST" && sha256sum -c history_ledger.sig )

echo "deployed ground truth -> $DEST (root:root, 0444)"
echo "note: the isolated POSIX users (sentinel/implementer/exerciser) and their"
echo "      0700 home directories are provisioned by the orchestrator layer (spec §1),"
echo "      not by this script, which owns only the §2 sources-of-truth plane."
