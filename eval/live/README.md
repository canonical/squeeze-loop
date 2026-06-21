# Live-model evaluation harness

Runnable implementation of `14-1145-live-model-plan.md` — the powered live-model run that
would close **CLM-070** and give the paper its first *measured* efficacy result (currently
deferred; see the paper's Scope statement and §Evaluation Protocol). It measures, per
**(model tier × skill × scenario × repetition)**, whether a live model decides instance
B's refund scenarios as the executable answer key (`reference_policy.decide`) does. The
model replaces the deterministic caving bot; **error = live decision ≠ oracle**.

This is deliberately *not* wired into the reflexive squeeze: live-model numbers are
non-deterministic and are never folded into the gated `\Res…` macros (the plan's honesty
rule). The harness writes a logged report + per-call transcript only.

## Files

- `harness.py` — the runner (stdlib only): seeded balanced scenario pool → one model call
  per case (per-task independence) → parse decision → score vs oracle → Wilson CIs, skill-
  effect gradient, error taxonomy → report + JSONL transcript under
  `verify/reports/live/`.
- `model_client.py` — the **pluggable** model adapter. Ships unimplemented (no API key in
  the repo). Wire `call_model(model_id, system, user)` to your provider (an Anthropic
  example is in the docstring).

## Run it

```bash
# 1. validate the pipeline with NO API (deterministic surrogate; not a measurement):
python3 eval/live/harness.py --dry-run --mini-pilot --stamp dry

# 2. wire eval/live/model_client.py to your provider, then mini-pilot per the plan:
python3 eval/live/harness.py --tiers strong --mini-pilot --stamp 2026-06-15-pilot

# 3. the full B run (the first real gradient):
python3 eval/live/harness.py --tiers weak,mid,strong \
      --scenarios 40 --reps 3 --seed 7 --stamp 2026-06-15-B
```

`--tiers` are your model ids, ordered weak→strong (the gradient axis). `--stamp` is the
run id used in the output filenames — **pass it in** (the harness does not invent a
timestamp, so runs stay reproducible/labelled).

## What it reports

- **error rate per cell** with a Wilson 95% CI;
- **skill effect = err(no-skill) − err(with-skill)** per tier — the CLM-070 headline (the
  pilot suggests this is sign-varying: positive for weak models, negative for strong);
- **error taxonomy**: `cave` (refund the policy withholds) / `over_escalate` / other /
  unparsed — the pilot showed the skill trades one for another;
- a **balanced** pool (equal REIMBURSE/DENY/ESCALATE oracle counts) so "always-X" cannot
  score well.

## Honesty rules (from the plan, enforced here)

- **No fabrication.** No client + no `--dry-run` ⇒ loud SKIP (exit 3), nothing run. The
  `--dry-run` surrogate is labelled `SURROGATE … NOT real model output` everywhere and
  validates plumbing only.
- **Logged, not gated.** Results live under `verify/reports/live/` with the seed, model
  ids, and full transcript. No `\Res…` macro may depend on a live number unless it is a
  frozen, archived run with the transcript committed.
- **No cherry-picking.** Every cell is reported, including null/negative skill effects.
  Do not scan tiers/scenarios for a flattering result.
- **Pilot-before-machinery.** `--mini-pilot` first (8 scenarios, 1 rep, one tier); scale
  only after it shows a non-zero error surface.

## Cost

Live calls = tiers × scenarios × 2 (skill) × reps. B alone at 3×40×2×3 ≈ **720 calls**.
This is a budgeted experiment, not an iteration — launch it explicitly.

## Extending to A / C / D

The plan says: run A/C/D only after a per-instance mini-pilot confirms a non-zero live
error surface (they may hit the near-zero wall the paper documents). Each needs its own
scenario builder + oracle adapter (B's are `SITUATIONS`/`CHARACTERS` + `reference_policy`
here); the scoring, metrics, and honesty scaffolding are reusable.

## Pipeline comparison (the H1 study -- 14-1145 sec. 7)

`pipeline_harness.py` runs the deferred comparison against alternative pipelines on B's
underspecified pool (prose policy only; the oracle encodes defaults the prose never states).
Each pipeline runs end-to-end with **reasoning allowed**, and its SHIPPED decision is scored
against the shared executable answer key (`reference_policy.decide`):

- **P0 raw**, **P1 self_critique**, **P2 same_ctx_critic**, **P3 llm_judge**,
  **P4 self_tests**, **P5a squeeze_exer** (disjoint exerciser from the spec only),
  **P5b squeeze_oracle** (the executable oracle is the gate).

Primary metric: **shipped-coherent-and-wrong** (shipped AND != oracle). Secondary:
**false-block** (blocked a correct decision) and **good-block**. Honest caveat (printed and
in 14-1145 sec. 7.4): P5b ships 0 wrong *by construction* -- it requires an executable
oracle (expressibility-from-below); that is the contribution, reported as such.

```bash
python3 eval/live/pipeline_harness.py --dry-run --scenarios 12 --stamp dry   # validate
python3 eval/live/pipeline_harness.py --tiers weak,mid,strong --scenarios 40 --reps 3 --stamp 2026-06-15-pipelines  # real
```
Non-deterministic -> logged under `verify/reports/live/`, NOT gated. No client + no
`--dry-run` => loud SKIP.
