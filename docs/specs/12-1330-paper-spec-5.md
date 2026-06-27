# 12-1330-paper-spec-5 — paper-impl loop, circle 5: a second executable terrain (Use Case B)

STATUS: DONE
Bring `src/B` (Archetype B, authored authority: autonomous refund bot) into the
paper as a second executable instance, turning the executable evidence from one
terrain into two and settling the instance-vs-archetype question.

## E-item — measure src/B, recomputably

- `src/B/evidence/measure_squeeze.py` (mirrors src/A's harness) runs the full B
  squeeze and emits `src/B/evidence/results.json` + `tex/macros/results_b.tex`
  (\ResB* macros; no hand-typed number).
- `src/B/evidence/seeded_wrong_bot.py`: a parametrized coherent-and-wrong bot
  (reuses the real bot's commit discipline, neuters one clause via SKIP_CLAUSE).

Measured: 3 clauses, 5 scenarios, 6 archive cases; the good bot passes all
scenarios + archive regression (no decision flips); seeded coherent-and-wrong
detection = 4/4 with the barrier on (one bot per clause + an always-refund bot),
0/4 with it off. Determinism: archive replay reproduces certified verdicts.

## L-item — new question → bibliography

Use Case B's adversary is conversational manipulation (legal-threat coercion,
social engineering, duplicate-refund attempts) against an action-taking agent —
the prompt-injection / jailbreak surface, absent from the bibliography. Added and
verified (read FULL): `perez2022ignore` (goal-hijacking / prompt injection) and
`greshake2023injection` (compromising action-taking LLM-integrated apps). Cited in
§\ref{sec:caseE}. CLM-048, CLM-049.

## W-item — manuscript

- New §\ref{sec:caseE} "A second terrain: authored authority (Use Case B)": the
  REST-app + adjudicated-archive lower bound, the authored refund policy upper
  bound, the conversational adversary, and the measures via \ResB* macros. Key
  point: the strategy ENFORCES the policy externally (independent exerciser + REST
  action lockpoint) rather than trusting in-model compliance — the prompt-injection
  lesson. The two executable instances now instantiate two of the three archetypes
  (transcription §\ref{sec:caseD}, authored authority §\ref{sec:caseE}): instances
  of the archetypes, not new ones.
- §\ref{sec:caseD} opening reworded ("first of two executable instances").
- Abstract + contribution (iii) + §6 ablation sentence updated to span both terrains.
- Ledger CLM-048/049 (CITE), CLM-050 (RESULT bound to src/B/evidence/results.json).

## Honest scope (carried into the manuscript)
Still constructed instances, deterministic, without a matched-difficulty baseline.
This is generalisation across terrains in kind (n=2), not the controlled,
comparative study of H1–H4 (§\ref{sec:eval}).

## Gates
- Gate B: build green (19 pp), all cites/refs/macros resolve, no bibtex warnings.
- Evidence: src/B/evidence/measure_squeeze.py exits MEASURE OK (4/4 caught on, 0/4
  off); see verify/reports/usecaseB-evidence-2026-06-12.md.

## Open questions for the next circle
1. H1/H2 controlled study under partial coupling at matched difficulty — still future.
2. The third archetype (split planes, §\ref{sec:archetypes} C) has no executable
   instance yet; a Use Case C would complete the archetype coverage.
3. The reflexive section could now fold in the cross-terrain generalisation as a
   further data point.
