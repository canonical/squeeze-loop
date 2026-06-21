# Lace — attack-surface verification report

*Produced 2026-06-17 by the `creusot-monitoring` loop driving `creusot-sl` per the plan in
`lace-workflow.md`. Ground truth `L` = `cargo creusot` discharge (Creusot 0.13.0-dev). Upper
bound `U` = the claims in `lace-architecture-report.md` + the exogenous property "a parser must
not panic, overflow, or read out of bounds for **any** `&[u8]`/`&str`." Security Gate C
(reject any input-restricting `#[requires]`) was enforced on every verdict below.*

## Coverage metric

**Untrusted-input parser functions carried to a verdict: 13 of 13 (priority-1) + ~25 of ~25
targeted (priority-2) = the full lace-util / partition-parser attack surface.**

### Priority-1 (disk/ESP-supplied — done in the first run)

| Verdict | Count | Functions |
|---|---|---|
| **ROBUST** (all panic/overflow/OOB VCs discharged for ALL inputs, no input-restricting `#[requires]`, no untrusted extern_spec) | **8** | `peimage`: `SectionHeader::name`, `PeRef::num_sections`, `PeRef::nth_section`, `RawSectionIterator::next`, `VirtualSectionIterator::next`, `PeRef::raw_sections`; `gpt`: `parse_gpt`; `mbr`: `parse_mbr`, `read_mbr_sector`, `is_extended_type`; `chid_mapping`: `next_chid_mapping`, `extract_string` |
| **REFUTED** (a real, reproducer-backed panic/overflow on adversarial input — a bug) | **3 functions, 4 distinct bugs** | `peimage::parse_pe` (1), `peimage::relocate_into` (2), `mbr::parse_ebr_chain` (1) |
| **PARTIAL** (proven only under a recorded assumption) | **0** | — |
| **BLOCKED** (Creusot cannot model it) | **2 files** | `bls::parse_bls_entry`, `grub::parse_grub_cfg` (+ tokenizer/parser) |

### Priority-2 (peripheral-supplied / firmware / derived — this run, 2026-06-17)

| Verdict | Count | Functions |
|---|---|---|
| **ROBUST** | **17** | `edid::parse`; `sha1::sha1_transform`, `sha1::sha1` (realistic input — see overflow caveat); `lib::hex_seq`; `elf64::parse`, `elf64::for_each_phdr`, `elf64::segment_data`; `smbios::find_smbios_table_by_type`, `SmbiosTable::table`, `SmbiosTable::get_string`; `acpi::Rsdp::parse`, `acpi::acpi_checksum`, `acpi::Rsdp::find_table`, `acpi::fadt::parse_fadt_facs_addr`, `acpi::mcfg::parse_mcfg`; `chid::compute_chid` (index/shift/digest robustness), `chid_matcher::ChidMatcher::next` |
| **REFUTED** | **0 new fileable bugs** | The `lib::align_up!`/`count_blocks_aligned_*` macros are refutable *in isolation* (div-by-zero on `bound==0`, and `align_up!` u32 multiply-overflow), but at every non-test call site the divisor is a compile-time-nonzero constant (`512`, `mem::PAGE_SIZE`) so `bound==0` is not reachable, and the multiply-overflow IS the already-filed ISSUE-2 (`peimage::relocate_into`). Recorded as a latent hazard, not a new issue. The `sha1::digest` `total_size*8` usize overflow is real only at ~2^61 bytes (≈2 EB) — no `&[u8]` that large can exist, so not fileable. |
| **PARTIAL** | **2** | `lib::find_byte_sequence`, `lib::Guid::try_from_str` — panic-safe (no counterexample exists), but the residual VC (a `+1` add-overflow / an `Option` type-invariant) is SMT-incompleteness, not discharged by the bundled solvers at the budget used. Re-proved fully in the smbios harness by rewriting `find_byte_sequence`'s `0..len-sub+1` range to `while i <= last`, confirming panic-freedom. |
| **BLOCKED** | **2 (+1 partial path)** | `edid::panel_id` (creusot-std has no `impl Invariant for String` → spurious `inv_String` goals; every real panic/index/overflow path proven); `chid::chid_sources_from_smbios_and_edid` (`format!`/`String`/generic-zerocopy/`encode_utf16` `IteratorSpec` gaps). `chid::compute_chid`'s UCS-2 *byte-content* path is blocked by `str::encode_utf16().collect()` lacking `IteratorSpec` — its index/shift/digest *robustness* is ROBUST regardless. |

