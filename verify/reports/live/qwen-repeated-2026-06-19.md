# Repeated qwen draws — does the contradiction floor survive sampling? (§6 follow-up) — 2026-06-19

**Why.** §6 reports the cross-provider qwen ladder at ONE draw per case (deterministic at
temperature~0): it "corroborates the floor but not finer size-ordering claims; a repeated qwen
version is future work." This is that repeated version: each contradiction case (instances A and C)
drawn **3 times at temperature~0.7** across two qwen sizes (the flagship `qwen3.6:27b-mlx` and the
smallest `qwen3.5:4b-mlx`), scored against the SAME executable oracle (`build_cases`), to test whether
the capability-invariant FLOOR survives *sampling* and whether finer size-ordering stabilises.

Runner: `eval/live/run_qwen_repeated.py` (control-gated; reuses `run_underspec` loader/scorer).
Both models PASSED the control gate (known-CONTRADICTION + known-CONSISTENT probes), so their errors
are coherent-and-wrong, not incompetence. Non-deterministic; logged, NOT gated.

**Measurement caveat (honest, up front).** At temperature~0.7 the models reason longer before
answering; on the long instance-**C** (API-contract) prompts they frequently ran past the 160-token
cap before emitting `ANSWER:`, producing **UNPARSED** truncations — **32/54 on the 27b, 25/54 on the
4b**. UNPARSED is an infrastructure truncation, **not** a coherent-and-wrong answer, and is
**excluded** from all rates below. Instance **A** prompts are short and barely truncated (1/45 each),
so A is clean and decisive; **C is truncation-limited and small-n** after exclusion — read it as
corroborating, not establishing.

## Per-model error rate (UNPARSED excluded)

| instance | qwen3.6:27b-mlx | qwen3.5:4b-mlx |
|---|---|---|
| A (contradiction, analytics) | 32/44 = 0.73 | 30/44 = 0.68 |
| C (contradiction, API)       | 5/22 = 0.23 (32 truncations excl.) | 9/29 = 0.31 (25 excl.) |

## A per-fork (UNPARSED excluded) — the floor

| fork | qwen3.6:27b | qwen3.5:4b | note |
|---|---|---|---|
| `active_ga4` vs product-council directive | **9/9 = 1.00** | 7/9 = 0.78 | FLOOR — both authorities legitimate |
| `survivorship` point-in-time vs GDPR Art.17 | **9/9 = 1.00** | 6/9 = 0.67 | FLOOR |
| `net` vs gross-revenue directive | 9/9 = 1.00 | 9/9 = 1.00 | legitimate-authority directive |
| `utc_halfopen` vs calendar policy | 5/8 = 0.62 | 7/9 = 0.78 | the more decidable conflict |
| `aov_zero_orders` | 0/6 = 0.00 | 1/5 = 0.20 | decidable — competence baseline intact |
| `distinct_nonadditive` | 0/3 = 0.00 | 0/3 = 0.00 | decidable — competence intact |

## C patch-null governance override (UNPARSED excluded; small-n)

| fork | qwen3.6:27b | qwen3.5:4b |
|---|---|---|
| Zalando-style ignore keeps `subtitle='S'` after a null patch | 3/3 = 1.00 | 3/3 = 1.00 |
| follows Zalando #123 (ignore null) instead of RFC 7396 | (all truncated) | 1/1 = 1.00 |

## Findings

**1. The contradiction floor SURVIVES repeated sampling.** On A, the legitimate-authority forks stay
at or near 100% wrong over three temp-0.7 draws per case: `net` 9/9 on both sizes, `active` 9/9 on the
flagship, `survivorship` 9/9 on the flagship. The single-draw §6 floor was not a temp-0 artifact — it
holds under sampling. In the parsed C subset the patch-null governance override is missed unanimously
(3/3, 3/3, 1/1), consistent with §6 though small-n after truncation.

**2. No improvement with capability — confirmed within the qwen family.** The *larger* 27b errs
**more** on the genuinely contested forks than the small 4b (`active` 1.00 vs 0.78; `survivorship` 1.00
vs 0.67), and they tie at 1.00 on `net`. Bigger is not better here; capability does not buy resistance
to the authority contradiction. This matches the Claude non-monotone result (§6) and is the opposite of
a clean "larger is more capable, so errs less" ordering.

**3. The floor is the defect, not incompetence.** Both models passed the control gate, and both score
near zero on the decidable forks (`aov_zero_orders`, `distinct_nonadditive`): 27b 0/9, 4b 1/8 (a lone
slip) — they CAN compute the unambiguous cases; they fail specifically where two legitimate authorities
collide. (No clean size ordering on the contested forks either: 27b and 4b tie at 1.00 on `net`, the 4b
errs *more* on `utc_halfopen`, and the 27b errs more on `active`/`survivorship` — non-monotone, like the
Claude ladder.) So the high floor
is coherent-and-wrong, exactly the failure mode the executable lower bound exists to catch.

**4. Size-ordering caveat stands, sharpened not settled.** With only two qwen sizes, and C
truncation-limited, this confirms "no improvement with capability" but still does not establish a fine
size *gradient*; the §6 lesson (single draws cannot settle ordering; the corrected C inversion) means
even these 3-draw cells warrant the hedge. A higher token cap (to kill the C truncation) and the full
4-size ladder remain the cleaner future run.

## Consequence for the paper (applied)
- §6 qwen-ladder caveat: the floor is now confirmed under *repeated* qwen draws (not just one temp-0
  draw), with the larger model no better (more wrong) on the contested forks; C corroborates but is
  truncation-limited. The "single draw per case ... a repeated qwen version is future work" hedge is
  updated to "repeated (3 draws) on two sizes: floor survives, no improvement with capability;
  full-ladder/higher-cap version still future work."
- §10 shared-priors: the within-second-family resistance-to-capability claim is strengthened from a
  single draw to repeated draws.

Raw: `qwen-repeated-2026-06-19.jsonl` (full transcript), `qwen-repeated-2026-06-19.json` (aggregates).
