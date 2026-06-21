# lace-workflow — validating `lace-architecture-report.md` with `creusot-monitoring`

How to point the **`creusot-monitoring`** loop (see `config/skills/creusot-monitoring/SKILL.md`,
driving `creusot-sl` per file) at the cloned **`lace/`** tree to (a) **check that the claims
in `lace-architecture-report.md` actually hold in the code**, and (b) **shrink the exploitable
attack surface** by formally proving as many `*.rs` as possible — prioritising the parsers of
**untrusted boot-time input**.

> Lace is a UEFI bootloader framework: it runs before the OS, with no sandbox, and parses
> data it does not control (a PE on the ESP, a `grub.cfg` on any disk, SMBIOS/EDID/ACPI from
> firmware/peripherals). A panic, integer overflow, or out-of-bounds read in those parsers is a
> pre-OS, pre-Secure-Boot-measurement bug. **Proving those parsers total (panic/overflow/OOB-free
> for *any* input) is the highest-value verification we can do** — and it is exactly what Creusot
> is good at, because `lace-util` is pure `no_std` zero-copy parsing.

---

## 1. Mission, bounds, and the one rule that makes it sound

**Mission (to the coordinator):** *"Analyze the crate `lace-util` (then `lace-platform`'s pure
parsers) in directory `lace/`. Validate each code-level claim in
`lace-architecture-report.md`, and prove panic/overflow/out-of-bounds freedom on every function
that consumes untrusted input. Maximise the number of input-facing functions proven robust."*

- **Upper bound `U` (guidance):** the claims in `lace-architecture-report.md` **plus** the
  property *"a parser must not panic, overflow, or read out of bounds for **any** `&[u8]`."*
  Behavioural/firmware claims (TPM PCR-12 measurement, Secure-Boot/SBAT, EFI handover) are
  **out of Creusot scope** — flag them, do not pretend to verify them.
- **Lower bound `L` (ground truth):** `cargo creusot` discharge for the Pearlite-specced
  functions, supplemented by static checks (`rg`, `clippy`, `cargo-geiger`) for structural
  claims (see §4).

**The load-bearing rule — no input-restricting preconditions.** For attack-surface work the
spec must cover the **full adversarial input domain**. A function proven *"no panic **if** the
header is well-formed"* is worthless here — malformed input is the whole point. So:

> **Gate C (security):** a robustness proof's only admissible `#[requires]` are *structural*
> ones the type system already implies (e.g. "the slice is a valid `&[u8]`"). A `#[requires]`
> that assumes well-formedness, a minimum length the parser is *supposed to check itself*, or
> excludes a byte pattern is a **vacuous/under-domained spec** → the monitor REJECTS it.

This is the `creusot-monitoring` "coherent-and-wrong" guard specialised to security: the
dominant failure is a green proof that quietly assumed the attacker away.

## 2. What Creusot can and cannot reach in Lace (honest scope)

| Area | Creusot-amenable? | Why |
|---|---|---|
| `lace-util` parsers (`peimage`, `smbios`, `edid`, `chid*`, `grub`, `bls`, `acpi`, `elf64`, `sha1`, `Guid`) | **Yes — priority 1** | pure `no_std`, zero-copy, `&[u8]`→view; the attack surface; few/no deps |
| `lace-platform` partition parsers (`fs/gpt.rs`, `fs/mbr.rs`) | **Yes — priority 2** | pure `zerocopy` parsing of untrusted disk structures |
| `lace-platform` PE loader / W^X (`efi/image.rs`) | **Partly** | the PE-attribute logic is checkable; the protocol re-install (FFI) is not |
| `lace-platform` firmware glue (`efi/*`, `bios/*`, FFI, `uefi`/`uefi-raw`) | **No (in place)** | depends on the `uefi` crate + raw FFI + firmware state Creusot can't model |
| `lace-stubble` / `lace-speedboot` top-level boot flow | **Mostly no** | dominated by firmware calls; their *parsing* is already in `lace-util` |
| host tools (`pewrap`, `collect-hwids`, …) | Out of mission | `std` host code, not the boot-time attack surface |

**Consequence:** the workflow concentrates Creusot on `lace-util` + the two partition parsers —
which is *both* the most verifiable code *and* the actual untrusted-input attack surface. The
unverifiable firmware boundary is handled by static evidence (§4), not pretended away.