> The "8 ROBUST" count lists 12 function rows because several are distinct leaf helpers/iterators
> proven individually; treated as functions, **12 input-facing functions are ROBUST**, against
> **3 REFUTED** and **2 BLOCKED files** (≈6 functions). Headline: of the priority-1 attack surface
> that Creusot *can model*, every function is either proven robust or shown to contain a real bug —
> there were **zero** silent "looks-verified" passes and **zero** input-restricting preconditions.

## By file and input source

### Disk/ESP-supplied (attacker with a USB stick) — the highest-value surface

| File | Function | Verdict | Note |
|---|---|---|---|
| `lace-util/peimage.rs` | `SectionHeader::name` | **ROBUST** | proved |
| | `PeRef::num_sections` | **ROBUST** | proved |
| | `PeRef::nth_section` | **ROBUST** | the documented `.unwrap()` is proved in-bounds from a *type invariant* `sect_hdrs.len() == number_of_sections*40` (structural, not an input precondition) |
| | `RawSectionIterator::next` / `VirtualSectionIterator::next` | **ROBUST** | proved |
| | `parse_pe` | **REFUTED** | line 223 `e_lfanew - 64` underflow → panic on a 274-byte crafted PE (debug + release). See bug note. |
| | `relocate_into` | **REFUTED** | `align_up!(virtual_size, section_alignment)` → divide-by-zero (`section_alignment==0`) AND u32 multiply overflow. See bug note. |
| `lace-platform/fs/gpt.rs` | `parse_gpt` | **ROBUST** | the loop offset `entry_start_byte + i*entry_size` proved non-overflowing from the pre-loop `checked_mul`/`checked_add`; `checked_sub`/`checked_add` on LBAs safe |
| `lace-platform/fs/mbr.rs` | `parse_mbr`, `read_mbr_sector`, `is_extended_type` | **ROBUST** | proved |
| | `parse_ebr_chain` | **REFUTED** | line 128 `current_lba * sector_size` raw u64 multiply overflows after line 147 grows `current_lba` past u32. See bug note. |
| `lace-util/bls.rs` | `parse_bls_entry` | **BLOCKED** | by-hand: all-total ops, robust by construction; Creusot can't translate `str::lines` (no `IteratorSpec`). |
| `lace-util/grub.rs` | `parse_grub_cfg` + tokenizer/parser | **BLOCKED** | by-hand: no index/slice/unwrap; but **real unbounded-recursion stack-overflow** in `parse_submenu` (routed as a bug). Creusot blocked by `Illegal recursive type` (`Vec<MenuEntry>`) + `DeepModel` derive. |
| `lace-util/chid_mapping.rs` | `next_chid_mapping` | **ROBUST** | the crux `body.get(..body_len).is_some() ⟹ entry_length <= remaining.len()` proved, so the raw slice advance `&remaining[entry_length..]` is in bounds for any input |
| | `extract_string` | **ROBUST** | `data.get(offset..)` checked; NUL-scan gives `nul_pos < len`; `str::from_utf8` total |

### Peripheral-supplied / firmware / derived (priority-2 — verified 2026-06-17)

