# Upper Bound `U_self` — Instance C (API contract guard)

*An authored-authority upper bound (Archetype B), mirroring the paper's root
`paper_upper_bound.md`, for any claim that **this instance** instantiates Hofstadter's
strange-loop account of selfhood. Same criterion, applied to instance C, so the
squeeze-strategy pattern is uniform across all five instances (paper + A/B/C/D).*

The criterion itself — cap, obligation clauses **O1–O5**, falsification tests
**N1–N3**, NOT-claims, the **Tier** ladder, and the done-condition — is stated
canonically in `paper_upper_bound.md`. This file records its **discharge for instance C**.

## Cap (same as the canonical bound)

The strongest admissible claim is **structural, not phenomenal**; **Tier 0**
("is conscious / has experience / feels") is **forbidden**. See `docs/glossary/tier.md`.

## Why instance C is object-level

Instance C is the squeeze applied **to** an API contract guard (Archetype C, split
planes) — an *object-level* task, not to itself. Its skill loop (`src/C/skill/`)
consolidates **API clause families** (no\_id\_leak, clean\_error, state\_machine,
idempotency, pagination); those denote the contract task across its document and
runtime planes, not the instance. C does not apply the method to itself.

## Discharge status (clause by clause)

| Clause | Exhibited? | Why |
|--------|-----------|-----|
| **O1** endogenous self-symbol | **NO** | the skill store denotes API clauses (the object task), not a representation that denotes instance C itself |
| **O2** level-crossing / downward causation | **NO** | gates act on HTTP responses and contract documents (object artifacts), not on a claim *about C's own method* |
| **O3** closure | **NO** | a one-directional object pipeline (manifest → server/schema → conformance check); it never evaluates claims-about-its-method and re-enters them |
| **O4** self-referential categorization | **NO** | the categories it consolidates are about the contract planes, not categories C invents about C and applies to C |
| **O5** persistence (self-model) | **NO** | the skill loop updates a deterministic store across cycles — a mechanism, not a perceived, re-categorized self-model (cf. the paper's circle-57 demotion of skill accumulation) |

## Falsification tests

With respect to *selfhood*, instance C falls in the **N1/N2 triviality class**: its
skill loop adapts over an object domain the way a thermostat or quine processes its
input — feedback/repetition without self-modelling. Correctly **rejected at O1/O4**.
**N3** (qualia) is forbidden as a NOT-claim.

## NOT-claims

As in the canonical bound: no phenomenal claim (NOT-1), no Hofstadter-endorsement
claim (NOT-2), necessary-not-sufficient (NOT-3), no primacy (NOT-4).

## Disposition ladder (instance C) and placement

The disposition-ladder *mechanism* (graded claims + loud-fail) is shared with the
canonical bound; the *rungs* below are instance C's self-reference claims. Lower
number = stronger claim; the prose may retreat down, never climb above its evidence.

| Tier | Claim about instance C | Admissible when |
|------|------------------------|-----------------|
| **0 — Forbidden** | "C is conscious / understands its domain" | **never** |
| **1 — Structural self-model** | C keeps a self-model it *consults to act* and *updates across iterations* (O1–O5), driving its own behaviour | O1–O5 discharged for C (a live self-model, not a fixed mechanism) |
| **2 — Self-modification (analogy)** | C changes its own future behaviour as a function of its own *caught errors* — a structural self-reference, offered as analogy | C runs a caught→consolidate loop that demonstrably alters later behaviour |
| **3 — Squeeze-produced & adaptive** | C is produced and verified by the squeeze method and adapts under a fixed exerciser | always |

**Placement: Tier 2 (self-modification, as analogy).**

- **Tier 1 — not met.** O1–O5 are not discharged (table above): C's skill store is a
  *deterministic mechanism* (cf. the paper's circle-57 demotion of skill accumulation),
  not a self-model it consults to decide. The structural-self-model / strange-loop Tier
  is reserved for the reflexive paper instance, which discharged O1–O5
  (`paper_upper_bound.md`).
- **Tier 2 — met.** `src/C/skill/` runs a caught→consolidate loop: it learns to honor
  the API clause families (no\_id\_leak, clean\_error, state\_machine, idempotency,
  pagination) it was caught blending, and its future behaviour changes accordingly.
  Held as *analogy* (deterministic, no self-model, no level-crossing), per the
  loud-fail rule.
- **Tier 3 — unconditional.** C is built and verified by the squeeze (coordinator–worker
  loop + gates) and adapts under the fixed independent exerciser.
- **Tier 0 — forbidden.**

The five instances share one ladder *shape*; **placement is the discriminator** — the
reflexive paper instance reaches the structural-self-model Tier (it is a strange loop),
while C reaches Tier 2 (it self-modifies but does not model itself).

## See also

- `paper_upper_bound.md` — the canonical U_self (paper instance; Tier 2 grounded).
- `docs/glossary/tier.md`, `docs/glossary/archetype.md`.
