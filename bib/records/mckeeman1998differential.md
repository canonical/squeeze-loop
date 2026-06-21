bibkey: mckeeman1998differential
citation: W. M. McKeeman, "Differential Testing for Software," Digital Technical Journal, vol. 10, no. 1, pp. 100-107, 1998.   access-date: 2026-06-12
read: FULL (open-access full-text PDF, 8 pp., Tufts course archive https://www.cs.tufts.edu/comp/150FP/archive/bill-mckeeman/DifferentailTesting.pdf; downloaded and pdftotext'd /tmp/mckeeman.txt; first page footer "100 / Digital Technical Journal / Vol. 10 No. 1 / 1998" and last page footer "Digital Technical Journal / Vol. 10 No. 1 / 1998 / 107" both present, confirming the 100-107 range. Metadata cross-checked against dblp journals/dtj/McKeeman98.)

CLAIM CARDS

1. [verbatim] Definition of differential testing -- requires two or more comparable systems. Anchor: abstract, p. 100.
"Differential testing requires that two or more comparable systems be available to the tester. These systems are presented with an exhaustive series of mechanically generated test cases. If (we might say when) the results differ or one of the systems loops indefinitely or crashes, the tester has a candidate for a bug-exposing test."
Paraphrase: Differential testing runs the same mechanically generated inputs through two-or-more comparable implementations and flags any input on which their results disagree (or one fails) as a candidate bug. This is the core "two independent computations must agree" pattern.

2. [verbatim] The mechanism, restated. Anchor: section "Differential Testing," p. 101-102.
"If a single test is fed to several comparable programs (for example, several C compilers), and one program gives a different result, a bug may have been exposed. For usable software, very few generated tests will result in differences. Because it is feasible to generate millions of tests, even a few differences can result in a substantial stream of detected bugs."
Paraphrase: Disagreement among comparable implementations on the same input is the bug signal; agreement is the (cheap, automatic) oracle, replacing human-designed expected outputs.

3. [verbatim] Independence / duplicating behavior of an existing reference. Anchor: applicability discussion, p. 101.
"The technology should also be important for applications for which there is a high premium on independently duplicating the behavior of some existing [system]."
Paraphrase: Differential testing is especially valuable when an implementation must independently reproduce the behavior of an existing reference -- mapping onto an implementer/exerciser checked against a certified baseline.

METHOD (three sentences)
This is an industrial-experience article describing differential testing of C compilers and run-time systems at DIGITAL/Compaq, including a working prototype. It combines mechanically generated random test cases (a stochastic grammar that produces mostly-valid C programs) with the differential oracle: feed each test to several comparable systems and investigate any output divergence. It also discusses practical issues -- test quality, ignoring uninteresting differences (e.g., rounding), test-case minimization, and cross-platform comparison -- and the social/organizational challenge of adopting an automatic bug finder.

LIMITATIONS
Differential testing presupposes two or more comparable implementations of the same specification; it cannot be applied when only a single implementation exists. It detects divergences, not "correctness": when all comparable systems share the same bug, no difference appears and the bug is missed (a blind spot for common-mode faults). Distinguishing genuine bugs from legitimate, specification-permitted differences (e.g., platform-dependent or rounding behavior) requires human-tuned filtering; the evidence is industrial experience with compilers rather than a controlled study.

CONTRIBUTION (why cited in THIS paper; which claim it supports; verdict)
Cited as the antecedent for the squeeze loop's independent-re-derivation check -- cross-validating independently derived values (implementer vs exerciser vs certified baseline), where agreement serves as the oracle and disagreement flags a defect. The source directly supports this: differential testing is defined as running the same inputs through "two or more comparable systems" and treating any divergence as a candidate bug, and McKeeman explicitly highlights the case of "independently duplicating the behavior of some existing" reference. Verdict: SUPPORTED (FULL read). Recommended over metamorphic testing for the "two independent computations must agree" framing (see return note); metamorphic testing concerns relations among outputs of a single program under related inputs and is a weaker fit here.
