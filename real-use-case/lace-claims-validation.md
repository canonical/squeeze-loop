# Lace — claims-validation matrix

*Produced 2026-06-17 by `creusot-monitoring`. Fills in `lace-workflow.md` §4. Each claim from
`lace-architecture-report.md` is bucketed VALIDATED / PARTIAL / REFUTED / DOCUMENTED /
UNVERIFIABLE-here, with evidence (a proven obligation, a static count, or "out of Creusot scope").
Honesty note: functional claims extracted from the implementation are an **endogenous** upper
bound — verifying them is a self-consistency check; the **robustness** property (no panic/overflow/
OOB for any input) is exogenous and the genuinely sound result.*

| # | Claim (from architecture report) | Verifier (L) | Verdict | Evidence |
|---|---|---|---|---|
| 1 | "zero-copy parsers do **explicit bounds checks** / no panic / no overflow" (peimage, chid, gpt, mbr) | creusot-sl: prove total robustness on each `parse_*` | **PARTIAL → mostly REFUTED** | **The claim does NOT hold uniformly.** Proven robust: `chid_mapping` (both fns), `gpt::parse_gpt`, `mbr::parse_mbr`/`read_mbr_sector`, all `peimage` section helpers/iterators. **Refuted (real panics on adversarial input):** `peimage::parse_pe` (line 223 `e_lfanew-64` underflow), `peimage::relocate_into` (`align_up!` div-by-zero + mul overflow), `mbr::parse_ebr_chain` (line 128 `lba*sector_size` mul overflow). 4 bugs, all with minimal reproducers + one-line fixes. The *intent* (explicit `checked_*`/`.get()`) is real, but four raw arithmetic/slice sites escaped it. |
| 2 | "parsers return **borrowed views**, no allocation" (peimage, chid_mapping) | signatures + `rg` for `alloc`/`Vec` in parse path | **VALIDATED (static)** | `peimage`/`chid_mapping` parse paths contain no `Vec`/`alloc::` (only the `#[cfg(test)]` builders and the `#[cfg(feature="std")]` serialize path do). `PeRef`/`ChidMapping` borrow `&'a`/`&'s` the source buffer. (`gpt`/`mbr` *do* allocate a `Vec<…Partition>` by design — they read from a device, not a borrowed slice; report does not claim otherwise.) |
| 3 | "`compute_chid` implements Microsoft CHID / RFC 9562 v5 (SHA-1 over namespace)" | functional `#[ensures]` vs a reference vector | **ROBUSTNESS VALIDATED / FUNCTIONAL UNVERIFIED-here (priority-2)** | `chid.rs`/`sha1.rs` verified for *total robustness*: `compute_chid`'s shifts/digest-read/`data4[0]` index and `sha1_transform` are ROBUST; `ChidMatcher::next` ROBUST. The RFC-9562 *functional* equality (digest = SHA-1 over the UCS-2 concatenation) is **not** machine-checked: the byte-content path through `str::encode_utf16().collect()` is BLOCKED (`EncodeUtf16` lacks Creusot `IteratorSpec`) and `sha1_transform`'s crypto state-equation was treated as opaque-but-total. So: no panic/overflow on any sources (validated); bit-exact RFC conformance still rests on the in-tree reference-vector unit tests, not a proof. |
| 4 | "GRUB parser handles only a documented subset" (no var-expansion, etc.) | read + parser's own tests | **DOCUMENTED** | Confirmed by reading `grub.rs` (module docs + code): tokenizer + recursive-descent, no variable expansion / command substitution / conditionals / loops. Not a safety property. |
| 5 | "`unsafe` concentrated at the boundary (~77 platform / ~5 util / 3 stubble / 0 speedboot)" | static `rg`-count per crate | **VALIDATED (static)** | Reproduced exactly: `lace-platform` **77**, `lace-util` **5**, `lace-stubble` **3**, `lace-speedboot` **0**. |
| 6 | "ACPI's only physical-memory access is a caller `deref` closure" | static `rg 'unsafe'` / pointer reads in `acpi/` + creusot-sl on the parsers | **VALIDATED (priority-2)** | The structural claim holds: `acpi/{mod,fadt,mcfg}.rs` take `&[u8]` slices (and, for `Rsdp::find_table`, a caller-supplied `deref: impl Fn(u64,usize)->&[u8]`) — no raw pointer reads in the parse logic. All five parsers (`Rsdp::parse`, `acpi_checksum`, `find_table`, `parse_fadt_facs_addr`, `parse_mcfg`) are **ROBUST**: proven panic/overflow/OOB-free for any bytes AND any `deref` closure (a negative control confirmed the bounds checks are load-bearing). The `unsafe` truly lives only in the caller's `deref`, outside this code. |
| 7 | "PE loader enforces **W^X**, rejects misaligned images" | creusot-sl on the attribute-derivation fn + read of reject paths | **PARTIAL / REFUTED** | The misalignment path lives in `relocate_into` (`align_up!`), which is **REFUTED** — `section_alignment==0` panics (divide-by-zero) instead of being rejected, and a large `virtual_size` overflows. The W^X *attribute* logic proper is in `lace-platform/efi/image.rs` (not reached). So the "rejects misaligned images" claim is *undermined* at the alignment-arithmetic layer. |
| 8 | "measured boot (TPM PCR-12), Secure-Boot SBAT, EFI handover" | out of Creusot scope | **UNVERIFIABLE-here → routed** | Firmware/behavioural; depends on TPM/UEFI state Creusot cannot model. Flagged, not pretended. |

