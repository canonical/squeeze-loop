bibkey: kambhampati2024position
citation: Subbarao Kambhampati, Karthik Valmeekam, Lin Guan, Mudit Verma, Kaya Stechly, Siddhant Bhambri, Lucas Saldyt, Anil Murthy. "LLMs Can't Plan, But Can Help Planning in LLM-Modulo Frameworks." arXiv:2402.01817 (2024); ICML 2024 (Position paper).
arxiv: 2402.01817   read: FULL (via ar5iv)   access-date: 2026-06-12

CLAIM CARDS

1. The framework is a generate-test-critique loop pairing LLM generation with external critics.
   Quote: "The underlying architecture is a Generate-Test-Critique loop, with the LLM generating candidate plans and a bank of critics critiquing the candidate." (LLM-Modulo framework section)
   Paraphrase: An LLM proposes candidate plans/solutions while a bank of external critics (verifiers) evaluates and critiques them in a loop.

2. Soundness comes from the external verifiers, not the LLM.
   Quote: "The soundness of the LLM-modulo framework is inherited from the soundness of the critics." (LLM-Modulo framework section)
   Paraphrase: Any correctness guarantee rests entirely on the external sound verifiers/critics; the LLM is only a candidate generator.

3. The LLM is a candidate generator / approximate knowledge source.
   Quote: LLMs generate "plausible (but not guaranteed to be correct) plan heuristics" that gain value only when externally validated. (Thesis / framework rationale)
   Paraphrase: The LLM's outputs are treated as guesses to be checked, never trusted on their own.

METHOD / THESIS (three sentences)
The paper argues LLMs cannot autonomously plan or self-verify, but are useful as approximate candidate generators. It proposes the LLM-Modulo framework: a Generate-Test-Critique loop in which an LLM proposes candidate plans and a bank of external model-based critics (hard-constraint correctness verifiers plus soft-constraint critics) accept, reject, or critique them. Soundness is inherited from the critics, letting the framework extend model-based reasoning to flexible specifications without sacrificing formal correctness.

LIMITATIONS (authors' own)
LLMs have no autonomous planning capability — they only produce "plausible (but not guaranteed to be correct)" candidates. The authors deliberately exclude humans from the iterative loop to avoid the "Clever Hans effect" and because tight human-in-the-loop prompting is infeasible at scale. The framework depends on external infrastructure (domain models such as PDDL, or simulators) that must be acquired or constructed separately.

CONTRIBUTION (why cited here; which manuscript claim it supports; verdict)
Cited for: "LLM-Modulo frameworks argue for pairing LLM generation with external sound verifiers." The body confirms the generate-test-critique architecture and explicitly states soundness is "inherited from the soundness of the critics," i.e., external sound verifiers. Verdict: SUPPORTED.
