# 12-2730-paper-spec-31 — paper-impl loop, circle 31: hard truth vs soft truth (new conceptual framing)

STATUS: DONE
Content circle (new framing requested by the author). The paper defined the upper
bound (normative artifact) and lower bound (executable ground truth) but never
named the deeper asymmetry: they are sources of truth of *opposite kind*, and the
squeeze is precisely what binds them.

## The idea added
- Lower bound = **hard** truth: executable, mechanical, interpretation-free verdict
  (test passes/fails, number recomputes or not, proof obligation discharges or not).
- Upper bound = **soft** truth: a norm / standard / spec in natural language,
  authoritative but interpretation-laden (even a precisely stated problem admits
  more than one faithful reading).
- The squeeze binds soft to hard: a deliverable is in-band iff it is a *reading* of
  the soft truth that the hard truth does not refute. Coherent-and-wrong is then a
  plausible interpretation of the soft upper bound that the hard lower bound
  contradicts (or, dually, a hard-check-passing artifact that betrays the soft
  intent). Neither suffices alone: hard can't say what *ought* to be computed, soft
  can't say what *is*.

## Changes
- §sec:strategy: new `\begin{remark}[Hard truth and soft truth]` directly after
  Definition 1 (Squeeze). Ties the distinction to the gates (Gate A adjudicates the
  soft truth editorially; Gate B the hard truth mechanically) and to the terrain
  archetypes (what varies across terrains is *how hard* the lower bound and *how
  soft* the upper bound; the binding is the invariant).
- Intro contribution (i): extended to name "the asymmetry it exploits between a
  hard executable lower bound and a soft normative upper bound, which the squeeze
  binds together."

## Additivity
No number or prior claim altered; this adds a framing remark and one clause. The
remark is consistent with Definition 1 (it elaborates U_i/L_i) and with §4
(how-hard/how-soft = "what the bounds are made of"). No new citation (authors'
framing; read-before-cite respected).

## Effect on numbers
- reflexive.tex regenerated: ResReflexSpecDocs -> 30 (this circle). Others unchanged.

## Gates
- Gate B: build green (18 pp), all cites/refs/macros resolve, no bibtex warnings.
- Determinism: reflexive harness re-run byte-identical.
- No ledger / manuscript-defect change.

## Note
This is independent of the review1 response queue (F1 appendix etc. still pending);
inserted at the author's request as circle 31.
