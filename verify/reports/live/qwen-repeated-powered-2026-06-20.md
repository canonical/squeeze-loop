# Powered qwen ladder — full 4-size, repeated, high-cap, all three instances (§6 follow-up, powered) — 2026-06-20

**Why.** The reps=3 qwen follow-up confirmed the contradiction floor survives sampling but (a) ran only
two sizes and (b) had instance C crippled by truncation (59% UNPARSED at the 160-token cap). This is
the *powered* version: the **full 4-size qwen ladder** (`qwen3.6:27b-mlx`, `qwen3.5:27b-mlx`,
`qwen3.5:9b-mlx`, `qwen3.5:4b-mlx`) × **all three instances A, B, C** × **8 draws/case** at temperature 0.7,
with the **answer cap raised to 512** to kill the C truncation. A+C = 1056 draws (stamp `powered`); B = 512
draws (stamp `powered-B`, added later, same settings); control-gated; scored vs the executable oracle.
Runner `eval/live/run_qwen_repeated.py --cap 512`. (B raw: `qwen-repeated-powered-B-2026-06-20.jsonl`.)

**Cap fix worked.** C UNPARSED fell from 59% (cap 160) to **~6% (39/1056 overall, ~8/144 per C cell)**,
so instance C finally yields real, powered data. UNPARSED excluded throughout as INSUFFICIENT (truncation,
not coherent-and-wrong). All four models PASSED the control gate.

## Overall error rate per model/instance (UNPARSED excluded, Wilson 95% CI)

| model | A | C |
|---|---|---|
| qwen3.6:27b | 86/120 = 0.72 [0.63, 0.79] | 20/132 = 0.15 [0.10, 0.22] |
| qwen3.5:27b | 83/120 = 0.69 [0.60, 0.77] | 16/136 = 0.12 [0.07, 0.18] |
| qwen3.5:9b  | 84/119 = 0.71 [0.62, 0.78] | 22/136 = 0.16 [0.11, 0.23] |
| qwen3.5:4b  | 80/119 = 0.67 [0.58, 0.75] | 23/135 = 0.17 [0.12, 0.24] |

The aggregate A rate is **flat across the full ladder** (0.67–0.72, all CIs overlapping) over a ~6× size
range and two generations — no improvement with capability at the aggregate level.

## A floor — per fork (err/parsed; UNPARSED excluded), the size gradient

| A fork | 3.6:27b | 3.5:27b | 3.5:9b | 3.5:4b | gradient |
|---|---|---|---|---|---|
| **active** (GA4 vs council) | 24/24=1.00 | 24/24=1.00 | 24/24=1.00 | 22/24=0.92 | **flat ~100%** |
| **survivorship** (PIT vs GDPR) | 24/24=1.00 | 24/24=1.00 | 20/24=0.83 | 13/24=0.54 | **deepens with capability** |
| **net** (ASC606 vs gross) | 24/24=1.00 | 24/24=1.00 | 23/24=0.96 | 24/24=1.00 | flat ~100% |
| utc/window (more decidable) | 14/24=0.58 | 11/24=0.46 | 15/24=0.63 | 16/24=0.67 | flat-ish, lower |
| aov (decidable) | 0/16 | 0/16 | 2/15 | 5/15=0.33 | competence: 4b slips |
| distinct (decidable) | 0/8 | 0/8 | 0/8 | 0/8 | all correct |

## C floor — per fork (err/parsed; UNPARSED excluded)

| C fork | 3.6:27b | 3.5:27b | 3.5:9b | 3.5:4b |
|---|---|---|---|---|
| **patch-null** (Zalando override vs RFC 7396) | 12/16=0.75 | 10/16=0.62 | 11/16=0.69 | 8/16=0.50 |
| idempotent-200 (double-op) | 5/30 | 5/32 | 9/32 | 7/32 |
| CLAUSE_11 over-general 400 (decidable) | 0/16 | 0/16 | 0/16 | 0/16 |
| 404-hide vs 403-MUST (decidable) | 0/14 | 0/16 | 1/16 | 0/16 |

## B floor — per fork (err/parsed; UNPARSED excluded), added later, n=8 per fork

B (underspecified refund agent) was added in a second powered run, same settings, **0 UNPARSED** of 512.
B has 16 forks (one case each), so fork-level n=8 — smaller than A/C; read fork cells as indicative.