## New finding beyond the matrix

- **`grub::parse_submenu` unbounded native recursion (stack-overflow DoS)** on deeply-nested
  `submenu { … }` input — a real robustness hole the report's "memory-safe parsing" framing does
  not cover. Found by by-hand analysis (Creusot is BLOCKED on `grub.rs` and would not model stack
  depth regardless). Routed to `bugs-to-report/`.

## Priority-2 findings (peripheral / firmware / derived parsers — 2026-06-17)

- **EDID (malicious monitor), SMBIOS, ACPI, ELF64 parsers are robust.** `edid::parse`,
  `smbios::find_smbios_table_by_type` (+ `table`/`get_string`), all three ACPI parsers, and
  `elf64::{parse,for_each_phdr,segment_data}` are **ROBUST** — panic/overflow/OOB-free for any
  adversarial input. The architecture report's "explicit-bounds-checks / no-panic" claim **holds**
  for the entire peripheral/firmware surface (unlike the disk/ESP surface, where 4 sites lapsed).
- **`lib::hex_seq` and the `Guid::try_from_str`/`find_byte_sequence` helpers** are panic-safe;
  the latter two stay PARTIAL only on SMT-incompleteness (a `len-sub+1` add the bundled solvers
  won't close, with no counterexample) — re-proved by a `while i <= last` rewrite in the smbios harness.
- **No new fileable bugs.** The `align_up!`/`count_blocks_aligned_up!` macros are refutable in
  isolation (`bound==0` div-by-zero; `align_up!` u32 mul-overflow), but every non-test call site
  passes a constant nonzero divisor, and the mul-overflow is the already-filed ISSUE-2. The
  `sha1` `total_size*8` overflow is real only at ~2^61 bytes (unreachable). Both recorded as residuals.

## Modeling gaps surfaced (routed to getting-better/)

- **creusot-std has no `&str` iterator extern specs** (`str::lines`/`Chars`/`Peekable`, `trim`,
  `split_once`, `starts_with`, `to_string`, `encode_utf16`) → BLOCKS `bls.rs`, `grub.rs`,
  `chid::chid_sources_from_smbios_and_edid`, and `compute_chid`'s byte-content path at translation.
  The parsers are robust by construction; the gap is purely in the modeling layer.
- **creusot-std has no `div_ceil` extern spec** → `align_up!`/`count_blocks_aligned_up!` translate
  vacuously, masking the div-by-zero/overflow VCs; the annotator hand-expanded the macro to surface
  them (which is how the `relocate_into` bugs were found, and how the priority-2 `bound==0` div0
  latent hazard was confirmed).
- **creusot-std has no `impl Invariant for String`** → any `&mut String` op (`String::push`) yields
  unprovable `inv_String` goals, BLOCKING `edid::panel_id` (every *real* VC there is discharged).
- **Missing byte-buffer extern specs** (`[T;N]` range Index/IndexMut, `to_be_bytes`/`from_be_bytes`,
  `rotate_left`, `usize::try_from(u64)`, `ChunksMut` `IteratorSpec`, `TryInto`/`AsRef` through blanket
  impls) → workaroundable with totality-only specs or byte-identical rewrites, but each adds a trusted
  assumption. Routed (`20260617-1241-creusot-std-missing-byte-buffer-extern-specs.md`).
- **Coma keyword collision** (a Rust param named `begin`/`end` produces an unparseable `.coma`) and
  **slice-range-index `in_bounds` not discharged through `&mut self`** — both routed with workarounds.

## Summary

The report's **structural** claims (borrowed views, `unsafe` confined to the firmware boundary,
GRUB subset, ACPI's `deref`-closure-only memory access) are **VALIDATED**. Its central **safety**
claim ("zero-copy parsers … no panic / no overflow") is **validated for the entire
peripheral/firmware surface** (EDID, SMBIOS, ACPI, ELF64 — all ROBUST) but **only partly true for
the disk/ESP surface**: across priority-1 + priority-2, **25 input-facing functions are provably
robust**, against **four real arithmetic/slice bugs** (3 functions across `peimage` and `mbr`,
ISSUE-1..3) that panic on adversarial disk/ESP input, plus the `grub::parse_submenu` recursion DoS
(ISSUE-4). The W^X "rejects misaligned images" claim remains undermined by the `align_up!`
div-by-zero/overflow (the same `relocate_into` site). The behavioural claims (TPM/Secure-Boot/handover)
are out of scope and routed. Net: priority-2 found **no new bugs** — the firmware/peripheral parsers
are disciplined and total — leaving the four disk/ESP bugs (each a one-line fix) as the only refuted
sites, and a handful of creusot-std modeling gaps (`String`/`format!`/`&str`-iterators) as the honest
unverified residual.
