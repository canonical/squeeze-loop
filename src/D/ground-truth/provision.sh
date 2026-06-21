#!/usr/bin/env bash
# Provision the Use Case D (Rocq) Low-Level Sources of Truth + four-user model
# inside the LXC container (spec D1 + D2). Run as root INSIDE the container,
# after `python3 build_ground_truth.py`. Idempotent: safe to re-run.
#
# HONESTY NOTE on Rocq install: Rocq/Coq is installed via opam and REQUIRES THE
# NETWORK. The squeeze itself runs with the network cut (run_in_lxc.sh hard-gates
# on no-internet). Therefore Rocq must be baked in / provisioned BEFORE the net
# is cut. This script's opam step is the "provision while networked" phase; if it
# runs with no network it will fail loudly rather than silently skip -- and the
# gate will later report DEPENDENCY UNMET rather than fake a pass.
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)"
SHARED_SRC="$SRC/shared"
SQUEEZE=/opt/squeeze
DEST="$SQUEEZE/shared"

if [ "$(id -u)" -ne 0 ]; then
    echo "error: must run as root (chown/chmod across four POSIX users)" >&2
    exit 1
fi

# --- 0. pinned Rocq compiler (NETWORKED step) --------------------------------
COQ_PIN="${COQ_PIN:-8.20.1}"
if command -v coqc >/dev/null 2>&1; then
    echo "[compute] coqc already present: $(coqc --version | head -1)"
else
    echo "[compute] installing Rocq/Coq $COQ_PIN via opam (NEEDS NETWORK) ..."
    if ! command -v opam >/dev/null 2>&1; then
        echo "error: opam not found; cannot install Rocq" >&2; exit 1
    fi
    # Networked provisioning. If the net is already cut this fails honestly.
    opam init --bare --disable-sandboxing -y || true
    opam switch create rocq-pin "ocaml-base-compiler" -y 2>/dev/null || opam switch set rocq-pin
    eval "$(opam env --switch=rocq-pin)"
    opam pin add -y coq "$COQ_PIN"
    opam install -y "coq.$COQ_PIN"
    eval "$(opam env --switch=rocq-pin)"
fi

# --- 1. four-POSIX-user isolation model (spec D1) ----------------------------
for u in sentinel formalizer prover exerciser; do
    id "$u" >/dev/null 2>&1 || useradd -m -s /bin/bash "$u"
done

# --- 2. shared sources of truth (root-owned) ---------------------------------
install -d -m 0755 -o root -g root "$SQUEEZE" "$DEST"

# Storage Plane: pinned stdlib, READ/EXECUTE ONLY (0555) so agents cannot
# hot-fix foundational axioms. Lay down the real stdlib of the pinned switch.
install -d -m 0555 -o root -g root "$DEST/rocq_stdlib"
install -m 0444 -o root -g root "$SHARED_SRC/rocq_stdlib/PIN.md" "$DEST/rocq_stdlib/PIN.md" 2>/dev/null || true
if command -v coqc >/dev/null 2>&1; then
    COQLIB="$(coqc -config 2>/dev/null | awk -F'=' '/COQLIB/{print $2}' | tr -d ' ')"
    if [ -n "${COQLIB:-}" ] && [ -d "$COQLIB" ]; then
        cp -a "$COQLIB/." "$DEST/rocq_stdlib/" 2>/dev/null || true
        echo "[storage] mirrored pinned stdlib from $COQLIB -> $DEST/rocq_stdlib (0555)"
    fi
fi
chmod -R a-w "$DEST/rocq_stdlib" || true

# Invariant Plane: certified proof registry trunk + signature, root-owned 0444.
install -d -m 0555 -o root -g root "$DEST/proof_registry"
for f in "$SHARED_SRC/proof_registry/"*.v "$SHARED_SRC/proof_registry/registry.sig"; do
    [ -e "$f" ] && install -m 0444 -o root -g root "$f" "$DEST/proof_registry/$(basename "$f")"
done

# --- 3. orchestrator (sentinel-owned 0700) + gate referee --------------------
install -d -m 0700 -o sentinel -g sentinel "$SQUEEZE/orchestrator" "$SQUEEZE/orchestrator/ledger"
for py in gate_sentinel.py rocq_kernel.py registry.py; do
    install -m 0700 -o sentinel -g sentinel "$SRC/$py" "$SQUEEZE/orchestrator/$py"
done

# --- 4. per-agent 0700 workspaces -------------------------------------------
install -d -m 0700 -o formalizer -g formalizer /home/formalizer/definition
install -d -m 0700 -o prover     -g prover     /home/prover/solution
install -d -m 0700 -o exerciser  -g exerciser  /home/exerciser/mutation

# --- 5. re-verify the registry signature at the deployed location ------------
( cd "$SQUEEZE/orchestrator" && python3 - <<PY
import sys; from pathlib import Path
sys.path.insert(0, ".")
import registry
ok, detail = registry.verify_signature(Path("$DEST/proof_registry"))
print("registry signature:", "OK" if ok else "FAIL", "--", detail)
sys.exit(0 if ok else 1)
PY
)

echo "deployed Use Case D ground truth -> $DEST"
echo "  storage   : $DEST/rocq_stdlib       (root:root 0555, pinned stdlib)"
echo "  invariant : $DEST/proof_registry    (root:root 0444, signed trunk)"
echo "  orchestr. : $SQUEEZE/orchestrator   (sentinel 0700, gate_sentinel.py)"
echo "  agents    : /home/{formalizer,prover,exerciser}/* (each 0700)"
if ! command -v coqc >/dev/null 2>&1; then
  echo "WARNING: coqc still absent -- Gate B will report DEPENDENCY UNMET (no fake pass)."
fi
