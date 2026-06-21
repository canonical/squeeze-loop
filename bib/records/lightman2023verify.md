bibkey: lightman2023verify
citation: Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, Karl Cobbe. "Let's Verify Step by Step." ICLR 2024. arXiv:2305.20050.
arxiv: 2305.20050   read: FULL (via ar5iv/arxiv-html)   access-date: 2026-06-12

CLAIM CARDS

1. Quote (§1 Introduction): "Outcome-supervised reward models (ORMs) are trained using only the final result of the model's chain-of-thought, while process-supervised reward models (PRMs) receive feedback for each step in the chain-of-thought."
   Anchor: §1 Introduction.
   Paraphrase: Outcome supervision rewards only the final answer; process supervision moves the training signal onto each individual (verified) reasoning step.

2. Quote (§4.1, "Process vs Outcome Supervision"): "process supervision significantly outperforms both forms of outcome supervision at all data collection scales."
   Anchor: §4.1 small-scale comparison.
   Paraphrase: Across data-collection scales, the PRM beats outcome supervision (including final-answer-checked variants).

3. Quote (Abstract / §3 Large-scale): "our process-supervised model solves 78% of problems from a representative subset of the MATH test set."
   Anchor: §3 large-scale results; Figure 3 reports PRM (~78.2%) above ORM (~72.4%) best-of-N on the MATH subset, the gap widening with N.
   Paraphrase: The large-scale PRM reaches 78% on MATH and dominates the ORM under best-of-N selection.

METHOD: The authors train reward models on the MATH dataset under two regimes - outcome supervision (label = final-answer correctness) and process supervision (human label on each reasoning step) - and release the PRM800K step-level annotation dataset. Reward models are used as verifiers to re-rank many sampled solutions (best-of-N). They compare PRM vs ORM at both large and controlled small scales.

LIMITATIONS (authors' own): Process supervision required expensive human step-level labels (mitigated partly via active learning); the strongest comparisons are on MATH and a generator finetuned from a large base model, so generalization beyond this setting is not guaranteed; best-of-N evaluation can be confounded by reward-model gaming at very large N.

CONTRIBUTION: Cited for "Process supervision moves the signal from outcomes to verified steps" and "process supervision significantly outperforms outcome supervision." Both are stated near-verbatim in the body (§1 for the step-vs-outcome signal; §4.1 for the "significantly outperforms ... at all data collection scales" result; §3/Fig 3 for the numbers). VERDICT: SUPPORTED. Body confirms the abstract; no overclaim.
