# 12-2230-paper-spec-23 — paper-impl loop, circle 23: polish the evaluation section (remove draft TODOs)

STATUS: DONE
Editorial circle (no new evidence). §sec:eval still carried 7 visible red
`\TODO{...}` markers (the macro rendered as bold red "[TODO: ...]"), draft
scaffolding that made a finished section look unfinished and, in the title case,
contradicted the now-honest operationalized framing (circles 16-22).

## Changes (7 TODOs resolved + dead macro removed)
- Section TITLE: "Proposed Evaluation Protocol \TODO{comparative runs pending
  model access}" -> "Proposed Evaluation Protocol". (Stale: the protocol is
  operationalized + piloted; the heading TODO contradicted that.)
- Protocol-status para: dropped the trailing "\TODO{execute the comparative runs
  ...}" -- redundant with the surrounding "wired as explicit stubs ... rather
  than fabricated numbers" and the What-we-ran / real-bug paragraphs.
- FOLDED INTO PROSE (substantive content kept, red marker removed):
  - Coherent-and-wrong rate: "...marginal value of the coverage gate (it requires
    logging the Gate~B and Gate~C verdicts independently)."
  - Ablations: "...measure the deltas ... (a full factorial would be too
    expensive, hence the one-factor-at-a-time list above)."
  - Tasks/baselines: "A remaining design choice is whether the coordinator and
    workers share a model family, which bears directly on the self-preference
    effect." (kept the real design question; dropped "negotiate compute budget".)
- DROPPED (pure logistics reminders, bullets already complete):
  - Defect-escape-rate audit-procedure/taxonomy TODO.
  - Human-audit recruitment/rubric/inter-rater TODO.
- Removed the now-dead `\newcommand{\TODO}` definition (line 22). A stray \TODO
  would now fail the build loudly rather than render red -- consistent with the
  gates-catch-it discipline.

## Additivity
No claim or number altered. The proposed-protocol design content is preserved
(measures, hypotheses, ablations, tasks, baselines, human audit all intact); only
draft working-notes were removed, two of them folded into prose where they carried
real content.

## Gates
- Gate B: build green (18 pp), all cites/refs/macros resolve, no bibtex warnings.
- grep: zero "TODO" occurrences in paper.tex.
- No ledger change (prose-only).
