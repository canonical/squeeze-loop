#!/usr/bin/env bash
# Regenerate annotate/VERDICTS.md (human summary) from annotate/.verdicts.tsv
# (machine log: <file>\t<verdict>\t<notes>). Verdicts: PROVED | PARTIAL(..) |
# FAILED | TRIVIAL. Used by the creusot-monitoring batch loop.
set -euo pipefail
TSV="${1:-annotate/.verdicts.tsv}"
OUT="${2:-annotate/VERDICTS.md}"
touch "$TSV"
total=$(find annotate -name '*.rs' | wc -l | tr -d ' ')
done=$(grep -c . "$TSV" || true)
proved=$(awk -F'\t' '$2=="PROVED"{c++} END{print c+0}' "$TSV")
partial=$(awk -F'\t' '$2 ~ /PARTIAL/{c++} END{print c+0}' "$TSV")
failed=$(awk -F'\t' '$2=="FAILED"{c++} END{print c+0}' "$TSV")
trivial=$(awk -F'\t' '$2=="TRIVIAL"{c++} END{print c+0}' "$TSV")
{
  echo "# creusot-monitoring run — analyze all \`*.rs\` in \`annotate/\`"
  echo
  echo "- **Guidance (U):** specify thoroughly (panic/overflow/out-of-bounds freedom + functional intent); no network access to disregard."
  echo "- **Ground truth (L):** \`cargo creusot\` discharge (Creusot -> Why3 -> SMT)."
  echo "- **Scheduler:** 241 independent single-file leaves; processed in parallel batches of 10 \`creusot-sl\` sub-agents."
  echo
  echo "**Progress: $done / $total processed** — PROVED $proved, PARTIAL $partial, FAILED $failed, TRIVIAL(empty) $trivial."
  echo
  echo "| File | Verdict | Notes |"
  echo "|---|---|---|"
  sort "$TSV" | awk -F'\t' '{printf "| `%s` | %s | %s |\n", $1, $2, $3}'
} > "$OUT"
echo "wrote $OUT ($done/$total)"
