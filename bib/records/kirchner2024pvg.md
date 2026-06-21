bibkey: kirchner2024pvg
citation: Kirchner, J. H., Chen, Y., Edwards, H., Leike, J., McAleese, N., & Burda, Y. (2024). Prover-Verifier Games Improve Legibility of LLM Outputs. arXiv:2407.13692.
arxiv: 2407.13692   read: ABSTRACT (arXiv abstract page)   access-date: 2026-06-15

CLAIM CARDS

1. Quote: "training small verifiers to predict solution correctness, 'helpful' provers to produce correct solutions that the verifier accepts, and 'sneaky' provers to produce incorrect solutions that fool the verifier" (abstract) -> Paraphrase: Three components are co-trained -- a small verifier, a helpful prover, and a sneaky prover rewarded for producing convincing wrong solutions.

2. Quote: "legibility training against small verifiers is a plausible technique for increasing output legibility" (abstract) -> Paraphrase: Training against a (weaker) verifier increases the legibility/checkability of the prover's outputs.

METHOD
Iteratively train, on grade-school math, a small verifier plus helpful and sneaky provers; the adversarial pressure pushes the helpful prover toward more legible, checkable reasoning. The verifier is deliberately smaller than the prover (a capability gap).

LIMITATIONS (authors' own)
Evaluated on grade-school math; human-verification study was time-constrained, leaving scalability and generalization open.

CONTRIBUTION (why cited here)
Supports two manuscript claims: (a) the 'sneaky' prover is an explicit, trained model of coherent-and-wrong ("incorrect solutions that fool the verifier"); (b) the prover/verifier capability gap (small verifier vs. stronger prover) is varied, paralleling our cross-model cast. VERDICT: SUPPORTED. Reinforces the trained-checkability vs. organizational-checkability distinction the paper makes.
