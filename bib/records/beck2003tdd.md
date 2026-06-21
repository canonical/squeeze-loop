bibkey: beck2003tdd
citation: Kent Beck, Test-Driven Development: By Example, Boston: Addison-Wesley (Pearson Education / Addison-Wesley Professional, Addison-Wesley Signature Series), 2003. ISBN 0-321-14653-0 (ISBN-13 978-0-321-14653-3). Copyright (c) 2003 by Pearson Education, Inc. and Kent Beck. Second printing, April 2003. xix + 220 pp.   access-date: 2026-06-12
read: PARTIAL (front matter read verbatim from the publisher's official sample-pages PDF, https://ptgmedia.pearsoncmg.com/images/9780321146533/samplepages/0321146530.pdf, served from ptgmedia.pearsoncmg.com = Pearson Technology Group Media. Extracted locally with pdftotext. The sample contains the complete title/copyright page, full Table of Contents, the complete Preface (pp. ix-xiii), and the Introduction (pp. xvii-xix, the WyCash/Ward Cunningham multi-currency story). The remaining body chapters (the worked Money and xUnit examples and the Part III patterns) were NOT read; for those I relied on SECONDARY sources: the InformIT/Pearson publisher page, Wikipedia "Test-driven development", and Martin Fowler's bliki. So: front matter = PARTIAL verbatim; body = SECONDARY.)

CLAIM CARDS

1. [verbatim] The two governing rules of TDD. Anchor: Preface, p. ix ("In Test-Driven Development, we").
"Write new code only if an automated test has failed" and "Eliminate duplication".
Paraphrase: Beck reduces TDD to exactly two rules: you may only add production code in response to a failing automated test, and you must remove duplication. The tests-first discipline (code is written only because a test demanded it) is stated as the first rule, in Beck's own words.

2. [verbatim] The red-green-refactor cycle. Anchor: Preface, p. x ("The two rules imply an order to the tasks of programming.").
"1. Red—Write a little test that doesn't work, and perhaps doesn't even compile at first. 2. Green—Make the test work quickly, committing whatever sins necessary in the process. 3. Refactor—Eliminate all of the duplication created in merely getting the test to work. Red/green/refactor—the TDD mantra."
Paraphrase: The canonical cycle is verbatim in Beck's Preface: write a failing test (red), make it pass quickly (green), then refactor. Beck himself coins the "red/green/refactor" mantra here.

3. [verbatim] "Done" / predictability. Anchor: Preface, p. ix, bullet list on clean-code-that-works.
"It is a predictable way to develop. You know when you are finished, without having to worry about a long bug trail."
Paraphrase: Beck claims TDD tells you when you are finished. This is the closest the front matter comes to "tests = definition of done": completion is defined by the tests passing. Note Beck phrases this as predictability/knowing-you-are-finished, not in the formal language of "the test is the definition of done".

4. [verbatim] What tests make clear (closest in-book analogue to "specification"). Anchor: Preface, p. x.
"...it further might be possible to dramatically reduce the defect density of code and make the subject of work crystal clear to all involved" and "writing only that code which is demanded by failing tests..."
Paraphrase: Beck argues tests-first makes "the subject of work crystal clear" and that production code is "demanded by failing tests." This conveys the idea that the test defines the desired behavior before the code exists — the substance of "executable specification" — BUT Beck does NOT use the word "specification" anywhere in the Preface or Introduction. The word "specif*" does not appear in the read front matter at all.

5. [verbatim] Tests as a ratchet (irreversible progress). Anchor: Preface, p. xi ("Courage" section).
"The tests in test-driven development are the teeth of the ratchet. Once we get one test working, we know it is working, now and forever."
Paraphrase: A passing test is a permanent, machine-checkable guarantee of behavior — supporting the framing of tests as the persistent, executable record of what the code must do.

6. [verbatim] Bibliographic confirmation. Anchor: copyright page (Library of Congress Cataloging-in-Publication Data).
"Beck, Kent. Test-driven development : by example / Kent Beck. ... ISBN 0-321-14653-0 (alk. paper) ... QA76.76.T48 B43 2003 ... Copyright (c) 2003 by Pearson Education, Inc. and Kent Beck ... Second printing, April 2003."
Paraphrase: Title, author, ISBN 0-321-14653-0, publisher (Pearson Education / Addison-Wesley, Boston), and copyright year 2003 are all confirmed verbatim from the book's own copyright page. (Note: some retailer listings show a Nov 2002 first-availability date; the book's own copyright/CIP and second-printing line state 2003. Cite as 2003.)

