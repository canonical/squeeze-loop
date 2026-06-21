# Cross-provider disjoint review (editorial gate, gold-standard axis)

backend: ollama
model: qwen3.6:27b-mlx
judge-provider: alibaba
author-provider: anthropic
cross-provider: yes (independent pretraining)
controls-passed: True
authoritative: True
status: AUTHORITATIVE (cross-provider and passes controls)

## probes
  control[contradiction]: expected CONTRADICT, got CONTRADICT -> OK  (CONTRADICT Sentence A states that no strand of in-house evidence is ranked above the other, while Sentence B claims one specific type is the "strongest," implyi)
  control[consistency]: expected CONSISTENT, got CONSISTENT -> OK  (CONSISTENT; Sentence A describes the current study's limitations (exploratory, small sample), while Sentence B proposes a more rigorous future study, which is a)
  live framing probe: CONSISTENT  (CONSISTENT because finding specific defects in a case study does not imply the study was a comprehensive verification or efficacy comparison.)

Non-deterministic (model output); logged, not gated. The standing editorial verdict in editorial_review.md remains the operative one; this records the cross-provider axis (R3: provider-disjointness vs capability). A capable cross-provider judge (OPENAI_API_KEY + CROSS_MODEL, or OLLAMA_HOST + CROSS_MODEL) is the gold standard; it corroborates the framing but is a narrow framing-consistency probe, not the full editorial review.