## 3. Attack-surface schedule (what the scheduler orders first)

The `creusot-monitoring` scheduler builds the call graph and orders **leaf-first**, but here it
also **ranks by input-exposure** so the highest-risk parsers are proven first and coverage is
reported as *fraction of the untrusted-input surface proven robust*:

1. **Disk/ESP-supplied (attacker with a USB stick):** `peimage.rs`, `fs/gpt.rs`, `fs/mbr.rs`,
   `grub.rs`, `bls.rs` — and `chid_mapping.rs` (parses the `.hwids` PE section).
2. **Peripheral-supplied (malicious monitor/firmware):** `edid.rs`, `smbios.rs`, `acpi/*`,
   `elf64.rs`.
3. **Derived/internal:** `chid.rs`/`chid_matcher.rs`, `sha1.rs`, `Guid`/byte helpers in `lib.rs`.

Within each file, order functions leaf-first (helpers before the public `parse_*`), propagating
each proven helper postcondition into its callers — exactly the loop's bottom-up rule.

## 4. The claims matrix — how each report claim is validated

Split the report's claims by what can actually establish them; only the first row is the
`creusot-sl` job.

| Claim (from `lace-architecture-report.md`) | Verifier (`L`) | Verdict bucket |
|---|---|---|
| "zero-copy parsers do **explicit bounds checks** / no panic / no overflow" (peimage, smbios, chid, …) | **creusot-sl**: prove total robustness on each `parse_*` | VALIDATED / REFUTED |
| "parsers return **borrowed views**, no allocation" | creusot-sl signatures + `rg` for `alloc`/`Vec` in the parse path | VALIDATED / REFUTED |
| "`compute_chid` implements Microsoft CHID / RFC 9562 v5 (SHA-1 over namespace)" | creusot-sl functional `#[ensures]` against a reference vector in `testdata/` | VALIDATED / PARTIAL |
| "GRUB parser handles only a documented subset" (no var-expansion, etc.) | read + the parser's own tests; not a safety property | DOCUMENTED |
| "`unsafe` concentrated at the boundary (~77 platform / 0 speedboot)" | **static**: `rg -c 'unsafe'` per crate (reproduce the counts) | VALIDATED (static) |
| "ACPI's only physical-memory access is a caller `deref` closure" | **static**: `rg 'unsafe'`/pointer reads in `acpi/` | VALIDATED (static) |
| "PE loader enforces **W^X**, rejects misaligned images" | creusot-sl on the attribute-derivation fn + read of the reject paths | PARTIAL |
| "measured boot (TPM PCR-12), Secure-Boot SBAT, EFI handover" | **out of Creusot scope** | UNVERIFIABLE-here → route |

Every VALIDATED row must cite the proven file/obligation; every REFUTED row is a real finding
(§7). UNVERIFIABLE rows are routed, never silently passed (`sl-monitoring-sl` honesty rule).

## 5. The loop, specialised (per file)

Reuses `creusot-sl` unchanged except for the security Gate C of §1.

1. **Coordinator** delegates a file (ranked per §3) with the guidance + the specific report
   claims that touch it.
2. **`creusot-sl` sub-agent** copies the function(s) into a Creusot project (§6), adds Pearlite
   specs that state **(i) total robustness** (`#[ensures]` the function returns `Ok`/`Err` for
   all inputs, never panics — i.e. discharge every implicit panic/overflow/index VC with **no
   input-restricting `#[requires]`**) and **(ii) the claimed functional property** where the
   report asserts one (e.g. a length/Field equality). Runs `cargo creusot`.
3. **Monitor** runs two gates: the **faithfulness gate** (`monitor-check.sh`: the annotated code
   strips back to the original Lace source — we are *verifying Lace, not rewriting it*) **and
   the security Gate C** (reject any `#[requires]` that narrows the input domain; a robustness
   proof that needed one is downgraded to PARTIAL with the assumption recorded as a *caveat*).
4. **Verdict** per function: **ROBUST** (all panic/overflow/OOB VCs discharged for all inputs),
   **PARTIAL** (proven only under a recorded assumption — a residual risk), **REFUTED** (a real
   panic/overflow/OOB the prover exhibits — a bug), **BLOCKED** (Creusot can't model it — FFI/dep).
5. **Capitalize** robust-parser Pearlite idioms into `config/skills/creusot/references/`; route
   findings (§7). Commit per batch.

## 6. Getting Lace into a Creusot-checkable form

Lace can't be compiled by `cargo creusot` in place (it targets `x86_64-unknown-uefi`, depends on
`uefi`/`zerocopy`/`fdt`). So each sub-agent works in an **isolated harness**:

