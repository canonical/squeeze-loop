# Lace — architecture report

*An analysis of [`canonical/lace`](https://github.com/canonical/lace) (cloned at `lace/`), produced 2026-06-17 by deep-reading the source with six parallel sub-agents, one per subsystem.*

---

## 1. What Lace is and does

**Lace is a Rust framework for writing UEFI boot applications**, developed by Canonical. It exists to make boot-time software (the code that runs after firmware but before the OS kernel) **memory-safe, platform-independent, and composable** — replacing C reference implementations like systemd-stub with `no_std` Rust built on a clean abstraction layer.

It ships **two end-user boot applications**, both built on shared libraries:

- **`lace-stubble`** — a *stub bootloader* (a Rust reimplementation of systemd-stub / the `stubble` project). A single signed EFI binary is "specialized" into a bootable image by embedding a kernel, initrd, command line and device trees into its own **PE sections**; at boot it reads those sections back out of itself and chain-loads Linux. This is the **Unified Kernel Image (UKI)** model.
- **`lace-speedboot`** — a *fast UEFI boot menu* that scans all disks for GRUB/BLS configurations, presents a menu, and boots the chosen Linux system.

Supporting both are three libraries — **`lace-platform`** (firmware abstraction: UEFI / legacy BIOS / a mock backend), **`lace-util`** (pure parsers for PE, ACPI, SMBIOS, EDID, CHID, GRUB/BLS, FDT), and **`lace-util-derive`** (proc-macros) — plus **host-side tools** (`pewrap`, `collect-hwids`, `fakeedid`, `xtask`) that build and test the boot images.

A distinctive theme is **hardware-identity binding (CHID)**: one signed stub can auto-select the correct device tree per machine model (using Microsoft-style Computer Hardware IDs computed from SMBIOS + EDID), so a single image safely targets many boards without per-device rebuilds.

## 2. Architecture at a glance

**Crate layering** (10-member Cargo workspace, edition 2024):

```
            apps  ┌─ lace-speedboot ─────────────┐   (multi-boot menu)
                  │        │                      │
                  │        ▼                      ▼
                  └─ lace-stubble ──────►  lace-platform   (stub UKI loader)
                                                 │   firmware abstraction
                                                 │   backends: efi / bios / mock
                                                 ▼
                              lace-util  ◄──  lace-util-derive  ◄── lace-util-derive-impl
                          (no_std parsers)     (proc-macro facade)    (testable macro logic)

  host tools (std):  pewrap · collect-hwids · fakeedid(UEFI) · xtask     ── share ──►  lace-util
```

The firmware crates (`lace-util`, `lace-platform`, `lace-stubble`, `lace-speedboot`) are `#![no_std]`; the tools are ordinary host `std` binaries that reuse the same `lace-util` parsers.

**Two-phase model (stubble).** Lace separates a *host build-time* step from a *firmware boot-time* step around a shared on-disk format — the PE image and its sections:

```
BUILD TIME (host, std)                          BOOT TIME (firmware, no_std)
──────────────────────                          ───────────────────────────
cargo build lace-stubble  ─►  stub.efi          firmware loads the image
                               │                       │
pewrap --linux/--initrd/       │                lace_app_main opens its own LoadedImage
  --cmdline/--hwids/--dtbauto ─┘                parse PE → read .linux/.initrd/.cmdline/
   embeds assets as PE sections                   .hwids/.dtbauto sections
        │                                              │
        ▼                                        pick DTB (firmware DTB → CHID match)
   bootable BOOTX64.EFI  ───────────────────►   measure cmdline into TPM PCR 12
                                                 boot_linux() → EFI handover, no return
```

The sections below detail each subsystem; §8 gives the integrated end-to-end view and security posture.

---

## lace-platform — platform abstraction

**Purpose & scope.** `lace-platform` is Lace's hardware/firmware abstraction layer: it lets a boot application (e.g. stubble/speedboot) be written once against a platform-neutral API and then compiled against one of three concrete backends — UEFI boot services (`efi`), legacy `bios`, or a hosted `mock` for unit testing. The backend is selected by a Cargo feature and aliased internally as `crate::p` (`lace-platform/src/lib.rs:22-30`), so all front-end modules call `crate::p::*` without knowing which firmware they target. The whole crate is `#![cfg_attr(not(feature = "mock"), no_std)]` with `extern crate alloc` (`src/lib.rs:6-8`): bare-metal targets are `no_std` + heap, while the mock backend pulls in `std` for tests.

**Module map.** The top level (`src/`) defines the portable interface; each file re-exports the platform implementation at its bottom:
- `mem.rs` — page-allocation trait (`PageAllocationIface`), allocation constraints, and `MemAttributes` (R/W/X protection) bitflags.
- `console.rs` — `Output`/`Input` traits, the global `log` logger, and a panic banner.
- `fs/` — the storage stack: `base.rs` (`BlockDevice`, `Filesystem`, `File`, `DirEntry`, `FsError` traits), `gpt.rs`/`mbr.rs` (portable partition-table parsers using `zerocopy`), `ext4.rs` (driver via the `ext4-view` crate), and `probe.rs` (device discovery → partition probing → filesystem mounting).
- `hwid.rs` — hardware identification (CHID/SMBIOS/EDID/DTB matching, via `lace-util`).
- `linux.rs`, `tpm2.rs` — Linux kernel boot and TPM2 measured-boot facades.
- `amd64/linux_bootparam.rs` — architecture-specific (x86_64) Linux boot-protocol structs.

Backends live under `efi/`, `bios/`, `mock/`, each mirroring the same submodule set (`console`, `fs`, `hwid`, `mem`, `linux`, `tpm2`, plus EFI-only `image.rs` and `proto/`).

**Internal architecture.** The portable layer is built almost entirely on **traits + feature-gated re-exports** rather than `dyn` indirection across the platform boundary: `mem.rs` defines `PageAllocationIface` with provided methods (`new_zeroed`, `new_init_prefix`) layered over a single `unsafe fn new_uninit`, then re-exports the concrete `PageAllocation` from `crate::p::mem` (`src/mem.rs:148`). Within the filesystem stack, runtime polymorphism *is* used (`Box<dyn BlockDevice>`, `Box<dyn Filesystem>`) since multiple disks/partitions coexist; `probe.rs` shares a disk among partition sub-views with `Rc<RefCell<Box<dyn BlockDevice>>>`, explicitly relying on the single-threaded boot context.

The **EFI backend wraps the `uefi` (uefi-rs) crate**, not raw FFI, for most work: it opens protocols via helpers like `open_first_protocol_exclusive` (`src/efi/mod.rs:23-30`), and `efi/fs.rs` adapts `SimpleFileSystem`, `DiskIo`, and `BlockIO` into the portable `Filesystem`/`BlockDevice` traits. It drops to **`uefi-raw` FFI** only where it must mutate firmware structures directly — re-installing the `LoadedImage` protocol to chainload a kernel (`efi/image.rs`), and implementing a `LoadFile2`/device-path protocol to hand an initrd to Linux (`efi/linux.rs`). The **allocator** is UEFI's global allocator (the `uefi` `global_allocator` feature); BIOS uses `linked_list_allocator`. `PageAllocation` is a Drop-guarded RAII owner of firmware pages (with an EDK2 attribute-clearing workaround, `efi/mem.rs:104-119`).

**Error handling** is per-platform: `lib.rs` re-exports `p::Error` (`uefi::Error` for EFI, a BIOS `Disk`/`Other` enum, a unit struct for mock). The portable `FsError` wraps that `Error` plus format errors and converts via `From` (`fs/base.rs:34`).

**Entry-point / lifecycle.** Apps mark their entry with `#[lace_platform::entry]` (re-exported from `lace-util-derive`), which exports the function as `lace_app_main`. Each backend supplies the real firmware entry that initializes subsystems and calls it: EFI uses `#[uefi::entry] fn efi_main` → `console::init` → `mem::init` → `lace_app_main` (`efi/mod.rs:33-47`); BIOS uses a `#[no_mangle] extern "C"` entry plus `global_asm!` startup (`bios/mod.rs:38-56`). Each non-mock backend also owns the `#[panic_handler]`, routing to `console::panic`.

**Interfaces & dependencies.** To boot apps, the crate exposes: page/memory allocation and protection, console/`log` I/O, filesystem discovery (`probe_all`, `probe_boot_device`) and access, hwid matching, TPM2 measurement (`hash_log_extend_event`), and Linux boot (`boot_linux`). Key deps: `uefi`/`uefi-raw` (EFI), `linked_list_allocator` (BIOS), `ext4-view` (ext4), `zerocopy` (on-disk structs), `bitflags`, `spin` (lock-free statics), `log`, and `lace-util`/`lace-util-derive`.

**Notable design decisions.** `unsafe` is concentrated at the firmware boundary — page-slice construction, protocol re-installation, FFI callbacks, config-table install/find — and is consistently paired with `// SAFETY:` notes and RAII receipts (`DtbReceipt`, `InitrdLoader`, `PageAllocation`) that undo firmware-global side effects on drop. The console design holds the `spin::Mutex` only across a single driver call so user `Display` code never runs with the lock held (no poisoning on panic). NX/W^X enforcement in `efi/image.rs` is a standout: it parses the PE, derives per-section `MemAttributes`, and refuses W&X or misaligned images. The partition parsers (`gpt.rs`/`mbr.rs`) and probe pipeline are fully platform-independent, so only raw block I/O needs a per-firmware implementation.

---

## lace-util — platform-independent utilities

`lace-util` is Lace's `no_std`-capable foundation crate: a collection of pure, allocation-light parsers and helpers for the binary formats and configuration files a UEFI boot application must understand, with no dependency on any specific firmware or OS. It is `#![no_std]` unless the `std` feature is on (`lace-util/src/lib.rs:5`), always pulls in `alloc`, and is gated by three features: `firmware` (ACPI/ELF parsing), `std` (libc for tempfiles), and `grub` (the GRUB parser). Its only real deps are `zerocopy` (safe byte-slice ↔ struct casting), `fdt` (flattened-device-tree reader), and the sibling proc-macro crate.

**Module map**

- `lib.rs` — the `Guid` type with compile-time `guid_str()`/`try_from_str` parsing and `OrderedGuid<O: ByteOrder>` (encodes LE-vs-BE byte order of GUID fields *in the type system*, for GPT/UEFI vs RFC 9562 hashing); byte helpers `find_byte_sequence`, `hexdump`; and `align_up!`/`align_down!`/`count_blocks_aligned_*` macros.
- `peimage.rs` — **PE/COFF (PE32+) parser**. DOS/NT/optional/section header structs, `parse_pe()` → `PeRef<'a>` (zero-copy view), `raw_sections()`/`virtual_sections()` iterators, `SectionHeader::name()`, and `relocate_into()` (lays the image out by virtual address). This is the PE handling that `tools/pewrap`, `lace-platform`, and `lace-stubble` build on to read/embed sections.
- `grub.rs` (feature `grub`) — a deliberately simplified GRUB2 `grub.cfg` parser (tokenizer + recursive-descent) extracting `MenuEntry::{Entry,Submenu}` with linux/initrd/cmdline. No variable expansion, command substitution, conditionals, or loops — just enough for cloud-image configs (used by speedboot).
- `bls.rs` — Boot Loader Specification Type 1 key-value parser → `BlsEntry`; unknown keys ignored for forward compatibility.
- `smbios.rs` — SMBIOS entry-point (v2 `_SM_` / v3 `_SM3_`) and table-type structs; `SmbiosTable<'s,T>` with 1-based string-table lookup; `find_smbios_table_by_type::<T>()`.
- `edid.rs` — EDID header parser yielding a `panel_id()` (manufacturer letters + product code), handling mixed BE/LE fields.
- `chid.rs` / `chid_mapping.rs` / `chid_matcher.rs` — **CHID machinery**. `chid.rs` builds `ChidSources` from SMBIOS+EDID and `compute_chid()` implements Microsoft's CHID / RFC 9562 v5 UUID (UCS-2 `&`-joined fields, SHA-1 over a namespace GUID). `chid_mapping.rs` parses the systemd `.hwids` section. `chid_matcher.rs` iterates mappings in most-to-least-specific priority — used for device-tree/firmware selection.
- `acpi/` (feature `firmware`) — RSDP v1/v2 (checksum-validated), RSDT/XSDT walking via a caller-supplied `deref` closure (isolating the one unsafe physical-memory access); `fadt.rs`, `mcfg.rs` (PCI ECAM).
- `elf64.rs` (feature `firmware`) — minimal ELF64 + `PT_LOAD` parser.
- `sha1.rs` — self-contained SHA-1, explicitly "non-security purposes only" (for CHID hashing).
- `units.rs` — `Timestamp`/`Size` display wrappers; `tempfile.rs` (feature `std`+unix) — RAII `mkostemp`/`mkdtemp` wrappers.

**Internal architecture.** The dominant pattern is **zero-copy parsing**: `#[repr(C)]`/`#[repr(C,packed)]` structs derive `zerocopy::{FromBytes,IntoBytes,Immutable,KnownLayout}` and are read in-place from `&[u8]` via `read_from_prefix`/`ref_from_prefix`, with explicit `checked_add`/`checked_mul`/`get(..)` bounds checks. Parsers return borrowed views tied to the source buffer (no allocation). Errors are per-module enums implementing the crate's derived `Display` (no `std::error::Error`, staying `no_std`). Endianness is explicit (`zerocopy` `U32<LE>`, `OrderedGuid<O>`, manual `from_le`/`to_be`). Platform independence is structural: ACPI's only physical-memory touch is delegated to a caller closure, and OS-specific code is feature-gated.

**Notable design decisions.** Compile-time GUID parsing; byte-order-in-the-type-system via `OrderedGuid`; a vendored SHA-1 flagged non-cryptographic; closure-injected memory access to keep ACPI testable and `unsafe`-free in the library; a frank, narrowly-scoped GRUB parser. Every module ships unit tests, several driving real `testdata/` fixtures (`grub.cfg`, `bls-entry.conf`, `t14s-dmi.bin`, `t14s-edid.bin`, signed-hwids blobs).

---

## lace-util-derive — procedural macros

**Purpose.** `lace-util-derive` exports four macros that cut boilerplate in Lace's `no_std`, panic-averse code:

- **`NumEnum`** (derive) — bidirectional conversions between a `#[repr(int)]` unit enum and integers (a direct `TryFrom<repr>`, nine delegating `TryFrom` impls for the other widths, and `From<Enum> for repr`); `Err(())` for unknown discriminants. The glue for turning raw firmware/protocol byte values into typed variants and back.
- **`NamedEnum`** (derive, `#[name(short=…, long=…)]`) — `short_name`/`long_name` accessors and `try_from_short_name`, for CLI/log-friendly naming.
- **`Display`** (derive, `#[display("…")]`) — a `core::fmt::Display` impl from a `format!`-style string per variant, used pervasively for `no_std` error enums (`PeError`, `EdidParseError`, …).
- **`entry`** (attribute) — rewrites a function with `#[unsafe(export_name = "lace_app_main")]`, the symbol the platform's EFI/BIOS shims call into. The app entry-point hook.

**Split design.** Logic lives in a separate plain library, `lace-util-derive-impl` (modules `display`, `entry`, `named_enum`, `num_enum`), while `lace-util-derive` is a thin shim (`proc-macro = true`) that only converts `proc_macro::TokenStream` ↔ `proc_macro2::TokenStream` and delegates. The reason, stated in-code, is **testability**: proc-macro crates can't be unit-tested or coverage-instrumented directly, so all real work operates on `proc_macro2::TokenStream`. `-impl` carries 30 unit tests (display 12, num_enum 7, named_enum 7, entry 4), including every `compile_error!` path.

**Internal architecture.** Each module: a public `derive`/`apply` entry calls a `try_*` returning `syn::Result<TokenStream>`, converting errors via `e.to_compile_error()` — malformed input yields a *spanned compiler error, not a panic*. Parsing uses `syn` (`parse2`, `parse_args`, `parse_nested_meta`); generation uses `quote!`; spans from `proc-macro2`. Compile-time validation per macro: `NumEnum`/`NamedEnum` reject non-enums/non-unit variants (`NumEnum` also requires `#[repr(int)]` + explicit discriminants); `Display` rejects unions/missing attrs and preserves generics via `split_for_impl`; `entry` rejects arguments and non-functions.

**Consumers & decisions.** `Display` is used across `lace-util` error types; `entry` is re-exported as `lace_platform::entry` and applied in `lace-stubble`/`lace-speedboot` `main.rs`. The facade/impl split trades a second crate for unit-testable macro logic; `core::fmt` (not `std`) keeps it `no_std`.

---

## The boot applications: lace-stubble & lace-speedboot

Both are end-user UEFI applications built on `lace-platform` (console, fs, `linux`, `hwid`, `tpm2`) and `lace-util` (`peimage`, `fdt`, `grub`, `bls`). Both pick the backend via `efi`/`bios`/`mock` features, are `#![no_std]`/`#![no_main]` on real targets, and use `#[lace_platform::entry]` as the firmware entry point.

### lace-stubble (stub bootloader)

A Rust reimplementation of `stubble` (a trimmed systemd-stub). A *single* EFI binary is specialized by `pewrap` injecting resources as PE sections; at runtime the stub reads its **own** image back, extracts those sections, and chain-loads Linux.

Key types: `StubbleImage<'a>` (`Loaded(&[u8])` from firmware vs `Raw(&[u8])` from disk), and `BootStubbleError` (`PeError`, `DuplicateSection`, `NotAStubbleImage`, `InvalidCommandLine`).

Boot flow (`src/main.rs` → `src/lib.rs::boot_stubble_image`):
1. **Entry** (EFI). Opens its own `LoadedImage`, turns `(ptr,len)` into `&[u8]` via `from_raw_parts`, decodes `load_options_as_bytes()` (UTF-16) into an optional external cmdline. Calls `boot_stubble_image(Loaded(slice), None, external_cmdline)`.
2. **PE parse.** `lace_util::peimage::parse_pe(data)`; sections walked with `virtual_sections()` (Loaded) or `raw_sections()` (Raw) — file offsets vs RVAs differ.
3. **Section dispatch.** A `section_filter` matches `sect.name()`: `.linux`→kernel, `.initrd`→initrd, `.cmdline`→UTF-8 cmdline, `.hwids`→CHID DB, `.dtbauto` (repeatable)→`Vec`. Single-shot sections use an `InsertOnce` trait so a duplicate → `DuplicateSection`.
4. **Fallbacks.** Missing `.cmdline`/`.initrd` → substitute the external cmdline / external initrd. Missing kernel → fatal (`NotAStubbleImage`).
5. **Device-tree auto-selection.** Compute the platform "compatible" first from the firmware DTB (`hwid::platform_compatible_using_firmware_dtb()`), else CHID-match against `.hwids`. Parse each `.dtbauto` with `fdt::Fdt`, read the root `compatible`, and on match `install_dtb(...)`, holding the receipt until boot.
6. **Measurement.** Measure the cmdline into **TPM 2.0 PCR 12** (`tpm2::hash_log_extend_event(12, …, EventType::IPL, …)`); failure logged, non-fatal.
7. **Handoff.** `lace_platform::linux::boot_linux(kernel, initrd, cmdline)` performs the EFI handover / chainload; does not return.

Features: kernel+initrd+cmdline+DTB from one binary, CHID/DTB auto-selection, cmdline fallback to Load Options, initrd via Load File2. Omitted vs systemd-stub: secure-boot policy, credentials, splash, multi-profile.

### lace-speedboot (fast boot menu)

A fast UEFI menu that discovers installed Linux systems across all block devices and boots a chosen one. Depends on `lace-util` (`grub`), `lace-platform` (`ext4`), and `lace-stubble` as a library.

Key types: `BootConfiguration` trait (`title()`, `start()`), `SimpleBootConfiguration` (title + optional linux/initrd/cmdline + a shared `Rc<RefCell<Box<dyn Filesystem>>>`), the `BootFlow` trait (`discover(fs) -> Vec<Box<dyn BootConfiguration>>`), and `SpeedbootError`.

Flow (`src/main.rs`):
1. **Discovery** (`bootflows/mod.rs::discover_all`). `fs::probe_all()` enumerates readable filesystems; each runs through a `BlsBootFlow` and a `GrubBootFlow`. Empty → `NoBootEntriesFound`.
2. **GRUB flow.** Probes seven well-known paths (`boot/grub/grub.cfg`, `EFI/ubuntu/grub.cfg`, …), reads + UTF-8 decodes, `grub::parse_grub_cfg`; `flatten_recursive` walks submenus (`parent > child`), one `SimpleBootConfiguration` per leaf.
3. **BLS flow.** Reads `loader/entries`/`boot/loader/entries`, parses each `*.conf` via `bls::parse_bls_entry`.
4. **Menu/UI** (`text.rs`). Numbered `[idx] title` to `console::stdout()`; `get_user_selection` reads `stdin().wait_input()` char-by-char (digits, backspace, Enter), range-checks the index.
5. **Boot.** `grub::load_boot_files` (with a `/boot/<path>` fallback) loads kernel/initrd, then *tries `lace_stubble::boot_stubble_image(Raw(kernel), …)` first* (the kernel may itself be a stubble UKI); on `NotAStubbleImage` falls back to `linux::boot_linux`.

Discovery is tolerant (per-fs/path errors skipped); `main` uses `.expect(...)` on discovery/selection/boot.

---

## Tooling & build/test support

Lace ships **host-side** helpers under `tools/` plus Python glue under `scripts/`/`data/`. Unlike the `no_std` UEFI crates, every tool is an ordinary `std` binary (or Python) running on the developer machine, sharing the `lace-util` library (PE/CHID/SMBIOS/EDID logic) with the firmware.

**pewrap** (`tools/pewrap/src/{main,cli,lib}.rs`) is the build-time counterpart to the runtime stub: it takes a pre-built `lace-stubble` PE (`--stub`) and *adds PE sections* carrying the payloads (`--linux`→`.linux`, `--initrd`→`.initrd`, `--cmdline`→`.cmdline`, `--sbat`→`.sbat`, `--dtbauto`→`.dtbauto`, `--hwids <dir>`→`.hwids`), emitting a self-contained image. Payloads are validated (the kernel must be a PE advertising LoadFile2 initrd support via `major_image_version >= 1`; DTBs parsed with `fdt`). The core is `PeRebuilder`: it clones the stub's headers + sections, `add_section` aligns each new section's VA up to `section_alignment` and raw size to `file_alignment`, and `fixup_offsets` recomputes `number_of_sections`/`size_of_*`/`size_of_headers`/`size_of_image`. Virtual space is constrained (these PEs carry only base relocations), so it errors `HeadersTooLarge` if headers would overrun the first section's VA; `--post-process-for-ukify` maximizes header room so `systemd-ukify` can later append sections. The `.hwids` section is the serialized CHID→DTB/firmware map (`lace_util::chid_mapping::serialize_chid_mappings`), enabling per-board DTB auto-selection from one image.

**collect-hwids** (`tools/collect-hwids/src/main.rs`) runs on a target laptop: reads SMBIOS from `/sys/firmware/dmi/tables/*` and EDID from `/sys/class/drm/card*-*/edid`, computes the 12 CHID sources + 18 CHID GUIDs, and (with `--output`) writes a ZIP of the raw blobs + `hwids.txt`. Curated results live in `data/hwids/` as fwupd-style `txt/*.txt`, converted by `hwid2json.py` into `json/*.json` (`{type,name,compatible,hwids:[...]}`) — the directory pewrap's `--hwids` consumes; `finddtbs.py` matches each `compatible` against a `.dtb` tree via `libfdt`.

**fakeedid** (`tools/fakeedid/src/*`) is the one tool that *is* a UEFI app (built for `*-unknown-uefi`): it reads `edid.bin`, installs an `EFI_EDID_DISCOVERED_PROTOCOL` with that data, then returns `NOT_STARTED` so firmware proceeds — letting a test VM present a chosen panel EDID so EDID-based CHID matching can be exercised without real hardware.

**xtask** (`tools/xtask/src/main.rs`) is the cargo-xtask automation crate (`cargo run -p xtask -- <cmd>`); currently it generates `man/{pewrap,collect-hwids}.1` from each tool's clap CLI via `clap_mangen`.

**scripts/vm_manage.py** orchestrates end-to-end VM testing: `init` builds a GPT disk from an Ubuntu cloud image (ESP + rootfs, +BIOS-boot on x86_64) via `libguestfs` and stages OVMF/AAVMF firmware; `start` builds the chosen app and, for stubble, drives **pewrap** with the extracted kernel/initrd/cmdline + `--hwids data/hwids/json`, uploads the result to the ESP as `BOOT{X64,AA64}.EFI`, then launches QEMU — optionally wiring up swtpm, a custom SMBIOS file, and **fakeedid** for EDID injection.

---

## Cross-cutting: workspace, build, and end-to-end architecture

**Workspace & crate graph.** A single Cargo workspace (`resolver = "2"`, edition 2024) with ten members in a clean layering: base *utility/derive* crates (`lace-util-derive-impl` → `lace-util-derive` → `lace-util`), then `lace-platform` (swappable backends), then the apps (`lace-stubble`, and `lace-speedboot` which depends on platform + stubble), with the host tools off to the side. Firmware crates are `#![no_std]` (`#![cfg_attr(not(feature="mock"), no_std)]`); tools and `lace-util-derive*` are host/std (`clap`, `serde`, `zerocopy`, `zip`).

**Build & targets.** Backends are mutually-exclusive Cargo features — `mock` (native std test binary), `efi` (`uefi`/`uefi-raw`), `bios` (`linked_list_allocator`) — threaded through every layer. Firmware builds use `panic = "abort"` (dev + release). UEFI targets are the standard `x86_64-unknown-uefi`/`aarch64` PE; BIOS uses a checked-in custom target spec + linker script (`lace-platform/src/bios/x86_64-bios.json`/`.ld`) with hand-written assembly stages (`bios/boot/stage1.s`, `stage2.s`, `start.s`). Allocator is backend-specific (EFI global allocator; BIOS `LockedHeap` over the E820 map). The entry-point glue: `#[lace_platform::entry]` rewrites an app's `main` to `export_name = "lace_app_main"`, which the EFI/BIOS shims call via `extern "Rust" { fn lace_app_main() }`, with `#[panic_handler]` per backend.

**End-to-end boot architecture.** *Stubble* is two-phase: at **build time** the stub `.efi` is compiled, then `pewrap` appends `.linux`/`.initrd`/`.cmdline`/`.sbat`/`.hwids`/`.dtbauto` sections (recomputing PE offsets) → a self-contained bootable `.efi`; at **boot time** firmware loads it, `lace_app_main` opens its own `LoadedImage`, parses the PE, extracts the sections, picks the platform "compatible" (firmware DTB → CHID), installs the matching DTB, measures the cmdline into **TPM PCR 12**, and chain-loads Linux. *Speedboot* shares the platform/stubble libraries but is a runtime menu: `discover_all()` scans all disks for GRUB + BLS configs, flattens submenus, renders a text menu, and boots the selection — composing the same filesystem (ext4/GPT/MBR) and Linux-boot primitives rather than embedded assets.

**Engineering practices.** Supply chain is enforced by `cargo-deny` (`deny.toml`): a permissive license allowlist + per-crate `GPL-2.0-only` exceptions, crates.io source pinning, `multiple-versions = "warn"`. Everything is **GPL-2.0-only OR GPL-3.0-only** with mandatory SPDX headers and a **Canonical CLA**; the Ubuntu CoC applies. Style beyond rustfmt is in `STYLE.md` (Canonical rust-best-practices, `bitflags`, test naming). Testing is layered: `#[cfg(test)]` units, the `mock` backend for host-side firmware-logic tests, CI (`.github/workflows/rust-ci.yml`: fmt, workspace clippy `-D warnings`, per-backend `efi`/`bios` clippy matrix, `cargo test`, tarpaulin→Coveralls), and a `pre-commit` mirror. Community on Matrix `#lace:ubuntu.com`.

**Security posture.** Memory safety is Rust `no_std` end-to-end with `unsafe` deliberately concentrated at the hardware boundary: `lace-platform` holds the overwhelming majority (~77 occurrences vs ~5 in `lace-util`, 3 in `lace-stubble`, 0 in `lace-speedboot`), so parser/policy layers stay safe while raw-pointer/protocol access is localized and `// SAFETY:`-documented. The boot path is **measured-boot aware** (TPM 2.0 PCR-12 cmdline measurement per the UAPI PCR registry) and **Secure-Boot aware** (`.sbat` section injection for fine-grained revocation; test VMs run on `*.secboot.fd` OVMF/AAVMF). CHID/HWID binding lets one signed stub safely target many platforms without per-device rebuilds. The PE loader enforces **W^X / NX** and rejects misaligned images.

---

## 3. Summary

Lace is a **layered, safety-first UEFI boot framework**: pure `no_std` parsers (`lace-util`) and proc-macros at the base, a trait-based firmware abstraction with EFI/BIOS/mock backends (`lace-platform`) in the middle, and two boot applications on top — `lace-stubble` (the systemd-stub-style single-image UKI loader) and `lace-speedboot` (a GRUB/BLS-discovering boot menu). A host toolchain (`pewrap`, `collect-hwids`, `fakeedid`, `xtask`, `vm_manage.py`) builds and tests the images around a shared on-disk contract — the PE image and its named sections. The standout architectural ideas are the **PE-section payload model** (build-time `pewrap` ⇄ boot-time self-extraction), **CHID hardware-identity binding** for one-image-many-boards device-tree selection, **measured/secure-boot integration** (TPM PCR 12, SBAT), and a disciplined **`unsafe`-at-the-boundary** safety model with RAII receipts that undo firmware-global side effects.
