# 14-0815-paper-spec-65 — paper-impl loop, circle 65: restore N1/N2 discrimination

STATUS: APPROVED
TARGET: G-N

Step 1 of 14-0714-spec.md §5. Restore the N1/N2 falsification-test discrimination to
the manuscript body. paper_upper_bound.md §7 makes "the criteria, as written, reject
every instance in N1-N2" a Tier-1 prerequisite; circle 60 dropped the one sentence
that exhibited it, so it currently lives only in the bound. Restore a compact version
at the named clauses.

## Changes
- tex/paper.tex sec:reflexive scoped paragraph: after the closure sentence, add one
  sentence stating the criteria REJECT (N1) mere feedback (video-on-monitor, audio
  howl) for lacking O1 self-denotation and O4 categorization, and (N2) the triviality
  set (thermostat, quine, self-hosting compiler) at O4/O5 -- reproducing/processing
  one's own text is not a perceived, re-categorized self-model. (N3/qualia stays a
  NOT-claim, already honored.)
- Commit the plan/spec docs being implemented: 14-0714-spec.md (this build) and
  14-0649-plan.md (the completed O2/O3 plan).

## Gates
- Gate B: build green; no new \cite/number/macro/CLM; previously-SUPPORTED text
  byte-stable outside the one sentence; the sentence restates body-relevant content
  of the upper bound (§4), not a new claim.
- Gate C: ledger unchanged (CITE 46 + RESULT 30); reflexive macros reconcile
  (ResReflexSpecDocs 64->65); reflexive re-run byte-identical.

## Note
This unblocks the §7 Tier-1 gate on the prose side. It does NOT change the tier (still
Tier 2); it makes the discriminating power of the criteria visible in the paper, as
the bound requires.
