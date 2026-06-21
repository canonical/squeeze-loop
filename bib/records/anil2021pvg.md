bibkey: anil2021pvg
citation: Anil, C., Zhang, G., Wu, Y., & Grosse, R. B. (2021). Learning to Give Checkable Answers with Prover-Verifier Games. arXiv:2108.12099.
arxiv: 2108.12099   read: ABSTRACT (arXiv abstract page)   access-date: 2026-06-15

CLAIM CARDS

1. Quote: "a trusted verifier network tries to choose the correct answer, and a more powerful but untrusted prover network attempts to persuade the verifier of a particular answer, regardless of its correctness." (abstract) -> Paraphrase: A trusted (weaker) verifier and a more powerful but untrusted prover are paired; the prover may push any answer, correct or not.

2. Quote: "The goal is for a reliable justification protocol to emerge from this game." (abstract) -> Paraphrase: Checkability is the trained objective -- a justification protocol the verifier can rely on emerges from the game.

METHOD
A game-theoretic framework (Prover-Verifier Games) with simultaneous and sequential variants; the authors identify game configurations with desirable equilibria and test instantiations on algorithmic tasks, showing the verifier learns robust decision rules even when frozen and the prover's messages are directly optimized to convince it.

LIMITATIONS (authors' own)
Abstract states no explicit limitations; results are on algorithmic tasks; robustness is framed positively even under direct optimization to fool the verifier.

CONTRIBUTION (why cited here)
Anchors the manuscript's claim that prover-verifier games are the closest machine-learning neighbour: checkability is pursued by TRAINING a prover/verifier pair, and the "more powerful but untrusted prover ... regardless of its correctness" is a trained model of our coherent-and-wrong. VERDICT: SUPPORTED. The distinction the paper draws -- trained-in-shared-weights vs. enforced organizationally over fixed models -- is consistent with this game-theoretic, training-time formulation.
