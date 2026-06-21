# Terrain archetype (Archetype A / B / C)

**Definition.** A *terrain archetype* is one of three categories of squeeze, sorted by
**where the sources of truth live** — i.e. what the upper bound (normative authority)
and the lower bound (executable ground truth) are *made of* for a given task. The
topology of the squeeze loop is invariant across archetypes; the archetype decides
what the two bounds are made of, which failure dominates, and which gate carries the
soundness argument.

The taxonomy has exactly **three** archetypes (A, B, C). It is distinct from the
count of **executable instances** (four), because one archetype can be instantiated
more than once: transcription (A) is realized twice — tabular analytics and formal
Rocq proofs.

## The three archetypes

### Archetype A — transcription
An **external written specification already says what correct is**; the task is to
transcribe it faithfully into an executable artifact.
- **Upper bound made of:** an external written specification.
- **Lower bound made of:** execution of the real thing.
- **Dominant failure:** improvisation; unfaithful transcription.
- **Load-bearing gate:** re-prove the external English against execution.
- **Instances:** tabular analytics (§`sec:caseD`); formal proofs in Rocq (§`sec:caseG`).

### Archetype B — authored authority
**No external authority exists for the property**, so the authority is a *property
spec authored upstream*, anchored to a flagship use case; the system's own
in-model compliance is not trusted — the policy is enforced externally.
- **Upper bound made of:** a property spec authored upstream, anchored to a flagship
  use case.
- **Lower bound made of:** the *shipped machinery* — what the system can already
  discharge.
- **Dominant failure:** coherent-and-wrong (a fluent, internally consistent artifact
  that misses the intended property).
- **Load-bearing gate:** the clause↔check coverage map, **defended by author
  independence** (the exerciser never saw the implementation) — because there is no
  external spec to diff against, independence *is* the soundness argument.
- **Instance:** an autonomous customer-refund agent (§`sec:caseE`).

> `paper_upper_bound.md` (the U_self strange-loop bound) is itself an **Archetype-B
> upper bound**: there is no external definition of Hofstadterian selfhood to diff
> against, so the document *authors* a defensible operationalization (its obligation
> clauses O1–O5) and its authority rests on that authored spec, not an external one.

A **monitor squeeze** inherits an archetype the same way. A skill- or claim-consistency
monitor ([Gate S](gates.md) and reflexive Gate S) is **Archetype B**: there is no
external definition of "this learned skill is over-general" or "this claim over-reaches,"
so the monitor *authors* what consistency means (the loop's own upper bound) and enforces
it externally against the executable oracle — the same authored-authority structure as
U_self, and the same dominant failure (coherent-and-wrong). The
[reflexive-monitors](reflexive-monitors.md) are these monitors applied to the paper's own
soft outputs.

### Archetype C — split planes

The correctness of a *single* construct is **split across two (or more) planes**,
each with its **own authority and its own executable ground truth**, and the
construct is correct only when the planes **agree**. Neither plane alone suffices: one
says what the construct is *supposed* to be, the other shows what it *actually does*,
and either can be satisfied while the other is violated. The characteristic failure is
**blending** — letting one plane's check stand in for the other's.

- **Plane:** one of the semantic surfaces on which the same construct's correctness is
  asserted, with its own authority (what it *says*) and its own runnable check (what it
  *is*). In the API instance the two planes are the **document plane** — an OpenAPI
  schema, checked by a linter (what the contract *promises*) — and the **runtime
  plane** — a live HTTP server (what the service *does*).
- **Precedence rule:** the stated relation the planes must hold so a conflict has a
  defined resolution — e.g. the runtime must conform to the document, and the document
  must not promise what the runtime cannot deliver. Without it, "the planes agree" is
  undefined when they diverge.

What makes C its own archetype is the **number of authorities**: A has one external
authority, B has one authored authority, **C has one authority per plane** — so the
new risk is not improvisation (A) or being fooled (B) but *conflation*: passing the
easy plane's check and inheriting the hard plane's claim.

- **Upper bound made of:** one authority per plane, plus a precedence rule (instance:
  an authored API-governance manifest + the OpenAPI schema).
- **Lower bound made of:** one executable ground truth per plane (instance: the
  OpenAPI document *and* the live server).
- **Dominant failure:** *blending* — one plane's weak check standing in for the
  other's strong claim. Both directions: compliant docs masking broken runtime, **or**
  a clean-running route that never updated its public contract.
- **Load-bearing gate:** per-plane machine checks **plus** an independence-defended
  no-blend check — the planes are verified *separately* and must agree, so neither can
  vouch for the other (the exerciser derives conformance cases from the schema alone
  and runs them against the live server).
- **Instance:** an API contract guard (§`sec:caseF`).

## Why the distinction matters

The archetype is the coordinator's **first** decision on a new instance: locate where
truth lives. That choice fixes the materials of the squeeze (upper/lower bound),
predicts the dominant failure, and tells you which gate must carry soundness. Real
systems mix archetypes per work item.

## Sources

- `tex/paper.tex` §`sec:archetypes` and Table `tab:archetypes` (the three-archetype
  table: upper/lower bound made of, dominant failure, load-bearing gate, instance).
- `tex/paper.tex` §`sec:caseD`–§`sec:caseG` (the four executable instances over the
  three archetypes; A and D both transcription).
- `tex/paper.tex` §`sec:synthesis` ("one topology, four materials").
- `paper_upper_bound.md` §1 (self-describes as "An authored-authority upper bound
  (Archetype B)").

## See also

- [tier](tier.md) — the disposition ladder used by Archetype-B upper bounds such as
  U_self to bound graded claims.
- [upper-bound](upper-bound.md) · [ground-truth](ground-truth.md) — the two bounds whose
  *materials* the archetype fixes.
- [gates](gates.md) · [reflexive-monitors](reflexive-monitors.md) — monitor squeezes that
  inherit an archetype (consistency monitors are Archetype B).
