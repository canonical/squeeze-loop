bibkey: baudin_acsl
citation: Patrick Baudin, Pascal Cuoq, Jean-Christophe Filliâtre, Claude Marché, Benjamin Monate, Yannick Moy, and Virgile Prevosto, "ACSL: ANSI/ISO C Specification Language", Version 1.23, CEA-List and Inria, 2009–2026 (© CEA-List, Inria), released as part of the Frama-C distribution.   access-date: 2026-06-12
read: FULL (PDF downloaded directly from frama-c.com/download/acsl.pdf, 1.2 MB, PDF v1.7; title page reads "Version 1.23" with copyright "© 2009-2026 CEA-List, Inria")

CLAIM CARDS

- [verbatim] Title page: "ANSI/ISO C Specification Language / Version 1.23 / Patrick Baudin, Pascal Cuoq, Jean-Christophe Filliâtre, Claude Marché, Benjamin Monate, Yannick Moy, Virgile Prevosto ... © 2009-2026 CEA-List, Inria". Paraphrase: confirms exact title, all seven authors in the bib order, version number 1.23, and the year range to fill the empty bib year. Corroborated directly by the PDF (/tmp/acsl.txt lines 1-9).

- [verbatim] Binder grammar / quantification (Sec. 2.2, "Terms"): "\forall binders ; pred" and "\exists binders ; pred"; "The grammar for binders and type expressions is given separately in Figure 2.4." and the figure caption "Figure 2.4: Grammar of binders and type expressions". Paraphrase: the manual defines a dedicated binder grammar covering \forall, \exists and \let bindings. Corroborated by PDF (lines 1895-1896, 1920, 2179).

- [verbatim] Quantification: "Universal quantification is denoted by \forall τ x1,...,xn ; e and existential quantification by \exists τ x1,...,xn ; e." Paraphrase: explicit quantifier (binder) syntax with typed bound variables. Corroborated (lines 1941-1942).

- [verbatim] Local binding: "Local binding \let x = e1 ;e2 introduces the name x for expression e1; x can then be used in [e2]." Paraphrase: \let is a binder introduced in the grammar. Corroborated (lines 1792, 2180).

- [verbatim] \at construct, Sec. 2.4.3 "Built-in construct \at": "Statement annotations usually need another additional construct \at(e,id) referring to the value of the expression e in the state at label id." Paraphrase: \at(e,label) evaluates expression e in the program state at the given label — exactly the \at semantics claimed. Corroborated (lines 3844, 3846-3847).

- [verbatim] \at well-formedness / scoping: "the label id must occur before the occurrence of \at(e,id) in the source"; "\old(e) is in fact syntactic sugar for \at(e,Old)." Paraphrase: \at is the primitive; \old is defined in terms of it. Corroborated (lines 3854, 3891).

- [verbatim] Predefined labels (Sec. 2.4.3, "Default logic labels"): "There are seven predefined logic labels: Pre, Here, Old, Post, LoopEntry, LoopCurrent and Init." Paraphrase: the standard labels used with \at (incl. Pre, Old, Here) are enumerated with their state semantics. Corroborated (line 3890). Usage examples confirm semantics: "\at(x,Pre)", "\at(i,Here)", "\at(i,LoopEntry)" (lines 4018, 4043, 4064).

METHOD: This is the official reference manual for ACSL, the behavioral specification language for C used by the Frama-C platform; it is a normative language-definition document (grammars, figures, and prose semantics) rather than an empirical study. Binders (\forall, \exists, \let) and their grammar are specified in Section 2.2 with Figure 2.4; the \at(e,label) construct and the seven predefined logic labels (Pre/Here/Old/Post/LoopEntry/LoopCurrent/Init) are specified in Section 2.4.3. It is the authoritative primary source authored by the language designers at CEA-List and Inria.

LIMITATIONS: A living document with no single fixed "publication year" — the version (1.23) and copyright range (2009–2026) are the only dating; different Frama-C releases ship different ACSL versions, so a citation must pin the version. It is a language specification, so it states intended semantics without machine-checked proofs.

CONTRIBUTION (why cited here): Supports the manuscript claim referencing "the ACSL binder grammar and \at semantics." The manual verbatim (a) defines the binder grammar — \forall/\exists/\let with typed binders, Figure 2.4 — and (b) defines \at(e,label) as evaluation of e in the state at a program label, with predefined labels Pre, Old, Here (Section 2.4.3). Both halves of the claim are directly confirmed. VERDICT: SUPPORTED. Found version/year to fill the empty bib field: Version 1.23, 2009–2026 (CEA-List, Inria).
