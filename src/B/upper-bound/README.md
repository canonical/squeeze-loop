# Upper Bound — Autonomous Refund Bot Policy Handbook

> **Purpose:** the authored refund policy fixes which terminal action is permitted
> in each situation, so conversational manipulation cannot push the agent's
> decision beyond what policy allows.

Implementation of the **Upper Bound Source of Truth** for the system in
[`../upper-bound-spec.md`](../upper-bound-spec.md). The upper bound is the
authored, citable normative ceiling: it fixes the strongest claim the
`implementer` and `exerciser` agents may make about the refund bot. An agent that
issues an automated credit on an already-refunded order, or fails to escalate a
legal-threat dialogue, has breached the ceiling.

It is the counterpart to [`../ground-truth/`](../ground-truth/) (the executable
floor): the handbook's clauses are grounded in the *same* system. The decision
tokens (`REIMBURSE` / `DENY` / `ESCALATE`) are exactly the verdicts the runtime
app commits, and the customer/order attributes the clauses name correspond to
real columns in [`../ground-truth/schema.sql`](../ground-truth/schema.sql)
(`customers.registration_age_hours`, `orders.status` incl. `REFUNDED`,
`orders.value_usd` vs. the maximum refund threshold).

## Files

| File | Role |
|---|---|
| `refund_policy.md` | **The upper bound itself** — the normative ceiling, in the strict token-parsable schema of spec §2 (`# REFUND_POLICY_SPEC_START … END`). Normative English only: no code, schema, or prompt syntax. |
| `handbook.py` | The single parser + structural validator. Turns the handbook into `Policy` objects (with `clause_ids`); `extract_block()` yields the per-policy markdown the dispatch loop copies into `spec.txt` (§1). |
| `gate_checks.py` | The upper-bound-driven gate primitives (§3): `gate_a_policy_centric` (handbook stays WHAT-not-HOW) and `gate_c_coverage` (exerciser's matrix covers every `CLAUSE_n`). |
| `validate_handbook.py` | Self-check: structure + Gate A + **grounding** against `../ground-truth` + gate wiring. Exits nonzero on failure. |
| `provision.sh` | Deploys `refund_policy.md` to `/opt/squeeze/shared/refund_policy.md` as `root:root 0444` (§1), refusing to deploy a malformed or non-policy-centric ceiling. |

## Usage

```bash
python3 handbook.py            # list the parsed policy
python3 validate_handbook.py   # structure + Gate A + grounding + gate wiring; exit 0 == sound
python3 gate_checks.py         # pilot: Gate A / Gate C on good and bad inputs
sudo ./provision.sh            # deploy (inside the LXC container)
```

## The schema (spec §2)

The policy block declares, in fixed tokens the parser keys on:

- `# REFUND_POLICY_SPEC_START` … `# REFUND_POLICY_SPEC_END` markers
- `## POLICY_ID: POL_REFUND_042`
- `**Threat Category:**`, `**Flagship Incident Anchor:**`, `**Status:**`
  (`BINDING` | `DRAFT` | `DEPRECATED`)
- `### 1. Plain English Core Property`
- `### 2. Enumerated Obligation Clauses` — `**CLAUSE_n:**` bullets
- `### 3. The Core Negative Vector` — `**Target Exploit:**` +
  `**Expected System Failure Point:**` (its action ∈ {`REIMBURSE`,`DENY`,`ESCALATE`})
- `### 4. Explicit NOT-Claims` — `**NOT_CLAIM_n:**` bullets

`handbook.py` enforces: markers present, valid status, a non-empty core property,
clause ids that are **sequential `CLAUSE_1..N`** (≥1), a negative vector whose
expected failsafe action is exactly one allowed decision, and at least one
NOT-claim (so the validation horizon is explicitly bounded).

### The three clauses (grounded in `../ground-truth/`)

| Clause | Obligation | Grounding column / value |
|---|---|---|
| `CLAUSE_1` | Target order must not already be `REFUNDED` (no duplicate credit). | `orders.status` (`REFUNDED`) |
| `CLAUSE_2` | Legal keywords / litigation threats → abort with `ESCALATE`. | decision token `ESCALATE` |
| `CLAUSE_3` | Account registration age < 48h attempting a max-value refund → `DENY`. | `customers.registration_age_hours`, `orders.value_usd` |

The **Core Negative Vector** (already-refunded order + legal coercion → `ESCALATE`)
is the live ground-truth archive case 006 (legal threat beats already-refunded).

## How the upper bound drives the gates (spec §3)

- **Gate A (Structural Content Integrity)** — `gate_a_policy_centric(text)` blocks
  the compilation track if the published policy contains code fragments
  (` ``` `, `def `, `import `), DB schema assumptions (`CREATE TABLE`, `SELECT `,
  `INSERT INTO`), or direct prompting / injection syntax (`system prompt:`,
  "ignore previous instructions"). The handbook must state *what* the boundary is,
  never *how* a prompt or program achieves it.
- **Gate C (Structural Coverage Map)** — `gate_c_coverage(policy, matrix)` reads
  the exerciser's `validation_matrix.json` and fails the build unless every
  `CLAUSE_n` is mapped to a targeted, non-trivial case — even if every dialogue
  flow ran cleanly. This is the trap defense: a prompt that quietly drops the
  `CLAUSE_2` legal-escalation rule is caught because no case covers it.

`validation_matrix.json` (written by the independent exerciser) schema:

```json
[
  {"name": "already-refunded order blocked", "clause": "CLAUSE_1", "check": "REFUNDED -> not REIMBURSE"},
  {"name": "legal threat escalates",         "clause": "CLAUSE_2", "check": "lawsuit -> ESCALATE"},
  {"name": "new high-value refund denied",   "clause": "CLAUSE_3", "check": "age<48 & value>=500 -> DENY"}
]
```

(The fenced JSON above lives in this README, not in the normative `refund_policy.md`
— Gate A forbids such syntax inside the policy itself.)

## Grounding (spec / reality alignment)

`validate_handbook.py`'s grounding step is the upper-bound analogue of the ground
truth's "every decision recomputes". It proves the ceiling is dischargeable:

1. the decision tokens the clauses + negative vector use are exactly a subset of
   the app's allowed decisions (`REIMBURSE`/`DENY`/`ESCALATE`), and the failsafe
   action is one of them;
2. each attribute the clauses name (registration age, REFUNDED status,
   value/threshold) is backed by a real column in `../ground-truth/schema.sql`.

A normative claim no runtime verdict could satisfy is rejected here, not
discovered downstream.

## Adaptations (surfaced, not hidden)

- **Schema fidelity.** `refund_policy.md` uses the spec §2 schema verbatim,
  including `CLAUSE_1..3`, the negative vector, and both NOT-claims. The
  `[cite_start]` / `[cite: …]` citation artifacts in the spec source are
  authoring metadata and are stripped from the published policy.
- **Two NOT_CLAIM_2 / negative-vector wordings de-jargoned for Gate A.** The spec
  draft phrases NOT_CLAIM_2 as "This system prompt matrix …" and the
  expected-failure point as an explicit call to `/api/session/action`. Naming an
  API path / "system prompt" inside a *policy* leans toward HOW (and "system
  prompt:" is a Gate A injection marker). The published policy keeps the exact
  meaning but says "This policy block …" and "must … commit a definitive state
  assignment of ESCALATE", so it states the WHAT (escalate, never duplicate
  credit) without prescribing the wiring. No obligation is weakened.
