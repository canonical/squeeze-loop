"""Mutation synthesis helpers (sentinel-side) for the Rocq squeeze runner.

Mirrors the role of src/A's runner/mutations.py: the catalogue of negative
challenges lives WITH the runner, not with either band. The exerciser only
*names* a mutation (and ships a .v for it); the implementer is blind to all of
this.

For Rocq the "mutation value" is a kernel verdict, not a number: a FALSE mutation
is caught iff `coqc` REJECTS its .v (nonzero exit). This module resolves the .v
source for a mutation entry -- either the exerciser's shipped `mutation_file`, or
a synthesized fallback from the `mutated_theorem_statement` (the contract's
documented synthesis: `<stmt>\nProof. intros. reflexivity. Qed.`) -- and hands it
to the capability-gated kernel. It NEVER fabricates a verdict.
"""

import tempfile
from pathlib import Path

# Synthesis template from shared/contract.md: a naive discharge that can only
# succeed if the (false) statement were actually provable by reflexivity.
SYNTH_TEMPLATE = "{stmt}\nProof. intros. reflexivity. Qed.\n"


def resolve_mutation_source(mut: dict, mutation_dir: Path) -> tuple[Path, bool]:
    """Return (path_to_v, is_temp).

    Prefer the exerciser's shipped `mutation_file` if it exists; otherwise
    synthesize a temp .v from `mutated_theorem_statement` per the contract.
    """
    mfile = mut.get("mutation_file")
    if mfile:
        p = mutation_dir / mfile
        if p.exists():
            return p, False
    stmt = mut["mutated_theorem_statement"]
    src = SYNTH_TEMPLATE.format(stmt=stmt)
    tf = tempfile.NamedTemporaryFile("w", suffix=".v", delete=False)
    tf.write(src)
    tf.close()
    return Path(tf.name), True


def compile_mutation(kernel, mut: dict, mutation_dir: Path, stdlib_dir: str):
    """Compile a mutation's .v through the capability-gated kernel.

    Returns the KernelResult (with `.available` False if Rocq is absent). The
    caller enforces catchability: for a FAIL mutation, `.ok` True == trap sprung.
    """
    path, is_temp = resolve_mutation_source(mut, mutation_dir)
    try:
        return kernel.coqc_compile(str(path), stdlib_dir)
    finally:
        if is_temp:
            try:
                path.unlink()
            except OSError:
                pass
