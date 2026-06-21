#!/usr/bin/env bash
# Deploy the Upper Bound (Refund Policy) into the LXC container (spec §1).
# Run as root INSIDE the container. Idempotent.
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)/refund_policy.md"
DEST="/opt/squeeze/shared/refund_policy.md"

if [ "$(id -u)" -ne 0 ]; then
    echo "error: must run as root (chown root:root)" >&2
    exit 1
fi
[ -f "$SRC" ] || { echo "error: $SRC missing" >&2; exit 1; }

# Validate before deploying: never publish a malformed ceiling, and never
# publish one that fails Gate A (code/schema/prompt syntax leaked into policy).
if command -v python3 >/dev/null; then
    ( cd "$(dirname "$SRC")" && python3 - <<'PY'
import sys, handbook, gate_checks
from pathlib import Path
try:
    handbook.parse()
except handbook.HandbookError as e:
    print(f"refusing to deploy malformed handbook: {e}", file=sys.stderr); sys.exit(1)
ga = gate_checks.gate_a_policy_centric(Path("refund_policy.md").read_text())
if not ga:
    print(f"refusing to deploy non-policy-centric handbook: {ga.detail}", file=sys.stderr)
    sys.exit(1)
PY
    ) || exit 1
fi

# Universally read-only, root-owned: no agent can edit the policy to make a
# broken test pass.
install -d -m 0755 -o root -g root /opt/squeeze /opt/squeeze/shared
install -m 0444 -o root -g root "$SRC" "$DEST"

echo "deployed upper bound -> $DEST (root:root, 0444)"
echo "note: the dispatch loop copies a single policy's block into"
echo "      /home/<agent>/spec.txt at delegation time (handbook.extract_block)."
