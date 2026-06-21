bibkey: wang2023voyager
citation: Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, Anima Anandkumar. "Voyager: An Open-Ended Embodied Agent with Large Language Models." arXiv:2305.16291, 2023 (TMLR 2024).
arxiv: 2305.16291   read: FULL (via ar5iv/arxiv-html)   access-date: 2026-06-12

CLAIM CARDS

1. Quote (§2.3): "During each round of code generation, we execute the generated program to obtain environment feedback and execution errors from the code interpreter, which are incorporated into GPT-4's prompt for the next round of code refinement."
   Anchor: §2.3 "Iterative Prompting Mechanism".
   Paraphrase: Skill code is generated, run in Minecraft, and the resulting environment feedback/errors are fed back to refine the next attempt - an iterative loop grounded in the embodied environment.

2. Quote (§2.3): "This iterative process repeats until self-verification validates the task's completion, at which point we add this new skill to the skill library."
   Anchor: §2.3.
   Paraphrase: Iteration continues until the task is verified as done; the validated skill is then stored, so acquisition is incremental and cumulative.

3. Quote (§2.2): "Complex skills can be synthesized by composing simpler programs, which compounds Voyager's capabilities rapidly over time."
   Anchor: §2.2 "Skill Library".
   Paraphrase: Stored skills (indexed by embeddings) are composed into more complex ones, so the agent's competence grows over time.

METHOD: Voyager is an LLM (GPT-4) agent in Minecraft with three components: an automatic curriculum that proposes progressively harder tasks (§2.1), an iterative prompting mechanism that writes/executes/refines skill code using environment feedback, execution errors, and self-verification (§2.3), and a skill library of validated executable programs retrievable by embedding (§2.2). Skill acquisition is grounded in repeated interaction with the embodied environment.

LIMITATIONS (authors' own): Reliance on GPT-4 (cost, and GPT-3.5 substitution sharply degrades skill generation); operates over a textual Mineflayer/JS abstraction rather than raw perception; occasional hallucinated/incorrect skills and inaccuracies in self-verification.

CONTRIBUTION: Cited for "Voyager iterates skill acquisition against an embodied environment." Body confirms the iterative generate-execute-refine loop grounded in the Minecraft environment, with validated skills accumulated into a growing library (§2.2, §2.3). VERDICT: SUPPORTED.
