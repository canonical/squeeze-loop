# Powered multi-provider replication — gemma + llama vs the powered qwen ladder — 2026-06-20

**Why.** The cross-provider replication (`xprovider-six-2026-06-19`) was reps=1; the qwen capability
ladder was powered but single-family. This run powers the cross-provider axis: the two non-qwen
genuinely-independent lineages — **Google `gemma4:31b`** and **Meta `llama4:16x17b`** — over instances
A, B, C at **8 draws/case, cap 512, temp 0.7** (784 draws), scored vs the executable oracle, to test
whether the contradiction/underspecification floor reproduces across providers *at power*. Runner
`eval/live/run_qwen_repeated.py --cap 512`; control-gated (both PASSED). Compared against the powered
qwen ladder (`qwen-repeated-powered-2026-06-20` + `-B`), flagship `qwen3.6:27b-mlx`.

Non-MLX models are slow (~85s gemma, ~63–130s llama); gemma completed fully before llama (banking).
UNPARSED excluded as INSUFFICIENT (18/784 total; llama C had 10 — the long API prompts).

## Overall error per instance (UNPARSED excluded, Wilson 95% CI)

| instance | qwen3.6:27b | gemma4:31b | llama4:16x17b |
|---|---|---|---|
| A (contradiction) | 86/120=0.72 [.63,.79] | 94/118=0.80 [.72,.86] | 84/120=0.70 [.61,.77] |
| B (underspecification) | 26/128=0.20 [.14,.28] | 9/128=0.07 [.04,.13] | 33/128=0.26 [.19,.34] |
| C (split-plane) | 20/132=0.15 [.10,.22] | 35/136=0.26 [.19,.34] | 28/134=0.21 [.15,.29] |

## Floor side by side (err/parsed; UNPARSED excluded)

| fork | qwen3.6:27b | gemma4:31b | llama4:16x17b |
|---|---|---|---|
| **active** (GA4 vs council, legit-vs-legit) | **24/24=1.00** | **24/24=1.00** | **24/24=1.00** |
| **survivorship** (PIT vs GDPR, legit-vs-legit) | **24/24=1.00** | **24/24=1.00** | **24/24=1.00** |
| **B delivered_default** (pure unstated default) | **8/8=1.00** | **8/8=1.00** | **8/8=1.00** |
| net (vs gross directive) | 24/24=1.00 | 24/24=1.00 | 16/24=0.67 |
| utc/window (more decidable) | 14/24=0.58 | 22/22=1.00 | 19/24=0.79 |
| C patch-null (Zalando override vs RFC 7396) | 12/16=0.75 | 16/16=1.00 | 7/16=0.44 |

## Findings

**1. A provider-invariant floor on the genuinely-balanced forks.** The two A forks where *both*
authorities are legitimate (`active`, `survivorship`) and B's pure unstated-default (`delivered_default`)
are wrong **100%** on all three genuinely-independent pretraining lineages — Alibaba, Google, Meta —
at powered n (24, 24, 8 per cell), none sharing pretraining with each other or with the Anthropic
author of the paper. This is the strongest form of the "owed cross-provider replication": where the
contradiction is real and balanced, every provider falls, every time.

**2. The softer forks diverge by provider — in BOTH directions.** Where one side of the conflict is
weaker (a sloppy `net`/gross directive, an over-broad clause, a vendor `patch-null` override), the
providers do *not* agree: on `net`, qwen/gemma are 1.00 but llama resists at 0.67; on C `patch-null`,
gemma 1.00 > qwen 0.75 > llama 0.44; on `utc`, 0.58/1.00/0.79. So this is **not** a generic
override-compliance bias that would inflate every fork — gemma is the most compliant, llama the least,
qwen between. The floor is high *specifically* on the genuinely-balanced contradictions, which is the
result the architecture predicts (the oracle is needed exactly where authorities genuinely collide).

**3. Overall rates differ but overlap the qwen band.** A is 0.70–0.80 across providers (gemma highest,
llama lowest); B and C differ more (gemma's B is a low 0.07 — it handles the non-floor refund forks
well — yet its `delivered_default` is still 8/8). Competence is intact: the decidable forks stay low
for all three. So the differences are in how each provider treats the *weaker-side* conflicts, not in
baseline ability.

## Consequence for the paper (to apply, scoped carefully)
- The multi-provider replication moves from "preliminary / reps=1" to **powered across three
  independent lineages** (qwen, gemma, llama) at n=24/contested-fork. Update §6 + §10.
- Scope the claim precisely: **uniform 100% holds only on the genuinely-balanced forks**
  (active, survivorship, delivered_default); `net`/`utc`/`patch-null` are provider-variable (llama
  resists `net` and `patch-null` more, gemma less). Do NOT claim uniform cross-provider 100% everywhere.
- This still corroborates "disjointness of evidence, not model weights, carries the gate": genuine
  model diversity does not save you on the real contradictions — the floor is provider-invariant there.

Raw: `qwen-repeated-xprov-powered-2026-06-20.jsonl` (transcript), `.json` (aggregates). qwen ladder for
comparison: `qwen-repeated-powered-2026-06-20.{jsonl,md}` + `-B`.
