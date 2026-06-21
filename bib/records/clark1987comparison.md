bibkey: clark1987comparison
citation: David D. Clark and David R. Wilson, "A Comparison of Commercial and Military Computer Security Policies," Proceedings of the 1987 IEEE Symposium on Security and Privacy, Oakland, CA, April 27-29, 1987, pp. 184-194. DOI: 10.1109/SP.1987.10001.   access-date: 2026-06-12

read: FULL
  Source: full PDF obtained and converted to text. Downloaded from
  https://theory.stanford.edu/~ninghui/courses/Fall03/papers/clark_wilson.pdf
  (11-page scan/PDF, course mirror of the IEEE S&P 1987 paper).
  curl -sL -A "Mozilla/5.0" "<url>" -o /tmp/cw.pdf ; pdftotext /tmp/cw.pdf /tmp/cw.txt
  NOTE on fidelity: the PDF is a two-column scan; pdftotext output is heavily
  reflowed (words interleaved/reordered across columns). I reconstructed the
  verbatim sentences below by reading the jumbled token stream in context. The
  reconstructions are faithful to wording but column-bleed means I treat them as
  [verbatim, reconstructed-from-OCR] rather than character-perfect transcription.

CLAIM CARDS

[verbatim, reconstructed-from-OCR] "Perhaps the most basic separation of duty
  rule is that any person permitted to create or certify a well-formed transaction
  may not be permitted to execute it (at least against production data)."
  Anchor: body text on p.~187 (extracted /tmp/cw.txt lines ~2660-2690).
  Paraphrase: The certifier/creator of a transaction must not be the same person who
  executes it -> the certifier != implementer/user principle, stated explicitly as
  the most basic separation-of-duty rule. This is the direct support for the
  manuscript claim.

[verbatim, reconstructed-from-OCR] Enforcement rule E4: "Only the agent permitted to
  certify entities may change the list of such entities associated with other
  entities, specifically [the list] associated with a TP. An agent that can certify
  an entity may not have any execute rights with respect to that entity."
  Anchor: enforcement rule E4, p.~190 (extracted /tmp/cw.txt lines ~5262-5340; also
  appears in the consolidated "Rules" box, p.~192).
  Paraphrase: The model's formal enforcement rule that operationalizes separation of
  duty: certification authority and execution rights over the same entity (TP) are
  mutually exclusive. Codifies certifier != implementer as a system-enforced rule.

[verbatim, reconstructed-from-OCR] "commercial policy is likely to be based on
  separation of responsibility among two or more users."
  Anchor: discussion of rule E1 / certification rules, p.~189 (lines ~4520-4560).
  Paraphrase: Separation of duty among multiple users is the foundation of the
  commercial integrity policy, distinguishing it from the disclosure-focused military
  (lattice/Bell-LaPadula) model.

[verbatim, reconstructed-from-OCR] "Separation of duty is a fundamental ... integrity
  principle ... [for] control." and "Separation of duty can be made very powerful by
  thoughtful application of the technique, such as the random selection of the sets of
  people to perform some operation, so that collusion is ... safe ... by chance."
  Anchor: p.~187 (lines ~2720-2810). (Token order partially garbled by OCR; sense
  preserved.)
  Paraphrase: Separation of duty is positioned as a core/fundamental mechanism of the
  commercial integrity model, strengthened by randomized assignment to defeat collusion.

[secondary] Metadata corroboration: authors David D. Clark and D. R. Wilson; title
  "A Comparison of Commercial and Military Computer Security Policies"; IEEE
  Symposium on Security and Privacy 1987 (Oakland, Apr 27-29); pp. 184-195; DOI
  10.1109/SP.1987.10001. Source: dblp (dblp.org/rec/conf/sp/ClarkW87.html).
  Corroborated in-PDF: title and author line ("Clark", "Wilson") appear on the first
  page of the extracted text; page-number markers "184" (first page) and "194" (last
  content page, end of references) are present in the extracted text, matching the
  pp. 184-194 range cited (dblp gives 184-195, including a possible trailing page).

METHOD
The paper articulates a commercial data-integrity policy drawn from long-standing
business accounting practice (well-formed transactions, double-entry-style internal
consistency, and separation of duty), then formalizes it as a set of certification
rules (C1-C5) and enforcement rules (E1-E4) over constrained data items (CDIs),
transformation procedures (TPs), and integrity verification procedures (IVPs).
It contrasts these mechanisms with the military lattice/Bell-LaPadula disclosure
model and argues a lattice is insufficient to express integrity (in particular the
requirement that data be manipulated only by specified, certified programs).
It is a conceptual/model paper: argument and rule definitions, not an empirical study
or implemented system evaluation.

LIMITATIONS
- Conceptual model, not an implementation; no experimental validation. The authors
  themselves note certification is partly outside the system's enforcement and relies
  on human/administrative trust.
- Access fidelity: the only full text obtained is a two-column scanned PDF whose
  pdftotext output is reflowed/garbled; verbatim quotes above are reconstructed from
  that OCR stream, not from a clean publisher copy. Exact punctuation/word boundaries
  could differ slightly. The substantive claim (certifier != implementer) is
  unambiguous and appears in multiple independent places in the text (the prose rule
  and enforcement rule E4), so it is robust to OCR noise.
- dblp lists pp. 184-195 vs the assignment's 184-194; the PDF's last content/reference
  page is marked 194, so the discrepancy is a one-page boundary detail only.

CONTRIBUTION (why cited here)
Supports the manuscript claim: "separation of duties / commercial integrity model
(certifier != implementer)." The paper is the canonical source of the Clark-Wilson
integrity model and states the certifier-must-differ-from-executor principle both in
prose ("any person permitted to create or certify a well-formed transaction may not be
permitted to execute it") and as a formal enforcement rule (E4: an agent that can
certify an entity may not have execute rights to it). This is a direct, on-point
citation.
VERDICT: SUPPORTED.
