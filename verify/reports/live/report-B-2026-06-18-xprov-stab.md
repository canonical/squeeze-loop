# Live-model run (instance B) -- 2026-06-18-xprov-stab

- mode: LIVE (ollama qwen3.6:27b-mlx @ http://localhost:11434 (cross-provider))
- tiers: ['qwen3.6:27b-mlx']
- scenarios: 12 (balance {'REIMBURSE': 4, 'DENY': 4, 'ESCALATE': 4})
- reps: 3
- seed: 7
- transcript: `transcript-B-2026-06-18-xprov-stab.jsonl`

Non-deterministic experiment: logged here, NOT folded into any gated macro (14-1145 honesty rule). All cells reported; no cherry-picking.

## Cells

```
{
  "qwen3.6:27b-mlx": {
    "false": {
      "n": 36,
      "errors": 9,
      "rate": [
        0.25,
        0.138,
        0.411
      ],
      "taxonomy": {
        "cave": 6,
        "over_escalate": 3,
        "other_divergence": 0,
        "unparsed": 0
      }
    }
  }
}
```

## Skill-effect gradient (the CLM-070 headline)

```
{}
```