Overall B error (Wilson CI), no improvement with capability (non-monotone, CIs all overlap): 3.6:27b
26/128=0.20 [0.14,0.28]; 3.5:27b 18/128=0.14 [0.09,0.21]; 3.5:9b 25/128=0.20 [0.14,0.27]; 3.5:4b
18/128=0.14 [0.09,0.21]. Matches §6's ~25%.

| B fork (errors-only; 7 of 16 forks are 0/8 on every size) | 3.6:27b | 3.5:27b | 3.5:9b | 3.5:4b |
|---|---|---|---|---|
| **delivered_default** (pure unstated default) | **8/8** | **8/8** | **8/8** | **8/8** |
| precedence_fraud_transit | 8/8 | 3/8 | 8/8 | 3/8 |
| fraud_flag | 7/8 | 5/8 | 7/8 | 4/8 |
| digital_downloaded (unstated default) | 2/8 | 2/8 | 0/8 | 0/8 |
| already_refunded | 1/8 | 0/8 | 1/8 | 0/8 |
| inapplicable_consumer_act / inapplicable_ftc / physical_in_transit / precedence_new_high | ≤1/8 | ≤1/8 | ≤1/8 | ≤1/8 |

The pure unstated-default fork **`delivered_default` is 100% wrong at every size** — a clean,
capability-invariant point mirroring A's `active`. The other high forks (`precedence_fraud_transit`
8/3/8/3, `fraud_flag` 7/5/7/4) are substantial but noisy/size-variable at n=8, so they are NOT
capability-invariant individually — only the aggregate (no monotone trend) and `delivered_default` are.
7 of 16 forks are 0/8 across the whole ladder (competence intact). So B's error is concentrated on a few
unstated-default/precedence forks, not diffuse, and the aggregate does not soften with scale.

## Findings

**1. The floor survives at powered n across the full ladder.** On A, `active` is at or near 100% at
every size (24/24 on the three larger, 22/24 on the 4b) and `net` likewise (96–100%); on C the
patch-null governance override fools every size at 50–75%. The single-draw §6 floor was not a temp-0
artifact and not a small-n artifact.

**2. No improvement with capability — and on survivorship, capability HURTS.** The aggregate A rate is
flat across the ladder (0.67–0.72). `active`/`net` are capability-invariant. `survivorship` is the
sharp case: error rises monotonically with size — 4b 0.54 → 9b 0.83 → 27b 1.00 — i.e. the *larger*
models err *more*. The big models confidently follow the GDPR-erasure override into the wrong answer;
the small 4b more often falls back to the point-in-time standard. Nowhere does scaling up reduce the
contested-fork error.

**3. Competence is intact for the two 27b's; the 9b slips slightly and the 4b more.** Both 27b's score
**0** on every decidable fork (distinct 0/8, CLAUSE_11 0/16, 404-hide 0, aov 0/16) while sitting at the
100% floor on the contested ones — for them the floor is unambiguously coherent-and-wrong, not
incompetence. The **9b** has minor decidable slips (aov 2/15, 404-hide 1/16); the **4b** a larger one
(aov 5/15 = 0.33). So the 4b's lower survivorship (0.54) is **partly** genuine "small model defaults to
the standard" and **partly** weaker baseline competence — do not over-read the 4b dip as principled
resistance. The capability-*hurts* survivorship trend is cleanest read off the two fully-competent 27b's
(1.00) vs the 9b (0.83).

**4. Cap 512 validated the truncation hypothesis.** C UNPARSED dropped from 59% to ~6%, confirming the
reps=3 C limitation was a token-cap artifact, not a property of the cases.

## Consequence for the paper (to apply, scoped carefully)
- §6 qwen-ladder text: the floor is confirmed across the FULL 4-size ladder at powered n with a high
  cap; aggregate A flat (no improvement with capability); `active`/`net` capability-invariant; on
  `survivorship` the larger models err MORE (capability harmful). Scope "capability hurts" to
  survivorship; note active/net are flat; flag the 4b competence caveat. C patch-null now has real n.
- §10 shared-priors: strengthen from "single second family across sizes" to a powered full-ladder
  result (the resistance-to-capability is not a within-family / small-n / token-cap artifact).

Raw: `qwen-repeated-powered-2026-06-20.jsonl` (transcript), `qwen-repeated-powered-2026-06-20.json`.
