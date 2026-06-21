# Issue 3 — `fs::mbr::parse_ebr_chain`: `current_lba * sector_size` u64 multiply overflow

- **Component:** `lace-platform/src/fs/mbr.rs:128` (`parse_ebr_chain`)
- **Class:** unchecked u64 multiply overflow → panic (debug) / wrong-sector read (release)
- **Severity:** Medium-High (pre-OS DoS, or a wrapped offset reading an attacker-chosen sector)
- **Reachable from:** any disk Lace probes (`fs::probe`) — a malicious USB stick / disk image with a crafted extended-partition (EBR) chain.

## Summary

The byte offset of the next EBR is computed with a **raw `u64` multiply** of two
attacker-influenced values:

```rust
// mbr.rs:128
let ebr = match read_mbr_sector(dev, current_lba * sector_size) {
```

`current_lba` is advanced each iteration from on-disk EBR link fields
(`mbr.rs:147 — current_lba = extended_start + next.lba_start.get() as u64`), which can grow
it to `~2^33` (two 32-bit fields summed) — beyond `u32`. Combined with a large
`sector_size`, the multiply overflows `u64`.

## Minimal adversarial input

- `extended_start = 0xFFFF_FFFF`, slot-1 EBR link `lba_start = 0xFFFF_FFFF`
  ⇒ `current_lba = 0x1_FFFF_FFFE`
- `sector_size = 0xFFFF_FFFF`
- product `36 893 488 130 239 234 050 > u64::MAX` → **debug** panic / **release** silent wrap.
- Valid `0x55AA` signatures at the two EBR offsets keep the reads from bailing early — all on-disk-controllable.

## How it was found

Creusot proved the whole EBR chain green **except** this one VC (the line-128 `u64`
multiply); the other two raw adds (lines 138, 147) discharged. Guarding the multiply with
`checked_mul` closes all 42 goals.

## Draft patch

Mirror the GPT parser, which already uses `checked_mul` for the same kind of LBA×size offset:

```diff
--- a/lace-platform/src/fs/mbr.rs
+++ b/lace-platform/src/fs/mbr.rs
@@ -125,7 +125,10 @@
         let sector_size = dev.sector_size() as u64;
-        let ebr = match read_mbr_sector(dev, current_lba * sector_size) {
+        let offset = current_lba
+            .checked_mul(sector_size)
+            .ok_or(FsError::Invalid)?;
+        let ebr = match read_mbr_sector(dev, offset) {
             Ok(s) => s,
             Err(FsError::NotFound) => break,
             Err(e) => return Err(e),
```

With the guard, the Creusot robustness proof of `parse_ebr_chain` discharges fully.