- `cargo creusot new` a scratch project under `$HOME` (per the existing run's convention).
- Copy the **pure function(s) and their `#[repr(C)]` structs** under test into it, replacing
  `zerocopy` reads with equivalent explicit `&[u8]` indexing + `creusot_std` where needed (or
  add `extern_spec!` for the few `zerocopy`/`core` calls — and **flag any `extern_spec!` as a
  trusted assumption**, since an over-strong extern spec is the second coherent-and-wrong here).
- Keep the executable logic byte-faithful to the Lace source (the faithfulness gate compares
  back against the original); only specs/imports are added.
- Where a function is too entangled with `zerocopy`/`fdt` to isolate cleanly, record **BLOCKED**
  and route a `getting-better/` note — do not fabricate a stripped-down version and call it proven.

## 7. Outputs

- **`lace/CLAIMS-VALIDATION.md`** (or under this repo) — the §4 matrix filled in: each claim
  VALIDATED / PARTIAL / REFUTED / DOCUMENTED / UNVERIFIABLE-here, each with its evidence
  (proven obligation, static count, or "out of scope").
- **`lace/ATTACK-SURFACE.md`** — the coverage metric: *N of M untrusted-input functions proven
  ROBUST*, broken down by file and input source (§3), with the residual (PARTIAL/BLOCKED)
  functions listed as the *remaining* attack surface.
- **`bugs-to-report/`** — every REFUTED claim and every actual panic/overflow/OOB found, with a
  minimal adversarial input (these are real, file-upstream-able security findings).
- **`getting-better/`** — Creusot gaps that blocked verification (e.g. "can't model `zerocopy`
  `ref_from_prefix`"), so the unverified surface is honest and actionable.

## 8. Running it

Drive it the same way as the `use-creusot` corpus run — either:
- **as a sub-agent:** invoke `creusot-monitoring` (one `Agent` call; it fans out `creusot-sl`
  sub-agents in batches of ~10 over the §3-ranked queue, monitor-gates, commits per batch); or
- **as a Workflow** (`workflow.md`): pass the ranked file list as `args.files`, pipeline
  `prove → security+faithfulness gate → committer`, budget-capped.

Queue = the `lace-util` `*.rs` plus `fs/gpt.rs`, `fs/mbr.rs`, ordered per §3. Each batch commits
the proofs + updates `ATTACK-SURFACE.md`/`CLAIMS-VALIDATION.md`.

## 9. What this does — and does not — establish (read before trusting the result)

- **What a ROBUST verdict buys:** that specific parser provably cannot panic / overflow / read
  OOB on *any* input — a hard guarantee that removes that function from the exploitable surface.
- **It validates code-level claims only.** "Memory-safe parsing" yes; "Secure Boot is enforced",
  "the kernel handed off is the right one", "TPM measurement is correct" — **no**; those are
  routed UNVERIFIABLE-here and need integration tests / audit, not Creusot.
- **The `unsafe` firmware boundary is not verified by this loop.** Reducing the *safe-Rust*
  parser surface is real and valuable, but the ~77 `unsafe` sites in `lace-platform` remain a
  separate audit target; the workflow *measures* that boundary (static counts) rather than
  proving it.
- **Trusted assumptions are part of the result.** Any `extern_spec!` for `zerocopy`/`core`, any
  PARTIAL proof's recorded `#[requires]`, and any BLOCKED function are the trust base — listed
  explicitly in `ATTACK-SURFACE.md`. An honest "we proved 23/31 input parsers robust, under
  these 4 trusted extern-specs, with 8 blocked" is the deliverable, **not** "Lace is verified."

This is the `creusot-monitoring` loop calibrated for a security audit: ground truth is
`cargo creusot`, the upper bound is the report's claims + total-robustness, the dominant
coherent-and-wrong (a proof that assumed the attacker away) is gated out, and the honest
residual — what stayed PARTIAL, BLOCKED, or out-of-scope — *is* the remaining attack surface.
