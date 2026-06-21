bibkey: meyer1992contract
citation: Bertrand Meyer, "Applying 'Design by Contract'", IEEE Computer, vol. 25, no. 10, pp. 40-51, October 1992. DOI: 10.1109/2.161279.   access-date: 2026-06-12
read: FULL (full-text PDF from Meyer's ETH group page: https://se.ethz.ch/~meyer/publications/computer/contract.pdf; 6-page reformatted reprint of the full article; running footer "October 1992" with page numbers 41/49/51 visible, body opens at "40". Downloaded to /tmp/meyer.pdf, extracted to /tmp/meyer.txt via pdftotext -layout.)

CLAIM CARDS

[verbatim] (a) Contracts ARE assertions in the code (pre/post/invariant).
Quote: "The mechanism ... preconditions and postconditions ... class invariants, constrain all the rou[tines] ... are called assertions." (Anchor: "Assertions: Contracting for ..." section, /tmp/meyer.txt L135-152.) Also verbatim: routine syntax uses "require" (precondition) and "ensure" (postcondition) clauses (Figure 1/2, L114, L127, L131, L384), and "The optional class invariant clause appears at the end of a class text" with an "invariant" keyword (L337-344). Paraphrase: In Eiffel, a contract is literally expressed as Boolean assertion clauses written in the source — require/ensure on routines and an invariant clause on the class.

[verbatim] (b) Assertions are MONITORED / CHECKED AT RUNTIME, and a violation raises an exception.
Quote: "assertions are monitored at runtime, depending on programmer wishes." (Anchor: "The role of assertions" section, L185-186.)
Quote: "For each class, you may choose from various levels of assertion monitoring: no assertion checking, preconditions only (the default), preconditions and postconditions, all of the above plus class invariants, or all assertions." (Anchor: "Monitoring assertions" section, L406-411.)
Quote: "The subsequent options cause evaluation of assertions at various stages: routine entry for preconditions, routine exit for postconditions, and both steps for invariants." (Anchor: L416-419.)
Quote: "Under the monitoring options, the effect of an assertion violation is to raise an exception." (Anchor: L423-426.)
Quote: "any runtime violation of an assertion is not a special case but always the manifestation of a software bug. ... A precondition violation indicates a bug in the client (caller). ... A postcondition violation is a bug in the supplier (routine)." (Anchor: "Observations on software contracts", L264-277.)
Paraphrase: The Eiffel environment can evaluate the assertion clauses during execution at well-defined points (routine entry/exit, plus invariant checks), with selectable monitoring levels; a failed assertion raises an exception. This is exactly the "executable specification / checkable at runtime" property.

[verbatim] Nuance — Meyer frames runtime checking as ONE use (debugging/monitoring), not the primary purpose; contracts are primarily specification + correctness.
Quote: "this is not a crucial question at this point. The prime goal of this discussion is to find ways of writing reliable software systems that work." (Anchor: L186-189, immediately after introducing runtime monitoring.)
Quote: "The main application of runtime assertion monitoring, then, is debugging. Turning assertion checking on ..." (Anchor: "Why monitor?" section, L432-435.)
Quote: "software elements should be considered as implementations meant to satisfy well-understood specifications, not as arbitrary executable texts." (Anchor: "The notion of contract" intro.)
Paraphrase: Meyer positions contracts first as specification/correctness/documentation devices (the "short" command extracts pre/postconditions as interface documentation, L416-431), and treats runtime monitoring as an optional, primarily debugging-oriented capability with selectable levels. So the faithful reading of "executable specifications" is: the specifications are written in code form and CAN BE checked at runtime — not that they are always executed or that execution is their main role.

[verbatim] Lineage: invariants derive from Hoare.
Quote: "The notion of class invariant comes directly from Hoare's data invariants." (Anchor: sidebar "Further sources", L212-218.) Paraphrase: pre/postconditions and invariants are grounded in axiomatic-semantics / Hoare-logic assertions.

METHOD (three sentences)
This is a methodological/position article, not an empirical study: Meyer presents Design by Contract as a set of principles for object-oriented reliability, drawing all examples from the Eiffel language and its libraries. He develops the human-contract analogy (obligations/benefits between client and supplier), then maps it onto Eiffel's require/ensure/invariant assertion constructs and shows how violations classify bugs. He further connects the theory to exception handling, inheritance (subcontracting), and documentation tooling, arguing by construction and example rather than by experiment.

LIMITATIONS
Single-language, single-vendor exposition (Eiffel / Interactive Software Engineering, Meyer's own product); no empirical evaluation, no comparison data, no measured defect/reliability outcomes. Eiffel assertions are restricted to Boolean expressions and cannot express full first-order properties (Meyer notes quantified properties "are not available" and that adding them "does not seem crucial" for industrial use, L355-382). Runtime monitoring is selectable and often partial (preconditions-only default), so contracts are not in general fully enforced at runtime. Title/abstract page on IEEE/ACM (dl.acm.org doi 10.1109/2.161279) returned HTTP 403 and Semantic Scholar fetch returned empty, so publisher-page metadata was not directly read; metadata below is confirmed from the article PDF's own running footers plus consistent secondary indexes.

CONTRIBUTION (why cited here; which manuscript claim it supports; verdict)
Cited to support the manuscript claim that Design by Contract "made specifications executable." The article directly and verbatim supports the faithful reading of that claim: contracts are written as in-code assertions (pre/post/invariant) and can be evaluated/monitored at runtime with a violation raising an exception. The one honest caveat is altitude: Meyer himself foregrounds specification/correctness/documentation and labels runtime monitoring as an optional, debugging-oriented feature ("the main application of runtime assertion monitoring ... is debugging"). VERDICT: SUPPORTED, provided the claim is phrased as "executable (runtime-checkable) specifications" rather than implying that execution/runtime-checking is the primary or always-on purpose.

METADATA CONFIRMED
Title (exact, with quotes): Applying "Design by Contract" — note Meyer encloses the phrase Design by Contract in quotation marks; the article title is NOT in quotes itself. Author: Bertrand Meyer (Interactive Software Engineering, per byline in PDF). Venue: IEEE Computer, vol. 25, no. 10, pp. 40-51, October 1992. DOI 10.1109/2.161279. The PDF body begins at page 40 and running footers read "October 1992" with page numbers up to 51, corroborating the 40-51 range and the month/year directly from the primary document.
