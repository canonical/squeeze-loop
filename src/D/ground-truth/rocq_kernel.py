"""Capability-gated wrappers around the Rocq/Coq kernel binaries.

This module is the ONLY place that shells out to `coqc` / `rocqchk`. Every call
is capability-gated:

  * If the binary is present on PATH, it is invoked FOR REAL and the genuine
    exit status / stdout / stderr are returned.
  * If the binary is ABSENT, NO verdict is fabricated. The wrapper returns a
    KernelResult with status == DEPENDENCY_UNMET. Callers must treat that as a
    hard "cannot decide" -- never as a pass.

The cardinal sin of this repository is faking a green check. There is no code
path here that returns "compiled OK" or "axiom-clean" or "mutation caught"
unless a real kernel binary actually said so.
"""

import shutil
import subprocess
from dataclasses import dataclass, field

# Logical root the spec mandates for the pinned stdlib plane.
LOGICAL_ROOT = "Top"

# Axiom-audit leak tokens (spec D3.2 / in-band §3): presence in --print-assumptions
# output means an escape hatch (Admitted) or an unauthorized Axiom.
LEAK_TOKENS = ("Admitted", "Axiom", "Axioms", "admit")
# The clean banner rocqchk/coqchk prints when a term is fully discharged.
CLEAN_TOKEN = "Closed under the global context"


@dataclass
class KernelResult:
    """Outcome of a kernel invocation. `available` distinguishes a real run from
    an unmet dependency so callers can never confuse the two."""
    available: bool
    returncode: int | None = None
    stdout: str = ""
    stderr: str = ""
    cmd: list = field(default_factory=list)

    @property
    def ran(self) -> bool:
        return self.available and self.returncode is not None

    @property
    def ok(self) -> bool:
        """True ONLY if a real kernel ran and returned exit 0."""
        return self.ran and self.returncode == 0


def have_coqc() -> bool:
    # Rocq 9.x rebrand: the compiler `coqc` became `rocq compile`. Accept either,
    # so the capability gate is true whenever a real compiler exists.
    return shutil.which("coqc") is not None or shutil.which("rocq") is not None


def have_rocqchk() -> bool:
    # Rocq renamed coqchk -> rocqchk; accept either as the audit tool.
    return shutil.which("rocqchk") is not None or shutil.which("coqchk") is not None


def _audit_binary() -> str | None:
    return shutil.which("rocqchk") or shutil.which("coqchk")


def coqc_compile(v_file: str, stdlib_dir: str, extra_R: list[tuple[str, str]] | None = None) -> KernelResult:
    """Compile a .v file against the pinned stdlib plane.

    Mirrors the spec's canonical invocation:
        coqc -R <stdlib_dir> Top <v_file>
    Additional `-R dir Name` mappings (e.g. the formalizer dir) may be appended.
    Returns DEPENDENCY_UNMET (available=False) if coqc is absent -- never a pass.
    """
    if shutil.which("coqc"):
        cmd = ["coqc", "-R", stdlib_dir, LOGICAL_ROOT]
    elif shutil.which("rocq"):
        # Rocq 9.x: `coqc <args>` -> `rocq compile <args>`.
        cmd = ["rocq", "compile", "-R", stdlib_dir, LOGICAL_ROOT]
    else:
        return KernelResult(available=False)
    for d, name in (extra_R or []):
        cmd += ["-R", d, name]
    cmd += [v_file]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return KernelResult(available=True, returncode=proc.returncode,
                        stdout=proc.stdout, stderr=proc.stderr, cmd=cmd)


def print_assumptions(solution_v: str, theorem: str, stdlib_dir: str,
                      extra_R: list[tuple[str, str]] | None = None) -> KernelResult:
    """Axiom audit via Rocq's `Print Assumptions <theorem>.`

    The correct way to detect an `Admitted` escape hatch or an unauthorized axiom
    on a single constant. (`rocqchk -o`/`--output-context` operates on whole
    modules, not a constant qualid, so it cannot decide this -- which is why the
    earlier wiring silently passed an Admitted cheat.) We copy the prover's
    solution to a sibling temp file (identical load path), append
    `Print Assumptions <theorem>.`, and compile it. A fully discharged Qed proof
    prints CLEAN_TOKEN; an Admitted/axiom-backed proof prints an `Axioms:`
    listing. Returns the real compiler output; available=False if no compiler
    exists -- never a fabricated verdict.
    """
    import os
    import tempfile
    if not have_coqc():
        return KernelResult(available=False)
    parent = os.path.dirname(os.path.abspath(solution_v)) or "."
    with open(solution_v) as f:
        src = f.read()
    fd, probe = tempfile.mkstemp(suffix=".v", prefix="_audit_", dir=parent)
    try:
        with os.fdopen(fd, "w") as f:
            f.write(src)
            f.write(f"\nPrint Assumptions {theorem}.\n")
        return coqc_compile(probe, stdlib_dir, extra_R)
    finally:
        stem = probe[:-2]  # strip ".v"
        for p in (probe, stem + ".vo", stem + ".vos", stem + ".vok", stem + ".glob"):
            try:
                os.remove(p)
            except OSError:
                pass


def audit_has_leak(audit_output: str) -> bool:
    """True if the Print Assumptions output is NOT the clean banner -- i.e. it
    lists axioms (an `Admitted` obligation appears as an axiom). Robust to the
    constant-name listing form, where the only stable token is the `Axioms:`
    header / the absence of the clean banner."""
    if CLEAN_TOKEN in audit_output:
        return False
    return any(tok in audit_output for tok in LEAK_TOKENS)
