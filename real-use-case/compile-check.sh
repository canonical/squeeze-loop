#!/usr/bin/env bash
#
# compile-check.sh — try to compile each stripped .rs file under $SRCDIR as a
# standalone library crate, and report which ones compile ("where they can").
#
# Each file is type-checked independently with `rustc --emit=metadata` (no
# codegen). Files that reference Creusot-only items (Int, Seq, Perm, ...) or
# leftover ghost variables are expected to fail; that is the point of the report.
#
# Configurable via environment (see the Makefile):
#   SRCDIR    directory to scan         (default: training-data)
#   BUILDDIR  where artifacts/logs go   (default: build/cc)
#   RUSTC     compiler invocation       (default: rustc +nightly-2026-04-21)
#   EDITION   Rust edition              (default: 2021)
#   JOBS      parallel jobs             (default: nproc)

set -uo pipefail

SRCDIR="${SRCDIR:-training-data}"
BUILDDIR="${BUILDDIR:-build/cc}"
RUSTC="${RUSTC:-rustc +nightly-2026-04-21}"
EDITION="${EDITION:-2021}"
JOBS="${JOBS:-$(nproc 2>/dev/null || echo 4)}"

if [ ! -d "$SRCDIR" ]; then
  echo "compile-check: source dir '$SRCDIR' not found" >&2
  exit 2
fi

mkdir -p "$BUILDDIR"
# Clear stale failure logs so a present *.err always means a current failure.
find "$BUILDDIR" -name '*.err' -delete 2>/dev/null || true

compile_one() {
  f="$1"
  rel="${f#"$SRCDIR"/}"
  base="${rel%.rs}"
  name="c_$(printf '%s' "$base" | tr -c 'A-Za-z0-9_' '_')"
  out="$BUILDDIR/$base"
  mkdir -p "$(dirname "$out")"
  if $RUSTC --edition "$EDITION" --crate-type lib --crate-name "$name" \
       --cap-lints allow --emit=metadata -o "$out.rmeta" "$f" 2> "$out.err.tmp"; then
    rm -f "$out.err.tmp" "$out.err"
  else
    mv -f "$out.err.tmp" "$out.err"
    rm -f "$out.rmeta"
  fi
}
export -f compile_one
export SRCDIR BUILDDIR RUSTC EDITION

find "$SRCDIR" -name '*.rs' -print0 \
  | sort -z \
  | xargs -0 -P "$JOBS" -I{} bash -c 'compile_one "$@"' _ {}

# ---- report ----
total=$(find "$SRCDIR" -name '*.rs' | wc -l | tr -d ' ')
mapfile -t errs < <(find "$BUILDDIR" -name '*.err' | sort)
fail=${#errs[@]}
pass=$((total - fail))

report="$BUILDDIR/REPORT.txt"
{
  echo "Compile check — $SRCDIR"
  echo "compiler: $RUSTC   edition: $EDITION"
  echo "==================================================="
  printf "compiled: %d / %d        failed: %d\n" "$pass" "$total" "$fail"
  echo
  if [ "$fail" -gt 0 ]; then
    echo "--- failures by first error code ---"
    grep -rhoE 'error\[E[0-9]+\]|error: ' "$BUILDDIR" --include='*.err' \
      | sort | uniq -c | sort -rn
    echo
    echo "--- failing files (first error) ---"
    for e in "${errs[@]}"; do
      src="$SRCDIR/${e#"$BUILDDIR"/}"; src="${src%.err}.rs"
      first=$(grep -m1 -E '^error' "$e" | sed 's/^/    /')
      echo "FAIL $src"
      [ -n "$first" ] && echo "$first"
    done
  fi
} | tee "$report"

echo
echo "Full per-file error logs: $BUILDDIR/**/<name>.err"
echo "Report saved to:          $report"
exit 0
