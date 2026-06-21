bibkey: wu2023autogen
citation: Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., Jiang, L., Zhang, X., Zhang, S., Liu, J., Awadallah, A. H., White, R. W., Burger, D., & Wang, C. (2023). AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation. arXiv:2308.08155.
arxiv: 2308.08155   read: FULL (via ar5iv HTML)   access-date: 2026-06-12

CLAIM CARDS

1. Quote: "a conversable agent is an entity with a specific role that can pass messages to send and receive information to and from other conversable agents." (§2.1) -> Paraphrase: Agents are message-passing entities with roles (the unit of the framework).

2. Quote: conversation programming "considers two concepts: the first is computation -- the actions agents take to compute their response ... And the second is control flow." (§2.2) -> Paraphrase: Conversation programming is a paradigm splitting multi-agent interaction into computation and control flow.

3. Quote: both steps are achieved "via a fusion of natural and programming languages" with "unified conversation interfaces ... including a send/receive function." (§2.2) -> Paraphrase: Developers program conversations by mixing natural language and code over a unified send/receive interface.

METHOD
AutoGen is an open-source framework whose core abstraction is the conversable, customizable agent that can combine LLMs, tools, and humans. Multi-agent applications are built via "conversation programming," which organizes the system around conversation-centric computation and control flow expressed through a fusion of natural and programming languages. The authors validate the framework empirically across six application domains (math, coding, decision-making) against baselines such as ChatGPT+Code Interpreter, LangChain ReAct, and Multi-Agent Debate.

LIMITATIONS (authors' own)
The authors note that "increasing the number of agents and other degrees of freedom ... may also introduce new safety challenges that require additional studies," and that human oversight remains essential for high-risk deployments.

CONTRIBUTION (why cited here)
Supports the manuscript reference to "AutoGen's conversation programming." §2.2 explicitly defines conversation programming as a paradigm of computation + control flow over conversable agents, matching the citation exactly. VERDICT: SUPPORTED.
