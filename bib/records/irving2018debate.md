bibkey: irving2018debate
citation: Irving, G., Christiano, P., & Amodei, D. (2018). AI Safety via Debate. arXiv:1805.00899.
arxiv: 1805.00899   read: FULL (via ar5iv HTML)   access-date: 2026-06-12

CLAIM CARDS

1. Quote: "two agents take turns making short statements up to a limit, then a human judges which of the agents gave the most true, useful information." (Abstract) -> Paraphrase: Two agents make length-limited statements; a human judge picks the winner.

2. Quote: "The two agents take turns making statements s0, s1, ..., sn-1 in S" up to "a limit." (§2, "The debate game") -> Paraphrase: Turn-taking statements are bounded in number/length.

3. Quote: "The judge sees the debate (q,a,s) and decides which agent wins." (§2, "The debate game") -> Paraphrase: The judge, not the agents, adjudicates; agents do not pool full private context.

4. Quote: "Our eventual goal is natural language debate, where the human judges a dialog between the agents." (§2.3) -> Paraphrase: The intended realization is judged natural-language dialogue (still a proposal).

METHOD
The paper proposes a game in which two agents, given a question, alternate short natural-language statements arguing for competing answers, trained via self-play as a zero-sum game. A human judge observes the transcript and declares a winner, under the hypothesis that refuting a lie is easier than constructing one, incentivizing honesty. Only a basic MNIST experiment is provided; natural-language debate remains a proposal.

LIMITATIONS (authors' own)
Debate is "proposal only for the natural language case," supported by just a "basic experiment for MNIST"; significant research is needed to learn whether debate works with real human judges, given belief bias and whether humans can adjudicate complex domain-specific arguments.

CONTRIBUTION (why cited here)
Supports the manuscript claim that "multi-agent debate has agents argue before a judge" with length-limited statements and a judge deciding the winner. The BODY (§2 "The debate game," Abstract) confirms this exactly. VERDICT: SUPPORTED, and it CORRECTLY excludes full-context-sharing: agents make bounded statements adjudicated by a judge -- they do not exchange full reasoning the way Du et al. 2023 do. This validates the manuscript's earlier correction (do not attribute Du-style full-context exchange to this paper).
