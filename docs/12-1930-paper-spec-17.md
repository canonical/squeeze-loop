# 12-1930-paper-spec-17 — paper-impl loop, circle 17: tighten the evaluation section

STATUS: DONE
Editorial circle (no new evidence). §sec:eval had grown to ~12 paragraphs over
circles 11-16, with four separate executed-experiment paragraphs (pilot-1,
self-authorship, weaker-model, powered study) repeating the same caveats
(underpowered, no-cherry-pick, guarantee-not-hope, near-zero error rate).

## Changes (consolidation; no claim or number altered)
- The four executed-experiment paragraphs (Pilot execution + two follow-ons +
  Powered attempt) collapsed into ONE "What we have run" paragraph: barrier-on vs
  barrier-off no difference (\ResPilotTasks), then self-authorship / weaker model
  / powered study yielding \ResPilotTwoBuggy / \ResPilotThreeBuggy / \ResStudyBuggy
  buggy impls (McNemar p=\ResStudyP), the near-zero-error-rate diagnosis, the
  no-cherry-pick stance, and the guarantee-not-hope framing --- once each.
- Intro paragraph trimmed: removed the restated synthesis data point (it lives in
  §sec:synthesis and Protocol status); now sets up the section in three sentences.
- Independence-measures coupling bullet trimmed: points to Figure~\ref{fig:coupling}
  instead of restating the A/B/C numbers; fixed a stale "two executable instances"
  (it listed three).
- "Protocol status" and "Toward a real-bug study" paragraphs kept as-is.

## Additivity (declared diff, nothing dropped)
Every result is preserved: the executed-pilot numbers via \ResPilot*/\ResStudy*
macros, the coupling via Figure 2, the SWE-bench wiring via \ResSwe*. The macros
whose §7 usages were removed (\ResPilotDetectionOn/Off, \ResPilotValidity*,
\ResCouplingA/B/C in the bullet) remain defined and are still used elsewhere
(Figure 2, §4); no number changed, no finding lost. Section paragraph count
12 -> 10; page count 19 -> 18.

## Gates
- Gate B: build green (18 pp), all cites/refs/macros resolve, no bibtex warnings.

## Note
No ledger change: no claim added or modified, only prose consolidated. This is a
quality/altitude edit, the kind the simplify pass targets.
