# Issue 1 — `peimage::parse_pe`: `e_lfanew - 64` subtraction underflow (panic on crafted PE)

- **Component:** `lace-util/src/peimage.rs:223` (`parse_pe`)
- **Class:** unchecked subtraction underflow → out-of-bounds slice → panic / DoS
- **Severity:** High (pre-OS DoS; the PE parser is used by `lace-stubble`, `lace-platform`, and `pewrap`)
- **Reachable from:** any PE handed to `parse_pe` — a malformed `.efi` on the ESP, a stubble image, an embedded section.

## Summary

The end index of a raw slice is an **unchecked subtraction** of the DOS-header size from
the attacker-controlled `e_lfanew` field. Nothing on the path forces `e_lfanew >= 64`, so a
small `e_lfanew` underflows.

```rust
// peimage.rs:223
let dos_data = &dos_data[..dos_hdr.e_lfanew as usize - size_of::<DosHeader>()];
```

`size_of::<DosHeader>()` is 64. The earlier validation only checks that the NT headers fit
*at* offset `e_lfanew` (`s.get(e_lfanew..)`); it never checks `e_lfanew` against the
DOS-header size, so an attacker can overlap the NT headers with the DOS-header region.

## Minimal adversarial input (274 bytes)

- `"MZ"` at offset 0; `e_lfanew = 10` (u32 LE @ 60); `"PE\0\0"` at offset 10;
  `size_of_optional_header = 240` (@ 30); optional `magic = 0x20b` (@ 34);
  `number_of_sections = 0` (@ 16).
- Passes every validation, reaches line 223 where `10 - 64`:
  - **debug:** `panicked: attempt to subtract with overflow`
  - **release:** wraps to `18446744073709551562`, then `&dos_data[..HUGE]` → `range end index … out of range` panic.

## How it was found

Specifying `parse_pe` for total robustness left exactly one `integer overflow` VC unproved
(`vc_parse_pe`, 30/31 discharged). Adding `if e_lfanew < 64 { Err }` closes all goals —
i.e. the unproved goal *is* the missing `e_lfanew >= size_of::<DosHeader>()` fact.

## Draft patch

```diff
--- a/lace-util/src/peimage.rs
+++ b/lace-util/src/peimage.rs
@@ -220,7 +220,11 @@
-    let dos_data = &dos_data[..dos_hdr.e_lfanew as usize - size_of::<DosHeader>()];
+    let dos_data_end = (dos_hdr.e_lfanew as usize)
+        .checked_sub(size_of::<DosHeader>())
+        .ok_or(PeError::Truncated)?;
+    let dos_data = dos_data
+        .get(..dos_data_end)
+        .ok_or(PeError::Truncated)?;
```

`checked_sub` rejects `e_lfanew < 64`; `.get(..)` (instead of the raw `[..]`) makes the
slice end fallible rather than panicking. With this guard the Creusot robustness proof of
`parse_pe` discharges fully.
