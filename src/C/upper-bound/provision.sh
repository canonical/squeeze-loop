#!/usr/bin/env bash
# Deploy the Upper Bound (API Policy Manifest) into the LXC container (spec §1).
# Run as root INSIDE the container. Idempotent.
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)/api_policy_manifest.md"
DEST="/opt/squeeze/shared/api_policy_manifest.md"

if [ "$(id -u)" -ne 0 ]; then
    echo "error: must run as root (chown root:root)" >&2
    exit 1
fi
[ -f "$SRC" ] || { echo "error: $SRC missing" >&2; exit 1; }

# Validate before deploying: never publish a malformed ceiling, and never publish
# one that fails Gate A (code/schema/impl syntax leaked into the manifest).
if command -v python3 >/dev/null; then
    ( cd "$(dirname "$SRC")" && python3 - <<'PY'
import sys, handbook, gate_checks
from pathlib import Path
try:
    handbook.parse()
except handbook.HandbookError as e:
    print(f"refusing to deploy malformed manifest: {e}", file=sys.stderr); sys.exit(1)
ga = gate_checks.gate_a_policy_centric(Path("api_policy_manifest.md").read_text())
if not ga:
    print(f"refusing to deploy non-policy-centric manifest: {ga.detail}", file=sys.stderr)
    sys.exit(1)
PY
    ) || exit 1
fi

# Universally read-only, root-owned: no agent can edit the manifest to make a
# broken contract test pass (physical isolation barrier C3).
install -d -m 0755 -o root -g root /opt/squeeze /opt/squeeze/shared
install -m 0444 -o root -g root "$SRC" "$DEST"

echo "deployed upper bound -> $DEST (root:root, 0444)"
echo "note: the dispatch loop extracts a single MANIFEST_ID block into"
echo "      /home/<agent>/spec.txt at delegation time (handbook.extract_block)."
