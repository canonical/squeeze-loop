# Rocq kernel (D's capability-gated oracle)

**Definition.** The only shell-out to the `coqc`/`rocqchk` binaries — D's instance of the
[ground truth](../../../../docs/glossary/ground-truth.md), the type-checker whose verdict
(compiled OK, axiom-clean, false mutation rejected) is mechanical and unalterable. It is
**capability-gated**: if Rocq is absent it prints `DEPENDENCY UNMET` (exit 3, SKIPPED) and
**never fabricates a verdict**.

The gating is the honesty discipline made executable: a missing prover yields an honest
SKIP, not a fake PASS. A proof is admissible only when this oracle accepts it *and* the
axiom audit shows it leans on no smuggled assumption.

## Sources

- `src/D/ground-truth/rocq_kernel.py` — `have_coqc()`, `coqc_compile()`,
  `print_assumptions()`, `KernelResult`; the gating logic.
- `src/D/ground-truth/gate_sentinel.py` — the three-gate referee that calls the kernel for
  Gate B (registry regression, solution compile, axiom audit, mutation catchability).
- `src/D/ground-truth/README.md` — the capability-gating / honesty section.

## See also

- [proof-registry](proof-registry.md) — the certified trunk the kernel re-checks.
- [textbook-manifest](textbook-manifest.md) — the statement the kernel verdict is about.
- [ground-truth](../../../../docs/glossary/ground-truth.md) ·
  [gates](../../../../docs/glossary/gates.md) — the shared oracle / Gate B concepts.
