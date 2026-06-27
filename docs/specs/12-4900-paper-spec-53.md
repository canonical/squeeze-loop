# 12-4900-paper-spec-53 — paper-impl loop, circle 53: polish the evaluation protocol section (coupling scope)

STATUS: APPROVED
Polish of sec:eval "Protocol status" fixing a scope imprecision in H2's discharge
statement. It reads "[H2] is discharged on the four executable instances ---
seeded-defect detection of ResAllCaught/ResAllSeeded ... versus ResAllBarrierOff/...,
and evidence--implementation coupling reported PER INSTANCE (Figure 2)". But H2 has
two parts measured on different sets: seeded-defect detection is on all four
instances (15/15 vs 0/15), while coupling is only on the THREE text-producing
instances -- D (deductive) has no text coupling (n/a). "Per instance", right after
"the four executable instances", reads as all four. Synthesis and Figure 2 are
careful ("three text-producing instances"; "H2, on three constructed instances");
align this line.

## Changes
- tex/paper.tex sec:eval "Protocol status" (~line 1041): "evidence--implementation
  coupling reported per instance (Figure~\ref{fig:coupling})" -> "...reported on the
  three text-producing instances (Figure~\ref{fig:coupling})".
- Regenerate reflexive.tex (ResReflexSpecDocs 52->53 for this new spec doc).

## Gates
- Gate B: build green; no new \cite/number/macro/CLM; fig:coupling ref resolves;
  previously-SUPPORTED text byte-stable outside the one phrase.
- Gate C: ledger unchanged (CITE 46 + RESULT 28); reflexive macros reconcile;
  reflexive re-run byte-identical.

## Note
Accuracy fix: distinguishes H2's all-four detection result from its
three-instance coupling result, consistent with sec:synthesis and the Figure 2
caption (coupling is undefined on the deductive instance; independence there is
enforced by the axiom audit).
