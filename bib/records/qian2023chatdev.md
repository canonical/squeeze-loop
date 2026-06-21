bibkey: qian2023chatdev
citation: Qian, C., Liu, W., Liu, H., Chen, N., Dang, Y., Li, J., Yang, C., Chen, W., Su, Y., Cong, X., Xu, J., Li, D., Liu, Z., & Sun, M. (2023). ChatDev: Communicative Agents for Software Development. arXiv:2307.07924. ACL 2024.
arxiv: 2307.07924   read: FULL (via ar5iv HTML)   access-date: 2026-06-12

CLAIM CARDS

1. Quote: "ChatDev, a virtual chat-powered software development company that mirrors the established waterfall model." (Abstract; §1) -> Paraphrase: ChatDev simulates a software company organized along waterfall phases.

2. Quote: phases are "designing, coding, testing, and documenting." (Abstract) with "The chat chain acts as a facilitator, breaking down each stage into atomic subtasks." -> Paraphrase: A chat chain decomposes the waterfall into role-paired atomic chats.

3. Quote: "ChatDev recruits multiple 'software agents' with different roles, such as programmers, reviewers, and testers." (§1) plus CEO/CPO/CTO/designer (§2.2) -> Paraphrase: Role-based agents drawn from a simulated company staff each phase.

4. Quote: each phase decomposes "into multiple atomic chats, each with a specific focus on task-oriented role-playing." (§2.1; Figure 2) -> Paraphrase: Within a phase, an instructor and assistant agent collaborate via multi-turn dialogue.

METHOD
ChatDev models software development as a virtual company executing the waterfall phases of design, coding, testing, and documenting. A "chat chain" decomposes each phase into sequential atomic chats between two role-playing agents (an instructor guiding and an assistant solving) that converse over multiple turns with a shared memory. A communicative-dehallucination / thought-instruction mechanism (role flip) reduces coding hallucinations, and the system is evaluated on generated software tasks.

LIMITATIONS (authors' own)
Best suited to "open and creative software production scenarios where variations are acceptable" given LLM randomness (§5); struggles to "generate perfect source code for high-level or large-scale software requirements" (§5); lacks malicious-intent detection for sensitive file operations, requiring human review before execution (§5).

CONTRIBUTION (why cited here)
Supports the manuscript reference to "ChatDev's software-company simulation" with a chat chain and role-based phases. Confirmed by the abstract and §2.1-2.2 (waterfall phases, chat chain, recruited role agents). VERDICT: SUPPORTED. Note: unlike MetaGPT, ChatDev's intra-phase communication is dialogue-based (multi-turn chat), which is exactly the contrast MetaGPT draws -- keep that distinction intact in the manuscript.
