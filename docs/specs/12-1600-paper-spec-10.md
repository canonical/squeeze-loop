# 12-1600-paper-spec-10 — paper-impl loop, circle 10: executable instances become the case studies

STATUS: DONE
Pivot the paper to rest entirely on the three executable, reproducible instances;
remove the internal field engagements; add the cross-terrain figure, the per-gate
analysis, and the Gödel--Escher--Bach motif.

## Removal — P-series / HAPPY / typing (and the companion guides)
The three internal field engagements (and every verbatim quote from
pycsl-prereqs-impl.md / happy-roadmap-impl.md / typing-global-impl.md) are
removed; the three executable instances (A/B/C) now ARE the archetype case
studies (option 4, with the mapping inverted by the removal). Edited:
- §4.1--4.3 (the field-engagement subsections + their `extract` quotes) deleted;
  the executable instances retitled "Archetype A/B/C --- ...".
- Table 2 "Case study" row -> "Executable instance" (tabular analytics / refund
  agent / API contract guard).
- Intro PyCSL paragraph + companion-guides footnote removed; abstract,
  contribution (iii), §2.4 (deductive case-study claim), §3.3 (the author-
  separation extract -> inline prose), Figure 1 caption, Gate B wording,
  stabilizers 3 and 6, the evaluation intro / coupling bullet / seeded-defect
  bullet / tasks, the limitations provenance, and the conclusion all reworded.
- Appendix A (worker definitions) and Appendix B (the three closing rules) ---
  both entirely guide content --- deleted; the `app:dod`/`app:worker` refs removed.
- Verified: zero residual P-series/HAPPY/STRIDE/PyCSL/typing mentions; build green.

## do 1 --- coupling-vs-detection figure
New Figure~\ref{fig:coupling} (pgfplots): evidence-implementation coupling (x) vs
seeded-defect detection (y), one point per instance, barrier on (100\%) vs off
(0\%). Numeric coordinates from new `\ResCoupling*val` macros emitted by
verify/coupling_measure.py. Added \usepackage{pgfplots}.

## do 3 --- per-gate cross-terrain analysis
New paragraph in §\ref{sec:synthesis}: which gate carries the soundness load per
archetype --- Gate B / total additivity (A), the coherent-and-wrong guard
defended by independence (B), the no-blend cross-check (C).

## Gödel, Escher, Bach
Added `hofstadter1979geb` (reading record, read: SECONDARY) and cited it in the
reflexive section: producing the paper under its own strategy is a "strange loop"
(the method's output includes a verification of the method). CLM-056.

## Gates
- Gate B: build green (18 pp, was 21), all cites/refs/macros resolve, no bibtex
  warnings; baudin_acsl now uncited (harmless; entry + record retained).
- The companion guides in bib/archive/ are retained but no longer cited.

## Honest scope
The paper now rests on three constructed, deterministic, reproducible instances;
still not the controlled, cross-model study (§\ref{sec:eval}).
