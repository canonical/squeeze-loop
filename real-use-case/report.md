# Report — verifying a Rust corpus with Creusot, driven by nested Squeeze Loops

**Date:** 2026-06-16
**Repo:** `use-creusot`
**Outcome:** Creusot installed and verified; a 241-file Rust corpus prepared; a two-level
Squeeze-Loop apparatus designed, committed, and then **run to completion unsupervised** —
every file analysed, **74 proved** with `cargo creusot`, all committed.

---

## 1. Executive summary

Starting from an empty repo with only `opam` present, this session:

1. **Installed Creusot** (the deductive verifier: Rust → Coma → Why3 → SMT) end-to-end and
   confirmed it proves a real spec.
2. **Built a clean Rust corpus** — copied Creusot's own test suite, **stripped all 289
   files of their Creusot annotations** with a `syn`-based tool, kept the 241 that compile
   as plain Rust, and added a `make check` harness.
3. **Designed a Squeeze-Loop (SL) system** to *re-annotate and prove* that corpus:
   - `creusot-sl` — verifies **one file** (annotate with Pearlite + prove).
   - `creusot-monitoring` — drives `creusot-sl` across the **whole crate**, monitoring it.
   - plus four generic methodology skills (`sl-builder`, `sl-internal`, `sl-monitoring-sl`,
     `sl-auditor`).
4. **Ran `creusot-monitoring` unsupervised** as a single sub-agent that fanned out
   `creusot-sl` sub-sub-agents in batches of 10, monitor-gated each, and committed every
   batch — clearing all **241 files** with no human "continue" between batches.

**Final verdicts:** PROVED 74 · PARTIAL 8 · FAILED 6 · TRIVIAL 153 (241/241). The whole run
is captured in **39 git commits** (`31636fd` … `117bac8`).

---

## 2. Environment setup

- Installed Rust (`rustup`, stable 1.96.0) and cloned `creusot-rs/creusot`; ran its
  `./INSTALL`, which built a local opam switch, Why3 1.8.2+git, why3find, and the provers
  **Alt-Ergo 2.6.2 / Z3 4.15.3 / CVC4 1.8 / CVC5 1.3.1**, pinned to nightly-2026-04-21.
- **Smoke test:** a spec'd `add_one` (`#[requires]`/`#[ensures]`) proved end-to-end
  (`Proved … ✔`), confirming the full Rust→Why3→SMT pipeline.

## 3. The corpus

- Copied Creusot's `tests` into `training-data/` (289 `.rs` files), then **stripped every
  Creusot construct** with a purpose-built `syn` tool (`/tmp/strip-creusot`): contract
  attributes, `#[logic]`/`#[predicate]`/`#[law]` items, `Invariant`/`View`/`DeepModel`
  impls, `proof_assert!`/`ghost!`/`snapshot!`/`pearlite!`/`extern_spec!` macros, and
  `creusot_std` imports — with a **re-parse safety net** (write back only if still valid
  Rust). `Ghost<T>`/`Snapshot<T>` were unwrapped to their inner types.
- Compile-checked each file as a library crate (`compile-check.sh` + `Makefile`):
  **241 / 289 compiled**; the 48 that referenced Creusot-only library items were removed.
- Result: a clean **plain-Rust corpus of 241 files**, committed at `31636fd`.

## 4. The Squeeze-Loop design

Committed at `d18a698`. A Squeeze Loop pins every actor between a **soft upper bound `U`**
and a **hard, executable lower bound `L`**, behind **physical barriers**, with
**gate-defined done** — so the loop converges on *correct* output, not *plausible-looking*
output. The dominant failure it targets is **coherent-and-wrong** (fluent but false).

- **`creusot-sl`** (`creusot-sl.md`): per-file loop. `U` = the requirement made precise as
  Pearlite; `L` = `cargo creusot` discharge + tests + a **mutation probe**. Cast:
  coordinator, spec author, annotator, verifier, probe — disjoint `(U,L)` pairs, physical
  barriers, gates A/B/C/S, and Gate-S-gated knowledge capitalization into
  `config/skills/creusot/`.
- **`creusot-monitoring`** (`config/skills/creusot-monitoring/`): per-crate loop that
  *monitors* `creusot-sl` (the `sl-monitoring-sl` meta-pattern). `U` = the mission
  guidance; `L` (ground truth) = the `creusot-sl` loop's own verdicts. Schedules files
  leaf-first, drives a `creusot-sl` per file, audits its soft outputs, routes tooling gaps
  to `getting-better/` and bugs to `bugs-to-report/`, capitalizes into
  `config/skills/creusot-monitoring/`.
