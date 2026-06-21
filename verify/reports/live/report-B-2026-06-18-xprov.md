# Live-model run (instance B) -- 2026-06-18-xprov

- mode: LIVE (ollama qwen3.6:27b-mlx @ http://localhost:11434 (cross-provider))
- tiers: ['qwen3.6:27b-mlx']
- scenarios: 12 (balance {'REIMBURSE': 4, 'DENY': 4, 'ESCALATE': 4})
- reps: 1
- seed: 7
- transcript: `transcript-B-2026-06-18-xprov.jsonl`

Non-deterministic experiment: logged here, NOT folded into any gated macro (14-1145 honesty rule). All cells reported; no cherry-picking.

## Cells

```
{
  "qwen3.6:27b-mlx": {
    "false": {
      "n": 12,
      "errors": 3,
      "rate": [
        0.25,
        0.089,
        0.532
      ],
      "taxonomy": {
        "cave": 2,
        "over_escalate": 1,
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
