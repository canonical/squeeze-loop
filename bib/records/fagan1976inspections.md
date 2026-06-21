bibkey: fagan1976inspections
citation: M. E. Fagan, "Design and Code Inspections to Reduce Errors in Program Development," IBM Systems Journal, vol. 15, no. 3, pp. 182-211, 1976. DOI: 10.1147/sj.153.0182   access-date: 2026-06-12
read: FULL (complete article body read via republished full-text HTML at linuxonly.nl, http://www.linuxonly.nl/docs/40/129_Design_and_code_inspections_to_reduce_errors_in_program_development.html; abstract, all sections, role definitions, process steps, and references present. Bibliographic metadata cross-checked against the ACM/IBM Systems Journal DOI record 10.1147/sj.153.0182, which was paywalled (HTTP 403) so confirmed via search-result metadata. Title capitalization taken from the canonical IBM Systems Journal listing; the linuxonly reprint renders it in sentence case.)

CLAIM CARDS

1. [verbatim] Defined roles for inspection participants. Anchor: "the people involved" section.
"The inspection team is best served when its members play their particular roles, assuming the particular vantage point of those roles." Roles enumerated: "Moderator", "Designer", "Coder/Implementor", "Tester".
Paraphrase: Fagan formalizes inspection as a multi-role activity (moderator, designer, coder/implementor, tester), each member adopting a defined vantage point — i.e., inspection is a structured team process, not solo self-review.

2. [verbatim] Moderator should be independent of the work; author separated from moderator role. Anchor: Moderator role definition.
"Moderator - The key person in a successful inspection. He must be a competent programmer but need not be a technical expert on the program being inspected. To preserve objectivity and to increase the integrity of the inspection, it is usually advantageous to use a moderator from an unrelated project."
Paraphrase: The person running the inspection is deliberately someone other than the author, drawn from an unrelated project, precisely to preserve objectivity — author-inspector separation is built into the role design.

3. [verbatim] Explicit rule preventing the author from filling every role (the strongest direct evidence of institutionalized author-inspector separation). Anchor: paragraph immediately after the role list.
"If the coder of a piece of code also designed it, he will function in the designer role for the inspection process; a coder from some related or similar program will perform the role of the coder. If the same person designs, codes, and tests the product code, the coder role should be filled as described above, and another coder - preferably with testing experience - should fill the role of tester."
Paraphrase: Fagan explicitly prescribes bringing in OTHER programmers when one person authored the design/code/test, so that inspection roles are not all occupied by the author. This is the institutionalization of author-inspector separation.

4. [verbatim] Reader is a peer, not the author/designer. Anchor: I-2 Inspection process step.
"A 'reader' chosen by the moderator (usually the coder) describes how he will implement the design. He is expected to paraphrase the design as expressed by the designer."
Paraphrase: The design is read/paraphrased back by someone other than its designer (the reader, usually the coder), so understanding and defects are surfaced by a second party.

5. [verbatim] Bibliographic + scope confirmation. Anchor: abstract.
"Substantial net improvements in programming quality and productivity have been obtained through the use of formal inspections of design and code... with well-defined roles for inspection participants... a mechanism for initial error reduction followed by ever-improving error rates can be achieved."
Paraphrase: The abstract itself foregrounds "well-defined roles for inspection participants," corroborating the role-separation thesis.

6. [secondary] Title and metadata. The canonical IBM Systems Journal title is "Design and Code Inspections to Reduce Errors in Program Development" (confirmed phrase "...in Program Development"); vol 15, no 3, pp 182-211, 1976; DOI 10.1147/sj.153.0182 (the ".153" segment encodes vol 15 / issue 3 / first page 182). Confirmed via search-result metadata and the DOI string; the ACM page itself returned HTTP 403.

METHOD (three sentences)
Fagan reports an industrial-experience study at IBM in which the programming process is partitioned into operations with explicit exit criteria, and formal inspections (I-1 design, I-2 code) are inserted as measurement/verification points. Each inspection is run by a four-person team in fixed roles (moderator from an unrelated project, designer, coder/implementor, tester) executing a defined sequence: overview, preparation, inspection, rework, follow-up. Defect data is categorized by type and severity and fed back for process control; results are compared against control samples (with explicit attention to the Hawthorne Effect) to estimate quality and productivity gains.

LIMITATIONS
Evidence is industrial case-experience from IBM systems/applications projects, not a controlled experiment; quantitative gains rest on the author's own project data and conservative self-reported figures. The author acknowledges potential bias (e.g., that inspection data could be misused against programmers) and defends it anecdotally. Generalizability beyond 1970s mainframe/structured-programming contexts and the specific organizational setting is not established.

CONTRIBUTION (why cited here; which manuscript claim it supports; verdict)
Cited to support the manuscript claim "Fagan inspections institutionalized author-inspector separation." The source directly and verbatim supports this: the moderator is deliberately drawn from an unrelated project "to preserve objectivity," and Fagan gives an explicit rule that when the author has designed/coded/tested the work, OTHER programmers must be brought in to fill the coder and tester roles so the author does not occupy all inspection roles. The claim is SUPPORTED at FULL read level. (One nuance worth preserving in the manuscript: the author/designer IS a participant in the inspection — answering questions and, if they also coded, serving in the designer role — so the institutionalized separation is that the author is NOT the moderator/sole inspector and roles are distributed across peers, rather than the author being excluded entirely.)
