# Ground truth (the lower bound / hard truth)

**Definition.** The **lower bound** of a squeeze: an *executable* process whose verdict
is mechanical and interpretation-free, and which an actor **cannot alter** — a test
that passes or fails, a number that recomputes or does not, a proof obligation that
discharges or does not. It is the **hard** truth, as opposed to the **soft**,
interpretation-laden [upper bound](upper-bound.md).

Ground truth answers *what is computed*; it cannot say what *ought* to be computed
(that is the upper bound's job). A claim that did not come out of an executable
artifact does not exist, for the loop's purposes.

## Forms it takes (per terrain)

- **Transcription (A/D):** execution of the real thing — a signed SQL warehouse +
  certified baseline (analytics), or the Rocq kernel + a signed proof registry (proofs).
- **Authored authority (B):** the shipped machinery — a frozen REST app + an
  adjudicated archive of certified cases; the certified decider `reference_policy.decide`
  is the runnable answer key.
- **Split planes (C):** one executable ground truth per plane — an OpenAPI document and
  a live server.

In the repository the executable floor lives under `src/<X>/ground-truth/` (the
oracle/answer-key), distinct from `src/<X>/upper-bound/` (the normative ceiling).

## Why it is load-bearing

The ground truth is the **oracle** every gate re-runs and every monitor differential-
tests against — including [Gate S](gates.md), which uses a use case's executable oracle
to decide whether a learned skill contradicts the upper bound. "The ceiling and the
floor describe the same system": the ground truth and the upper bound constrain one
deliverable from opposite directions.

The same floor anchors the **recursive** monitors ([reflexive-monitors](reflexive-monitors.md)):
the over-reach audit reads executable artifact markers, and the perturbation gate's
"different seed" arm *re-runs* a sampling result rather than trusting one draw. It is
moreover the honest floor for the paper's own claims: because a self-monitor cannot
self-certify, reflexive Gate~S **routes** an empirical self-claim to a disjoint base
that is precisely this executable lower bound — the instances re-run — sending only the
irreducibly interpretive claims to external review.

## Sources

- `tex/paper.tex` §`sec:strategy`: Definition 1 (the lower bound `L`); the
  hard/soft-truth remark.
- `paper-impl.md` §0: "Lower bound — tests, measures, experiments, proofs."
- `src/<X>/ground-truth/` (e.g. `src/B/ground-truth/reference_policy.py`).

## See also

- [upper-bound](upper-bound.md) — the soft, normative counterpart.
- [squeeze-loop](squeeze-loop.md) — how the two bounds bracket each actor.
- [gates](gates.md) — the gates and Gate S that re-run / differential-test the oracle.
- [reflexive-monitors](reflexive-monitors.md) — the recursive monitors anchored on this
  floor; the disjoint base reflexive claims route to.
