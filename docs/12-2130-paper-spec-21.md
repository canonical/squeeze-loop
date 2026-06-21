# 12-2130-paper-spec-21 — paper-impl loop, circle 21: polish the limitations section

STATUS: DONE
Editorial circle (no new evidence). Polish §sec:limitations for accuracy.

## Audit
- Checked the H4 reference in "Cost and latency" ("hypothesis H4 conjectures ...
  where this amortizes"): H4 (amortization) is still defined in §sec:eval
  (line ~999). NOT stale -- kept as is.
- All other entries (Shared priors / Knight--Leveson, single point of judgment,
  executable lower bound required, terminology) accurate -- kept.

## Change (one accuracy fix)
- "Provenance of the evidence" tail: was "the generalization claim rests on the
  evaluation of Section~\ref{sec:eval}, which is future work." After circles
  19-20, §eval is operationalized + piloted; only the POWERED study is future
  work. Now: "... which is operationalized and piloted but not yet powered ---
  the pilots met a near-zero natural error rate, leaving the effect size to a
  real-bug study." Matches the abstract/conclusion framing.

## Additivity
No new claim: the sentence restates §sec:eval (pilots run, near-zero error rate,
real-bug study pending) and the abstract/conclusion. No number altered.

## Gates
- Gate B: build green (18 pp), all cites/refs/macros resolve, no bibtex warnings.
- No ledger change (prose-only).