7. [secondary] The first test as a beginning specification. Anchor: Wikipedia "Test-driven development".
"that first test functions as the beginning of an executable specification."
Paraphrase: The "executable specification" framing is explicitly the wording of the Wikipedia article (and the broader TDD literature / Fowler's "self-testing code" idea), NOT a quotation from Beck's book. It is a fair gloss on Beck's "code demanded by failing tests" but should be attributed to the secondary literature, not to Beck verbatim.

8. [secondary] Self-testing code / interface-first design. Anchor: Martin Fowler, bliki "TestDrivenDevelopment".
Fowler: TDD is "Write a test for the next bit of functionality... Write the functional code until the test passes... Refactor," "often summarized as Red - Green - Refactor"; writing the test first is "a way to get SelfTestingCode" and "forces us to think about the interface to the code first."
Paraphrase: Fowler, the series co-signer, independently corroborates the red-green-refactor cycle and the tests-first discipline, and frames the test as both verification and a design/interface specification.

9. [secondary] Table of contents (publisher-confirmed). Anchor: InformIT/Pearson page + the book's own Contents page (verbatim from sample PDF).
Part I: The Money Example (chs. 1-17); Part II: The xUnit Example (chs. 18-24); Part III: Patterns for Test-Driven Development (chs. 25-32: TDD Patterns, Red Bar Patterns, Testing Patterns, Green Bar Patterns, xUnit Patterns, Design Patterns, Refactoring, Mastering TDD); Appendix I: Influence Diagrams; Appendix II: Fibonacci; Afterword; Index.
Paraphrase: The structure (two worked examples then a pattern catalogue) is confirmed both by the publisher page and by the Contents page in the official sample.

METHOD (three sentences)
The book is a worked-example tutorial, not an empirical study: Beck teaches TDD by reproducing, step by tiny step, two pair-programming sessions — a multi-currency Money model (Part I) and the construction of an xUnit testing framework (Part II) — each developed strictly by writing a failing test, making it pass, and refactoring. Part III abstracts the demonstrated techniques into a reference catalogue of patterns for deciding what tests to write, how to write them in xUnit, and which design patterns/refactorings recur. Evidence for TDD's benefits is argued by demonstration, analogy (the "ratchet"), and the author's experience, plus the anchoring WyCash field anecdote in the Introduction, rather than by controlled measurement.

LIMITATIONS
This is a methodology/tutorial book by the practice's originator; its claims (reduced defect density, predictability, "fear management") are asserted and illustrated, not statistically demonstrated. Beck himself flags scope limits in the Preface: "There certainly are programming tasks that can't be driven solely by tests... Security software and concurrency, for example, are two topics where TDD is insufficient to mechanically demonstrate that the goals of the software have been met." Access here is PARTIAL: only the front matter (Preface, Introduction, TOC, copyright page) was read verbatim; the worked examples and patterns are known only through secondary summaries, so any fine-grained claim about chapter content carries secondary-source risk.

CONTRIBUTION (why cited here; which manuscript claim it supports; verdict)
Cited to support the manuscript claim that TDD "made specifications executable" — i.e., a test written BEFORE the code defines desired behavior, is run and must fail (red), then code is written to make it pass (green). VERDICT: SUPPORTED, with one wording caveat. The red-green-refactor cycle and the tests-first rule ("Write new code only if an automated test has failed") are confirmed VERBATIM from Beck's own Preface (claim cards 1, 2), and the idea that a failing test specifies/demands the next behavior and defines when you are "finished" is present in Beck's words (cards 3, 4, 5). HOWEVER, the specific phrase "executable specification" is NOT Beck's; it comes from the secondary TDD literature (Wikipedia; the spirit of Fowler's "self-testing code"). So the *practice* the manuscript describes is faithfully Beck's; the *label* "executable specification" is a later gloss. The framing very mildly OVERCLAIMS only if a reader takes "made specifications executable" to be Beck's own slogan or his stated goal — Beck's stated goal is "clean code that works," and his rules are about failing tests and removing duplication, not about a theory of specifications.
Suggested rewrite to stay precise: instead of "Beck's TDD made specifications executable," write — "Beck's TDD treats the failing test written before the code as the executable definition of the next desired behavior: 'Write new code only if an automated test has failed,' run it (red), make it pass (green), then refactor (Beck 2003, Preface). Later commentators describe this first test as 'the beginning of an executable specification' (Wikipedia, TDD; cf. Fowler, self-testing code)." This keeps the verbatim-Beck material separate from the secondary "specification" label.
