# 14-1600-paper-spec-71 — paper-impl loop, circle 71: make Gate S first-class in the strategy's vocabulary

STATUS: APPROVED

Promote the skill-consistency check from a described-but-unnamed finding to a NAMED,
DEFINED gate in the strategy's gate vocabulary, alongside Gate A/B/C.

## Changes
- tex/paper.tex sec:mechanics: after the Gate A/B/C paragraph, add a paragraph defining
  **Gate S** (skill consistency). Honest framing: it is NOT a fourth per-item gate but a
  gate on a different cadence -- it fires when the loop ACCUMULATES a learned skill. A
  monitor squeeze (disjoint evidence base = the loop's own upper bound + executable
  oracle) differential-tests the skill and returns pass / carve-out / reject. It is the
  no-blend rule + disjointness principle (sec:disjoint) pushed down a level: a squeeze
  monitoring a squeeze. Demonstrated deterministically in sec:eval.
- tex/paper.tex sec:eval (circle-70 paragraph): NAME it -- "a monitor ..." becomes
  "Gate~S (the skill-consistency gate, Section~\ref{sec:mechanics})", so the finding
  references the now-defined gate.
- docs/glossary/gates.md: update the Gate S status -- now NAMED and DEFINED in
  sec:mechanics (no longer internal-only).

## Gates
- Gate B: build green; ResGateS* macros still used (no orphan); no new \cite/number/macro;
  previously-SUPPORTED text byte-stable outside the planned hunks.
- Gate C: ledger UNCHANGED (CITE 46 + RESULT 33) -- gate *definitions* are DEFN-typed and
  not individually ledgered (consistent with A/B/C); CLM-081 (the Gate S RESULT) already
  exists. Reflexive macros reconcile (ResReflexSpecDocs bumps for this spec doc).

## Note
Definitional/naming change; no new empirical claim. Keeps "three gates structure each
item" true (A/B/C are per-item) and adds Gate S as the distinct-cadence skill gate.
Modest scope: no new contribution row, no tier change.
