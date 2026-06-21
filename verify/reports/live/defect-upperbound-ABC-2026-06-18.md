# Defect-based upper bounds: capable-model error surface (A, C) — 2026-06-18

- **Model:** Claude subagents acting as tiers (weak=haiku-4.5, mid=sonnet-4.6, strong=opus-4.8),
  one subagent per (instance, tier), each answering all cases in isolation, given ONLY the
  prose upper bound + scenario (no oracle/ground-truth access).
- **Design change:** the A and C upper bounds were rebuilt to be genuine SOFT truths *with
  defects* — internally contradictory clauses / a clause that contradicts its own example /
  conflicting cited standards — instead of the earlier "too good" pinned specs (which gave 0%
  error because a capable model just complies). Oracle = the executable lower bound
  (A: metrics.py; C: reference_server) which implements ONE defensible resolution.
- **Status:** logged, NOT gated. One draw per tier (small n per cell).

## Error rate vs the executable oracle (coherent-and-wrong reading of the defective spec)

A was rebuilt TWICE: v1 ("formula vs sloppy example") washed out at opus; v2 was the
authority-vs-authority redesign but a prompt leak ("the value the executable definition
intends") let opus key on the oracle; v3 below is authority-vs-authority WITH the leak
removed (neutral "resolve the conflict and report the figure you would").

| Instance (defect-based upper bound) | haiku (weak) | sonnet (mid) | opus (strong) |
|---|---|---|---|
| **A v1 — formula vs sloppy example** | 8/13 = 62% | 3/13 = 23% | 0/13 = **0%** |
| **A v3 — authority-vs-authority (de-leaked)** | 12/15 = **80%** | 9/15 = **60%** | 6/15 = **40%** |
| C (pre-audit: predict-the-server framing + annotated options) | 4/18 = 22% | 0/18 = 0% | 2/18 = 11% |
| **C — authority-vs-authority (de-leaked, commit framing)** | 0/18 = **0%** | 2/18 = **11%** | 2/18 = **11%** |

### C audit + de-leak

C had no hard oracle leak (the manifest's §6 "which side the server takes" was kept out of the
model-facing text), but it was NOT measured like A v3: it asked "what does the SERVER do?"
(predict-the-oracle) and annotated each option with its source authority. Both were fixed to
match A: implementer-commit framing ("how would YOU implement this endpoint?") and bare options
(operational gloss only, no RFC/Zalando/AIP/CLAUSE tags). Oracles unchanged.

The de-leak made the result CLEANER: all error now concentrates on the single `patch-null`
fork (RFC 7396 null-deletes vs an explicit Zalando "GOVERNANCE OVERRIDE" null-ignores), and it
is **capability-INVERTING** — haiku trusts the defining RFC and is right (0/18); sonnet and opus
both defer to the authoritative-sounding "GOVERNANCE OVERRIDE" and are wrong (2/18 each). Every
other C fork (404-vs-403, error taxonomy, Retry-After over-reach, idempotency, terminal-state)
was resolved toward the oracle by all tiers via "MUST beats MAY / specific beats general /
reject the over-broad clause" — capability-robust, decidable conflicts.

### A v3 per-fork capability pattern (the key result)

| Fork (two named authorities) | haiku | sonnet | opus | verdict |
|---|---|---|---|---|
| net: ASC 606 (net) vs Finance Directive (gross) | wrong | wrong | OK | capability-DEPENDENT |
| window: ISO half-open vs Calendar Policy (inclusive) | wrong | OK | OK | capability-DEPENDENT |
| **active: GA4 any-event vs Product Council (exclude login)** | wrong | wrong | **wrong** | **capability-INVARIANT** |
| **survivorship: point-in-time vs GDPR Art.17 (exclude deleted)** | wrong | wrong | **wrong** | **capability-INVARIANT** |

opus's own reasoning: it rejected the gross directive ("an internal directive can't redefine
GAAP revenue for investors") and the inclusive window ("double-counts the boundary"), but
**deferred to the override on the two genuinely-contested forks** — "active user has no binding
external standard, a company may define its own engagement metric" (excluded login) and "GDPR
erasure is binding law over an internal point-in-time convention" (excluded deleted). Both are
coherent-but-wrong per the executable oracle. That 6/15 = 40% is opus's capability-invariant
floor: the two forks where BOTH authorities are legitimate and no first-principles tiebreak
exists, so only the executable lower bound adjudicates.

### B run with Claude tiers (2026-06-18) -- two faces of B

B was run with Claude subagent tiers two ways, and the contrast reinforces the "thin vs
defective" lesson:

| B probe | haiku | sonnet | opus | character |
|---|---|---|---|---|
| **12-case gap pool** (genuinely underspecified; 2026-06-15 study, same subagent-tier method) | 6/24 = **25%** | 8/24 = **33%** | 6/24 = **25%** | **capability-INVARIANT** |
| 16-case enriched `src/B` probe (new, 2026-06-18) | 1/16 = **6%** | 2/16 = **12.5%** | 0/16 = **0%** | "too good": clauses specified the gaps away |

The gap pool is the B that belongs next to A and C: a genuine soft-truth defect (silence) that
even opus does not resolve (25%, flat across tiers). The enriched 16-case probe ADDED explicit
clauses (partial-refund, dispute, digital, precedence, statute) that closed most gaps -- so opus
gets 0% and only the residual `delivered_default` pure-gap trips the weaker tiers
(haiku/sonnet picked DENY; opus correctly ESCALATEs). This is the same "too good" effect that
made the first A/C attempts give 0%: enriching an upper bound toward COMPLETENESS removes the
error surface; only enriching it toward genuine DEFECT (gap or contradiction) keeps it.

(For reference, the gap pool also gave a cross-provider qwen ~19-25%.)

## Findings

1. **The defect redesign produces a real error surface** (vs the old pinned specs = 0%).
   A capable model, handed a self-contradictory soft spec, commits coherent-and-wrong readings
   that only the executable lower bound catches.

2. **A's defects are capability-DEPENDENT (monotonic 62% → 23% → 0%).** A's contradictions are
   mostly "the binding formula vs a sloppy narrative/example": stronger models resolve them
   correctly by trusting the executable formula. So a *sloppy* contradiction is a soft-truth gap
   that capability closes — not a capability-invariant one.
   - haiku fell for the wrong worked example (reported gross-as-net), the login-exclusion
     clause, and the exclude-deleted clause.
   - sonnet only fell for the active=any-event vs logins-never-count contradiction.
   - opus resolved all of them toward the oracle.

3. **C's `patch-null` defect is capability-NON-monotonic (opus 11% > sonnet 0%).** This is the
   most interesting result. The defect is framed as an explicit *"GOVERNANCE OVERRIDE"* clause
   (Zalando #123: null==absent) contradicting the defining standard the server implements
   (RFC 7396: null deletes). **opus deferred to the authoritative-sounding governance directive
   and got it wrong; sonnet trusted the defining RFC and got it right.** Capability did not
   protect the strongest model against an authoritative-sounding *wrong* clause — only the
   executable lower bound caught it. haiku additionally mis-resolved the terminal-state
   idempotency contradiction (200 no-op instead of 409).

## Bearing on the "near-zero error rate" concern

A nonzero, comparative baseline now exists, and it demonstrates the squeeze thesis sharply:
the value of the executable lower bound is exactly to adjudicate a *defective soft spec* that a
capable model reads coherently-but-wrongly. The richest case (C `patch-null`) shows the failure
is not merely a weak-model artifact: the strongest model is the one an authoritative-sounding
contradictory clause fools. The honest nuance is that not all defects are capability-invariant
(A's sloppy-example contradictions wash out by opus); the capability-invariant ones are the
*authority-vs-authority* contradictions, which is the kind worth foregrounding.

Caveat: one draw per tier; a powered version needs repetitions and more cases per fork.

## Cross-provider qwen capability ladder (control-gated; 2026-06-18)

To test whether the A floor and the C inversion are Claude-specific, the SAME A/C/B probes were
run through a qwen ladder on Ollama (Alibaba; sizes 4B/9B/27B, generations 3.5 and 3.6).
CONTROL GATE: every model passed both control probes (known-contradiction + known-consistent) and
emitted parseable answers, so their errors are coherent-and-wrong, not incompetence. Error vs the
executable oracle (one draw per case; logged via run_qwen_ladder.py + subagent_eval.py):

| Model (Alibaba)   | A          | C          | B (enriched) |
|-------------------|------------|------------|--------------|
| qwen3.5:4b        | 12/15=80%  | 2/18=11%   | 2/16=12.5%   |
| qwen3.5:9b        | 10/15=67%  | 3/18=17%   | 3/16=19%     |
| qwen3.5:27b       | 13/15=87%  | 3/18=17%   | 3/16=19%     |
| qwen3.6:27b       | 10/15=67%  | 6/18=33%   | 6/16=38%     |

REPRODUCTION VERDICT — both headline patterns hold across the independent provider family:
- A capability-invariant FLOOR reproduces, now provider- AND scale-invariant: the `active` fork is
  wrong for ALL qwen sizes (3/3 each) AND opus; `survivorship` wrong for 3/3 on three qwens + opus
  (2/3 on the 9B). The floor is the defect, not Claude -- it survives the jump to Alibaba and the
  drop to a 4B.
- C INVERSION reproduces: `patch-null` (defer to the "governance override" vs RFC 7396) is wrong
  2/2 for BOTH 27B qwens (matching sonnet+opus), but only 1/2 for qwen 9B/4B and 0/2 for haiku --
  larger/more-capable models are more fooled by the authoritative-sounding override, second
  provider.

Caveats: the four qwen are ONE provider family across two generations and three sizes (a
second-family size+generation gradient, NOT four independent providers); qwen errs more on A
overall (67-87%) and on B than Claude, partly a competence gap on the multi-clause B policy plus a
little UNPARSED noise on the 27B; one draw per cell. Records: answers_{A,C,B}_qwen*.json,
qwen-ladder-controls.md.
