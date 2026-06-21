bibkey: filliatre2013why3
citation: Jean-Christophe Filliâtre and Andrei Paskevich, "Why3 — Where Programs Meet Provers", in Programming Languages and Systems (ESOP 2013, 22nd European Symposium on Programming), eds. Matthias Felleisen and Philippa Gardner, Lecture Notes in Computer Science vol. 7792, Springer, pp. 125–128, 2013.   access-date: 2026-06-12
read: FULL (4-page tool/demo paper; full text obtained as PDF from author Paskevich's site tertium.org/papers/esop-13.pdf, identical content to the HAL hal-00789533 deposit which was blocked behind an Anubis anti-bot challenge; metadata cross-checked against the Toccata team BibTeX and Springer/DBLP)

CLAIM CARDS

- [verbatim] "We present Why3, a tool for deductive program verification, and WhyML, its programming and specification language." (Abstract, p.125). Paraphrase: Why3 is a deductive-verification tool; WhyML is its programming + specification language. Corroborated directly by the downloaded PDF (/tmp/why3.txt line 7-8).

- [verbatim] "Why3 is a platform for deductive program verification. It provides a rich language of specification and programming, called WhyML, and relies on external theorem provers, both automated and interactive, to discharge verification conditions." (Introduction, p.125). Paraphrase: Why3 generates verification conditions and dispatches them to back-end provers (both SMT/automated and interactive) which discharge them. Corroborated by PDF (lines 21-24).

- [verbatim] "Verification conditions are discharged by Why3 with the help of various existing automated and interactive theorem provers." (Abstract). Paraphrase: the obligations are sent out to existing provers rather than proved internally. Corroborated by PDF (line 12).

- [verbatim] "... readily suitable (via Why3) for multiple automated and interactive provers, such as Alt-Ergo, CVC3, Z3, E, SPASS, Vampire, Coq, or PVS. When a proof obligation is dispatched to a prover that does not [support some feature, Why3 applies a transformation]." (Sec. 2, p.126). Paraphrase: explicit list of SMT solvers and interactive provers (Coq, PVS) to which proof obligations are dispatched. Corroborated by PDF (lines 33-35).

- [verbatim] "Verification conditions are generated using a standard weakest-precondition procedure." (Sec. on programs, p.127). Paraphrase: VC/proof-obligation generation uses a standard WP calculus. Corroborated by PDF (line 60).

- [verbatim] "... it produces a proof obligation every time an rarray [access requires it] ..." and "to generate first-order proof obligations, WhyML is also limited to the first order". Paraphrase: the unit of work is a (first-order) proof obligation. Corroborated by PDF (lines 48, 71).

- [secondary, supporting binary-outcome reading] The paper repeatedly frames the workflow as obligations that are either discharged by a prover or not (a prover either proves the obligation or fails/times out). The manuscript's phrasing "a proof obligation either discharges or it does not" is an accurate characterization of this dispatch-and-discharge model, though that exact sentence is the manuscript's own gloss, not a verbatim quote from the paper.

METHOD: This is a 4-page tool/system-demonstration paper that presents the Why3 platform and its WhyML language, describing the logic (first-order with rank-1 polymorphism, algebraic/inductive types), the programming features (mutable records, type invariants, ghost code, static alias control), and the verification pipeline (weakest-precondition VC generation plus translation/dispatch to many external provers). It demonstrates the approach on small but non-trivial verification examples and the OCaml extraction mechanism. It is an authoritative primary source by the tool's authors.

LIMITATIONS: Short demo paper (pp.125-128), so it summarizes rather than fully specifies; the specification component is deferred to a companion reference, and WhyML is deliberately first-order and memory-model-free, which the authors note as a design restriction (no higher-order functions, statically known aliases).

CONTRIBUTION (why cited here): Supports the manuscript claim that "Why3 makes the strongest lower bounds available: a proof obligation either discharges or it does not." The paper verbatim establishes Why3 as a deductive-verification platform that generates verification conditions / proof obligations and dispatches them to external theorem provers, where the outcome is binary (proved or not). VERDICT: SUPPORTED.
