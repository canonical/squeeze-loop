#!/usr/bin/env python3
"""Build the Low-Level Sources of Truth for Use Case D (Rocq) into ./shared/.

Lays out the four-user directory MODEL conceptually, pins the stdlib plane (the
PIN.md version contract), and SIGNS the certified proof registry trunk.

  shared/rocq_stdlib/      Storage Plane    -- pinned env (PIN.md version contract)
  shared/proof_registry/   Invariant Plane  -- certified .v trunk + registry.sig

What this script does WITHOUT Rocq (always):
  * verifies the stdlib PIN.md contract exists
  * signs the proof registry trunk (sha256 manifest -> registry.sig)
  * prints the four-POSIX-user layout that provision.sh will enforce as root

What it does NOT do here: chown/chmod to the four users, lay down the real
stdlib `.vo` tree, or run coqc. Those need root + a provisioned Rocq and live in
provision.sh / the LXC step (we are unprivileged here).

Idempotent and deterministic: re-running reproduces an identical registry.sig.
"""

import sys
from pathlib import Path

import registry

HERE = Path(__file__).resolve().parent
SHARED = HERE / "shared"
STDLIB = SHARED / "rocq_stdlib"
REGISTRY = SHARED / "proof_registry"

# The four-POSIX-user isolation model (spec D1). Documented here; enforced by
# provision.sh as root inside the LXC (we cannot chown without root).
USER_MODEL = [
    ("sentinel",   "/opt/squeeze/orchestrator", "0700", "orchestrator + gate_sentinel.py"),
    ("formalizer", "/home/formalizer/definition", "0700", "theorem statements (.v)"),
    ("prover",     "/home/prover/solution",       "0700", "tactical proof scripts (.v)"),
    ("exerciser",  "/home/exerciser/mutation",    "0700", "negative mutation matrix"),
]


def main():
    if not (STDLIB / "PIN.md").exists():
        print(f"error: missing storage-plane pin contract {STDLIB/'PIN.md'}")
        return 1

    vfiles = registry.registry_files(REGISTRY)
    if not vfiles:
        print(f"error: certified proof registry {REGISTRY} has no .v files")
        return 1

    trunk = registry.write_signature(REGISTRY)

    print("[storage]   rocq_stdlib/      : pin contract present (PIN.md)")
    print(f"[invariant] proof_registry/   : {len(vfiles)} certified proof(s): "
          + ", ".join(p.name for p in vfiles))
    print(f"[invariant] registry.sig      : trunk {trunk}")
    print("\n[model] four-POSIX-user isolation (enforced by provision.sh as root):")
    for user, path, mode, role in USER_MODEL:
        print(f"          {user:<10} {path:<28} {mode}  {role}")
    print("\n[compute]   Rocq engine       : pinned in the LXC image "
          "(opam coq 8.20.1; see provision.sh / PIN.md)")
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
