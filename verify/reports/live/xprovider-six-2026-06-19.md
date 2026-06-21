# Cross-provider §6 replication — does genuine model diversity decorrelate the blind spot? — 2026-06-19

**Why.** §6 shows model-based casts ship the SAME coherent-and-wrong reading on
contradiction/underspecification cases, and only the executable oracle catches it. The paper
(abstract, §4.4, §10) flagged the STRONGER claim — that the evidence barrier beats *genuine model
diversity* — as "owed a cross-provider replication." This is that replication: the SAME
`build_cases()` A/B/C cases used in §6, rerun across pretraining lineages INDEPENDENT of the
Anthropic author, scored against the SAME executable oracle.

Runner: `eval/live/run_xprovider_six.py` (reuses `run_underspec.load_probe`/`score`, so cases and
scoring are byte-identical to §6's runner). Non-deterministic; logged, NOT gated.

## Providers actually run (genuinely independent lineages)

| provider | model | status |
|---|---|---|
| Anthropic | claude haiku/sonnet/opus | anchor — from the §6 repeated-draws run (`six-repeated-draws-2026-06-19.md`) |
| Alibaba | `qwen3.6:35b` (MLX) | **full A/B/C, clean** |
| Google | `gemma4:31b` | **A/B clean**; C incomplete (host degraded mid-run, see below) |
| Meta | `llama4:16x17b` | spot-check only (smoke); full run not feasible (see below) |
| DeepSeek | `deepseek-r1:70b` | spot-check only; full run not feasible |
| OpenAI | `gpt-oss:120b` | **EXCLUDED — unloadable model blob** (`failed to load model from .../blobs/sha256-90a618…`) |

**Infrastructure honesty (INSUFFICIENT ≠ coherent-and-wrong).** This ran on a local ollama host
where only the qwen MLX builds are fast (~6 s/draw). The non-MLX large models are slow
(gemma ~88 s/draw on long prompts; llama4 ~76 s for even a one-word reply; deepseek-r1:70b a
reasoning model at ~200 s/draw that `think:false` did not tame), and partway through the host
degraded — a trivial gemma call began timing out at 60 s — producing empty/UNPARSED responses on
the long C (API-contract) prompts. **UNPARSED/timeout responses are infrastructure failures, not
coherent-and-wrong answers, and are EXCLUDED from rates** (never counted as errors). The run was
stopped rather than let host timeouts contaminate the C cells. DeepSeek-r1 (reasoning latency) and
OpenAI gpt-oss (unloadable) could not be run in full; a powered multi-provider replication on
adequate hardware remains future work. What follows is **preliminary but real** cross-provider
evidence — two full independent lineages plus a four-lineage spot check — not a powered study.

## Per-provider error rate (error = answer ≠ executable oracle; UNPARSED excluded)

| instance | Alibaba qwen3.6:35b | Google gemma4:31b | Anthropic Claude (§6, weak/mid/strong) |
|---|---|---|---|
| A (contradiction, analytics) | **11/15 = 0.73** | **11/15 = 0.73** | 46/75, 25/75, 40/75 = .61/.33/.53 |
| B (underspecified refund)    | 2/16 = 0.12 | 1/16 = 0.06 | 15/80, 13/80, 14/80 ≈ .17 |
| C (contradiction, API)       | 4/15 = 0.27 (3 timeouts excl.) | incomplete (excluded) | 11/90, 12/90, 10/90 ≈ .12 |

Two independent non-Anthropic lineages land at the **identical 0.73** error on archetype A.

## Convergence — the load-bearing analysis

The question is not just "do independent providers err" but "do they err the SAME WAY" — if genuine
model diversity decorrelated the blind spot, independent lineages would scatter across readings.
They do not.

**A (contradiction), Alibaba vs Google, 15 comparable cases:**
- identical answer (right OR wrong) on **13/15**;
- both wrong on **10** cases — and on **10/10 (100%)** they chose the **SAME wrong reading**;
- per fork, the two lineages err in lockstep: `active` 3/3 & 3/3, `net_vs_gross` 3/3 & 3/3,
  `survivorship` 3/3 & 3/3, `utc_halfopen` 2/2 & 2/2.

**B (underspecified refund), Alibaba vs Google, 16 comparable cases:**
- identical answer on **15/16**; the single both-wrong case → **same wrong reading (1/1)**.

**Four-lineage spot check (smoke, 1 case/instance, `xprovider-six-smoke.jsonl`):**
- A `net_vs_directive`: oracle A → Alibaba, DeepSeek, Google, Meta **all chose B** (identical).
- B `delivered_default`: oracle ESCALATE → all four **chose REIMBURSE** (identical).
- C `patch_null`: oracle DELETED → Alibaba & Google **chose UNCHANGED** (identical; Meta/DeepSeek
  got it right here).

## Conclusion for the paper

The "owed" cross-provider question is answered in the predicted direction. On the contradiction
archetype, two genuinely independent pretraining lineages (Alibaba qwen, Google gemma) reproduce the
coherent-and-wrong error at the **same rate (0.73)** and, where they err, on the **same fork with
the same wrong reading (10/10)**; a four-lineage spot check adding Meta and DeepSeek lands on the same
wrong reading on two of three sampled cases (split on C, where Meta and DeepSeek read it correctly —
convergence strong, not total). **Genuine model diversity largely does NOT decorrelate the blind spot** — it lives
in the task (the authority contradiction / unstated default), not in the weights. This is exactly
why model-disjointness alone cannot catch it and the executable lower bound must. It corroborates,
across providers, the §6 finding and the architecture's central attribution (disjointness of
EVIDENCE, not of model weights, carries the gate). Stated as preliminary, not powered: the full
runs were limited by host hardware (qwen MLX fast; gemma/llama/deepseek slow or stalling;
gpt-oss unloadable), so a powered multi-provider study on adequate hardware remains future work.

Raw: `xprovider-six-2026-06-19.jsonl` (full transcript), `xprovider-six-2026-06-19.json`
(aggregates + convergence), `xprovider-six-smoke.jsonl` (four-lineage spot check).
