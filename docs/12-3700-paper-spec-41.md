# 12-3700-paper-spec-41 — paper-impl loop, circle 41: polish the related work

STATUS: APPROVED
Polish of sec:sota (State of the Art). The section is already dense and every cite
is record-bound, so the polish stays strictly in the literature plane. The one
valuable improvement: since circle 37 made skill accumulation / generativity a
prominent contribution (vii), the single-agent-loops subsection -- which already
cites Voyager's skill acquisition -- should position Voyager as the closest prior
analogue to that finding. This is the SAFE direction (it credits prior work,
understating our novelty) and is a contrast, NOT the two-plane blend the strategy
forbids: it states Voyager's growing skill library (literature plane, SUPPORTED by
the record) and forward-points to our generativity result (Section~\ref{sec:reflexive}),
without fusing them into "prior work shows X and our results confirm it."

## Changes
- tex/paper.tex, sec:sota single-agent-loops subsection (~line 208-210): extend the
  "the loops are correspondingly robust" sentence with a clause naming Voyager's
  growing skill library as the closest prior analogue to the generativity the
  squeeze itself produces (forward ref to Section~\ref{sec:reflexive}).
- Regenerate reflexive.tex (ResReflexSpecDocs 40->41 for this new spec doc).

## Evidence backing (verifier check)
- "Voyager's growing skill library": bib/records/wang2023voyager.md, anchored
  quotes from Voyager §2.2/§2.3 ("add this new skill to the skill library";
  "composing simpler programs ... compounds Voyager's capabilities ... over time")
  -- record VERDICT SUPPORTED.
- "the generativity we later find the squeeze itself produces": forward ref to
  sec:reflexive, contribution (vii), already SUPPORTED in the body.

## Gates
- Gate B: build green; no new \cite (wang2023voyager already cited + recorded), no
  number, no new macro, no new CLM; previously-SUPPORTED text byte-stable outside
  the one sota hunk; sec:reflexive ref resolves.
- Gate C: ledger unchanged (CITE 46 + RESULT 28); reflexive macros reconcile;
  reflexive re-run byte-identical.

## Note
No-blend check: the new clause separates the literature-plane fact (Voyager
accumulates a skill library) from the forward reference to our own finding; it does
not claim prior work confirms our result. Direction is understatement (Voyager
credited as the closest analogue), which the strategy explicitly permits.
