bibkey: yao2022react
citation: Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao. "ReAct: Synergizing Reasoning and Acting in Language Models." ICLR 2023. arXiv:2210.03629.
arxiv: 2210.03629   read: FULL (via ar5iv/arxiv-html)   access-date: 2026-06-12

CLAIM CARDS

1. Quote (§2): "ReAct prompts LLMs to generate both verbal reasoning traces and actions pertaining to a task in an interleaved manner."
   Anchor: §2 "ReAct: Synergizing Reasoning + Acting".
   Paraphrase: ReAct alternates between free-form reasoning traces (thoughts) and task actions in a single trajectory.

2. Quote (§2): "This allows the model to perform dynamic reasoning to create, maintain, and adjust high-level plans for acting (reason to act), while also interact with the external environments to incorporate additional information into reasoning (act to reason)."
   Anchor: §2.
   Paraphrase: Reasoning guides action selection, and the information returned from acting (observations) is folded back into subsequent reasoning - a bidirectional loop.

3. Quote (§3.2): "Each trajectory consists of multiple thought-action-observation steps."
   Anchor: §3.2 (HotpotQA/Fever setup).
   Paraphrase: The concrete unit of a ReAct rollout is the thought -> action -> observation triple, repeated.

METHOD: ReAct is a prompting paradigm in which the LLM emits interleaved reasoning traces and executable actions; actions query an external environment (e.g. Wikipedia search/lookup API, or ALFWorld/WebShop) and return observations appended to the context for the next step. It is evaluated on multi-hop QA (HotpotQA), fact verification (Fever), and interactive decision tasks (ALFWorld, WebShop). Reasoning helps plan actions while observations ground and correct reasoning.

LIMITATIONS (authors' own): ReAct's performance is bounded by the quality/coverage of the external knowledge it retrieves (non-informative search results can derail reasoning); structured action spaces can be restrictive; it can underperform pure CoT when internal reasoning suffices and retrieval adds noise (motivating CoT-ReAct combinations).

CONTRIBUTION: Cited for "ReAct interleaves chain-of-thought reasoning with actions whose observations feed back into the next step." Body states this explicitly (§2 interleaving and "act to reason"; §3.2 thought-action-observation steps). VERDICT: SUPPORTED. Exact match between claim and body.
