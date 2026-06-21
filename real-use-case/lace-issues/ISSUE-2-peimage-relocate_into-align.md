# Issue 2 — `peimage::relocate_into`: `align_up!` divide-by-zero and multiply overflow

- **Component:** `lace-util/src/peimage.rs:293-296` (`relocate_into`)
- **Class:** divide-by-zero panic; u32 multiply overflow (panic in debug, **silent wrap → wrong memory layout** in release)
- **Severity:** High (pre-OS panic; release-mode wrong-length layout is a memory-correctness hazard in the loader path)
- **Reachable from:** any PE with a crafted optional/section header passed to `relocate_into`.

## Summary

`relocate_into` aligns each section's virtual size up to `section_alignment`, which is read
straight from the **attacker-controlled** optional header and never validated:

```rust
// peimage.rs:293
let virt_size = align_up!(
    shdr.virtual_size,
    self.nt_hdrs.optional_header.section_alignment
) as usize;
```

`align_up!(v, a)` expands to `v.div_ceil(a) * a` (`lace-util/src/lib.rs:66`). Two independent bugs:

- **(A) divide-by-zero.** `section_alignment == 0` ⇒ `virtual_size.div_ceil(0)` panics in
  *all* profiles.
- **(B) multiply overflow.** `div_ceil(a) * a` overflows `u32` (e.g. `virtual_size = u32::MAX`,
  `section_alignment = 0x1000` ⇒ `0x100000 * 0x1000 = 0x1_0000_0000 > u32::MAX`):
  **debug** panics; **release** silently wraps to a wrong `virt_size`, after which the
  subsequent `get_mut` copy/fill operate on a corrupted length.

This also undermines the architecture report's "PE loader rejects misaligned images (W^X)"
claim at the alignment-arithmetic layer.

## How it was found

Specifying `relocate_into` for total robustness left two independent unproved VCs
(`division by zero` and `integer overflow`); both vanish under the guard below.

## Draft patch

`u32::checked_next_multiple_of` returns `None` for **both** a zero alignment *and* overflow,
so it fixes (A) and (B) in one line:

```diff
--- a/lace-util/src/peimage.rs
+++ b/lace-util/src/peimage.rs
@@ -290,10 +290,10 @@
-            // Virtual size must be aligned to section alignment, the linker is not required to align this for us.
-            let virt_size = align_up!(
-                shdr.virtual_size,
-                self.nt_hdrs.optional_header.section_alignment
-            ) as usize;
+            // Virtual size must be aligned to section alignment, the linker is not required to align this for us.
+            // `checked_next_multiple_of` returns None on a zero alignment OR on overflow.
+            let virt_size = shdr.virtual_size
+                .checked_next_multiple_of(self.nt_hdrs.optional_header.section_alignment)
+                .ok_or(PeError::Truncated)? as usize;
```

(Equivalently, validate `section_alignment` is a non-zero power of two when the optional
header is first parsed, since the PE spec requires `section_alignment >= file_alignment` and
a power of two — that would reject these images earlier and protect every later use.)
