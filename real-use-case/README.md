# use-creusot — verifying Rust with Creusot, driven by Squeeze Loops

This repo holds a methodology for verifying Rust with **[Creusot](https://github.com/creusot-rs/creusot)**
(the deductive verifier that translates Rust to the Why3 platform and discharges
proof obligations with SMT solvers), organized as two nested **Squeeze Loops**:

- **`creusot-sl`** — verifies **one `*.rs` file**: it annotates the code with Pearlite
  contracts and proves them with Creusot.
- **`creusot-monitoring`** — verifies a **whole crate**: it schedules the files
  leaf-first and drives a `creusot-sl` sub-loop on each, while *monitoring* what those
  sub-loops do.

> A **Squeeze Loop (SL)** is a multi-agent workflow that converges on a *genuinely
> correct* result instead of a *plausible-looking* one. Every actor is pinned between
> an **upper bound `U`** (a soft, citable authority — the strongest claim it may make)
> and a **lower bound `L`** (a hard, executable oracle whose verdict it can't alter).
> The load-bearing rule is **disjointness**: each actor answers to a *different*
> `(U,L)` pair behind *physical* barriers, so no actor certifies its own work and every
> blind spot is caught by someone who can't share it. "Done" is decided by machine
> gates, never self-report. Full theory: [`config/skills/sl-internal/SKILL.md`](config/skills/sl-internal/SKILL.md).

---

## `creusot-sl` — verify a single file

Full spec: **[`creusot-sl.md`](creusot-sl.md)**.

It takes existing Rust (the implementation is a fixed input) and decides whether it
provably satisfies a specification authored *independently of the code's body*.

- **Bounds.** `U` = an external requirement made precise as **Pearlite** contracts
  (`#[requires]`/`#[ensures]`/`#[invariant]`/`#[variant]`); `L` = `cargo creusot`
  (Creusot → Coma → Why3 → SMT) discharging every obligation, plus `cargo test` and a
  **mutation probe** (perturb the code → the proof *must* break).
- **Cast** (canonical, disjoint `(U,L)` pairs, physical barriers):

  | Role | Builds | Barrier |
  |---|---|---|
  | **Coordinator** | Gate-A approvals, sequencing, gap docs, DONE verdicts | judges vs `U`, never edits artifacts |
  | **Spec author** | the Pearlite contracts (from the requirement) | ⊥ implementation |
  | **Annotator** | proof scaffolding: invariants, ghost, `proof_assert!` | ⊥ acceptance evidence |
  | **Verifier** | adversarial properties + mutation probes; runs the oracle | ⊥ implementation + diff |
  | **Probe** | minimal Creusot/Why3 capability experiments | — |

- **Gates.** A (editorial: contracts vs requirement) → B (machine: all VCs discharge,
  no `#[trusted]`/`assume!` escape hatches) → C (non-vacuity / mutation probe / no
  plane-blend) → S (audit any learned heuristic).
- **Capitalization.** After a file is DONE, each role distills a reusable heuristic,
  Gate-S-audited by a disjoint monitor, into per-role files under
  [`config/skills/creusot/references/`](config/skills/creusot/references/) — so the next
  file starts smarter without crossing a barrier.
- A lighter **3-agent variant** (summarize → specify → prove) is kept as an appendix
  for when no external requirement exists (a self-consistency check only).

Pearlite/annotation reference: **[`config/skills/creusot/SKILL.md`](config/skills/creusot/SKILL.md)**.

---

## `creusot-monitoring` — verify a whole crate (a loop monitoring a loop)

Full spec: **[`config/skills/creusot-monitoring/SKILL.md`](config/skills/creusot-monitoring/SKILL.md)**.

Given a mission like *"analyze the crate `xxx` in directory `yyy`"* plus **guidance**
(e.g. *"specify thoroughly the Rust file but disregard network access"*), it:

1. **Schedules** the files **leaf-first** (topological order of the call/module graph),
   propagating each proven callee `#[ensures]` up as the caller's `#[requires]`.
2. **Drives** a full `creusot-sl` sub-loop on each file, threading the guidance in.
3. **Monitors** `creusot-sl` (the [`sl-monitoring-sl`](config/skills/sl-monitoring-sl/SKILL.md)
   meta-pattern): it squeezes the base loop's *soft outputs* — its learned skills and
   inferred contracts — and returns **PASS / CARVE-OUT / REJECT**.

- **Bounds.** `U` = the **mission guidance** (the soft authority on *what / how much* to
  verify); `L` = **the `creusot-sl` loop itself** — its machine verdicts are the ground
  truth the monitor reads but can't alter.
- **Why the monitor exists.** The dominant failure is a crate that *looks* verified
  (every file went green) but where the base loop **strengthened a contract for local
  convenience that is globally or guidance-wrong** — e.g. specified network behaviour
  the guidance said to disregard. The monitor holds the guidance + the cross-unit oracle
  (a *disjoint* base from the agents that produced the contract), so it can catch this.
- **Routing — surprises are routed, never absorbed.** Confirmed tooling gaps →
  [`config/skills/creusot-monitoring/getting-better/`](config/skills/creusot-monitoring/getting-better/)
  (feature suggestions); confirmed bugs →
  [`config/skills/creusot-monitoring/bugs-to-report/`](config/skills/creusot-monitoring/bugs-to-report/).
  Filenames: `YYYYMMDD-hhmm-simple-name.md` (e.g. `20260616-1547-handle-reference.md`).
- **Capitalization.** Top-agent heuristics (coordinator / scheduler / monitor) accrue,
  Gate-S-gated, under
  [`config/skills/creusot-monitoring/references/`](config/skills/creusot-monitoring/references/).

---

## How they fit together

```
creusot-monitoring   (per crate; U = mission guidance, L = creusot-sl verdicts)
│
├── schedule files leaf-first  ──►  for each file:
│        creusot-sl            (per file; U = requirement→Pearlite, L = cargo creusot)
│        coordinator · spec author · annotator · verifier · probe
│        gates A → B → C → S        ──►  file DONE / gap-N
│
├── base-SL monitor: audit creusot-sl's learned skills + inferred contracts
│        ──►  PASS / CARVE-OUT / REJECT
│
└── route surprises  ──►  getting-better/ (features)   bugs-to-report/ (bugs)
```

Both loops are designed with **[`sl-builder`](config/skills/sl-builder/SKILL.md)** and
can be audited with **[`sl-auditor`](config/skills/sl-auditor/SKILL.md)**.

---

## Repository layout

```
creusot-sl.md                      base loop spec (verify one file)
config/skills/
  creusot/                         Pearlite reference + base-loop learned files
  creusot-monitoring/              top loop spec + learned files + getting-better/ + bugs-to-report/
  sl-builder, sl-internal,         generic Squeeze Loop methodology
  sl-monitoring-sl, sl-auditor
training-data/                     241 Creusot-stripped Rust files that all type-check
Makefile, compile-check.sh         `make check` — compile every corpus file as a lib crate
```

`.claude/skills` is a symlink to `config/skills/`, which wires these skills into the
Claude Code harness.

## Status

- **Creusot is installed and verified** end-to-end (`cargo creusot version` for the
  toolchain; a spec'd `add_one` proved during setup).
- **`training-data/`** is a clean plain-Rust corpus — run `make check` to confirm all
  241 files compile.
- **The two loops are specifications** (documents + skills), not yet an automated
  runner. They define the roles, bounds, barriers, gates, and capitalization an
  orchestrator (human or agent harness) should follow to verify Rust with Creusot.
