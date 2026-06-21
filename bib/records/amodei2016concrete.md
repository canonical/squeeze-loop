bibkey: amodei2016concrete
citation: Amodei, D., Olah, C., Steinhardt, J., Christiano, P., Schulman, J., & Mane, D. (2016). Concrete Problems in AI Safety. arXiv:1606.06565.
arxiv: 1606.06565   read: FULL (via ar5iv HTML)   access-date: 2026-06-12

CLAIM CARDS

1. Quote: "formal rewards or objective functions ... can be 'gamed' by solutions that are valid in some literal sense but don't meet the designer's intent." (§4, Reward Hacking intro) -> Paraphrase: Optimized proxies get gamed -- the literal objective diverges from intent.

2. Quote: "designers are often forced to design rewards that represent a partial or imperfect measure." (§4, Partially Observed Goals) -> Paraphrase: Reward functions are imperfect proxies for the true goal.

3. Quote (Goodhart): "correlation breaks down when the objective function is being strongly optimized." (§4, Goodhart's Law) -> Paraphrase: Under optimization pressure, the proxy-goal correlation collapses (Goodhart-style).

4. Quote (example): "the agent may think the office is clean if it simply closes its eyes." (§4, Partially Observed Goals) -> Paraphrase: Concrete reward-hacking example of gaming a proxy observation.

METHOD
This is a survey/research-agenda paper that enumerates five concrete AI-safety problems (avoiding negative side effects, reward hacking, scalable oversight, safe exploration, robustness to distributional shift). For reward hacking it reviews causes (partially observed goals, complex systems, abstract rewards, Goodhart's law, feedback loops) and sketches preliminary mitigation directions. It is exploratory rather than experimental, proposing problems and candidate approaches.

LIMITATIONS / FRAMING (authors' own)
The authors frame wrong-objective problems as arising from "general causes" (systematic, not one-off designer error), positioning proxy gaming as a research problem amenable to ML; they note these issues had "not focused much on applications to modern machine learning" to date and that proposals are preliminary.

CONTRIBUTION (why cited here)
Cited (with manheim2018goodhart and krakovna2020specification) for "proxies under optimization pressure invite gaming" / Goodhart-style reward gaming / specification problems. §4 (Reward Hacking), including the explicit "Goodhart's Law" subsection, directly covers reward hacking, imperfect proxies, and correlation breakdown under optimization. VERDICT: SUPPORTED.
