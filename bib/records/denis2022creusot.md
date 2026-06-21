bibkey: denis2022creusot
citation: Denis, X., Jourdan, J.-H., & Marché, C. (2022). Creusot: A Foundry for the Deductive Verification of Rust Programs. In Formal Methods and Software Engineering (ICFEM 2022), LNCS 13478, pp. 90–105. Springer. DOI 10.1007/978-3-031-17244-1_6.
read: Abstract + §1 Introduction + §1.1 (ICFEM 2022 author PDF) + tool description   access-date: 2026-06-19

CLAIM CARDS

1. Quote: "We present the foundations of Creusot, a tool for the formal specification and deductive verification of Rust code." (Abstract) -> Paraphrase: Creusot is a deductive verifier for Rust — the executable lower bound the lace application uses.

2. Quote: "Creusot has a specification language, Pearlite, which allows users to write function contracts and loop invariants, where logic formulas can make use of a novel operator ^ (pronounced final) to denote prophecies." (§1) -> Paraphrase: specs are written in Pearlite (contracts/invariants); prophecies (^) reason about mutable borrows in harmony with Rust ownership.

3. Quote: "Creusot uses a prophetic translation in the lineage of RustHorn, but aims to verify real-world programs, pushing the size, scope and features of programs far beyond RustHorn." (§1) -> Paraphrase: translates Rust (from the compiler's MIR) into the Why3 platform's intermediate language and discharges the resulting verification conditions with Why3/automated provers; targets real programs.

4. Quote: "Creusot does not permit the verification of unsafe code but allows the specification of safe abstractions like Vec." (§1.1) -> Paraphrase: scope is safe Rust + specified safe abstractions; logical abstraction of data is via a Model trait used "pervasively in our case studies."

METHOD
A deductive-verification tool, not an empirical study: it formalizes Rust verification by translating annotated Rust (via MIR) to the Why3 platform (Coma/WhyML), generating verification conditions discharged by Why3's automated and interactive provers. Demonstrated on worked examples (e.g. a generic Gnome-sort with sorted/permutation post-conditions) and case studies; auto-active (user supplies contracts/invariants, solvers discharge VCs).

LIMITATIONS / FRAMING (authors' own)
Positioned as a foundations/tool paper "going beyond a proof-of-concept verification tool"; verifies safe Rust only (not unsafe code); soundness rests on the prophetic translation and the Why3 backend. A verification condition either discharges or does not — an undischarged VC marks an obligation the provers could not close (which the squeeze paper repurposes as a bug-finder when a total-robustness spec is imposed).

CONTRIBUTION (why cited here)
Cited in §4 (sec:realworld) as the executable lower bound for the external lace application: "a deductive verifier translating Rust through Why3 to SMT solvers, with specifications in its Pearlite contract language", and as the engine whose unproved VCs surface the four security defects (the defect-FINDING attributed to Creusot, not to the squeeze). The Pearlite / Why3-translation / prophecy / safe-only characterization in the manuscript matches the paper. VERDICT: SUPPORTED.
