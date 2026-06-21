bibkey: knight1986independence
citation: John C. Knight and Nancy G. Leveson. "An Experimental Evaluation of the Assumption of Independence in Multiversion Programming." IEEE Transactions on Software Engineering, SE-12(1):96-109, January 1986.   access-date: 2026-06-12
read: FULL (original article PDF, author copy http://sunnyday.mit.edu/papers/nver-tse.pdf, full text incl. results, statistical model section 5, and conclusions section 8; corroborated against the IEEE Xplore record and a KTH seminar summary of the same paper)

CLAIM CARDS

- [verbatim] "A total of twenty seven versions of a program were prepared independently from the same specification at two universities and then subjected to one million tests." (Abstract / §3 The Experiment). Anchor: abstract; also §3. Paraphrase: 27 independently written versions, two universities (versions 1-9 from UVA, 10-27 from UCI), 1,000,000 randomly generated test cases.

- [verbatim] "There were twenty seven versions (i.e. N = 27), one million tests were executed (i.e. n = 1,000,000), and the number of tests in which more than one version failed was 1255 (i.e. K = 1255). With these parameters, the statistic z has the value 100.51. This is greater than 2.33 which is the 99% point in the the standard normal distribution, and so we reject the null hypothesis with a confidence level of 99%." (§5 Model of Independence). Paraphrase: the binomial/normal model that assumes independent failures predicts far fewer coincident failures than the 1255 observed; the test statistic z=100.51 vastly exceeds the 2.33 critical value, so the independence null hypothesis is rejected at the 99% level.

- [verbatim] "However, clearly the only potential problem with the model is that it is derived from the assumption of independent failures. Thus, we reject this assumption." (§5). Paraphrase: rejecting the model is equivalent to rejecting the assumption that versions fail independently.

- [verbatim] "For the particular problem that was programmed for this experiment, we conclude that the assumption of independence of errors that is fundamental to the analysis of N-version programming does [not hold]." (§8 Conclusions). Paraphrase: the foundational independence assumption of N-version programming did not hold for this application.

- [verbatim] "Of the twenty seven, no failures were recorded by six versions and the remainder were successful on more than 99% of the tests. Twenty three of the twenty seven were successful on more than 99.9% of the tests." (§4 Experimental Results). Paraphrase: the individual versions were individually very reliable — yet they still failed together far more than independence predicts. This is the crux: high individual reliability + correlated joint failure.

- [verbatim] "We find it surprising that test cases occurred in which eight of the twenty seven versions failed." (§4). Paraphrase: the most extreme coincident-failure test case saw 8 of 27 versions fail on the same input.

- [verbatim] "we have found that approximately one half of the total software faults found involved two or more programs." (§8). Paraphrase: ~50% of distinct faults were shared across two or more versions — correlation at the fault level, not just the failure level.

- [verbatim, caveat] "A second point is that our result does not mean that N-version programming does not work or should never be used. It means that the reliability of an N-version system may not be as high as theory predicts under the assumption of independence." (§8). Paraphrase: the authors explicitly scope the claim — they reject the independence assumption, not the technique wholesale.

METHOD (three sentences)
27 graduate/senior students at UVA (9) and UCI (18) each independently wrote a Pascal program (DECIDE, a "Launch Interceptor" anti-missile decision procedure) from the same requirements specification, with independent development stressed; each version had to pass an acceptance test before inclusion. All 27 versions plus a high-reliability "gold" oracle program were run on one million randomly generated test cases, with a failure recorded whenever any of the 241 result values differed from the gold program. The observed count of test cases with two-or-more coincident failures (K=1255) was compared against a binomial/normal model that assumes independent failures, yielding z=100.51 and rejection of the independence null hypothesis at 99% confidence.

LIMITATIONS
Single application (one anti-missile decision problem) and a student-programmer population, so generality is explicitly disclaimed by the authors ("for the particular problem... we conclude"). Programmer skill varied widely; the result bounds the independence assumption but does not by itself quantify achievable N-version reliability with engineered diversity. The conclusion is about the *statistical independence assumption*, not a claim that diversity is useless (authors note hardware uses engineered, not random, diversity).

CONTRIBUTION (why cited here; which manuscript claim it supports; verdict)
This is the load-bearing source for the manuscript claim that "the Knight-Leveson experiment showed that independence cannot be assumed — independently written versions fail on correlated inputs." The paper supplies exactly that: independently written versions, individually very reliable, failed together (1255 coincident-failure test cases; up to 8/27 at once; ~half of faults shared) at rates that statistically refute (z=100.51 vs 2.33, 99% confidence) the independence assumption underpinning N-version programming. Verdict: SUPPORTED. One precision note for the manuscript: the rejected object is the *assumption of independence of errors*, scoped to the studied application — phrasing like "independence cannot be assumed" is faithful; avoid implying the authors concluded N-version programming "does not work," which they explicitly disclaim.
