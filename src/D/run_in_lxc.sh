#!/usr/bin/env bash
# Run the Use Case D Rocq squeeze inside an unprivileged LXC container WITH
# internet (rootless, via slirp4netns -- see src/lxc_common.sh). The internet lets
# the in-band layer be enriched and lets the container install its OWN Coq/Rocq
# kernel (matching its own glibc) rather than borrowing the host's.
#
# Gate B is still capability-gated: if the kernel is somehow absent the squeeze
# prints DEPENDENCY UNMET and SKIPS -- it never fabricates a proof verdict.
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"; SRC_PARENT="$(dirname "$SRC")"
. "$SRC_PARENT/lxc_common.sh"

NAME="${LXC_NAME:-ucD}"; TOP=D; GUEST="/root/$TOP"

lxc_prereqs
lxc_up           "$NAME" "${LXC_RELEASE:-resolute}"
lxc_net_up       "$NAME"
lxc_assert_internet "$NAME"

# --- install the Coq/Rocq kernel in-container (needs the internet we just got) ---
log "ensuring the Coq/Rocq kernel is installed in $NAME"
lxc-attach -n "$NAME" -- /bin/sh -c '
  if command -v coqc >/dev/null 2>&1 || command -v rocq >/dev/null 2>&1; then
    echo "[compute] kernel already present: $(coqc --version 2>/dev/null | head -1)$(rocq --version 2>/dev/null | head -1)"
  else
    export DEBIAN_FRONTEND=noninteractive
    apt-get update >/tmp/apt.log 2>&1
    (apt-get install -y rocq-prover || apt-get install -y coq) >>/tmp/apt.log 2>&1 \
      && echo "[compute] installed: $(coqc --version 2>/dev/null | head -1)" \
      || { echo "[compute] kernel install FAILED (see /tmp/apt.log); Gate B will SKIP honestly"; tail -3 /tmp/apt.log; }
  fi
'

lxc_sync "$NAME" "$SRC_PARENT" "$TOP"

log "running the Use Case D squeeze inside $NAME (with internet)"
lxc-attach -n "$NAME" -- /bin/sh -c '
  cd '"$GUEST"'/ground-truth
  command -v coqc >/dev/null 2>&1 && echo "[engine] $(coqc --version 2>/dev/null | head -1)" || echo "[engine] kernel ABSENT -- Gate B will SKIP (no fake pass)"
  python3 build_ground_truth.py >/dev/null && echo "[1] ground truth built (registry signed)"
  python3 verify_ground_truth.py >/tmp/v.out 2>&1;                              echo "[2] verify rc=$? -> $(tail -1 /tmp/v.out)"
  python3 gate_sentinel.py --fixtures --solution exercise_good.v >/tmp/g.out 2>&1; echo "[3] gate(good)  rc=$? -> $(tail -1 /tmp/g.out)"
  python3 gate_sentinel.py --fixtures --solution exercise_admitted.v >/tmp/a.out 2>&1; echo "[4] gate(admitted-cheat) rc=$? (1=correctly caught) -> $(grep -m1 -iE "escape hatch|FAILURE" /tmp/a.out || true)"
  cd '"$GUEST"'
  python3 in-band-deliverable/runner/execute_squeeze.py >/tmp/s.out 2>&1;        echo "[5] in-band squeeze rc=$? -> $(tail -1 /tmp/s.out)"
  python3 evidence/measure_squeeze.py >/tmp/m.out 2>&1;                          echo "[6] measure rc=$? -> $(tail -1 /tmp/m.out)"
  python3 -c "import json;d=json.load(open(\"evidence/results.json\"));print(\"    real counts:\",{k:d.get(k) for k in [\"rocq_available\",\"proof_type_checks\",\"axiom_clean\",\"defects_caught\",\"ablation_barrier_on_catchable\",\"ablation_barrier_off_catchable\",\"coherent_wrong_caught\"]})"
'

log "DONE -- Use Case D ran inside $NAME (unprivileged, with internet)."
