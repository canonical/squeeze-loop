# creusot-sl — a full SL-compliant loop for Creusot verification

**Name:** `creusot-sl` (the Creusot Squeeze Loop).

A **Squeeze Loop (SL)** that annotates **existing** Rust with Pearlite and proves it
with Creusot, structured so the loop converges on *correct* code-with-specs rather
than on a *plausible-looking* one. This document defines the full, SL-compliant
form (coordinator + canonical cast + disjoint bounds + physical barriers + gates +
gap-document mechanics). A lighter 3-agent variant is kept in the appendix.

> Drafted with the `sl-builder` methodology. Interview slots that the established
> context did not fix are marked `ASSUMPTION:`; unresolved forks are listed under
> *Open questions*. Run the C1/C2 checks (end of doc) before trusting an instance.

---

## 0. Deliverable & correctness
- **Deliverable:** the original Rust functions, annotated with Pearlite, such that
  `cargo creusot` discharges every obligation **and** the proved theorem is the
  property the requirement intends (no escape hatches on the target).
- **"Correct" means (checkable):** every requirement clause is expressed as a
  Pearlite contract clause that Why3 + the SMT backends discharge against the
  original Rust, and a mutation of the code that violates the requirement is caught
  by some VC or adversarial property.
- **Terrain archetype: A/B mix.** The *requirement* is external (transcription, A),
  but the *Pearlite contracts* that make it checkable are **authored upstream** by
  an actor that never sees the implementation (authored authority, B). **Author
  independence carries the soundness argument.**
- **Dominant coherent-and-wrong to guard:** a **vacuously-true / weaker-than-intended
  contract** (`#[ensures(true)]`, an unsatisfiable `#[requires]`, a postcondition
  that proves an adjacent weaker property). Why3 discharges, but the theorem is not
  the intended one.

## 1. Bounds
- **Upper bound `U`** = the **external requirement** (plain English / standard /
  ticket) **made precise as Pearlite contracts** (`#[requires]`/`#[ensures]`/
  `#[invariant]`/`#[variant]`, logic/ghost functions). The strongest claim the code
  must satisfy.
- **Lower bound `L`** = `cargo creusot` → Creusot→Coma→Why3 → SMT discharge
  (`Proved … ✔`), **plus** `cargo test` execution **plus** the **mutation probe**
  (perturb the Rust; the proof must break). A mechanical verdict no actor can alter.
  - *Pilot-confirmed:* `add_one` proved end-to-end during install.

## 2. Actors and their disjoint `(U,L)` pairs

