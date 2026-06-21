---
name: write-a-paper
description: A general-purpose academic-paper-writing companion that encodes hard-won lessons (many from reviewer feedback) for writing a clear, honest, and defensible paper. Covers saying each idea once, resolving forward references, connective tissue, avoiding overclaim, citing responsibly, tightening the abstract, keeping front matter in sync with the body, cross-section consistency, bounding speculative material, quantifying honestly, figures, length discipline, and independent editorial review. Use whenever the user says "help me write a paper", "review my paper draft for clarity", "is my abstract overclaiming", "academic writing help", "polish my manuscript", "did I make a forward reference", "say it once", "check my paper for consistency", "read the full paper for consistency", "make sure each term is defined / introduced before use", "run a summary-vs-body faithfulness sweep", "make this qualifier/term consistent everywhere", "is this claim defensible", "how should I cite this", "did I leave stale future-work language", or asks for a pre-submission readiness check. Also consult it to know which standing review sweep to propose next when iterating on a near-done paper.
---

# Write a Paper

Your job is to help a researcher produce a paper that a skeptical, time-pressured
reviewer will find **clear, honest, and defensible** — and to catch, before submission,
the specific defects that reviewers most reliably flag. The principles below are
field-agnostic: apply them to any paper in any discipline.

Use this skill in two modes:

- **Drafting** — apply the principles as you write or restructure sections.
- **Review** — audit an existing draft against the principles and the pre-submission
  checklist, and report findings grouped by severity.

Each principle below carries a short rationale and a concrete do/don't. Treat every
reviewer-caught defect you encounter as a reusable checklist item (Principle 13) so the
same mistake cannot silently return in a later revision.

## The principles

### 1. Say each idea once, crisply

**Rationale.** A reviewer reads under time pressure. Restating the same point three ways —
once in the abstract, again in the intro, again in the body — does not reinforce it; it
makes the paper feel padded and forces the reviewer to re-parse the same claim. Dense,
recursive sentences that fold three thoughts into one clause have the same effect.

- **Do** pick the single canonical home for each idea (usually the body), state it once,
  and *reference* it elsewhere ("as established in §4") rather than restating it.
- **Don't** let the abstract, intro, and body each contain a full, slightly different
  restatement of the same contribution. Don't write a sentence the reader must read twice.

### 2. Define every term, and introduce it before use

**Rationale.** A reader must never meet a load-bearing term they cannot resolve. If a
named construct, method, or component appears before it is defined — or is never defined at
all, or is named two different ways — the reader is stuck. This decays silently: as a paper
is revised over many sessions, new coined terms and acronyms accrete and the discipline that
every one is introduced before use quietly lapses. Re-checking it is a sweep worth running
periodically (Principle 14), not a one-time pass.

