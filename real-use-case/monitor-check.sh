#!/usr/bin/env bash
# Base-SL monitor faithfulness check: an annotated file must contain the SAME
# executable code as the original stripped corpus — the annotator may only ADD
# Pearlite specs, never invent/alter code. Strip annotations from annotate/<rel>
# and compare to training-data/<rel>. Prints ACCEPT | FABRICATED | NOORIG.
set -uo pipefail
rel="$1"
orig="training-data/$rel"
cur="annotate/$rel"
[ -f "$orig" ] || { echo "NOORIG"; exit 0; }
[ -f "$cur" ]  || { echo "MISSING"; exit 0; }
tmp=$(mktemp -d)
mkdir -p "$tmp/$(dirname "$rel")"
cp "$cur" "$tmp/$rel"
/tmp/strip-creusot/target/release/strip-creusot "$tmp" >/dev/null 2>&1 || true
/tmp/strip-creusot/target/release/strip-creusot "$tmp" --unwrap-types >/dev/null 2>&1 || true
norm() { grep -vE '^\s*$' "$1" | sed 's/[[:space:]]\+/ /g; s/^ //; s/ $//'; }
if diff -q <(norm "$tmp/$rel") <(norm "$orig") >/dev/null 2>&1; then
  echo ACCEPT
else
  echo FABRICATED
fi
rm -rf "$tmp"
