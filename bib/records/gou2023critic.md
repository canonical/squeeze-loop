bibkey: gou2023critic
citation: Zhibin Gou, Zhihong Shao, Yeyun Gong, Yelong Shen, Yujiu Yang, Nan Duan, Weizhu Chen. "CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing." ICLR 2024. arXiv:2305.11738.
arxiv: 2305.11738   read: FULL (via arxiv PDF text extraction; ar5iv/arxiv-html conversion failed)   access-date: 2026-06-12

CLAIM CARDS

1. Quote (§4.1 QA, Results, point 4): "Tool-interaction plays a critical role in CRITIC, as the model's own critiques contribute marginally to the improvement (-0.03 and +2.33 F1 with the two LLMs), and even fall short compared to the initial output."
   Anchor: §4.1 "Free-form Question Answering", Results; Table 1 row "CRITIC w/o Tool".
   Paraphrase: When the search tool is removed (CRITIC w/o Tool), self-critique adds almost nothing (-0.03 / +2.33 F1) and on one model is worse than the uncorrected output. Tool feedback is what drives the gains.

2. Quote (§4.2 Math, Results, point 3): "Without execution feedback from the interpreter, the ability of LLMs to correct programs becomes limited and unstable. This can result in surprising performance deterioration, such as the 1.8-point decrease observed on text-davinci-003."
   Anchor: §4.2 "Mathematical Program Synthesis", Results; Table 2 row "w/o Tool" (e.g. GSM8k 78.2 -> 77.0; column with +0.0 / -1.8 deltas).
   Paraphrase: Removing the interpreter (intrinsic-only correction) yields limited, unstable correction and can actively degrade accuracy.

3. Quote (Contributions, §1): "Highlighting the inadequacy of LLMs in self-verification and self-correction, and emphasizing that feedback from external tool interaction is crucial for consistent self-improvement of LLMs."
   Anchor: §1 Introduction, contribution (3).
   Paraphrase: The paper's stated thesis is that intrinsic self-verification is inadequate; external tool feedback is the crucial ingredient.

4. Quote (§1): "We observe that exclusive reliance on self-correction without external feedback may yield modest improvements or even deteriorate performance."
   Anchor: §1 Introduction (abstract-echoing finding).
   Paraphrase: Intrinsic-only self-correction gives at best modest gains and can hurt.

5. Quote (Analysis appendix / §5 discussion): "such a 'Self-Verification and Self-Correction' can be remarkably unreliable across [tasks] ... self-correction might surprisingly deteriorate performance for many tasks, even worsening the initial answer (as demonstrated in Table 1, 2 under CRITIC w/o Tool, and in Table 10 under Self-Refine)."
   Anchor: Appendix "On The Unreliability of Self-Correction" (cross-refs Tables 1, 2, 10).
   Paraphrase: Authors explicitly tie intrinsic self-correction's unreliability to the w/o-Tool ablation rows and to Self-Refine.

METHOD: CRITIC is a framework that lets a frozen LLM verify-then-revise its own output by interacting with external text-to-text tools (search API for QA, code interpreter for math, Perspective API for toxicity), using only few-shot prompts and no extra training. It is evaluated on ChatGPT, Text-Davinci-003 and LLaMA-2 (7B/13B/70B) across free-form QA, math program synthesis, and toxicity reduction. The central ablation ("CRITIC w/o Tool") removes the external tool while keeping the same prompting, isolating the contribution of intrinsic self-critique.

LIMITATIONS (authors' own): An LLM "may not always need or be able to leverage appropriate external feedback for different inputs" (Limitations section); the approach depends on access to suitable tools/APIs; the work also notes safety/transparency considerations around self-verification.

CONTRIBUTION: Cited to support the manuscript claim that "CRITIC grounds critiques in external tools and finds such external feedback crucial to sustained self-improvement, where purely intrinsic self-critique falls short." The body contains the direct tool vs no-tool ablation (Tables 1, 2; §4.1 point 4; §4.2 point 3) showing intrinsic-only correction is marginal-to-harmful. VERDICT: SUPPORTED. The softened version is well within what the body proves; notably the original STRONGER comparative ("intrinsic self-critique falls short / can deteriorate performance") would ALSO have been supported verbatim by the body (§4.2: "performance deterioration"; §4.1: "even fall short compared to the initial output"). Abstract alone only asserts "crucial importance of external feedback"; the body upgrades this to an explicit head-to-head ablation, so the BODY strengthens (does not weaken) the verdict.