The canonical cast, instantiated for Creusot verification of existing code. A role
exists only for a **new evidence base**; the *implementer* here is an **annotator**
(it adds proof scaffolding, it does not rewrite the program's behaviour).

| Actor | Builds | U (above) | L (below) | Forbidden move | Must NOT see |
|---|---|---|---|---|---|
| **Coordinator** | approvals (Gate A), sequencing, gap-doc adjudication, DONE verdicts | the requirement + plan sections | the machine gate output (why3find logs, test + mutation results) | edit Rust/Pearlite; approve an unjudged plan; let a self-report end an item | — (judges against `U`, never a producer's rationale) |
| **Spec author** | the Pearlite **contracts** (requires/ensures + the requirement's invariants) | the **external requirement** + public signatures | expressibility: each clause dischargeable by *some* Why3 mechanism | read or infer the implementation body | the implementation; the adversarial properties |
| **Annotator** (implementer) | internal **proof scaffolding**: `#[invariant]`, `#[variant]`, ghost/snapshot, intermediate `proof_assert!`, minimal proof-preserving refactor | the contracts (strongest mandated claim) | `cargo creusot` discharge + standing test suite | weaken a contract/gate to land; add `#[trusted]`/`assume!` to the target; touch acceptance evidence | the adversarial/acceptance properties |
| **Exerciser/Verifier** | adversarial properties + the **mutation probes**; runs `cargo creusot` fresh | the requirement's acceptance clauses + the documented public surface | what actually discharges/proves when run | read the implementation or the annotator's diff | the implementation; the annotator's diff |
| **Probe** | minimal Creusot/Why3 capability experiments (does WP handle this construct? does this prover discharge?) | one design claim per probe | Creusot/Why3's *actual* behaviour | implement a fix | — |

**Disjointness (C1):** the spec author holds the requirement (never the code); the
annotator holds the contracts (never the adversarial properties); the verifier holds
the requirement + the runnable oracle (never the code or the diff); the coordinator
holds the requirement + gate output (never producing an artifact it grades).
**Intersection** = Rust that *both* discharges contracts authored from the
requirement *and* survives adversarial properties derived independently from that
same requirement — and no single actor can certify it alone.

**Catchability (C2):**
- annotator games a weak contract → caught by the verifier's adversarial properties
  + Gate C mutation probe;
- spec author writes a **vacuous** contract → caught at Gate C (mutation probe fires)
  and by the verifier (adversarial properties that *should* fail against a vacuous
  spec but don't);
- spec author **misreads the requirement** → caught by the coordinator at Gate A
  (judges contracts against the requirement);
- verifier anchors to the implementation → structurally prevented (barrier) and the
  coordinator confirms each adversarial property derives from `U`.

## 3. Physical barriers (not honorary)
- **Spec author ⊥ implementation** and **Verifier ⊥ implementation+diff.** Their
  contexts contain only the requirement + public signatures/surface; the function
  bodies and the annotator's diff are *absent*, not merely off-limits.
- **Annotator ⊥ acceptance evidence.** The adversarial properties and mutation set
  are not in its context, so it cannot tune the code to them.
- **Coordinator judges against `U`.** It reads the requirement and the gate output,
  never a producer's account of *why* its artifact is right.
- **Anchoring tell:** if the verifier's adversarial properties or the contracts start
  mirroring implementation quirks (a magic constant, an off-by-one), a barrier has
  leaked — re-delegate from a fresh, body-free context.

## 4. Gates
- **Gate A — editorial (judgment).** The coordinator judges the contracts + plan
  against the requirement: each requirement clause is typed and pre-bound to a
  Pearlite obligation; the strongest-claim check; explicit `NOT`-claims. **Amend /
  cut / sharpen, never rubber-stamp.** No Rust/Pearlite edit flows from a `DRAFT`.
- **Gate B — machine.** `cargo creusot` → **all VCs discharged**; `cargo test`
  passes; **no escape hatch on the target** (no new `#[trusted]`, `assume!`,
  unproven `#[law]`/axiom, over-promising `extern_spec!`, `absurd`/unreachable on
  reachable code); **standing proof count** holds (previously discharged VCs stay
  discharged); determinism re-run gives the identical verdict.
- **Gate C — coverage / no-blend / coherent-and-wrong.** Every requirement clause
  maps to a *proven* contract clause, **and the proved theorem is the intended one**:
  the **mutation probe** must break the proof (non-vacuity); the **proof plane**
  (Why3 discharge) and the **test plane** (runtime) never substitute for one another.
- **Gate S — skill-consistency.** When a role consolidates a reusable Creusot
  heuristic (an invariant template, "introduce a `found` flag", a prover-selection
  tip), audit it with the `sl-monitoring-sl` pattern: a **disjoint monitor** squeezes
  the skill against `U` and `L`; return **PASS / CARVE-OUT / REJECT**. Only PASS /
  CARVE-OUT entries are written to the role's learned file under
  `config/skills/creusot/` (§11). A soft skill may never silently stand in for the
  requirement, and a producer may never commit its own skill unaudited.

## 5. Loop steps (per function / unit)
Work circulates through a **DRAFT → APPROVED → DONE** handshake; the only backward
motion is a **gap document** carrying the same number as the plan it answers.

1. **Coordinator** delegates an item: requirement clauses + public signature +
   barriers + acceptance lines. Each agent first **loads its own learned file**
   (§11) so prior capitalization compounds.
2. **Spec author** writes the Pearlite contracts from the requirement @ `STATUS: DRAFT`.
3. **Gate A** → `APPROVED` (coordinator judges contracts vs requirement; amend/cut/sharpen).
4. **Annotator** adds proof scaffolding to the original Rust, runs `cargo creusot`
   locally, runs the standing invariant.
5. **Exerciser/Verifier** runs `cargo creusot` fresh + authors adversarial properties
   and mutation probes from requirement + surface only.
6. **Gate B** (machine) → **Gate C** (coverage / non-vacuity / no-blend).
7. Item `DONE` → next. Any divergence (a VC won't discharge; a mutant still proves; a
   probe surprises) → `gap-N` doc → re-plan (re-spec, re-annotate, or flag a code
   bug / a Creusot limitation) — **never** a silent local `assume!`.
8. **Capitalize (§11):** each producing role distills ≤1 reusable, role-appropriate
   heuristic from this file; a disjoint monitor runs **Gate S**; PASS/CARVE-OUT
   entries are appended (with provenance) to that role's learned file under
   `config/skills/creusot/`.

## 6. Executable oracle setup
`cargo creusot [PATTERN]` over the unit; **a verdict = the per-obligation discharge
status** from why3find, plus a determinism re-run. The mutation probe is scripted
(flip a comparator, drop a `+1`, widen a bound) and required to break the proof.
Pilot on the smallest function end-to-end before any sweep (done: `add_one`).

## 7. Done criteria
Per item: contracts approved at Gate A against the requirement; spec authored blind
to the body; **all proof obligations discharged** with no `#[trusted]`/`assume!`/
axiom shortcut on the target; `cargo test` green; the mutation probe breaks the
proof; determinism re-run agrees; any consolidated skill passed Gate S and was
appended to its role's learned file with provenance (§11). **No actor's self-report
ends an item — only the gates.**

## 8. Stabilizers engaged (collapse mode → blocker)
- *Self-judging* → forbidden moves are load-bearing (annotator never authors the
  acceptance evidence; verifier never reads the code).
- *Honorary barrier* → spec author & verifier delegated from fresh, body-free
  contexts (physical, not instructed).
- *Self-declared done* → done is gate-defined (Gate B/C machine output).
- *Coherent-and-wrong / weakened clause* → author independence + Gate C mutation
  probe; **strictness has a safe direction** (the contract may be *stronger* than the
  requirement, never weaker, to land).
- *Rubber-stamp approval* → Gate A must amend/cut/sharpen.
- *Absorbed surprise* → a non-discharging VC routes to a gap doc, never a local
  `assume!`.
- *Unpinned reality* → the probe pins one Creusot/Why3 capability claim before
  machinery is built on it.
- *Shared evidence between actors who must disagree* → the C1 disjointness audit.

## 9. Execution order
Pilot/oracle first (**done**). Then **leaf functions first**, propagating each
proven callee `#[ensures]` as the caller's `#[requires]`; sequence by mechanism reuse
(each item rides the proof machinery the previous one hardened); parallelize only
across functions that share no evidence base.

## 10. Compliance check (run before trusting an instance)
- **C1 Disjointness:** ✓ five distinct `(U,L)` pairs; no actor relieves its own
  bound; certification requires the intersection. *(Holds only if §3 barriers are
  physical.)*
- **C2 Catchability:** ✓ every characteristic blind spot has a named catcher (§2).
- **C3 Physical barriers:** ✓ iff spec author/verifier contexts are built from the
  requirement + surface, never the source or the diff.
- **C4 Gate-defined done:** ✓ done = discharge + no escape hatch + mutation-probe
  breaks + Gate S; no self-report counts.

---

## 11. Knowledge capitalization — `config/skills/creusot/`

`creusot-sl` analyzes **one file at a time**; after a file reaches DONE, each
producing role distills at most one reusable, role-appropriate heuristic and
capitalizes it into the shared `creusot` skill, so the next file starts smarter.
This is **append-only learning under Gate S** — the loop's defense against learning a
*coherent-and-wrong* heuristic (right on the common case, silently wrong on a
governed exception).

**Per-role learned files** (under `config/skills/creusot/references/`):

| File | Role | Records (role-scoped) |
|---|---|---|
| `learned-coordinator.md` | Coordinator | judgment/gate heuristics: clause-typing, NOT-claim patterns, when a DRAFT must be cut/sharpened |
| `learned-spec-author.md` | Spec author | requirement→Pearlite patterns: how a *kind* of requirement maps to `requires`/`ensures`/`invariant`; modelling idioms — **requirement-level only** |
| `learned-annotator.md` | Annotator | proof-scaffolding patterns: invariant templates per loop shape, ghost/snapshot idioms, prover-selection tips |
| `learned-verifier.md` | Verifier | adversarial-property & mutation patterns: which mutation exposes a vacuous spec of a given shape |

**Discipline for every new entry:**
1. **Drafted** by the role that learned it — but **never committed by that role** (its
   producer shares the skill's blind spot; self-auditing is the move the squeeze
   forbids).
2. **Gate S audit by a disjoint monitor.** The **coordinator** acts as skill-monitor
   for the producing agents; the **coordinator's own** heuristics are audited by the
   verifier or a human — never self-audited. The monitor squeezes the heuristic
   against `U` (Pearlite/requirement semantics) and `L` (`cargo creusot`'s actual
   behaviour), classifies it (ignore-signal → trigger test → carve-out;
   defer-to-oracle → validity test → prune if spurious), and returns **PASS /
   CARVE-OUT / REJECT**.
3. **Append only PASS / CARVE-OUT**, each with **provenance** (the file or `gap-N`
   that produced it) and, for a carve-out, the exact requirement clause it defers to.
   REJECT → discard and log; never silently keep.
4. **Barrier preservation (load-bearing).** An entry may record only generalizable,
   role-appropriate knowledge — **never forbidden evidence**. The `spec-author` and
   `verifier` files must contain **no implementation specifics** (those roles never
   saw the code); the `annotator` file must generalize to a *pattern*, never a copy
   of one program. An entry that would leak the implementation to a barriered role is
   a barrier breach → REJECT.

**Read-back:** at delegation (step 1) each agent loads its own learned file first, so
capitalization compounds across files without ever crossing a barrier.

**Entry format:**
```
### <short heuristic title>
- Kind: ignore-signal | defer-to-oracle      (Gate S classification)
- Gate S: PASS | CARVE-OUT
- Arose from: <file / gap-N>
- Heuristic: <the reusable rule>
- Carve-out: <exception deferring to requirement clause …>   (if any)
```

---

## Appendix — lightweight variant (the original 3-agent flow)
A simpler, **endogenous** form of `creusot-sl`, useful when **no external
requirement exists** and you only want a self-consistency check:

1. **Summarizer** reads the Rust → English summary of intended behaviour.
2. **Spec author** (blind to the code) writes Pearlite from that summary + signatures.
3. **Prover** runs `cargo creusot` against the original Rust.

Here a coordinator/driver still runs the gates, but `U` is derived from a *summary of
the code*, so the loop tests **self-consistency**, not conformance. It catches panics/
overflow and code that contradicts its own apparent intent, but **not a faithfully-
transcribed bug** — the full loop above closes that gap by sourcing `U` from an
external requirement and adding the independent exerciser + mutation probe.

**Which to use:** full loop when a requirement/standard exists (terrain A/B);
lightweight variant only as a quick self-consistency pass, with its soundness limit
stated out loud.

---

## ASSUMPTIONS & open questions
- `ASSUMPTION:` deliverable = the `training-data/` Rust corpus (or a target crate),
  functional correctness, partial-correctness unless `#[variant]` is in scope.
- **Requirement source.** The full loop needs an *external* `U`. **OPEN:** where does
  the requirement come from for your files — docstrings, a spec doc, the original
  Creusot contracts (as ground truth), or must a human author it? Without one, you
  are restricted to the lightweight variant.
- **Actors = agents or humans?** **OPEN:** are the five roles separate LLM agents
  delegated by a harness coordinator, or a human + a few agents? This decides how the
  physical barriers (§3) are enforced.
- **Cross-module.** **OPEN:** single functions, or contracts coordinated across
  compilation units? The latter makes this a nested loop (`sl-monitoring-sl`,
  bottom-up, leaves first).
- **Termination.** **OPEN:** partial correctness only, or total (`#[variant]` +
  `#[check(terminates)]`)?