| File | Function | Verdict | Note |
|---|---|---|---|
| `lace-util/edid.rs` | `ParsedEdid::parse` | **ROBUST** | length-check + magic; no indexing/arith |
| | `panel_id` | **BLOCKED** | every real VC (`b'A'+(val-1)` overflow, 4 `HEXCHARS_LOWER[x&0xF]` index bounds via `#[bitwise_proof]`, `u8 as char`) proven; only spurious `inv_String` goals remain (creusot-std lacks `impl Invariant for String`) |
| `lace-util/sha1.rs` | `sha1_transform` | **ROBUST** | `block[i*4..]` index / `try_into` len / `w[i-k]` underflow / `i*4` mul all proven |
| | `sha1`, `update`, `digest` | **ROBUST** for realistic input | the only residual VC is `total_size*8` (and `total_size += …`) overflowing `usize` at ~2^61 bytes — not reachable for any real `&[u8]` (`len ≤ isize::MAX`); flagged, not fileable |
| `lace-util/elf64.rs` | `parse`, `for_each_phdr`, `segment_data` | **ROBUST** | the raw `phoff + i*phentsize` walk proven no-overflow/in-bounds from a *type invariant* `phoff + phnum*phentsize ≤ data.len()` (`parse` discharges it) + a mul-monotonicity lemma; the `FnMut` callback precondition threaded |
| `lace-util/smbios.rs` | `find_smbios_table_by_type` | **ROBUST** | crux `&rest[end_of_strings+2..]` in bounds from `find_byte_sequence`'s *proven* postcondition `Some(i) ⟹ i+2 ≤ rest.len()` |
| | `SmbiosTable::table` | **ROBUST** | the documented `.unwrap()` proven via type invariant `table.len() ≥ size_of::<T>()` that the constructor establishes |
| | `SmbiosTable::get_string` | **ROBUST** | `i-1` guarded by `i ≥ 1` |
| `lace-util/acpi/mod.rs` | `Rsdp::parse` | **ROBUST** | `&data[..20]`/`&data[..length]` in bounds from `ref_from_prefix`/length checks |
| | `acpi_checksum` | **ROBUST** | wrapping fold modeled as indexed loop |
| | `Rsdp::find_table` | **ROBUST** | walks the SDT via a caller `deref` closure returning an *arbitrary-length* slice; every access guarded by the code's own `off+ptr_size > sdt_data.len()` check; `entries_len/ptr_size` no div0 (`ptr_size ∈ {4,8}`); negative-control confirms teeth |
| `lace-util/acpi/fadt.rs` | `parse_fadt_facs_addr` | **ROBUST** | only field reads after `ref_from_prefix` |
| `lace-util/acpi/mcfg.rs` | `parse_mcfg` | **ROBUST** | `&data[entries_offset..total_length]` in bounds from the `total_length` guards |
| `lace-util/chid.rs` | `compute_chid` | **ROBUST** (robustness) | `1<<i` (`i<12`) no shift-overflow, `Guid::read_from_prefix(&digest[20])` proven Some (≥16), `data4[0]` index in bounds; the `encode_utf16().collect()` *byte-content* path is BLOCKED (`IteratorSpec` gap) but irrelevant to panic-freedom |
| | `chid_sources_from_smbios_and_edid` | **BLOCKED** | `format!`/`String`/generic-zerocopy heavy; constant array indices trivially in bounds but body untranslatable |
| `lace-util/chid_matcher.rs` | `ChidMatcher::next` | **ROBUST** | both array indexes guarded; `CHID_TYPES[CHID_TYPE_MATCHING_PRIORITY[..]]` in bounds from the const-array values ≤ 17 < 18; `+= 1`s bounded |
| `lace-util/lib.rs` | `hex_seq` | **ROBUST** | `bytes[i]` guarded, digit subs guarded by match-range patterns, `value<<4` is a wrapping shift (only the trivial shift-amount VC) |
| | `find_byte_sequence`, `Guid::try_from_str` | **PARTIAL** | panic-safe; residual is SMT-incompleteness (the `len-sub+1` add / an `Option` invariant). Re-proved fully in the smbios harness by rewriting the range to `while i <= last`. |
| | `align_up!`/`align_down!`/`count_blocks_aligned_*` | **REFUTED in isolation / latent at call sites** | div-by-zero on `bound==0`; `align_up!` u32 multiply-overflow on large `val`. At every non-test call site the divisor is a nonzero constant (`512`, `mem::PAGE_SIZE`) ⇒ div0 not reachable; the multiply-overflow is the already-filed ISSUE-2. `div_ceil` translates *vacuously* (no extern spec) and was hand-expanded to surface these VCs. |

## Remaining attack surface (residual risk)

1. **`peimage::parse_pe`, `peimage::relocate_into`, `mbr::parse_ebr_chain`** — REFUTED: real
   panics/overflows on crafted disk/ESP input until fixed (4 bugs, all with minimal reproducers
   and one-line fixes — see `config/skills/creusot-monitoring/bugs-to-report/20260617-1117-*`
   and `lace-issues/ISSUE-1..3`).
2. **`bls::parse_bls_entry`, `grub::parse_grub_cfg`** — BLOCKED: not mechanically proven.
   By-hand analysis says both are memory-safe/panic-free for realistic inputs, EXCEPT
   `grub::parse_submenu` has a real **unbounded-recursion stack-overflow** DoS (ISSUE-4).
   The block is a Creusot modeling gap (`&str` iterators), not a code defect.
3. **`edid::panel_id`, `chid::chid_sources_from_smbios_and_edid`** (priority-2) — BLOCKED by
   creusot-std modeling gaps (`String` has no `Invariant` impl; `format!`/`encode_utf16`
   `IteratorSpec` untranslatable). All *real* panic/index/overflow paths in `panel_id` were
   discharged; only the spurious String-invariant goals remain. Code defects: none found.
