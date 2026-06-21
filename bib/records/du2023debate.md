bibkey: du2023debate
citation: Du, Y., Li, S., Torralba, A., Tenenbaum, J. B., & Mordatch, I. (2023). Improving Factuality and Reasoning in Language Models through Multiagent Debate. arXiv:2305.14325. ICML 2024.
arxiv: 2305.14325   read: FULL (via ar5iv HTML)   access-date: 2026-06-12

CLAIM CARDS

1. Quote: "Individual responses from other agents are concatenated and given as context to each agent." (Figure 2 caption; §2.1) -> Paraphrase: Each debater receives the full responses of the other agents as context.

2. Quote: "We iteratively repeat this debate procedure over multiple rounds for improved performance." (§2.1) -> Paraphrase: The full-response exchange recurs across multiple rounds.

3. Quote: "After each agent generates a response, we feed each agent a consensus prompt ... using the updated responses of each agent." (§2.1) -> Paraphrase: Updated full responses are re-fed each round to drive convergence.

METHOD
Multiple LLM instances independently answer a query, then each agent is given the concatenated full responses of the other agents plus a prompt to revise its own answer. This debate is repeated over several rounds until answers converge, with the final answer taken from the consensus. Evaluated on reasoning and factuality benchmarks (arithmetic, GSM8K, biographies, MMLU), showing gains over single-agent and self-consistency baselines.

LIMITATIONS (authors' own)
Computationally expensive (multiple generations and rounds); current models struggle to fully process long debate transcripts, tending to focus on recent generations; debates can converge to confident but incorrect answers, and models lack proper uncertainty expression.

CONTRIBUTION (why cited here)
Supports the manuscript claim that "in its LLM realization the debaters exchange full reasoning across rounds." The BODY (§2.1, Figure 2) confirms agents receive each other's full concatenated responses across multiple rounds. VERDICT: SUPPORTED. Important contrast: this full-context-sharing mechanism is Du et al.'s, and must NOT be attributed to Irving et al. 2018 (which uses length-limited statements before a judge) -- see irving2018debate record.
