# 12-4300-paper-spec-47 — paper-impl loop, circle 47: polish the evaluation protocol section

STATUS: APPROVED
Polish of sec:eval that removes the section's only hand-typed numbers, enforcing
protocol rule 3 (no digit typed by hand; every number from a generated macro). The
"Protocol status" paragraph states H2's discharge as "seeded-defect detection of
100\% with the barrier on versus 0\% with it off" -- two hand-typed percentages.
The same aggregate result is already macro-bound everywhere else (synthesis line:
ResAllCaught/ResAllSeeded with the barrier on, ResAllBarrierOff/ResAllSeeded off;
reflexive section identically). Bind this occurrence to the same macros (15/15 vs
0/15), matching the paper's standard form and the single source of truth.

## Changes
- tex/paper.tex sec:eval "Protocol status" (~line 1039): "seeded-defect detection
  of 100\% with the barrier on versus 0\% with it off" -> "seeded-defect detection
  of \ResAllCaught/\ResAllSeeded{} with the barrier on versus
  \ResAllBarrierOff/\ResAllSeeded{} with it off".
- Regenerate reflexive.tex (ResReflexSpecDocs 46->47 for this new spec doc).

## Gates
- Gate B: build green; the two hand-typed percentages replaced by existing macros
  (ResAllCaught 15, ResAllSeeded 15, ResAllBarrierOff 0), no NEW macro/cite/number/
  CLM; previously-SUPPORTED text byte-stable outside the one sentence; sec:eval now
  has zero hand-typed figures.
- Gate C: ledger unchanged (CITE 46 + RESULT 28); synthesis + reflexive macros
  reconcile; reflexive re-run byte-identical.

## Note
Discipline alignment, not a value change: 15/15 and 0/15 are exactly 100% and 0%,
but now derived from the regenerated synthesis macros rather than typed, so the
figure cannot silently go stale if the aggregate changes. Matches how synthesis and
sec:reflexive already state the same result.