- **Do** introduce (define or gloss) every key term at or before its first use. If a use
  must precede the definition, signpost it with an explicit forward reference ("the
  validation step, defined in §3.3").
- **Do** expand every acronym at first use — domain acronyms especially: a reader from an
  adjacent field will not know `UEFI`, `MBR`, `ASC 606`, `SMT`, or `GDPR`. Give every coined
  methodological term ("existence demonstration", "wiring check", "no-blend") an explicit
  one-clause gloss the *first* time, not merely a meaning the reader must infer from context.
  Keep a short glossary of the load-bearing terms.
- **Do** use one name for one concept and one concept per name. Reconcile any dual-labelling
  scheme in a single explicit place — the classic trap is the same letters (A/B/C…) labelling
  both *categories* and *instances*, where the reader must independently realise the two
  schemes differ.
- **Don't** name a construct in passing — the classic defect is referring to a named
  component (say, "the reconciliation pass") in an early remark while it is not defined
  until a much later section. The reader at that point cannot know what it is. Don't leave an
  acronym unexpanded or a coined term inferable from context only.

### 3. Connective tissue — every part orients itself

**Rationale.** A paper is not done when each paragraph is locally correct; it is done when
a reader can see *why each part exists and how it relates to the whole*. The relation is
recursive: a subsection orients itself within its section, a section within the paper.

- **Do** open every section and subsection with an orienting sentence: its role in the
  bigger picture and a brief preview of its parts, *before* diving into a definition or a
  sub-header.
- **Don't** start a section by dropping straight into a definition, a formula, or a table
  with no statement of why the reader is now here.

### 4. Honesty — no overclaim

**Rationale.** Overclaiming is the fastest way to lose a careful reviewer's trust, and one
caught overclaim makes them doubt everything else. Reviewers are especially alert to a
modeled quantity dressed up as a measured one, and to an illustrative number that quietly
implies a rate.

- **Do** report null results as null; scope every empirical claim to its real conditions
  (small-n, single instance, single setting); clearly distinguish a *guarantee* claim
  ("the method always …") from a *frequency* claim ("in our runs the method usually …").
- **Don't** hunt across the task space for a configuration that finally shows an effect and
  then present it as the result. Don't present a structural or modeled figure as if it were
  measured. Don't let an illustrative example number read as an empirical rate.

### 5. Citations

**Rationale.** A fabricated or misattributed citation is a credibility-ending defect, and
citing from memory or from a survey routinely produces both.

- **Do** read a source before citing it; attribute precisely (what *paper Y said about X*
  is not the same as *X itself*); keep one short reading record per source so the claim you
  attach to a citation is the claim the source actually makes.
- **Don't** cite from an abstract, a survey's summary, or memory. Never invent a reference
  or a page number to fill a gap.

### 6. The abstract

**Rationale.** The abstract is read by the most people and trusted the most; it is also
where compression most easily introduces an overclaim or drops a material caveat.

- **Do** keep it tight; make every sentence faithful to the body; surface the strongest
  *real* result early and plainly.
- **Don't** let compression upgrade a hedged body claim into an unhedged abstract claim,
  drop a caveat the body considers material, or bury the strongest result under setup.

### 7. Front matter must track the body

**Rationale.** As the work advances, the abstract, intro, contributions list, and scope
statement drift out of sync with the body. Stale front matter is a *coherent-but-wrong*
inconsistency: each piece reads fine alone, but together they contradict.

- **Do** update the abstract, intro, contributions, and scope whenever the body advances —
  a result becomes available, a study gets run, a limitation is resolved.
- **Don't** leave "deferred / future work" language describing something the body now
  reports as done, or a superlative in one place the body elsewhere contradicts.

### 8. Cross-section consistency

**Rationale.** Two sections can each be individually defensible yet make contradictory
*ranking* claims. The paper's account of its own method must also match what the artifacts
actually do.

- **Do** make any "only / first / strongest / best" claim unique and deliberate; ensure the
  description of the method matches what the code, data, or apparatus actually produce.
- **Don't** call one result "the strongest evidence" in one place while framing several
  results as co-equal elsewhere. Don't describe a procedure the artifacts do not implement.

### 9. Keep philosophical / meta material from overshadowing

**Rationale.** A speculative or meta thread, placed up front and in non-standard vocabulary,
makes a skeptical reviewer doubt the rigor of everything before they reach the real
contribution.

- **Do** bound any speculative thread explicitly, keep the main body's vocabulary in the
  field's standard terminology, and put the speculative apparatus in an appendix so the
  rigorous contribution is met first.
- **Don't** let invented terminology or a grand framing dominate the introduction and crowd
  out the concrete, defensible result.

### 10. Quantify what you honestly can; defer the rest explicitly

**Rationale.** Reviewers will want a number you may not have instrumentation for (cost,
latency, overhead). Giving the part you can derive — and naming the rest as future work —
is far stronger than fabricating a complete table.

- **Do** report the structural or derivable portion of the quantity and state plainly that
  the measured portion is future work.
- **Don't** fabricate a measurements table, or pad it with plausible-looking numbers you
  did not actually obtain.

### 11. Figures

**Rationale.** Figures are scanned, not read. A clean vector figure communicates structure
in a glance; an ASCII diagram or an oversized figure does not.

- **Do** prefer clean vector / flowchart figures, keep them faithful to the content they
  replace, and ensure they fit within the text margins.
- **Don't** ship ASCII-art diagrams as final figures, or let a figure bleed past the
  margins or drift from what the prose says it shows.

### 12. Proportion and length discipline

**Rationale.** A section's size signals its importance; a long section on a minor point and
a cramped one on the main result misleads the reader and wastes the page budget.

- **Do** size each section in proportion to its contribution; trim restatement first when
  over budget; respect the page limit.
- **Don't** hit a page budget by gutting a real result, or let restatement and throat-
  clearing consume space the core contribution needs.

### 13. A independent editorial pass

**Rationale.** The most reliable way to catch what self-review misses is a reviewer who is
*not* the author. A same-author or same-model-family check shares the author's blind spots;
a genuinely different perspective does not.

- **Do** get a independent editorial pass — a different person, or a different model family —
  and convert each defect it finds into a standing checklist item so it cannot silently
  return in a later revision.
- **Don't** rely solely on re-reading your own draft, or treat a fix as final without
  recording the lesson that produced it.

### 14. A near-done paper is reviewed repeatedly, along rotating dimensions

**Rationale.** A paper that is "basically finished" is not reviewed once and shipped; it is
swept again and again, each pass along a *different* dimension, until passes stop finding
things. Two findings recur every time and are worth internalising. First, **drift
concentrates in the summary surfaces** — the abstract, the contributions list, table cells
and captions, and the conclusion. These paraphrase the body, and each edit to the body leaves
them subtly behind; the body itself usually stays clean. Weight every sweep there. Second, a
fix in one pass can introduce a fresh defect the *next* pass catches (a verb tightened to cure
an over-claim becomes a different over-claim) — which is exactly why the sweeps are disjoint
and repeated rather than trusted once.

- **Do** run the standing sweeps below as a rotating menu, each one *disjointly* (a reviewer —
  or model — that is not the author, ideally a different model family, since a same-author or
  same-family check shares the blind spots). After substantive edits, or when several sweeps
  have passed without a fresh dimension being tried, **proactively propose the next sweep** —
  do not wait to be asked. The point of recording them here is that the author should not have
  to remember to request each one.
- **Do** fold every new class of defect a sweep uncovers into this skill (Principle 13) so the
  sweep that found it becomes a standing dimension, not a one-off.
- **Don't** treat "I read it once for consistency" as done, and don't re-run only the
  dimension that last found something — rotate, because the unsearched dimension is where the
  next defect is hiding.

## Standing review sweeps

A rotating menu. Each is run disjointly (Principle 13/14), weighted toward the summary
surfaces, and proposed proactively. This list grows as new defect classes are found.

- **Full-paper consistency read** — one end-to-end pass: every number that appears twice
  agrees (and matches its source/macro); every cross-reference points at content matching the
  citing sentence; terminology is uniform; no claim contradicts another across sections.
- **Term-definition & introduction sweep** (Principle 2) — build an inventory of every coined
  term, acronym, symbol, gate/role name, and label; for each, confirm it is defined somewhere
  and introduced (or forward-signposted) before first use; flag used-before-defined,
  never-defined, late-expanded acronyms, and one-concept-two-names / one-name-two-concepts.
- **Summary-vs-body faithfulness sweep** — decompose each summary surface (abstract,
  contributions, conclusion, every table cell and caption) into atomic claims; match each to
  the precise body passage that substantiates it; judge FAITHFUL / OVERSTATED / UNDERSTATED /
  UNSUPPORTED / CONTRADICTED. This is the highest-yield sweep, because it targets exactly where
  drift concentrates. (A claim the body never makes at all — a table cell invented during
  editing — is the worst case and this sweep is what catches it.)
- **Terminology / qualifier uniformity sweep** — pick a load-bearing qualifier or coined
  phrase (e.g. a scope caveat that must accompany a claim everywhere) and verify it is phrased
  *identically* at every occurrence; a qualifier present in four places and dropped or
  reworded in the fifth reads as a different, broader claim.
- **Numeric & arithmetic sweep** — independently recompute every sum, ratio, and disposition
  the paper states; confirm each figure traces to a single source of truth (a macro / a script
  output) rather than being hand-typed in two places that can diverge.
- **Full recompute / build-harness run** — if the paper is *generated* (numbers from
  macros/scripts, citations backed by reading records, PDF built by a pipeline), periodically run
  the **whole** harness, not just the cheap linters above: regenerate every figure and assert it is
  byte-identical to what is committed, and confirm every citation resolves to a reading record. The
  lightweight sweeps do **not** catch a *stale generated number* (a committed value the generator no
  longer reproduces, e.g. because its source artifact changed) or an *unrecorded citation* — only
  the full recompute does. Run it periodically, **not just at submission**: a long run of edit-cycles
  that exercises only the fast gates lets generated artifacts drift out of sync unnoticed (the cheap
  gates are *not* the full harness). This is also the sweep most likely to catch defects in the
  paper's *own apparatus* rather than its prose.

## Pre-submission checklist

Run these ~10 yes/no checks before submitting. A "no" is a finding to fix.

1. Is each load-bearing idea stated once, in one canonical place, and referenced (not
   restated) elsewhere?
2. Is every load-bearing term defined or glossed at or before its first use (or signposted
   forward), every acronym expanded at first use, every coined term given an explicit gloss,
   and every label scheme one-name-one-concept?
3. Does every section and subsection open with an orienting sentence (why it exists, how it
   relates to the whole)?
4. Is every empirical claim scoped to its real conditions, with guarantee vs frequency
   claims kept distinct and no modeled quantity presented as measured?
5. Was every citation read before citing, attributed precisely, and free of fabrication?
6. Is the abstract tight, faithful to the body, free of any compression-introduced
   overclaim or dropped caveat, and does it surface the strongest real result?
7. Does the front matter (abstract, intro, contributions, scope) match the current state of
   the body, with no stale "future work" or contradicted superlative?
8. Are all "only / first / strongest / best" claims unique and deliberate, and does the
   method description match what the artifacts actually do?
9. Is any speculative / meta material bounded and confined to an appendix, with the main
   body in standard terminology?
10. Are figures clean vector (not ASCII), faithful, and within margins; are sections sized
    in proportion to their contribution; and has the draft had a independent editorial pass?
11. Has each standing review sweep (consistency, term-definition, summary-vs-body faithfulness,
    qualifier uniformity, numeric) been run *disjointly* and recently — not just the one that
    last found something — with every new defect class folded back into this skill?
