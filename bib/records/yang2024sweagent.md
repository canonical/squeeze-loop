bibkey: yang2024sweagent
citation: John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, Ofir Press. "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering." arXiv:2405.15793 (2024); NeurIPS 2024.
arxiv: 2405.15793   read: FULL ATTEMPTED (ar5iv/arxiv HTML conversion failed with "Fatal error"; verified via arXiv abstract page + cross-reference to SWE-bench protocol)   access-date: 2026-06-12

NOTE ON ACCESS: The ar5iv and arxiv.org/html renderings of this paper both returned a fatal HTML-conversion error, so body section text could not be extracted. The claims below are verified against the arXiv abstract (quoted verbatim) plus the structural fact that SWE-bench (jimenez2023swebench) defines a single evaluation protocol that any system evaluated on it necessarily uses.

CLAIM CARDS

1. Evaluated on SWE-bench.
   Quote: "We evaluate SWE-agent on SWE-bench and HumanEvalFix, achieving state-of-the-art performance on both with a pass@1 rate of 12.5% and 87.7%, respectively, far exceeding the previous state-of-the-art achieved with non-interactive LMs." (Abstract)
   Paraphrase: SWE-agent is benchmarked on SWE-bench, scoring 12.5% pass@1 (resolved), beating prior non-interactive baselines.

2. Main contribution is the agent-computer interface (ACI), not test methodology.
   Quote: "SWE-agent's custom agent-computer interface (ACI) significantly enhances an agent's ability to create and edit code files, navigate entire repositories, and execute tests and other programs." (Abstract)
   Paraphrase: The paper's contribution is the ACI design that lets an LM agent operate the repository; it adds nothing to how correctness is judged.

3. Inherits SWE-bench's test-based evaluation (held-out tests).
   Quote: "We evaluate SWE-agent on SWE-bench ... with a pass@1 rate of 12.5%." (Abstract)
   Paraphrase: Reporting a SWE-bench "resolved"/pass@1 number means the agent's patches are scored by SWE-bench's PR-derived FAIL_TO_PASS/PASS_TO_PASS held-out tests; SWE-agent does not redefine that oracle.

METHOD (three sentences)
SWE-agent equips an LM with a purpose-built agent-computer interface (ACI) offering commands to read, search, navigate, create, and edit files and to run tests and programs in a repository sandbox. The agent autonomously interleaves these actions to localize and fix a bug described by a GitHub issue, producing a patch. The system is then evaluated unchanged on SWE-bench's existing benchmark and its held-out, PR-derived test suites.

LIMITATIONS (authors' own)
Body limitations text could not be extracted due to the HTML conversion failure. The abstract notes performance is bounded by interface design and that ACI design choices materially affect agent behavior; absolute resolve rate (12.5% pass@1) remains low, indicating the task is far from solved. (Flag: limitations not verified at body level.)

CONTRIBUTION (why cited here; which manuscript claim it supports; verdict)
Co-cited with jimenez2023swebench for "held-out tests as ground truth." The abstract confirms SWE-agent is evaluated ON SWE-bench and that its own contribution is the ACI, not the test methodology, exactly as the manuscript states. The test protocol is therefore inherited, not introduced, by this paper. Verdict: SUPPORTED (caveat: confirmed from abstract + structural inheritance, not body text, because the HTML rendering was broken; recommend a re-check against the PDF if body-level quotes are required for camera-ready).
