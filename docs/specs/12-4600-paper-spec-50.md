# 12-4600-paper-spec-50 — paper-impl loop, circle 50: polish the related work (precise Voyager analogue)

STATUS: APPROVED
Polish of sec:sota fixing a cross-reference precision issue introduced in circle 41.
That circle added "Voyager's growing skill library is ... the closest prior analogue
to the generativity we later find the squeeze itself produces
(Section~\ref{sec:reflexive})". But Voyager's hallmark is a SKILL LIBRARY -- agents
banking reusable skills over time -- whose most literal analogue in this paper is
the AGENT skill accumulation of sec:eval (skills accumulating across cycles, circles
37+), NOT the paper's reflexive category-carving in sec:reflexive (which is
generativity but not a skill library). Re-aim the analogy at sec:eval and sharpen
"generativity" to "skill ... accumulate across cycles", the precise match.

## Changes
- tex/paper.tex sec:sota single-agent-loops subsection (~line 210-213): "Voyager's
  growing skill library is, moreover, the closest prior analogue to the generativity
  we later find the squeeze itself produces (Section~\ref{sec:reflexive})." ->
  "Voyager's growing skill library is, moreover, the closest prior analogue to the
  skill our own squeezed agents accumulate across cycles (Section~\ref{sec:eval})."
- Regenerate reflexive.tex (ResReflexSpecDocs 49->50 for this new spec doc).

## Gates
- Gate B: build green; no new \cite/number/macro/CLM; sec:eval ref resolves;
  previously-SUPPORTED text byte-stable outside the one sentence. Still a contrast
  (Voyager lit-plane skill library vs our agent skill accumulation), not a
  two-plane blend; still the understatement direction (Voyager credited as closest
  analogue).
- Gate C: ledger unchanged (CITE 46 + RESULT 28); reflexive macros reconcile;
  reflexive re-run byte-identical.

## Note
Precision fix: the literature-plane fact (Voyager accumulates a skill library,
SUPPORTED by bib/records/wang2023voyager.md §2.2/§2.3) is unchanged; only the
forward reference now targets the matching result (agent skill accumulation,
sec:eval, CLM-075) instead of the looser reflexive generativity.
