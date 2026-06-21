# 12-5500-paper-spec-59 — paper-impl loop, circle 59: novelty delta + base-rate honesty (review2 #3 + minor)

STATUS: APPROVED
Final planned review2 circle. (minor) Name the 3-part novelty delta crisply in one
place (SOTA "the gap"). (#3) Acknowledge in Limitations that the base rate of the
prevented failure on realistic tasks is itself unmeasured (the cost-benefit case
rests on the literature + the deferred real-bug study).

## Changes (tex/paper.tex)
1. sec:sota "The gap": after "composes with, rather than replaces, the loops
   surveyed above", add a sentence naming the genuinely new pieces vs the closest
   antecedents: (a) physical CONTEXT barriers specific to LLM agents (vs Cleanroom's
   don't-run-your-own-code), (b) disjointness of authority PAIRS (vs a single
   author--inspector split: Fagan, IV&V), (c) an explicit construction for the
   no-external-authority case (Archetype B) that document-centric pipelines (MetaGPT)
   leave open. Antecedents named, not re-cited (already cited/recorded earlier).
2. sec:limitations "Cost and latency": add that, because current models rarely
   produce coherent-and-wrong on the small tasks exercised here, the base rate of the
   failure the protocol prevents on realistic tasks is itself unmeasured -- resting
   for now on the Section~\ref{sec:sota} literature and the deferred real-bug study.

## Gates
- Gate B: build green; no new \cite (antecedents already cited), number, macro, or
  CLM; refs resolve; previously-SUPPORTED text byte-stable outside the two hunks.
- Gate C: ledger unchanged (CITE 46 + RESULT 28); reflexive macros reconcile;
  reflexive re-run byte-identical.

## Note
Names the novel contribution crisply (helps reviewers see the delta) and states the
cost-benefit limitation plainly (safe direction). No empirical claim strengthened.
