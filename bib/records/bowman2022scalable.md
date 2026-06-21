bibkey: bowman2022scalable
citation: Bowman, S. R., Hyun, J., Perez, E., Chen, E., Pettit, C., Heiner, S., Lukosiute, K., Askell, A., Jones, A., Chen, A., et al. (2022). Measuring Progress on Scalable Oversight for Large Language Models. arXiv:2211.03540.
arxiv: 2211.03540   read: FULL (via ar5iv HTML)   access-date: 2026-06-12

CLAIM CARDS

1. Quote: "scalable oversight: the problem of supervising systems that potentially outperform us on most skills relevant to the task at hand." (§1) -> Paraphrase: Scalable oversight is supervising systems more capable than the supervisor.

2. Quote: scalable oversight is "the ability to provide reliable supervision ... to models in a way that will remain effective past the point that models start to achieve broadly human-level performance." (§1) -> Paraphrase: It targets supervision that holds at and beyond human-level capability.

3. Quote (sandwiching): "a model is already more capable than a typical human, but less capable than an expert ('sandwiching' ...)." (§2) -> Paraphrase: The sandwiching paradigm tests non-expert humans overseeing a model that beats them but trails experts.

4. Quote: non-expert participants are "missing some crucial skills or knowledge, such that without assistance they cannot reliably ... oversee a model's performance." (§2) -> Paraphrase: Weaker (non-expert) overseers supervise a stronger worker model.

METHOD
The paper frames scalable oversight and proposes the "sandwiching" experimental paradigm: pick tasks where a model sits between typical humans and domain experts in capability. Non-expert humans interact with a 52B dialog model on QA benchmarks (MMLU, time-limited QuALITY) without external resources, and human-model team accuracy is compared to unassisted humans, the model alone, and expert baselines. Results are a proof-of-concept that human-model teams can outperform either alone.

LIMITATIONS (authors' own)
Acknowledges six limitations including: relaxations depart from full sandwiching (static models, no fine-tuning); revealing correct answers removes deployment reliability challenges; only directly-elicited knowledge is extracted; outlier removal creates selection effects; human-model teams still make confident errors; and multiple-choice QA covers tasks the model already trained on.

CONTRIBUTION (why cited here)
Supports the manuscript claim that "scalable-oversight research asks how weaker judges can supervise stronger workers." §1 and §2 define scalable oversight and the sandwiching paradigm precisely in these terms (non-experts overseeing a more-capable model). VERDICT: SUPPORTED.
