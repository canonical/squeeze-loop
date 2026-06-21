"""Certified Proof Registry -- the Invariant Plane (spec D2, Step 2).

The registry is the set of previously verified exercise `.v` files plus a
signature pinning the certified trunk. This module is PURE PYTHON and runs
without Rocq: it enumerates the trunk deterministically, computes the trunk
digest, and writes/verifies `registry.sig`. The actual *re-compilation* of the
trunk (the Gate B regression check) is delegated to rocq_kernel.coqc_compile and
is capability-gated separately.

registry.sig format (sha256sum(1)-compatible, sorted by filename):
    <sha256-of-file>  <filename>
    ...
    <sha256-of-manifest>  registry.sig.trunk
The final TRUNK line is the digest of the concatenation of the per-file lines,
so a single changed byte in any registered proof changes the trunk digest.
"""

import hashlib
from pathlib import Path

TRUNK_LABEL = "registry.sig.trunk"


def registry_files(registry_dir: Path) -> list[Path]:
    """Deterministic, sorted list of certified .v files in the trunk."""
    return sorted(registry_dir.glob("*.v"), key=lambda p: p.name)


def _file_digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def compute_manifest(registry_dir: Path) -> tuple[list[str], str]:
    """Return (lines, trunk_digest).

    lines are the per-file 'sha  name' rows; trunk_digest is sha256 over their
    exact concatenation (the certified-trunk fingerprint)."""
    lines = [f"{_file_digest(p)}  {p.name}" for p in registry_files(registry_dir)]
    body = ("\n".join(lines) + "\n").encode("utf-8") if lines else b""
    trunk = hashlib.sha256(body).hexdigest()
    return lines, trunk


def write_signature(registry_dir: Path) -> str:
    """(Re)sign the trunk -> registry.sig. Returns the trunk digest."""
    lines, trunk = compute_manifest(registry_dir)
    sig_path = registry_dir / "registry.sig"
    out = "\n".join(lines + [f"{trunk}  {TRUNK_LABEL}"]) + "\n"
    sig_path.write_text(out)
    return trunk


def verify_signature(registry_dir: Path) -> tuple[bool, str]:
    """Recompute the trunk and compare against registry.sig.

    Returns (ok, detail). ok is False if the sig is missing, malformed, lists a
    different file set, or any file digest / the trunk digest disagrees."""
    sig_path = registry_dir / "registry.sig"
    if not sig_path.exists():
        return False, "registry.sig missing"

    recorded = {}
    recorded_trunk = None
    for raw in sig_path.read_text().splitlines():
        if not raw.strip():
            continue
        try:
            digest, name = raw.split("  ", 1)
        except ValueError:
            return False, f"malformed line: {raw!r}"
        if name == TRUNK_LABEL:
            recorded_trunk = digest
        else:
            recorded[name] = digest

    lines, trunk = compute_manifest(registry_dir)
    actual = {}
    for ln in lines:
        d, n = ln.split("  ", 1)
        actual[n] = d

    if recorded_trunk is None:
        return False, "no trunk line in registry.sig"
    if set(recorded) != set(actual):
        return False, (f"file set drift: sig={sorted(recorded)} "
                       f"disk={sorted(actual)}")
    for name, d in actual.items():
        if recorded[name] != d:
            return False, f"digest mismatch for {name}"
    if recorded_trunk != trunk:
        return False, f"trunk digest mismatch ({recorded_trunk[:12]} vs {trunk[:12]})"
    return True, f"trunk {trunk[:12]}... ({len(actual)} file(s))"
