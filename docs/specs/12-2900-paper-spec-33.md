# 12-2900-paper-spec-33 — paper-impl loop, circle 33: integrate the convergence findings

STATUS: DONE
Content circle. Integrates the 100-iteration convergence finding
(100-iteration-report.md) into §eval: the diversity loops are unbiased Monte-Carlo
estimators whose running mean converges to a fixed population rate (LLN), not drift.

## Why
Extends circle 32. The level-up paragraph established that random sampling restores
a varying trial; this adds the natural follow-up -- running the loop longer
*converges* the estimate -- and makes it recomputable.

## Recomputable anchor (the discipline point)
The convergence is demonstrated on the REFUND terrain (B), the one case whose
population error rate is computable EXACTLY and entirely in the Python standard
library (no Coq, no warehouse): enumerate all 100 discussions x 5 characters ->
342/500 = exact rate; B's seeded Monte-Carlo then converges onto it. A/C/D show the
same behaviour (D needs the kernel), reported in 100-iteration-report.md; B is the
recomputable anchor cited in the paper.

## Changes
- NEW generator verify/convergence_measures.py -> tex/macros/convergence.tex
  (computes B's exact population 342/500 and runs the seeded 100-cycle Monte-Carlo;
  pure Python, byte-identical on re-run). Preamble \input added; added to
  src/paper/_paperlib.py GENERATORS.
- §eval "Enriching the upper bound" paragraph extended: each loop is an unbiased
  estimator; the refund rate is exactly \ResConvBExactNum/\ResConvBExactDen (=
  \ResConvBExpected of \ResConvSample) and the Monte-Carlo gap shrinks from
  \ResConvBGapTen at ten cycles to \ResConvBGapHundred at \ResConvCycles --
  sampling noise around a constant rate, not drift; this fixes the sample size a
  powered study needs.
- Ledger: CLM-071 RESULT (the convergence finding, bound to
  verify/convergence_measures.py). RESULT 23 -> 24.

## Numbers (all macro-driven, recomputable with stdlib only)
ResConvCycles 100, ResConvSample 20, ResConvBExactNum 342, ResConvBExactDen 500,
ResConvBExpected 13.7, ResConvBMeanTen 14.5, ResConvBMeanHundred 13.6,
ResConvBGapTen 0.8, ResConvBGapHundred 0.1.

## Additivity
No prior claim altered. Adds the convergence result; the gradient claim stays OPN
(CLM-070, unchanged). Ledger +1 RESULT (23 -> 24).

## Gates
- Gate B: build green, all cites/refs/macros resolve, no bibtex warnings.
- Gate C: ledger RESULT (24) == regenerated ResReflexResultRows (24).
- Determinism: convergence_measures.py re-run byte-identical (pure Python, seeded).