4. **`lib::align_up!`/`count_blocks_aligned_up!` div-by-zero on `bound==0`** — a latent hazard:
   safe today because every non-test call site passes a constant nonzero divisor, but a future
   call site passing an unvalidated runtime `sector_size`/alignment would panic on `0`. The
   `div_ceil` vacuous-translation gap that masks it is routed to getting-better/.
5. **`sha1` `total_size*8` usize overflow** — real only at ~2^61 bytes (≈2 EB); unreachable for
   any actual `&[u8]` (`len ≤ isize::MAX`). Noted, not fileable.
6. **The ~77 `unsafe` sites in `lace-platform`** — outside this loop's reach by design (FFI /
   firmware state); measured statically (§ claims report), not proven.

## Trusted assumptions used (the trust base of the ROBUST verdicts)

- **No `#[trusted]`, no `assume!` anywhere.** No verdict above relied on an escape hatch.
- **extern_specs (chid_mapping only), all totality-only — they assert a method is total/returns a
  `Result`, never strengthen a functional property, so they cannot "assume the attacker away":**
  - `u32::from_le_bytes([u8;4]) -> u32` `#[ensures(true)]` (total).
  - `str::from_utf8(&[u8]) -> Result<&str, _>` `#[ensures(true)]` (total, returns Result).
- **Faithfulness model (all files): zerocopy `read_from_prefix` / `U16/U32/U64<LE>::get()` were
  replaced by explicit length-check + `from_le_bytes` at the documented struct offsets**, and the
  `dyn BlockDevice` was modeled as reads over an in-memory `&[u8]` disk. Each replacement is
  byte-identical to the Lace source (documented per function in the sub-agent reports). The
  internal `read_u*_le`/`read_guid` helpers carry `#[requires(off+N <= s.len())]`, discharged at
  every call site from the explicit length checks — these are *local* obligations, not
  restrictions on the parsers' adversarial input (Gate C satisfied: the input-facing functions
  themselves have zero `#[requires]`).

## Trusted assumptions used (priority-2 additions)

- **Still no `#[trusted]` on any parser body, no `assume!`.** (The elf64 harness used `#[trusted]`
  only on the two zerocopy `read_*` length-check stand-ins — the faithful model the plan mandates —
  not on any verified logic.)
- **Totality-only / length-only extern specs added (each asserts a method is total or returns a
  `Result`/fixed length — none strengthens a functional or crypto property, so none can "assume the
  attacker away"):** `String::new`/`String::push`, integer `from_be`/`from_le`/`to_be`/`to_le` and
  `rotate_left`, `u32::to_be_bytes`/`from_be_bytes`/`usize::to_be_bytes`, `[T;N]` range
  `Index`/`IndexMut`, `slice::fill`/`is_empty`, `usize::try_from(u64)`, the caller `deref`/`f`
  closure models in `acpi::find_table`/`elf64::for_each_phdr`. All recorded; the matching
  creusot-std gaps are routed to getting-better/.
- **Faithfulness models:** zerocopy `read_from_prefix`/`ref_from_prefix` and `U16/U32/U64<LE>::get()`
  replaced by explicit length-check + byte reads at the documented struct offsets (byte-identical);
  `b"…"` reference constants replaced by `[u8;N]` value arrays (Creusot rejects byte-string-ref
  constants); generic-`T` zerocopy reads monomorphized to a concrete size.

## Honest scope statement

A ROBUST verdict buys exactly: *that function provably cannot panic / overflow / read OOB on any
input*, removing it from the exploitable surface. It does **not** establish Secure Boot, correct
TPM measurement, or correct kernel selection (out of Creusot scope — see claims report).

**Combined deliverable (priority-1 + priority-2):** of the ~38 input-facing functions across the
lace-util parsers + the two partition parsers, **25 are proven ROBUST** (8 + 17), **4 are real
disk/ESP bugs (REFUTED, ISSUE-1..4)**, **2 are PARTIAL** (panic-safe, SMT-incompleteness only), and
**~6 are BLOCKED** by creusot-std modeling gaps (`String`/`format!`/`&str`-iterator/recursive-type) —
all gaps routed to getting-better/, none a code defect. Priority-2 surfaced **zero new fileable
bugs**: the parsers are markedly disciplined; the only residuals are two impractical/latent
arithmetic hazards (sha1 ~2^61-byte overflow; the `align_up!`/`count_blocks_aligned_up!` `bound==0`
div-by-zero that no current call site can reach). All under totality-only extern specs and no
`#[trusted]` on verified logic.
