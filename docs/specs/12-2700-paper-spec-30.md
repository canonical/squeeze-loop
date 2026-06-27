# 12-2700-paper-spec-30 — paper-impl loop, circle 30: review1 mechanical + anonymization fixes

STATUS: DONE
Second circle of the review1 response cycle. Three small, self-contained,
user-decided/mechanical fixes (no new content, no claims).

## Changes
- **G2 (decided: anonymize).** Author block replaced with "Anonymous Author(s) /
  Affiliation withheld for double-blind review". The deanonymizing name,
  affiliation, email, and GitHub URL are removed for double-blind submission; the
  full author block remains recoverable from git history (set in an earlier
  circle).
- **G1 (decided: hardcode in abstract only).** The abstract's
  "\ref{item:laststab}~stabilizers" -> "thirteen stabilizers", so standalone
  abstract extraction / arXiv metadata renders the number instead of a broken ref
  (review §"Mechanical"). The body keeps \ref{item:laststab} in BOTH remaining
  sites (intro contribution (iv), §stabilizers), so the count stays drift-proof
  where it matters; if a 14th rule were added, the body refs would show 14 against
  the abstract's "thirteen" -- a visible same-build mismatch, not a silent lie.
- **G5.** Removed the unused `extract` block-quote environment (dead code; only the
  definition existed, no \begin{extract} anywhere).

## Additivity
No claim or number altered. Anonymization removes author metadata; the abstract
number is unchanged (13), now literal there; dead code removed.

## Effect on numbers
- reflexive.tex regenerated: ResReflexSpecDocs -> 29 (this circle). All other
  macros unchanged.

## Gates
- Gate B: build green (18 pp), all cites/refs/macros resolve, no bibtex warnings.
- Determinism: reflexive harness re-run byte-identical.
- No ledger / manuscript-defect change.

## Cycle status
Done so far: A1 (Gate A caption, c29), G1/G2/G5 (c30). Next queued: F1 (re-add
appendix with an instantiated squeeze table + delegation-prompt excerpt -- decided
yes), then G4 (ASCII pipeline -> tikz figure) and C11 (preprint->venue citation
metadata), then the formal-core / redundancy / framing / literature / methodology
circles per docs/12-2600-review1-response-plan.md.
