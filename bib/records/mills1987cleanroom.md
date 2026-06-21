bibkey: mills1987cleanroom
citation: Harlan D. Mills, Michael Dyer, and Richard C. Linger. "Cleanroom Software Engineering." IEEE Software, 4(5):19-25, September 1987.   access-date: 2026-06-12
read: FULL (original 7-page article PDF, University of Toronto course copy http://www.cs.toronto.edu/~chechik/courses07/csc410/mills.pdf; OCR partly scrambled by two-column layout but all load-bearing passages read in context; corroborated against flylib/SEI Cleanroom summary and Wikipedia citation of the same paper)

CLAIM CARDS

- [verbatim] "This first priority is achieved by using human mathematical verification in place of program debugging to prepare software for system test." (p.19, opening process description). Paraphrase: developers verify code by mathematical reasoning instead of running/debugging it; the prepared-for-system-test artifact is produced without developer execution.

- [verbatim] "developers essentially never resorted to debugging (less than 0.1 percent of the cases) to isolate and repair reported defects." (p.22; also a pull-quote: "In verified software, developers essentially never resorted to debugging."). Paraphrase: in the verified-software portions, developers virtually never executed/debugged to find defects.

- [verbatim] "Another major difference is an insistence on human mathematical verification with no program debugging before representative-user testing at the system level." (p.22). Paraphrase: no developer program debugging is permitted before testing is done at the system level by representative-user (statistical) testing.

- [verbatim] "More than 90 percent of total product defects were found before first execution. This is in marked contrast to the more customary experience of finding 60 percent of product defects before first execution." (p.20). Paraphrase: the bulk of defects are caught by human verification prior to any execution of the code.

- [verbatim] "In the Cleanroom model, structural testing that requires knowledge of the design is replaced by formal verification, but functional testing is retained." (p.22). Paraphrase: testing that needs developer/design knowledge (white-box) is removed; only black-box functional/statistical testing remains, performed for certification.

- [verbatim] "statistical certification of the software's quality through representative-user testing at the system level. The measure of quality is the mean time to failure..." (p.19). Paraphrase: acceptance evidence is statistical-usage certification (MTTF), separate from the verification developers do.

- [verbatim] "Cleanroom software engineering requires a development cycle of concurrent fabrication and certification of product increments..." (p.19). Paraphrase: fabrication (development) and certification are distinct, concurrent activities on each increment.

- [secondary] The crisp organizational formulation — "small, independent development and certification (test) teams" — is quoted from a Cleanroom summary (flylib / SEI tradition), corroborating the two-team separation; see also Wikipedia citing the same 1987 paper. [secondary]

METHOD (three sentences)
This is an experience/position paper reporting IBM's Cleanroom process across three industrial projects (a 40,000-line IBM language product, a 35,000-line Air Force helicopter flight program, a 45,000-line NASA planning system) plus a University of Maryland controlled student experiment. It describes a development life cycle in which structured specifications are decomposed by stepwise refinement, every control structure is verified by human (functional) mathematical verification in group inspection, and code is prepared for system test without developer debugging. Quality is then certified by statistical usage testing at the system level, yielding a measured mean-time-to-failure for the delivered product.

LIMITATIONS
Experience report, not a controlled study (the only controlled comparison is the small Maryland student experiment, 1000-2000 LOC); reported metrics (90% defects before first execution, defect counts halved, 1/5 correction time) are project anecdotes without released raw data. The strong "separate independent certification team" organizational claim is canonical Cleanroom doctrine but is articulated most explicitly in later Cleanroom literature; this 1987 paper states the *principle* (verification replaces debugging; no developer debugging before system-level statistical testing; concurrent fabrication-and-certification) rather than naming a separate test team in those words.

CONTRIBUTION (why cited here; which manuscript claim it supports; verdict)
Cited for: "Cleanroom forbids developers from executing their own code and routes all execution through a separate certification team — the clearest pre-LLM statement of 'the implementer never touches the acceptance evidence.'" The first half is directly and verbatim supported: developers verify rather than execute/debug, "no program debugging before representative-user testing," developers "essentially never resorted to debugging," and structural (developer-knowledge) testing is replaced by verification. The second half — a *separate certification team* owning all execution — is supported in substance (concurrent fabrication-and-certification; statistical certification distinct from development) and by Cleanroom secondary literature, but the explicit two-team wording is not verbatim in this 1987 paper. Verdict: SUPPORTED, with a precision caveat. Suggested tightening: anchor the "execution barrier" half to this 1987 paper's verbatim language ("verification in place of program debugging," "no program debugging before representative-user testing at the system level"), and if the "separate certification team" phrasing must be load-bearing, add a secondary Cleanroom cite (e.g., Cobb & Mills 1990 or Linger 1994) rather than resting that organizational claim solely on the 1987 paper.
