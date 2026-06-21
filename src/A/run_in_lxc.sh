#!/usr/bin/env bash
# Run the Use Case A squeeze inside an unprivileged LXC container WITH internet
# (rootless, via slirp4netns -- see src/lxc_common.sh), so the in-band layer can
# fetch what it needs. The squeeze itself is stdlib-only Python; the internet is
# available for enrichment.
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"; SRC_PARENT="$(dirname "$SRC")"
. "$SRC_PARENT/lxc_common.sh"

NAME="${LXC_NAME:-ucA}"; TOP=A; GUEST="/root/$TOP"

lxc_prereqs
lxc_up           "$NAME" "${LXC_RELEASE:-resolute}"
lxc_net_up       "$NAME"
lxc_assert_internet "$NAME"
lxc_sync         "$NAME" "$SRC_PARENT" "$TOP"

log "running the Use Case A squeeze inside $NAME (with internet)"
lxc-attach -n "$NAME" -- /bin/sh -c '
  set -e
  cd '"$GUEST"'
  echo "[engine] sqlite $(python3 -c "import sqlite3;print(sqlite3.sqlite_version)")"
  python3 ground-truth/build_ground_truth.py >/dev/null && echo "[1] ground truth built"
  python3 ground-truth/verify_ground_truth.py | tail -1
  python3 upper-bound/validate_handbook.py | tail -1
  python3 in-band-deliverable/exerciser/build_validation_matrix.py >/dev/null && echo "[4] matrices built"
  python3 in-band-deliverable/runner/execute_squeeze.py | tail -2
'

log "negative control: a coherent-and-wrong implementer must be REJECTED"
if lxc-attach -n "$NAME" -- /bin/sh -c "cd $GUEST && COMPUTE_METRIC=$GUEST/evidence/coherent_wrong_fixture.py python3 in-band-deliverable/runner/execute_squeeze.py" \
   >/tmp/lxc-negctrl-a.out 2>&1; then
  echo "UNEXPECTED: coherent-and-wrong implementer was NOT rejected"; exit 1
else
  grep -E 'GATE B CRASH' /tmp/lxc-negctrl-a.out || true
  echo "OK: coherent-and-wrong implementer rejected inside the container."
fi

log "DONE -- Use Case A ran inside $NAME (unprivileged, with internet)."
