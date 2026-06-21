# 12-4500-paper-spec-49 — paper-impl loop, circle 49: polish the conclusion (referent disambiguation)

STATUS: APPROVED
Polish of sec:conclusion fixing a referent ambiguity that circle 38 introduced.
Circle 38 added the skill-accumulation sentence ("Nor was this confined to the
paper's self-application: ... the squeezed agents themselves, whose skill bases
enrich ...") immediately before "The resulting self-applying, category-carving,
self-sustaining loop instantiates the structural form of a Hofstadterian strange
loop". With the agent-skill sentence now adjacent, "The resulting ... loop" can be
misread as resulting from the agent skill loops -- but the strange-loop claim must
stay tied to the PAPER's self-application, not the agents (the scoping circle 39
deliberately preserved in the abstract: the agent skill loops are NOT claimed to be
strange loops). Anchor the referent explicitly.

## Changes
- tex/paper.tex sec:conclusion (~line 1290-1291): "The resulting self-applying,
  category-carving, self-sustaining loop instantiates the structural form ..." ->
  "The paper's own self-applying, category-carving, self-sustaining loop
  instantiates the structural form ...". Drops the ambiguous "resulting"; binds the
  strange-loop claim to the paper's self-application, away from the agent skill
  loops.
- Regenerate reflexive.tex (ResReflexSpecDocs 48->49 for this new spec doc).

## Gates
- Gate B: build green; no new \cite/number/macro/CLM; previously-SUPPORTED text
  byte-stable outside the one conclusion phrase; meaning preserved (restatement).
- Gate C: ledger unchanged (CITE 46 + RESULT 28); reflexive macros reconcile;
  reflexive re-run byte-identical.

## Note
Overclaim-guard / clarity, not new content: keeps the strange-loop (Tier-2,
structural) claim scoped to the paper's self-applying construction, consistent with
the abstract (circle 39), the reflexive section, and paper_upper_bound.md. The
agent skill loops remain a generativity witness, never a strange-loop claim.
