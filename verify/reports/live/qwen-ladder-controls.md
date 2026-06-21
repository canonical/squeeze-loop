# Cross-provider qwen capability ladder (control-gated) — A/C/B probes

host: http://localhost:11434


## qwen3.6:27b-mlx  (qwen36-27b-mlx)
controls: PASS
- control expected CONTRADICT got CONTRADICT -> OK
- control expected CONSISTENT got CONSISTENT -> OK
  - A: 15 cases, 0 unparsed -> answers_A_qwen36-27b-mlx.json
  - C: 18 cases, 2 unparsed -> answers_C_qwen36-27b-mlx.json
  - B: 16 cases, 1 unparsed -> answers_B_qwen36-27b-mlx.json

## qwen3.5:27b-mlx  (qwen35-27b-mlx)
controls: PASS
- control expected CONTRADICT got CONTRADICT -> OK
- control expected CONSISTENT got CONSISTENT -> OK
  - A: 15 cases, 0 unparsed -> answers_A_qwen35-27b-mlx.json
  - C: 18 cases, 1 unparsed -> answers_C_qwen35-27b-mlx.json
  - B: 16 cases, 0 unparsed -> answers_B_qwen35-27b-mlx.json

## qwen3.5:9b-mlx  (qwen35-9b-mlx)
controls: PASS
- control expected CONTRADICT got CONTRADICT -> OK
- control expected CONSISTENT got CONSISTENT -> OK
  - A: 15 cases, 0 unparsed -> answers_A_qwen35-9b-mlx.json
  - C: 18 cases, 1 unparsed -> answers_C_qwen35-9b-mlx.json
  - B: 16 cases, 0 unparsed -> answers_B_qwen35-9b-mlx.json

## qwen3.5:4b-mlx  (qwen35-4b-mlx)
controls: PASS
- control expected CONTRADICT got CONTRADICT -> OK
- control expected CONSISTENT got CONSISTENT -> OK
  - A: 15 cases, 0 unparsed -> answers_A_qwen35-4b-mlx.json
  - C: 18 cases, 1 unparsed -> answers_C_qwen35-4b-mlx.json
  - B: 16 cases, 0 unparsed -> answers_B_qwen35-4b-mlx.json
