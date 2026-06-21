# Section 6 repeated-draws — A/B/C contradiction & underspecification ladders — 2026-06-19

**Why.** §6's live finding ("no improvement with capability; only the executable oracle catches")
was reported at ONE draw per case (review14 #3). This repeats every case 5x per Claude tier
(haiku/sonnet/opus) to convert single-draw cells into rates and test whether the patterns survive
repetition. 49 cases x 3 tiers x 5 reps = 735 draws, Claude sub-agents (workflow wf_d6e4148b-cad),
scored answer-vs-executable-oracle. 0 failures.

## Per-instance × tier error rate (error = answer != oracle; n = cases×5)

| instance | haiku | sonnet | opus | single-draw was |
|---|---|---|---|---|
| A (contradiction, analytics) | 46/75 = 0.61 | 25/75 = 0.33 | 40/75 = 0.53 | 12/15, 9/15, 6/15 |
| B (underspecified refund)    | 15/80 = 0.19 | 13/80 = 0.16 | 14/80 = 0.18 | ~3/12 per tier |
| C (contradiction, API)       | 11/90 = 0.12 | 12/90 = 0.13 | 10/90 = 0.11 | 0/18, 2/18, 2/18 |

## Findings

**1. "No improvement with capability" — confirmed and strengthened.** A is non-monotone (opus 0.53 ≈
haiku 0.61, both above sonnet 0.33); B is flat (~0.17, opus ≈ haiku); C is flat (~0.12). The strongest
model is never reliably better than the weakest. The single-draw A "12/15→9/15→6/15" looked like a
clean monotone decrease; it was not — repetition shows it non-monotone.

**2. The A capability floor is now sharp.** Per-fork errors (n=15/fork/tier where a fork has 3 cases):
- `active` (GA4 active-user vs product-council): **15/15 = 100% wrong at haiku, sonnet, AND opus** — a
  clean capability-invariant 100% floor on a fork where both authorities are legitimate.
- `survivorship` (point-in-time vs GDPR Art.17): 15/15 haiku & opus, 4/15 sonnet — high, non-monotone.
- `net_vs_gross_directive`: 10 / 0 / 4 (haiku/sonnet/opus) — the more decidable conflict; capability helps.
- `utc_halfopen_vs_calendar`: 6 / 6 / 6 — flat.

**3. The C "inversion" was a single-draw artifact — CORRECTED.** The single draw had haiku 0/18
("weakest model right"), read as a capability-inversion. Over 5 reps the weakest tier errs **11/90**,
and all three tiers are flat ~0.12 — there is NO inversion. The governance-override fork persists
across tiers (patch-null/Zalando ~4–5 at every tier; the over-broad-CLAUSE_10 fork is actually worse
at the weakest tier, 4/1/0). So C is capability-flat, not inverting; "the weakest model trusts the
RFC and is right" does not survive repetition.

**4. B's unstated-default forks persist across tiers.** `delivered_default` errs 5 at every tier;
`digital_downloaded` 4–5 — the pure unstated-default cases are missed regardless of capability,
consistent with §6.

## CASE-SET NOTE (important)
A and C here are the SAME case sets as §6 (15 and 18 cases — my n is exactly 5×). So A and C are
clean repeated-draw updates of the §6 contradiction ladders. **B is NOT**: `build_cases('B')` is the
16-case run_underspec refund probe, whereas §6's underspecification refund result quotes a *balanced
12-case gap pool* (the within-family / qwen-comparison subset, "3/12", "three cases missed"). So the B
result above (16 cases, ~0.17) is a separate, corroborating repeated measurement — it is NOT
substituted into the §6 12-pool sentences, to avoid conflating two different case sets.

## Consequence for the paper (applied)
- §6 A: replaced the single-draw 12/15→9/15→6/15 (apparent monotone fall) with the repeated rates and
  a non-monotone framing; foregrounded the `active` 100%-at-all-tiers floor.
- §6 C: corrected "the pattern inverts (weakest right)" -> capability-flat ~0.12, no inversion (the
  single-draw inversion did not replicate); the governance-override fork fools all tiers similarly.
- §6 B (12-pool) + the cross-provider 3/12: LEFT UNCHANGED (case-set mismatch above); B corroborates
  "flat, no improvement" but is not folded in.
- §9 recap: A/C updated to the repeated figures (5 draws/case); B left at the 12-pool 3/12.
- abstract / contribution (iii) / conclusion: dropped the draw-count claim (the contradiction finding,
  A/C, is now repeated; the underspecification 12-pool stays single-draw) — qualitative "no monotone
  trend / non-monotone" only.
- qwen ladder (§6/§10): kept the floor reproduction (consistent); SOFTENED the qwen patch-null
  "fools larger qwens more" — one-draw-per-case on qwen, and the Claude repeated draws show
  single-draw inversions are unreliable. (A qwen repeated-draws run is the natural follow-up.)

Raw aggregate: workflow wf_d6e4148b-cad return value (in-workflow scoring vs oracle).
