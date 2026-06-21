# Issue 4 — `grub::parse_submenu`: unbounded native recursion (stack-overflow DoS)

- **Component:** `lace-util/src/grub.rs` (`GrubParser::parse_submenu`)
- **Class:** unbounded recursion → native stack overflow → process abort (DoS)
- **Severity:** Medium (pre-OS DoS from a malicious `grub.cfg`; especially acute on the small fixed stack of a `no_std`/UEFI build, where `lace-speedboot` parses configs from every scanned disk)
- **Reachable from:** a `grub.cfg` on any disk `lace-speedboot` scans.

## Summary

`parse_submenu`, on encountering a nested `submenu` word at `brace_depth == 1`, recursively
calls `self.parse_submenu()` with **no depth limit**:

```rust
// grub.rs (parse_submenu body)
Token::Word(w) if brace_depth == 1 => match w.as_str() {
    ...
    "submenu" => {
        if let Some(entry) = self.parse_submenu() {   // <-- self-recursion, no cap
            entries.push(entry);
        }
    }
```

Adversarial input of deeply nested submenus drives native recursion until the stack
overflows:

```
submenu 'x' { submenu 'x' { submenu 'x' { ... (tens of thousands deep) ... } } }
```

A kilobyte-scale input (a few tens of thousands of nesting levels) aborts the process; on a
fixed UEFI stack the threshold is far lower. (`menuentry` does not self-recurse into nested
blocks — only `submenu` does.)

**Secondary (debug-only):** `brace_depth += 1` is an `i32` add; ~2.1 billion unmatched `{`
(a ~2 GB input) overflows it in debug / wraps in release. Impractical, noted for completeness.

## How it was found

Call-graph analysis — Creusot is **blocked** on `grub.rs` (creusot-std lacks extern-specs
for `str::lines`/`Chars`/`Peekable`, and `Vec<MenuEntry>` triggers an "Illegal recursive
type"), so a stack-depth property is out of its reach here; this is a source-level finding.

## Draft patch

Thread an explicit depth counter and cap it. **Care:** a naive early `return None` *before*
consuming the `submenu` token would re-encounter it and **infinite-loop**. The fix consumes
`submenu` first, then bails at the cap — the caller's brace-counting loop then skips the
over-deep body (nested submenus past the cap are simply not parsed, never executed).

```diff
--- a/lace-util/src/grub.rs
+++ b/lace-util/src/grub.rs
@@
-                    "submenu" => {
-                        if let Some(entry) = self.parse_submenu() {
-                            entries.push(entry);
-                        }
-                    }
+                    "submenu" => {
+                        if let Some(entry) = self.parse_submenu(0) {
+                            entries.push(entry);
+                        }
+                    }
@@
-    fn parse_submenu(&mut self) -> Option<MenuEntry> {
-        // Consume 'submenu'
-        self.advance();
+    fn parse_submenu(&mut self, depth: usize) -> Option<MenuEntry> {
+        const MAX_SUBMENU_DEPTH: usize = 32;
+        // Consume 'submenu'
+        self.advance();
+        if depth >= MAX_SUBMENU_DEPTH {
+            // Refuse to recurse further. 'submenu' is already consumed, so the
+            // caller's brace-counter skips this body (its nested submenus are at
+            // brace_depth > 1 and are not parsed). Prevents stack-overflow DoS.
+            return None;
+        }
@@
-                    "submenu" => {
-                        if let Some(entry) = self.parse_submenu() {
-                            entries.push(entry);
-                        }
-                    }
+                    "submenu" => {
+                        if let Some(entry) = self.parse_submenu(depth + 1) {
+                            entries.push(entry);
+                        }
+                    }
```

(The two `submenu` arms are the top-level `parse()` call site and the recursive call inside
`parse_submenu`'s own body.)
