# 12-1200-paper-spec-2 — paper-impl loop, circle 2: Use Case A as executable lower bound

STATUS: DONE
Coordinator circle. Mapping for this engagement (per the user's framing):
- **Upper bound** = the verified bibliography (literature plane, `bib/records/`).
- **Lower bound / ground truth** = `src/A/` (the executable squeeze-loop instance).

## Plan (what this circle delivers)

1. **E-item** — build a re-runnable measurement harness over `src/A` that emits
   real numbers (paper-bench-agent role).
2. **W-item** — put those numbers in the paper via generated macros (no hand-typed
   number); add the executable instance as Section~\ref{sec:caseD}.
3. **L-item** — answer the new positioning question the measures raise (below).

## E-item — `src/A/evidence/measure_squeeze.py`

Runs the full stack (ground-truth verify, upper-bound validate, in-band squeeze,
a seeded coherent-and-wrong negative control, determinism re-run) and emits
`src/A/evidence/results.json` + `tex/macros/results.tex`. Deterministic:
results.json byte-identical on re-run. Fixture `coherent_wrong_fixture.py` (gross
revenue where net is mandated) is the permanent seeded defect.

Measured: 2 metrics / 5 clauses; 8/8 positive cells in three-way agreement
(implementer == exerciser == certified ledger); 5/5 seeded defects caught (100%);
coherent-and-wrong implementer rejected at Gate B; isolation clean; total
additivity stable; warehouse 50 users / 291 events; 24 certified ledger metrics.

## L-item — the new question the evidence raised → bibliography focus

Running the instance made explicit that the negatives are **seeded mutants killed
by an independent suite** (mutation testing) and the three-way agreement is
**independent computations that must agree** (differential testing) — neither
was in the bibliography. Added and verified (reading records written):
- `demillo1978hints` (FULL) — origin of program mutation / kill criterion.
- `jia2011analysis` (SECONDARY; IEEE paywalled) — canonical survey.
- `mckeeman1998differential` (FULL) — differential testing (recommended over
  metamorphic testing, which concerns one program under related inputs).

Cited in §2.5 (classical antecedents) and §\ref{sec:caseD}. CLM-036..038.

## W-item — manuscript changes

- New `\input{macros/results}` (guarded by `\IfFileExists`).
- New §\ref{sec:caseD} "An executable instance: the tabular-analytics terrain"
  with all numbers via `\ResWorked*` macros; framed as a constructed existence
  demonstration, NOT the controlled eval (strictness safe direction: claim less).
- Abstract + contribution (iii) updated to mention the executable instance.
- §2.5 mutation/differential-testing sentence.
- §6 updated: first executable data point exists; comparative eval still future;
  reflexive note that this manuscript is itself produced under the loop.
- Ledger CLM-036..043 (3 CITE + 5 RESULT, RESULT bound to results.json).

## Gates

- **Gate B** — build green (17 pp), every `\cite`/`\ref`/macro resolves, no
  bibtex warnings; previously SUPPORTED text untouched outside the planned diff.
- **Evidence/Gate C** — numbers re-derived: results.json byte-identical on
  re-run; macros consistent with results.json. See
  `verify/reports/usecaseA-evidence-2026-06-12.md`.

## Open questions for the next circle (not yet done)

1. `jia2011analysis` is SECONDARY (paywall) — upgrade to read:FULL for camera-ready.
2. The instance has no baseline configuration → H1 (disjointness vs shared-context)
   is still unmeasured. A natural next E-item: a shared-context variant of Use
   Case A (implementer sees the exerciser's tests) to measure the catch-rate delta.
3. The reflexive case study (this paper's own loop) needs ≥1 more circle before it
   is reportable as a section.
4. Does adding a 4th *executable* terrain disturb the three-archetype taxonomy
   (§4)? Currently filed as an instance, not a new archetype — revisit if a 2nd
   executable terrain is added.
