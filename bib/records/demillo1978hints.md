bibkey: demillo1978hints
citation: R. A. DeMillo, R. J. Lipton, and F. G. Sayward, "Hints on Test Data Selection: Help for the Practicing Programmer," Computer, vol. 11, no. 4, pp. 34-41, April 1978. DOI: 10.1109/C-M.1978.218136   access-date: 2026-06-12
read: FULL (open-access full-text PDF, 8 pp., PUCRS course mirror https://www.inf.pucrs.br/~zorzo/cs/demillo-mutants.pdf; downloaded /tmp/demillo.pdf, pdftotext /tmp/demillo.txt; cover reads "0018-9162/78/0400-0034$00.75 (c) 1978 IEEE", running heads "April 1978 / 35" present, masthead "COMPUTER". Bibliographic metadata (vol 11, no 4, pp 34-41, DOI 10.1109/C-M.1978.218136) cross-checked against the ACM/IEEE DOI record, dblp, and a Northwestern course summary. NOTE: source PDF is two-column and pdftotext interleaves adjacent columns, so several quotes below are reconstructed across interleaved lines; each was checked to read unambiguously.)

CLAIM CARDS

1. [verbatim] Mutation testing originates here as a test-data-adequacy method. Anchor: opening / "program mutation" passage, p. 34-35.
"This method, known as program mutation, is used interactively: A programmer enters from a terminal a program, P, and a proposed test data set whose adequacy is to be determined. ... The mutation system then creates a number of mutations of P that differ from P only in the occurrence of simple errors (for instance, where P contains the expression 'B.LE.C' a mutation will contain 'B.EQ.C'). Let us call these mutations P1, P2, ..., Pk."
Paraphrase: The paper introduces "program mutation": seed many small (single simple-error) variants of the program under test, then judge a test set by whether it exposes them. This is the origin of mutation testing.

2. [verbatim] The kill/live (dead/live mutant) criterion. Anchor: "dead"/"live" mutant passage, p. 35.
"In case (1) Pi is said to be dead: the 'error' that produced Pi from P was indeed distinguished by the test data. In case (2), the mutant Pi is said to be live; a mutant may be live for two reasons: (1) the test data does not contain enough sensitivity to distinguish the error ... or (2) Pi and P are actually equivalent programs and no test data will distinguish them."
Paraphrase: A mutant is "dead" (killed) when the test data distinguishes it from the original; it is "live" if the suite is too weak to distinguish it, or if the mutant is equivalent. Adequacy = no live (non-equivalent) mutants remain. This is the canonical kill definition (the word "kill" is also used directly in the worked examples, e.g. "Let us try to kill as many of these mutants as ...", "The 'best' A vector kills 703 mutants").

3. [verbatim] The competent programmer hypothesis. Anchor: section "The coupling effect," p. 34.
"Programmers, however, have one great advantage that is almost never really exploited: they create programs that are close to being correct! Programmers do not create programs at random; competent programmers, in their many iterations through the design process, are constantly whittling away the distance between what their programs look like now and what they are intended to look like."
Paraphrase: Competent programmers produce programs that are already close to correct, so real faults are small deviations from the intended program -- the justification for seeding only small (simple-error) mutants. This is the competent programmer hypothesis, originating here.

4. [verbatim] The coupling effect. Anchor: boxed statement, p. 35.
"The coupling effect: Test data that distinguishes all programs differing from a correct one by only simple errors is so sensitive that it also implicitly distinguishes more complex errors."
Paraphrase: A test set that kills all simple (single-fault) mutants will also detect complex (multi-fault) errors -- complex errors are "coupled" to simple ones. The paper states it is "an empirical principle" with "no hope of 'proving'" it; it later reports evidence (e.g. "adequate simple-error data kills multiple-error mutants" for BUGGYFIND). This is the origin of the coupling effect.

5. [verbatim] The underlying mutation-system logic (correct-or-inadequate). Anchor: p. 35.
"The mutation system first executes the program on the test data; if the program gives incorrect answers then certainly the program is in error. On the other hand, if the program gives correct answers, then it may be that the program is still in error, but the test data is not sensitive enough to distinguish that error: it is not adequate."
Paraphrase: Passing the existing tests is not evidence of correctness; mutation measures whether the test set is sensitive enough to catch the kinds of errors a competent programmer would make.

METHOD (three sentences)
This is a methods/position article (with worked examples) by the originators of mutation testing, drawing on prototype mutation systems built at Yale and Georgia Tech for Fortran. It presents program mutation as an interactive criterion for test-data adequacy: seed many simple-error mutants of P, run the candidate test set, and treat mutants the data fails to distinguish ("live") as a demand for stronger tests. It supports the approach with small worked examples (MAX, FIND/BUGGYFIND) and reports empirical evidence consistent with the coupling effect, while explicitly framing the competent-programmer and coupling-effect claims as empirical conjectures rather than proofs.

LIMITATIONS
The two foundational claims are presented as empirical hypotheses, not proofs: the authors write that there is "no hope of 'proving' the coupling effect; it is an empirical principle." The article addresses only implementation-level errors (it explicitly sets aside specification/requirement error classes), and the equivalent-mutant problem (mutants no test can kill) is acknowledged as a built-in source of residual live mutants. Evidence is from small Fortran programs and early prototype systems; computational feasibility is asserted and deferred to other papers, and the demonstrations are illustrative rather than a controlled study.

CONTRIBUTION (why cited in THIS paper; which claim it supports; verdict)
Cited as the origin of mutation testing / seeded-fault detection -- the historical antecedent of the squeeze loop's "seeded falsifications" (deliberately clause-violating variant queries the test suite must kill). The source directly and verbatim supports every part of the intended use: it introduces program mutation (seeding small faults), the dead/live = killed criterion (a test is adequate when it distinguishes every non-equivalent mutant), the competent programmer hypothesis, and the coupling effect, all of which originate here. Verdict: SUPPORTED (FULL read).