- A key principle was added to `sl-monitoring-sl` mid-session (`3317a87`): **the monitor
  must launch the observed loop as a sub-agent** — the delegation boundary makes the
  author-separation barrier *physical* (only returned soft outputs cross back, never the
  base loop's rationale) and keeps the monitor's context bounded so it scales.

## 5. Running `creusot-monitoring` unsupervised

The loop was invoked as **one sub-agent** that itself spawned `creusot-sl`
**sub-sub-agents** — the two-level architecture verified earlier (a probe confirmed
sub-agents *can* spawn sub-agents in this harness). This kept the heavy proof work in
isolated leaf contexts; only short verdicts returned to the coordinator, and only three
coordinator summaries returned to the main thread.

The run spanned **three sub-agent invocations** (one died on a transient API 500 after
~59 min but had already committed its batches; the others completed cleanly), processing
**20 batches of 10** plus fast-pathed trivial stubs:

| Stage | Files | Notes |
|---|---|---|
| Seed + batches 1–5 | 92 | batch 1 monitor **caught 8 fabrications** → self-corrected (faithfulness gate + stub fast-path + anti-fabrication prompt) |
| Batches 6–11 | +60 | zero fabrications; faithful `vec!` fix discovered |
| Batches 12–20 | +89 | **queue emptied** |

Per batch the coordinator: computed the queue from the verdict log, fast-pathed
no-op/stub files to TRIVIAL, fanned out 10 `creusot-sl` agents, ran the **monitor
faithfulness gate** (`monitor-check.sh`: stripping annotations must reproduce the original
code) on every PROVED, reverted any FABRICATED, committed the batch, and capitalized
Gate-S-passed heuristics.

## 6. Results

**241 / 241 files, queue = 0:**

| Verdict | Count | Meaning |
|---|---|---|
| ✅ PROVED | **74** | real `cargo creusot` discharge, faithfulness-gated, no escape hatches |
| ◐ PARTIAL | 8 | all real functions proved; blocked by `panic!()`/`println!`/`main` stubs |
| ✗ FAILED | 6 | genuinely unclosable without a forbidden `#[trusted]` |
| ▫️ TRIVIAL | 153 | no-op/stub/empty — nothing to verify |

- **39 git commits**, 37 of them `creusot-monitoring` batch/capitalize commits.
- **Zero fabrications survived** — the monitor caught and reverted every one (8 in batch 1,
  plus `100doors`, `bug/1312` later).
- Full per-file table in `annotate/VERDICTS.md`; machine log in `annotate/.verdicts.tsv`.

## 7. Knowledge the loop produced

The loop didn't just emit verdicts — it **capitalized reusable knowledge**, Gate-S-gated:

- **39 annotator heuristics** in `config/skills/creusot/references/learned-annotator.md`,
  e.g.: pair `#[variant]` with `#[check(terminates)]` (a bare variant is silently ignored);
  `#[bitwise_proof]` for SWAR/bitmask overflow; recursive-ADT models via `#[logic]`
  recursion on `self` (not `Box::view`); generic `FnMut`/`FnOnce` precondition
  re-establishment with *fresh-state* quantification; `&mut`-prophecy patterns
  (`*`/`^`/`old`); the faithful `vec!` fix `use creusot_std::prelude::{vec, *}`.
- **Monitor/coordinator heuristics** in `config/skills/creusot-monitoring/references/`,
  e.g. "trivial stubs invite fabricated proofs — fast-path them"; "the faithfulness gate is
  line-oriented, so formatting-altering annotations FABRICATE".

**Routed findings (surprises routed, never absorbed):**
- `getting-better/` — **8 feature suggestions**: `#[variant]` silently ignored without
  `#[check(terminates)]`; `derive(Clone)`/`vec!` prelude-glob ambiguities; `println!`-in-
  `main` blocks crate translation; polymorphic-recursion termination; doubly-existential
  `Filter::produces` intractable; illegal-recursive-type rejection; tree-height overflow
  over a non-`WellFounded` private-field ADT.
- `bugs-to-report/` — **1 bug**: `cargo creusot new/init` silently skips `why3find.json`
  inside a Cargo workspace.

## 8. Honest limitations

The 6 FAILED and 8 PARTIAL are **real limits, recorded — not forced**:
- **PARTIAL:** all functions proved, but an irreducible `random(){panic!()}` stub called
  live, or a `println!`/`main` that Creusot can't translate, blocks the *crate-level*
  verdict (`rusthorn/inc_some_*`, `filter_positive`, `bitvectors/{popcount,bitwalker}`).
- **FAILED:** `specification/trusted` (illegal recursive type — rejected at translation),
  `syntax/10_mutual_rec_types` (tree-height overflow over a non-`WellFounded` Box-nested
  mutual-recursive ADT), `bug/874`/`100doors`/`bug/1312` (macro-ambiguity/formatting cases
  not faithfully annotatable in place).

Each was routed or documented rather than closed with `#[trusted]`/`assume!`. That
restraint — **loud-fail, never an approximation** — is the loop working as designed.

## 9. Architecture lessons

- **Two-level sub-agents preserve context and scale.** `main → creusot-monitoring (agent)
  → creusot-sl (sub-agents)`: the coordinator's window only accrues small summaries; the
  proof work lives in leaf contexts. This is also a *barrier* — the monitor structurally
  cannot see a base agent's rationale, only its returned soft outputs.
- **The monitor is the load-bearing piece.** Without it, batch 1's fabrications would have
  shipped as green proofs. The faithfulness gate (strip ⇒ must equal original) made
  "coherent-and-wrong" mechanically catchable, unattended.
- **No MCP server was used** — the Creusot oracle was invoked via `Bash` (`cargo creusot`).
  An MCP server (a typed `creusot_prove` tool + shared verdict/queue/skill resources) would
  standardise the oracle and erase the environment foot-guns hit here, but wasn't required.

## 10. Artifacts

| Path | What |
|---|---|
| `creusot-sl.md` | per-file loop spec |
| `config/skills/creusot-monitoring/` | per-crate loop + learned files + getting-better/ + bugs-to-report/ |
| `config/skills/creusot/` | Pearlite reference + learned annotator/role files |
| `config/skills/sl-*` | generic SL methodology |
| `annotate/` | the 241 files, now annotated/proved (with `VERDICTS.md`, `.verdicts.tsv`) |
| `training-data/` | the stripped plain-Rust corpus (faithfulness oracle) |
| `Makefile`, `compile-check.sh`, `monitor-check.sh`, `gen-verdicts.sh` | tooling |
| `README.md`, `workflow.md` | overview + how to run the loop as a Workflow |

**Reproduce / continue:** `cargo creusot version` (toolchain); `make check` (corpus
compiles); the verdict log is the source of truth, so re-invoking `creusot-monitoring`
resumes from any unprocessed files automatically.
