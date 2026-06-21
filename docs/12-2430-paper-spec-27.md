# 12-2430-paper-spec-27 — paper-impl loop, circle 27: polish the reflexive case study section

STATUS: DONE
Verification circle (the reflexive section's own numbers recompute). §sec:reflexive
is the section that claims the paper's numbers all recompute; this pass holds it to
that standard and found it stale -- the same regression circle 18 caught, recurred.

## Audit
- Prose is accurate and well-formed: cites hofstadter1979geb, uses \ref for all
  cross-references, frames the result honestly as "an illustration of the mechanism
  at n=1, not a controlled result."
- Defect enumeration: \ResReflexDefects=7 (\ResReflexDefectsLit=4,
  \ResReflexDefectsEvid=3) match verify/manuscript_defects.tsv (D1-D3,D7 literature;
  D4-D6 evidence). The prose lists 3 literature + 3 evidence examples under the
  hedge "they included ..." -- a DELIBERATE sample, with the macro as the
  authoritative count. Kept: this is the more disciplined design (prose =
  examples, macro = single source of truth, robust if the ledger grows). Listing
  all 7 would make the prose a second source of truth that drifts when the TSV
  changes -- the very failure mode the paper warns against.

## Change (numbers recompute; no claim or prose altered)
- Regenerated tex/macros/reflexive.tex via verify/reflexive_measures.py.
- Only \ResReflexSpecDocs changed: 16 -> 26. The other 9 macros are byte-identical
  (circles 19-26 added prose only -- no reading records, no ledger rows).
- Cause: circles 19-26 (the section-by-section polish sweep) are themselves
  paper-impl loop circles, each producing a per-circle spec doc; the reflexive
  count of "per-circle plans" had frozen at circle 18. The section now honestly
  reports the full loop including the polish phase.

## Strange-loop note (the fixed point)
This spec doc (spec-27) is itself counted in the \ResReflexSpecDocs it updates: the
trail was written first (-> 26 files on disk), then the harness regenerated
(-> macro = 26), then committed together, so the committed macro equals the
committed file count. A number that counts the document it lives in, settled at its
fixed point -- which is exactly the strange loop the section is about.

## Gates
- Gate B: build green (18 pp), all cites/refs/macros resolve, no bibtex warnings.
- Determinism: re-running the harness is byte-identical; on-disk spec-doc count
  (26) == \ResReflexSpecDocs (26).
- No ledger change (no new claim; regenerating a count is not a claim).
