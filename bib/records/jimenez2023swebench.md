bibkey: jimenez2023swebench
citation: Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, Karthik Narasimhan. "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" arXiv:2310.06770 (2023); ICLR 2024.
arxiv: 2310.06770   read: FULL (via ar5iv/arxiv-html)   access-date: 2026-06-12

CLAIM CARDS

1. Tests are PR-derived.
   Quote: "We create candidate tasks by selecting the merged PRs that ... make changes to the test files of the repository, which indicates that the user likely contributed tests." (§2.1, Repository / attribute filtering)
   Paraphrase: The ground-truth tests come from the test-file changes inside the merged pull request that fixed the issue.

2. At least one fail-to-pass test per instance.
   Quote: "For each task instance, there is at least one fail-to-pass test which was used to test the reference solution, and 40% of instances have at least two fail-to-pass tests." (§2.3 / dataset characterization)
   Paraphrase: Every instance has >=1 FAIL_TO_PASS test that the gold patch turns from failing to passing; many have several.

3. Evaluation metric uses both test sets.
   Quote: "we check that all FAIL_TO_PASS and PASS_TO_PASS tests are found and have a pass status in the evaluation test-to-status mapping." (Appendix A.4, Evaluation)
   Paraphrase: A patch is "resolved" only if all FAIL_TO_PASS tests now pass (issue fixed) AND all PASS_TO_PASS tests still pass (no regression).

4. Tests are NOT given to the model (held out).
   Quote: "A model is given an issue text description and a complete codebase. The model is then tasked to make an edit to the codebase to resolve the issue." (§2.2, Task Formulation)
   Paraphrase: Model input is only the issue text + codebase; the tests are applied afterward ("we apply the generated patch ... and then execute the unit and system tests"), so they function as held-out ground truth.

5. Execution-based validation requires a state transition.
   Quote: "we check that there exists at least one t_i where s changes from fail to pass." (Appendix A.3, Execution-Based Validation)
   Paraphrase: During dataset construction the gold patch must demonstrably flip at least one test from fail to pass, validating the test as a discriminator.

METHOD (three sentences)
SWE-bench is built by mining merged GitHub PRs across 12 Python repositories in three stages: repository selection, attribute filtering (merged PRs that resolve an issue and modify test files), and execution-based validation that the gold patch flips >=1 test from fail to pass. Each task gives a model an issue description plus the pre-PR codebase snapshot, and the model must produce a patch. Evaluation applies the patch and runs the PR-derived tests, scoring "resolved" only if all FAIL_TO_PASS tests pass and all PASS_TO_PASS tests still pass.

LIMITATIONS (authors' own)
"SWE-bench task instances are all in Python" (§7) — single-language coverage. Also (§7): "relying solely on this method [execution-based testing] is insufficient to guarantee reliable performance ... automated code generations from LMs can frequently be less comprehensive, efficient, or readable compared to human-written solutions" — passing tests does not equal quality.

CONTRIBUTION (why cited here; which manuscript claim it supports; verdict)
Cited to support: "SWE-bench ... use held-out tests as ground truth." The body confirms (a) the tests are PR-derived (§2.1, A.2), (b) they are NOT provided to the model (§2.2), and (c) they are the sole correctness oracle via FAIL_TO_PASS/PASS_TO_PASS (A.4). Verdict: SUPPORTED.
