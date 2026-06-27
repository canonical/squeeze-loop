# 12-3300-paper-spec-37 — paper-impl loop, circle 37: integrate the skill-accumulation results

STATUS: APPROVED
Integrates the end-to-end skill-accumulation experiments (src/{A,B,C,D}/skill,
committed 9e71218 + cdd974c) into the evaluation section. The squeeze's
"get caught -> consolidate a new skill" mechanism — from
docs/skill-accumulation-design.md — is realized on all four executable instances
and measured: the deciding agent's skill base ENRICHES across cycles, the
solvable error rate falls to 0, and the enrichment is causal and deterministic.
This grounds the generativity finding (O4 / contribution (vii)) in the squeezed
*agents*, not only in the paper's reflexive self-application — with the honest
caveat that the deciding agents are deterministic programmatic learners over
fixed catalogs, not live LLMs (the per-model gradient stays OPN, CLM-070).

## Changes
- New generator verify/skill_measures.py -> tex/macros/skill.tex. Reads the four
  committed src/{A,B,C,D}/skill/skill_enrichment_results.json (no kernel, no LLM):
    ResSkillInstances 4, ResSkillCycles 100, ResSkillLearned 19 (4+8+5+2 skills),
    ResSkillBClasses 8, ResSkillBErrFirst 2.9, ResSkillBErrLast 0,
    ResSkillMaxSolvableLast 0 (every instance's solvable rate reaches 0),
    ResSkillDTactics 2, ResSkillDWall 16, ResSkillDPool 100.
  Preamble \input added; skill_measures.py added to src/paper/_paperlib GENERATORS.
- Manuscript (sec:eval): new paragraph "Skill accumulation: new concepts in the
  squeezed agent" after the "Enriching the upper bound" paragraph. Reports the
  enrichment curve (B 0->8, errors 2.9->0), the aggregate (19 skills across 4
  instances, every solvable rate -> 0, causal + deterministic), and D's bounded
  conceptual leap (lia/nia learned; residual 16/100 conceptual-leap wall —
  the frontier where the deferred mechanism would act). Honest scope clause:
  programmatic learners, not live models; ties to CLM-070 (gradient OPN).
- Contribution (vii): extend to note the generativity mechanism is also exhibited
  in the squeezed agents (Section~\ref{sec:eval}), not only the reflexive paper,
  scoped by the programmatic-learner caveat.
- Ledger: CLM-075 RESULT (skill accumulation across 4 instances: enrich + rate->0
  + causal + deterministic), CLM-076 RESULT (D bounded conceptual leap + residual
  wall). RESULT 26 -> 28; reflexive macro ResReflexResultRows 26 -> 28.

## Gates
- Gate B: build green; \input resolves; skill.tex macros all defined and used;
  previously-SUPPORTED text byte-stable outside the planned diff.
- Gate C: ledger CITE 46 + RESULT 28 == regenerated reflexive macros
  (gate_checks.py reconciles); skill_measures.py + reflexive_measures.py re-run
  byte-identical; the four skill tests still PASS.

## Honesty note
Deciding agents are deterministic programmatic learners over fixed catalogs, not
live LLMs. The claim is that the squeeze's caught->consolidate mechanism enriches
skill and is causal/deterministic — NOT that a live model's error gradient was
measured (that remains CLM-070 OPN). D's residual wall is reported as a persistent
floor, not as solved.
