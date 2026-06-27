# 12-5300-paper-spec-57 — paper-impl loop, circle 57: reframe eval body (review2 #1/#5/#6)

STATUS: APPROVED
Fourth review2 circle: the evaluation-section body.

## Changes (tex/paper.tex sec:eval)
1. (#5) Skill paragraph -> a clearly-labelled MECHANISM demonstration. Retitle
   "Skill accumulation: new concepts in the squeezed agent." -> "A mechanism
   demonstration: caught-then-consolidate in the squeezed agent." Drop the
   learning/"enriches"/"skills acquired"-as-finding framing; state plainly that a
   deterministic loop eliminates exactly the errors it consolidates against (the
   tautology is the point), that this only shows the machinery is wired and causal,
   and that live-model learning stays open. All macros retained (no orphans).
2. (#1) Protocol status: "H2 is discharged on the four executable instances ---
   ... 15/15 ... versus 0/15 ..." -> "H2 is demonstrated ... as a consistency
   check ...", with the barrier-off 0/15 explicitly labelled a deterministic
   full-anchoring model (real-agent pilot below finds no difference). No 0 stands
   unqualified.
3. (#6) Coupling bullet (Independence measures): soften -- low bigram overlap is
   "consistent with" independence but does not by itself establish it (assertions
   and implementation differ in vocabulary even under anchoring); the informative
   quantity is the delta vs a measured barrier-off coupling, which remains future
   work.

## Gates
- Gate B: build green; all ResSkill*/ResAll* macros stay in use (no orphan);
  no new cite/number/macro/CLM; refs resolve; previously-SUPPORTED text byte-stable
  outside the three hunks.
- Gate C: ledger unchanged (CITE 46 + RESULT 28); reflexive macros reconcile;
  reflexive re-run byte-identical.

## Note
Safe direction: relabels skill as a mechanism demonstration, marks the modeled 0,
and downgrades the coupling claim to "consistent with". No empirical claim
strengthened.
