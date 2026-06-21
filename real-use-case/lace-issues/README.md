# Lace — security issues found by attack-surface verification

Issues in [`canonical/lace`](https://github.com/canonical/lace) found by running the
`creusot-monitoring` attack-surface verification (`lace-workflow.md`) over the
untrusted-input parsers. Each is a **panic / overflow / DoS reachable from data the
bootloader does not control** (a PE on the ESP, a partition table on any disk, a
`grub.cfg`), i.e. **pre-OS, pre-Secure-Boot-measurement**. Three of four were found as
**unproved Creusot verification conditions**; one (recursion) by call-graph analysis.

| # | Component | Class | Found by |
|---|---|---|---|
| [1](ISSUE-1-peimage-e_lfanew-underflow.md) | `lace-util/peimage.rs:223` `parse_pe` | OOB / subtraction underflow → panic | Creusot VC (`vc_parse_pe`) |
| [2](ISSUE-2-peimage-relocate_into-align.md) | `lace-util/peimage.rs:293` `relocate_into` | div-by-zero + u32 mul overflow | Creusot VCs |
| [3](ISSUE-3-mbr-ebr-chain-mul-overflow.md) | `lace-platform/fs/mbr.rs:128` `parse_ebr_chain` | u64 mul overflow → panic / wrong-sector read | Creusot VC |
| [4](ISSUE-4-grub-submenu-unbounded-recursion.md) | `lace-util/grub.rs` `parse_submenu` | unbounded native recursion → stack-overflow DoS | call-graph analysis |

Each report contains a minimal adversarial input and a **draft patch** (a one-/few-line
fix). The patches are written against the current `canonical/lace` source; apply them in
the `lace/` checkout.

**Caveat (how these were found, honestly):** issues 1–3 are precisely the Creusot
verification conditions that did *not* discharge when the parsers were specified for total
robustness (no panic for *any* input); adding the proposed guard closes the goal. Issue 4
is a source-level call-graph finding (Creusot is blocked on that file — see
`config/skills/creusot-monitoring/getting-better/20260617-1117-creusot-std-no-str-iterator-extern-specs.md`).
The `e_lfanew` underflow and the `mbr` multiply were reproduced on rustc 1.96.0 in both
debug and release.
