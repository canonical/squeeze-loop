#!/usr/bin/env bash
# Deploy the Upper Bound (Textbook Manifest) into the LXC container -- Use Case D,
# spec §1. Run as root INSIDE the container. Idempotent.
#
#   1. Install textbook_manifest.md at /opt/squeeze/shared/textbook_manifest.md
#      as root:root 0444 (universally read-only): no agent can soften a claim to
#      clear a stuck proof.
#   2. Extract the active EXERCISE_ID block and write it to
#      /home/formalizer/spec.txt and /home/exerciser/spec.txt, each owned by /
#      readable only by that agent. The raw manifest stays hidden from `prover`.
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)/textbook_manifest.md"
DEST="/opt/squeeze/shared/textbook_manifest.md"
ACTIVE_EXERCISE="${1:-EX_ROCQ_074}"

[ -f "$SRC" ] || { echo "error: $SRC missing" >&2; exit 1; }

# Validate before deploying: never publish a malformed ceiling. (No Rocq needed.)
if command -v python3 >/dev/null; then
    ( cd "$(dirname "$SRC")" && python3 - "$ACTIVE_EXERCISE" <<'PY'
import sys, manifest
try:
    exercises = manifest.parse()
    manifest.by_id(exercises, sys.argv[1])   # active exercise must exist
except manifest.ManifestError as e:
    print(f"refusing to deploy malformed manifest: {e}", file=sys.stderr)
    sys.exit(1)
PY
    ) || exit 1
else
    echo "error: python3 required to validate the manifest before deploy" >&2
    exit 1
fi

# ---- root-only filesystem operations (guarded) -----------------------------
if [ "$(id -u)" -ne 0 ]; then
    echo "NOTE: not root -- skipping privileged install (chown root:root, 0444," \
         "per-agent spec.txt). Validation above already passed." >&2
    echo "      Re-run as root inside the LXC container to deploy." >&2
    exit 0
fi

# (1) Universally read-only, root-owned manifest -- the physical barrier.
install -d -m 0755 -o root -g root /opt/squeeze /opt/squeeze/shared
install -m 0444 -o root -g root "$SRC" "$DEST"
echo "deployed upper bound -> $DEST (root:root, 0444)"

# (2) Extract the active exercise block to each agent's spec.txt (hidden from prover).
extract_block() {
    python3 - "$SRC" "$ACTIVE_EXERCISE" <<'PY'
import sys, manifest
sys.stdout.write(manifest.extract_block(sys.argv[2], sys.argv[1]))
PY
}

for agent in formalizer exerciser; do
    home="/home/$agent"
    if ! id "$agent" >/dev/null 2>&1; then
        echo "WARN: user '$agent' does not exist; skipping $home/spec.txt" >&2
        continue
    fi
    install -d -m 0700 -o "$agent" -g "$agent" "$home"
    extract_block > "$home/spec.txt"
    chown "$agent:$agent" "$home/spec.txt"
    chmod 0400 "$home/spec.txt"
    echo "wrote $home/spec.txt ($agent:$agent, 0400) for $ACTIVE_EXERCISE"
done

echo "note: the raw manifest is NOT placed in prover's space; prover never sees" \
     "the English spec, only the formalizer's naked theorem signature."
