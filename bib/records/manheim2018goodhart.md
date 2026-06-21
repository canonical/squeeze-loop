bibkey: manheim2018goodhart
citation: David Manheim and Scott Garrabrant. "Categorizing Variants of Goodhart's Law." arXiv preprint arXiv:1803.04585, 2018.
arxiv/url: arXiv:1803.04585   read: FULL (ar5iv HTML, body sections 1-4)   access-date: 2026-06-12
CLAIM CARDS (each: a <25-word verbatim quote + §/section anchor + paraphrase)
- "Optimization causes a collapse of the statistical relationship between a goal which the optimizer intends and the proxy." [§ overview / Goodhart effect]
  Paraphrase: Optimizing a proxy degrades its statistical link to the intended goal — the core Goodhart mechanism the paper formalizes.
- "When selecting for a proxy measure, you select not only for the true goal, but also for the difference between the proxy and the goal." [§1 Regressional Goodhart]
  Paraphrase: First categorized mechanism: selection on a proxy also amplifies the proxy-goal gap.
- "Worlds in which the proxy takes an extreme value may be very different from the ordinary worlds in which the relationship between the proxy and the goal was observed." [§2 Extremal Goodhart]
  Paraphrase: Pushing a proxy to extremes leaves the regime where it tracked the goal.
- "When the causal path between the proxy and the goal is indirect, intervening can change the relationship between the measure and proxy." [§3 Causal Goodhart]
  Paraphrase: Intervening on a non-causal proxy breaks the correlation it relied on.
- "The agent then acts by changing the observed causal structure due to incompletely aligned goals in a way that creates a Goodhart effect." [§4 Adversarial Goodhart / Cobra Effect]
  Paraphrase: A misaligned actor able to influence the metric will manipulate it, producing gaming under optimization pressure.
- "The agent choice of metric need not be a useful proxy for their goal absent the regulator's action." [§4 Adversarial Goodhart / Campbell's Law]
  Paraphrase: An optimizing agent games a regulator's metric, correlating its own action with the regulator's proxy rather than the true target.
METHOD (three sentences)
The paper formalizes Goodhart effects over systems with states S, a true goal G(s), and a proxy metric M(s), expanding Garrabrant's earlier observation that "(at least) four different mechanisms" relate to Goodhart's Law. It defines and distinguishes four mechanistic categories — Regressional, Extremal, Causal, and Adversarial Goodhart (the last split into Adversarial Misalignment / Campbell's Law and Cobra Effect) — using causal diagrams and simple equations. The stated aim is "to explore these mechanisms further, and specify more clearly how they occur."
LIMITATIONS
The authors note the proposed categories "do not match what was originally discussed" historically and that terminology across Goodhart's Law, Campbell's Law, and the Lucas critique is ambiguous; a forthcoming paper is said to address the formal relationships. The treatment is conceptual/illustrative rather than empirically validated, and the Adversarial category is the least formalized.
CONTRIBUTION (why cited here; which manuscript claim it supports; verdict)
Cited (co-cited with amodei2016concrete) for "Goodhart's law in organizational form" and the claim that "proxies under optimization pressure invite gaming" / "the acceptance signal is a proxy, and any actor able to influence its own proxy will, under optimization pressure, satisfy the proxy rather than the target." The paper directly categorizes the mechanisms by which optimizing a proxy diverges from the true goal, and its Adversarial Goodhart section (Campbell's Law / Cobra Effect) specifically covers a self-interested actor that can influence its own metric and games it. VERDICT: SUPPORTED. Body evidence: "The agent then acts by changing the observed causal structure due to incompletely aligned goals in a way that creates a Goodhart effect." Minor caveat: "organizational form" is the manuscript's framing; the paper's term is the multi-agent "Adversarial Goodhart," which maps cleanly onto organizational gaming but does not use that exact phrase.
