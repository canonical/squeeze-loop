# Metric handbook (A's upper bound)

**Definition.** The machine-parseable, read-only normative specification that fixes every
clause an implementer and exerciser must satisfy when computing a metric; A's instance of
the [upper bound](../../../../docs/glossary/upper-bound.md). As a transcription
([Archetype A](../../../../docs/glossary/archetype.md)) instance, this is an *external*
written spec — the task is to transcribe it faithfully, not to author it.

It states, per metric, the exact definition (e.g. net revenue = gross − refunds, in the
reporting timezone, deduplicated at the order grain). A deliverable over-claims the moment
it reports a number the handbook does not license; the safe direction is down.

## Sources

- `src/A/upper-bound/metric_handbook.md` — the artifact (the clauses).
- `src/A/upper-bound/handbook.py` — the parser that makes the clauses machine-checkable.
- `src/A/upper-bound/README.md` — governance.

## See also

- [certified-baseline](certified-baseline.md) — the hard counterpart the handbook is
  re-proved against.
- [naive-vs-intended](naive-vs-intended.md) — the wrong-vs-correct readings the handbook
  disambiguates.
- [upper-bound](../../../../docs/glossary/upper-bound.md) ·
  [archetype](../../../../docs/glossary/archetype.md) — the shared concepts this instantiates.
