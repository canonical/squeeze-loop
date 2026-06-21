bibkey: jia2011analysis
citation: Y. Jia and M. Harman, "An Analysis and Survey of the Development of Mutation Testing," IEEE Transactions on Software Engineering, vol. 37, no. 5, pp. 649-678, September 2011. DOI: 10.1109/TSE.2010.62   access-date: 2026-06-12
read: FULL (open-access author copy / accepted manuscript, 31 pp., obtained from Mark Harman's CREST page at http://crest.cs.ucl.ac.uk/fileadmin/crest/sebasepaper/JiaH10.pdf; downloaded /tmp/jia.pdf [HTTP 200, application/pdf, 31 pages], pdftotext /tmp/jia.txt. The PDF header reads "This article has been accepted for publication in a future issue of this journal ... IEEE TRANSACTIONS ON SOFTWARE ENGINEERING / An Analysis and Survey of the Development of Mutation Testing / Yue Jia ... and Mark Harman", i.e. the IEEE-accepted version of the article. The IEEE TSE / dl.acm.org full text is paywalled (HTTP 403 on dl.acm.org/doi/10.1109/TSE.2010.62), but the CREST author copy carries the complete text; definitions below are quoted verbatim from it. Bibliographic metadata -- vol 37, no 5, pp 649-678, 2011, DOI 10.1109/TSE.2010.62 -- cross-checked across IEEE/ACM listing, dblp, and SciRP. UPGRADE 2026-06-12: previously SECONDARY (docslib reproduction); now FULL after retrieving the CREST author PDF.)

CLAIM CARDS

1. [verbatim] Definition of mutants / mutation operators. Anchor: Sec. I (Introduction), p. 1 (CREST author copy).
"Such faults are deliberately seeded into the original program, by simple syntactic changes, to create a set of faulty programs called mutants, each containing a different syntactic change."
Paraphrase: Mutation testing builds many faulty versions of the program by applying mutation operators that make single small syntactic changes -- i.e., seeds faults. Matches the seeded-fault framing.

2. [verbatim] How a mutant is killed. Anchor: Sec. II ("Mutation Testing Process"), p. 4 (CREST author copy).
"each mutant p [should read p'] will then be run against this test set T . If the result of running p' is different from the result of running p for any test case in T , then the mutant p' is said to be 'killed', otherwise it is said to have 'survived'."
The Introduction (p. 1) gives the same criterion: "If the result of running a mutant is different from the result of running the original program for any test cases in the input test set, the seeded fault denoted by the mutant is detected."
Paraphrase: A mutant is killed when some test case distinguishes its output from the original program's output (otherwise it survives) -- the canonical kill criterion. Directly supports "a mutant is killed if a test distinguishes it from the original."

3. [verbatim] Mutation score = test-suite adequacy. Anchor: Sec. II, p. 4 (CREST author copy).
"Mutation Testing concludes with an adequacy score, known as the Mutation Score, which indicates the quality of the input test set. The mutation score (MS) is the ratio of the number of killed mutants over the total number of non-equivalent mutants. The goal of mutation analysis is to raise the mutation score to 1, indicating the test set T is sufficient to detect all the faults denoted by the mutants."
(The Introduction states the looser form: "The mutation score is the ratio of the number of detected faults over the total number of the seeded faults.")
Paraphrase: Mutation testing measures test-suite adequacy by the mutation score -- killed mutants over total non-equivalent mutants -- with score 1 meaning the suite detects every (non-equivalent) seeded fault. Confirms the survey frames mutation testing as a test-adequacy criterion. (Equivalent mutants -- "syntactically different but functionally equivalent" and provably undetectable in general because program equivalence is undecidable -- are excluded from the denominator.)

4. [verbatim] The two founding hypotheses, attributed to the founders. Anchor: Sec. I (Introduction) and Sec. II foundations, pp. 1, ~6 (CREST author copy).
Competent Programmer Hypothesis: "The general principle underlying Mutation Testing work is that the faults used by Mutation Testing represent the mistakes that programmers often make." Coupling Effect (quoting DeMillo et al. 1978): "Test data that distinguishes all programs differing from a correct one by only simple errors is so sensitive that it also implicitly distinguishes more complex errors."
Paraphrase: The survey restates and names the competent programmer hypothesis and the coupling effect, attributing both to DeMillo et al. (1978) and noting Offutt later refined the coupling effect into the Coupling Effect Hypothesis / Mutation Coupling Effect Hypothesis.

5. [verbatim] Historical attribution / canonical-survey status. Anchor: Sec. I (Introduction), p. 1 (CREST author copy).
"The history of Mutation Testing can be traced back to 1971 in a student paper by Richard Lipton. The birth of the field can also be identified in papers published in the late 1970s by DeMillo et al. and Hamlet."
Paraphrase: Jia & Harman explicitly credit DeMillo et al. (1978) and Hamlet (1977) as the founders, situating their work as the comprehensive retrospective survey of the field.

METHOD (three sentences)
This is a comprehensive survey (IEEE TSE) of ~30+ years of mutation-testing research, organizing the literature into definitions, theory (competent programmer hypothesis, coupling effect), cost-reduction techniques (selective mutation, weak mutation, mutant sampling/clustering, higher-order mutation), and tools/applications. It synthesizes a large bibliography rather than reporting a new experiment, and provides a development-tree/timeline of the field. It standardizes terminology (mutants, mutation operators, killed/live mutants, equivalent mutants, mutation score) that the community now treats as canonical.

LIMITATIONS
As a survey it reports no new empirical result; its claims about technique effectiveness are aggregated from heterogeneous primary studies of varying rigor. The equivalent-mutant problem and the cost of mutation testing are discussed as open issues rather than solved. Currency: it covers work up to ~2010, so post-2010 developments (e.g., large-scale industrial mutation testing, LLM-based mutant generation) are out of scope.

CONTRIBUTION (why cited in THIS paper; which claim it supports; verdict)
Cited as the standard/canonical survey defining mutation testing as test-suite adequacy via mutant detection -- backing the manuscript's framing of seeded falsifications as a calibration of detector (verifier) sensitivity. The source directly supports the intended use: it defines a mutant as a small seeded syntactic fault, defines "killed" as a test distinguishing the mutant's output from the original, and defines the mutation score as the adequacy metric. Verdict: SUPPORTED (FULL read -- definitions quoted verbatim from the CREST open-access author copy of the IEEE-accepted manuscript; the published IEEE/ACM PDF remains paywalled but metadata is independently confirmed).
