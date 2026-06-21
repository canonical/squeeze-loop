bibkey: hong2023metagpt
citation: Hong, S., Zhuge, M., Chen, J., Zheng, X., Cheng, Y., Zhang, C., Wang, J., Wang, Z., Yau, S. K. S., Lin, Z., Zhou, L., Ran, C., Xiao, L., Wu, C., & Schmidhuber, J. (2023). MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework. arXiv:2308.00352. ICLR 2024.
arxiv: 2308.00352   read: FULL (via ar5iv HTML)   access-date: 2026-06-12

CLAIM CARDS

1. Quote (SOP): "we follow SOP in software development, which enables all agents to work in a sequential manner." (§3.1) -> Paraphrase: MetaGPT encodes Standard Operating Procedures into a sequential multi-agent pipeline of specialized roles.

2. Quote (roles): workflow runs Product Manager -> Architect -> Project Manager -> Engineers -> QA Engineer (§3.1; Figure 1). -> Paraphrase: Tasks are decomposed into role-specific actionable procedures.

3. Quote (STRUCTURED vs CHAT -- the special-scrutiny claim): "Unlike ChatDev ... agents in MetaGPT communicate through documents and diagrams (structured outputs) rather than dialogue." (§3.2) -> Paraphrase: BODY explicitly contrasts MetaGPT's structured-document communication against free-form chat.

4. Quote (shared message pool): "we introduce a shared message pool that allows all agents to exchange messages directly ... Any agent can directly retrieve required information from the shared pool." (§3.2; Figure 2) -> Paraphrase: Communication is mediated by a centralized shared message pool, not point-to-point dialogue.

5. Quote (publish-subscribe): "Agents use a shared message pool to publish structured messages ... subscribe to relevant messages based on their profiles." (Figure 2 caption; §3.2) -> Paraphrase: A role-based publish-subscribe mechanism routes structured messages to dependent agents.

METHOD
MetaGPT instantiates human Standard Operating Procedures from software engineering as a fixed sequence of specialized agent roles, each producing typed artifacts (PRD, design/diagrams, code, tests). Instead of free chat, agents publish structured outputs to a shared message pool and subscribe to the artifacts relevant to their role, activating only when prerequisite dependencies are met. The system is evaluated on code-generation benchmarks (e.g., HumanEval, MBPP) and a self-built SoftwareDev dataset against single-agent and other multi-agent baselines.

LIMITATIONS (authors' own)
Each software project is executed independently with no cross-project learning (Appendix A.1); the framework modifies role specialization but not the structured-communication interface itself, indicating incomplete adaptation across workflow dimensions (§3.2). (The paper also notes occasional resource/token overhead and that complex large-scale requirements remain hard.)

CONTRIBUTION (why cited here)
Supports BOTH manuscript claims: (1) MetaGPT encodes SOP pipelines with role specialization (§3.1), and (2) -- the load-bearing claim -- roles communicate through typed/structured documents via a shared message pool with publish-subscribe, NOT free chat. The BODY (§3.2, Figure 2) states this verbatim and explicitly contrasts it with ChatDev's dialogue. The distinction is in the body, not just the abstract. VERDICT: SUPPORTED (body-confirmed for the structured-document / message-pool claim).
