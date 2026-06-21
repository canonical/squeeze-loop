bibkey: shinn2023reflexion
citation: Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao. "Reflexion: Language Agents with Verbal Reinforcement Learning." NeurIPS 2023. arXiv:2303.11366.
arxiv: 2303.11366   read: FULL (via ar5iv/arxiv-html)   access-date: 2026-06-12

CLAIM CARDS

1. Quote (§3): "Reflexion is flexible enough to incorporate various types (scalar values or free-form language) and sources (external or internally simulated) of feedback signals."
   Anchor: §3 Reflexion framework.
   Paraphrase: The feedback driving reflection is not a single fixed signal; it can be scalar or linguistic, external or self-simulated - test signals are one option among several.

2. Quote (§4.2, HotpotQA): "we use exact match answer grading using the environment to give a binary success signal."
   Anchor: §4.2 (reasoning task).
   Paraphrase: For reasoning, the grounding signal is exact-match correctness, not unit tests.

3. Quote (§4.3, Programming): the implementation uses self-generated unit tests - "we use Chain-of-Thought prompting to produce diverse, extensive tests" and then "filter for syntactically valid test statements by attempting to construct a valid abstract syntax tree (AST)."
   Anchor: §4.3 (code generation; HumanEval/MBPP).
   Paraphrase: Only the programming tasks ground reflection in (self-generated) unit-test signals; AlfWorld uses heuristic scalar rewards and HotpotQA uses exact-match - confirming test-signal grounding is one mode among several.

METHOD: Reflexion converts task feedback into verbal self-reflections stored in an episodic memory buffer, which condition the agent on subsequent trials (verbal reinforcement learning, no weight updates). The feedback source is task-dependent: heuristic scalar rewards in decision-making (ALFWorld), exact-match binary signals in reasoning (HotpotQA), and self-generated unit tests in programming (HumanEval, MBPP). Reflections accumulate across trials to improve performance.

LIMITATIONS (authors' own): Depends on the LLM's self-evaluation/self-reflection quality, which can be inaccurate; for code, self-generated tests can be wrong, producing false pass/fail signals; bounded by the long-term memory window and by tasks where useful natural-language feedback can be derived.

CONTRIBUTION: Cited for "Reflexion ... (optionally grounding it in test signals)." The body confirms test-signal grounding is exactly that - optional and task-specific (used for code/HumanEval via self-generated unit tests, §4.3), while other tasks use scalar reward (ALFWorld) or exact-match (HotpotQA, §4.2), with §3 explicitly stating feedback types/sources vary. VERDICT: SUPPORTED. The "optionally" / "one mode among others" framing is accurate per §3 and the per-task implementations.
