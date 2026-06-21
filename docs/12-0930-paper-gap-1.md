# 12-0930-paper-gap-1 — literature-plane overclaims (Gate C, SoTA section)

STATUS: DONE
Observed by: coordinator-driven literature verification pass (§3 lit plane)
Section: W-sota (`tex/paper.tex` §2, State of the Art)
Failure codes: F3 (overclaim) ×2

## Divergence

A verification pass re-opened every cited source in §2 and judged whether the
manuscript sentence is supported by the source as written. Two sentences
claimed more than the verified source warrants.

### F3-a — CRITIC comparative stated above the source's level (§2.1)

- **Sentence (before):** "CRITIC \citep{gou2023critic} makes the comparison
  explicit: critiques grounded in external tools outperform purely intrinsic
  self-critique."
- **Finding:** The source frames external feedback as *crucial to
  self-improvement* (abstract level). The clean head-to-head comparative
  ("outperform purely intrinsic self-critique") is the manuscript's inference;
  it is borne out by the paper's tool-free baselines but is stated more
  strongly than the source asserts at the level the manuscript cites.
- **Fix:** Restated to the strongest source-supported claim: "...grounds
  critiques in external tools and finds such external feedback crucial to
  sustained self-improvement, where purely intrinsic self-critique falls
  short." (Understatement is the safe direction; §0 of the guide.)

### F3-b — debate full-context claim mis-applied to irving2018debate (§2.3)

- **Sentence (before):** "Multi-agent debate
  \citep{du2023debate,irving2018debate} deliberately shares full context ---
  appropriate for argument-checking, but orthogonal to independence of
  evidence."
- **Finding:** `irving2018debate` ("AI Safety via Debate") is *length-limited,
  judge-mediated* debate — agents make short statements before a judge — which
  is the opposite of full-context pooling. The full-context-sharing
  characterization is true of `du2023debate` (LLM instances exchanging full
  reasoning across rounds), not of `irving2018debate`. Lumping both under
  "shares full context" mis-states the foundational citation (borderline F2).
- **Fix:** Split the two: "Multi-agent debate
  \citep{irving2018debate,du2023debate} has agents argue before a judge; in its
  LLM realization \citep{du2023debate} the debaters exchange full reasoning
  across rounds --- deliberately shared context, appropriate for
  argument-checking but orthogonal to independence of evidence."

## Also tightened (precision, not a separate gap)

- `bai2022constitutional`: "generator and critic share weights and context" is
  exactly true only of CAI's self-critique stage (the RLAIF stage uses a
  separate preference model). Qualified to "in its self-critique stage."

## Resolution

All three edits applied to `tex/paper.tex`; build re-run green, every `\cite`
resolves, no other SUPPORTED sentence touched. See
`verify/reports/lit-verification-2026-06-12.md` for the full per-citation
verdict table.
