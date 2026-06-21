# Disjoint editorial review (standing Gate A) -- record

Checked by `verify/editorial_gate.py`. The gate enforces that a *current* disjoint
editorial judgment is on file for the exact manuscript; it does NOT perform the judgment
(that would be the author grading itself). See paper-impl.md, "Completing the gates."

paper-sha256: 69d064cafc79b94b204d9f2d9e6c02137c0d58f6e866d0a927bb634e09523cdb
judge: claude-sonnet-4-6 (Claude Code sub-agent, independent context)
disjoint-from-author: PARTIAL -- author is claude-opus-4-8; judge is a different model but
  the SAME provider family. R3 (Section 7) shows same-family casts share the author's blind
  spot, so this is partial disjointness. Gold standard: cross-provider model or human review.
verdict: ACCEPT-WITH-FIXES
date: 2026-06-18
scope: cross-section framing consistency and faithfulness to evidence (the interpretive
  residual the machine gates cannot verify). NOT grammar/citations/build/page-count.
cross-provider-check: see claims/cross_provider_review.md. GOLD STANDARD NOW MET on the
  editorial (framing-consistency) axis. A CAPABLE, genuinely cross-provider judge --
  qwen3.6:27b-mlx (Alibaba, independent pretraining from the Anthropic author), run via Ollama
  on a remote host (OLLAMA_HOST=http://localhost:11434 + CROSS_MODEL) -- is AUTHORITATIVE:
  it passes both control probes (known-contradiction and known-consistent) and judges the
  paper's live framing CONSISTENT, reproducibly. So the framing-consistency review is now
  corroborated by a fully provider-disjoint capable judge, not only the operative same-family
  Sonnet pass. (Earlier the only reachable cross-provider model, qwen2.5-coder:1.5b-base, was
  non-authoritative -- too small to pass a control.) The operative verdict above stays the
  full Sonnet Gate C (a complete read-the-paper review, which this narrow probe is not), so
  disjoint-from-author remains PARTIAL for the full review while the cross-provider judge
  corroborates its framing. NOTE: this is the cross-provider EDITORIAL judge; it does NOT
  supply the cross-provider EXPERIMENT replication of the Knight--Leveson result (re-running
  the underspecification instance with genuinely independent providers), which the paper still
  lists as owed (Sec 3.4 / Sec 6 / Sec 10).

## Pre-launch: fix stale README title + a genuine Use-Case-C validator failure (2026-06-21)

Checking the repo for the public push surfaced two real issues:
- README opening line still cited the OLD title ("Operating Multi-Agent Workflows on Disjoint Sources of
  Truth") -> updated to the current oracle-centric title. (All other README-referenced paths resolve.)
- src/C/evidence/results.json's upper_bound_validate_ok was a stale committed `true`; regenerating
  (measure_squeeze.py) produced `false` -- a GENUINE Use-Case-C failure: validate_handbook.py flagged
  (a) a false code-token "import" in api_policy_manifest.md prose, and (b)/(c) the 400/401 error shapes
  present in base_schema.json but no longer mentioned in API_POLICY_081's clauses / negative vector.
  Fixed by SYNCING the manifest (CLAUSE_3 now names `400`; the negative vector names `401`; "import
  directives" -> "draw on directives") -- NOT by weakening the validator (gate-weakening is the
  anti-pattern). Did NOT touch the deliberate §5 contested-point contradictions. validate_handbook.py ->
  VALIDATE OK; results.json upper_bound_validate_ok genuinely `true`; the paper recompute harness
  (verify_ground_truth) stays byte-identical (paper numbers unaffected; results_c.tex unchanged).
  Publishing the stale `true` would have hand-faked a harness number -- the exact thing the paper's
  "every number harness-generated" guarantee forbids.

## Repo cleanup for public release (2026-06-21)

Prepping the repo to go live at github.com/canonical/squeeze-loop. paper.tex change: removed the stray
draft line "July 26 Note \#1" from the author block (cosmetic; prior editorial verdict still applies, sha
updated). Repo-wide (not paper content): deleted working notes (review*.md, level-up-*.md, timestamped
plans, scratch); scrubbed the internal ollama IP localhost -> localhost across all going-public
scripts/docs/reports and the home path in real-use-case/workflow.md; gitignored .claude/ (symlink to
config/skills) + build intermediates; included real-use-case/ harness (docs, scripts, the 4 lace bug
write-ups) but excluded the vendored GPL lace source + build/work trees. No credentials were present.
Left for the author: src/C/evidence/results.json had an uncommitted upper_bound_validate_ok true->false
flip (predates cleanup) -- restored to committed (true) for the clean push, flagged for separate review.
28pp; 4 reflexive + editorial + cross-provider (AUTHORITATIVE) gates PASS.

## Add Zenodo DOI to the page footer (2026-06-21)

Formatting-only: added \usepackage{fancyhdr} + a footer carrying the Zenodo DOI 10.5281/zenodo.20787816
(clickable \href to https://doi.org/...), on every page including the title page (via a redefined
\fancypagestyle{plain}); page number centered, DOI right, no header rule. No content/claim change. Renders
on all 28 pages; 4 reflexive + editorial + cross-provider gates PASS.

## Two-remark trim: de-refrain the honest irony + drop a stale conclusion hedge (2026-06-21)

Two surgical Gate-A cuts (coordinator removing redundancy/hedge -- not new prose, so done directly):
1. The "honest irony" (reproducible numbers aren't the load-bearing ones) read as a refrain at three
   appearances; kept it in §1 Scope + §9 Provenance (Limitations), dropped the §8 (eval) echo --- cut
   "and rest the paper's empirical weight on the two live findings above" from the "What a full
   evaluation would add" paragraph (the sentence still says the powered comparison is specified-but-unrun
   and the exploratory pieces were run).
2. Conclusion carried a stale within-family hedge "(the mid tier the lowest, not a measured invariance)"
   that re-litigated the weaker tier-result right after the stronger qwen-ladder survivorship trend the
   conclusion now leads with --- cut the parenthetical, let the survivorship sentence stand.
28pp; 4 reflexive + editorial + cross-provider gates PASS. (No disjoint exerciser: pure deletions of
material flagged redundant, build+gates green --- a full review would be churn.)

## Post-review16 Gate-A: five fixes, run as a COMPLIANT squeeze loop (dogfood) (2026-06-21)

A fresh Gate-A judgment (ACCEPT-WITH-MINOR-REVISIONS; "further passes beyond two targeted edits would be
churn. Stop.") flagged five items. The user asked: are these done via the SL or directly? Answer (honest):
prior cycles were a PARTIAL loop -- disjoint exerciser + executable gates real, but implementer=coordinator
(a C1 collapse). For this pass the user chose the PROPER SL, so we dogfooded the paper's own method:
- IMPLEMENTER (barriered): five Sonnet sub-agents, each given only its review item + the exact target
  LaTeX + a spec, blind to the coordinator's preferred wording and to each other; each returned only
  replacement text.
- COORDINATOR (me): sequenced; at Gate A applied each edit, amended ONE (W2 site G's implementer invented
  a \ref{sec:intro} -> applied as a clean cut instead) and restored the n=1 hedge W5 dropped (Gate-A
  sharpen, not re-authoring), and INSTALLED the implementers' text (did not write the prose).
- EXERCISER (disjoint): a sixth Sonnet, blind to implementer/coordinator rationale, read the items + the
  revised paper and judged.
- LOWER BOUND: build + 4 reflexive gates + editorial + cross-provider.

The five edits:
- W1 (highest value): §6 barrier-null -> COMMIT to interpretation (a) -- for a competent model the context
  barrier is structurally present but EMPIRICALLY REDUNDANT (it follows explicit authority over the
  artifact regardless); not claiming inertness for weak judges; oracle+authority carry the load. Resolves
  the "present both, endorse neither" indecision.
- W4: SWE-bench "Toward a real-bug study" ~100-word unrun-study paragraph -> one sentence.
- W3: Figure caption -> point-estimate / no-CI note + qualitative trend as the replicable target.
- W5: contribution (iv) reflexive defects -> "of varying severity (structural ... to editorial)".
- W2: "existence demonstrations, not efficacy" recurred ~10x -> trimmed 5 most-redundant sites (kept the
  contextually-distinct ones).

EXERCISER VERDICT: W1/W3/W4/W5 ADDRESSED; W2 PARTIAL (still ~6, but each contextually distinct -- over-
trimming would need unique-content judgment, so stopped); NO new error/contradiction; W1 consistent with
the abstract and with nothing-else-calls-barrier-load-bearing. This is a genuinely C1-compliant pass
(implementer != coordinator != exerciser, disjoint evidence bases) -- the construction applied to itself.
28pp; 4 reflexive + editorial + cross-provider PASS. Per the Gate-A reviewer: STOP (converged).

## review16 cycle: retitle (oracle-centric) + resolve the "load-bearing" collision (2026-06-21)

Author reversed the keep-title call: subtitle "Operating Multi-Agent Workflows on Disjoint Sources of
Truth" -> "Catching Coherent-and-Wrong Artifacts with an Author-Independent Executable Oracle" (resolves
the W1/review16 title item). Then a paper cycle on review16.md, whose #1 item was: "load-bearing" pointed
two directions (front matter: oracle; but Remark 2 "centerpiece", §3.4 "named centerpiece", Conclusion
"The load-bearing decision --- the disjointness principle"). Fix = scope it everywhere: oracle is
load-bearing in general; disjointness load-bearing ONLY on the oracle-free terrain (Archetype B).
Edits:
- Conclusion: removed the flat "load-bearing decision --- the disjointness principle"; now "what actually
  CATCHES ... is the executable lower bound --- not a smarter model, not more agents, not hiding the code
  from the judge" (the author's unifying claim), disjointness scoped to Archetype B.
- Remark 2: "(C1) is the centerpiece" -> "the construction's distinctive design point" + a scoping
  sentence (both live findings land on the oracle; disjointness load-bearing only where no oracle).
- §3 intro: "the load-bearing condition (disjointness)" -> "the condition that makes the wiring sound".
- §3.4: "named centerpiece (disjointness)" -> "structural precondition"; "evidence barrier ... carries
  the gate" -> "the independent executable oracle ... carries the gate".
- Contribution (iv): dropped the oversold "lightweight" (review16 #3; §3 unchanged in weight).
- Abstract: rewritten to the author's THREE-THINGS synthesis (mechanical proof check; contradiction
  scaling hurts 0.54->1.00; the named mechanism doesn't measurably matter) + the unifying claim ---
  plainer, foregrounds the two positives + the honest negative (review16 #4, #6).
- Figure caption: now LEADS with "scaling makes the error worse" (review16 #5).

DISJOINT reviewer (review16 + revised paper, blind to rationale): all 6 review16 items ADDRESSED,
collision resolved (no site flatly crowns disjointness), title matches body, no gutting. Caught ONE new
issue I introduced: abstract "the mechanism the paper is named for" was anachronistic post-retitle ->
"the mechanism the strategy is built around". Fixed. 28pp; 4 reflexive + editorial + cross-provider PASS.

## Post-review15 Gate-A: fix restructure housekeeping (W2-W5); title kept (W1) (2026-06-21)

Fresh disjoint Gate-A judgment on the post-review15 paper: ACCEPT-WITH-MINOR-REVISIONS; "the restructure
landed the oracle-centric frame credibly", negative result not buried. Five flagged; verified the
factual ones and fixed W2-W5 (W1 = title, kept per the author's standing call):
- W3 (CONFIRMED bug from my §5 compression): archetype subsections -> \paragraph turned three
  \ref{sec:caseD}--\ref{sec:caseG} RANGES into "Section 5--5". Fixed all three sites -> \ref{sec:archetypes}.
- W4 (CONFIRMED inconsistency): "four-size qwen ladder" everywhere vs Figure 1's 3-tick axis (4B/9B/27B,
  the two 27B generations pooled). Fixed all 5 mentions (abstract, contribution, §6 body, figure caption,
  §11) -> "qwen capability ladder (4B/9B/27B)" / "(4B--27B)"; caption notes the pooling.
- W2: §3 opening led with "the cure is to remove the artifact from the judge's context" + "disjointness
  ... is what catches" (pre-reframe narrative) -> reoriented to oracle-first (the executable lower bound
  is the load-bearing element; the barrier is the structural guarantee whose outcome effect was null).
- W5: §1 Scope tension (executable instances "claimed" yet "not load-bearing") -> bridged ("these
  establish existence of the construction, not efficacy; the efficacy weight rests on the two live findings").

W1 (title/body mismatch -- the subtitle names the empirically-null mechanism) flagged by the reviewer as
#1 / desk-reject risk; author chose KEEP. Reviewer's own convergence note: "after these five fixes,
further editing is churn." 28pp; 4 reflexive + editorial + cross-provider gates PASS.

## Paper SL for review15 -- installment 2: targeted trim + cheap PARTIALs (2026-06-21)

Human chose "targeted" for the gap-doc (trim verbose un-itemized sections, PRESERVE the negative-result/
scope; plus the cheap PARTIALs). Done:
- #4 de-hedge: replaced the worst §6 nested-hedge ("observation, not a measured invariance: ... not an
  identical or guaranteed rate") with a clean claim + figure pointer.
- #3 survivorship: now its own \paragraph{Scaling makes the contradiction worse.} (separate billing).
- §2 classical antecedents: ~25 lines -> ~10 (all citations kept).
- §eval barrier-isolation: ~55 lines -> ~25, preserving the full negative result (0/12 escape, 324 then
  504 draws, the isolate-vs-exhibit tension, the honest reading) -- cut the fixture/per-tier detail.
- §limitations shared-priors: ~48 lines -> ~18, cutting the numbers that now duplicate §6/Figure 1,
  keeping Knight--Leveson + the dependency statement + "we claim ... and no more".
Verified the load-bearing negative-result/scope phrasing survived (grep). 28pp / ~15.6k words (from
32pp / 18.4k). Body reduction is larger than the page delta shows (the §7/§8 detail moved to appendices
rather than deleted). 4 reflexive gates PASS.

Left as deliberate non-cuts (diminishing returns / churn risk, per the converged-paper discipline): #5
remaining table weight and #9 terminology/glossary -- deep-cutting these risks re-introducing fiddling
and erasing the squeeze vocabulary the hybrid frame keeps. Honest status vs review15's "lose 35-40%":
we reached a clean ~targeted cut (pages 32->28; body more), not the full 35-40%, by the author's choice
to preserve the negative-result/scope honesty over hitting the number.

## Paper SL for review15 -- installment 1: structural cut + hybrid reframe (2026-06-21)

Launched a Squeeze Loop (sl-builder plan, human-approved: hybrid framing / keep title / full structural
cut) to take review15.md into account. review15 is structural: the named centerpiece (disjointness/
barrier) is empirically null (§eval isolation, 504 draws), so reframe around the executable oracle,
foreground the two wins (lace gate, contradiction/survivorship), cut ~35-40%.

Installment 1 (this commit) -- the structural moves + reframe:
- §7 stabilizers (13 + collapse table) -> Appendix~\ref{app:stabilizers} (in-body refs kept).
- §8 reflexive -> half page (detail to Appendix A / paper-impl.md).
- §6 dense fraction-prose -> Figure~\ref{fig:floor} (pgfplots: error rate vs qwen capability; the
  survivorship rise 0.54->1.00 made visual) + trimmed prose.
- §5 terrain archetypes: 4 subsections -> 4 compact \paragraph entries (caseD/E/F/G labels kept);
  redundant tab:archetypes dropped (kept tab:synthesis); synthesis prose trimmed.
- Hybrid reframe: Contributions reordered to lead with (i) the lace faithfulness gate, (ii) the live
  contradiction finding + survivorship "scaling makes it worse 0.54->1.00", (iii) a CLEAN NEGATIVE
  RESULT on the context barrier (outcome effect undetectable; oracle carries the load), (iv) the squeeze
  demoted to "an organizing frame". Abstract: survivorship billed; negative result foregrounded.
- Table 1 Barrier column: squeeze mark -> \checkmark$^{\circ}$ (structural present, no measured outcome
  effect) in the column, caption key updated.
- Honest irony elevated from a Limitations aside into the §1 Scope block.

DISJOINT EXERCISER (Sonnet, blind to edit rationale; read only review15 + the revised paper): 8/12
ADDRESSED, 4 PARTIAL (#3 survivorship lacks its own heading; #4 per-sentence hedging persists in §6/§eval
body; #5 table-weight remains; #9 glossary still ~11 coined terms), and confirmed NO GUTTING (clean
demotion; one borderline: reflexive mechanism detail elided to paper-impl.md). GAP DOC (raised to the
human, per the un-squeezed-coordinator stabilizer): the cut is ~17%, not 35-40%; reaching the target
needs deeper trims to §eval/§limitations/§2 -- sections review15 did NOT itemize and which hold the
negative-result/scope honesty the reframe just elevated. Awaiting the author's call before cutting those.
29pp (from 32); 4 reflexive gates PASS.

## Final convergence cycle -- promote the replication target to the claim sites (2026-06-21)

A third Gate-A judgment (ACCEPT-WITH-MINOR-REVISIONS) declared the paper CONVERGED: "further passes
beyond [one fix] would be churn." The single high-value remaining change: the two load-bearing live
findings rest on non-deterministic logged runs, disclosed only in §11 -- an inverted evidentiary
structure. Fix = promote the replication target to the SITE of the claims, not buried in Limitations.
Added a compact \paragraph{Replication} at the end of §4 (lace) and §5 (underspec), each stating what a
replicator needs + the qualitative confirmed target (the FLOOR, not the per-draw decimal) + that the
defect-finding/exact-rate is logged-not-gated, cross-referencing §11 for the full path. Did NOT touch
weaknesses 2-5 (the reviewer flagged them as diminishing-returns/churn risk -- e.g. consolidating B's
repeated hedges would risk re-introducing the fiddling the trim cycle just undid).

CAUGHT A REAL OVERCLAIM mid-edit (and a latent one from the W3 cycle): the first draft of the §5
Replication note said the genuinely-balanced floor is "near-100% reproduced across every model we ran"
-- but the qwen LADDER shows survivorship DEEPENS with capability (4b 0.54, 9b 0.83, 27b 1.00), so it is
NOT near-100% at small qwen sizes. active (>=0.92) and delivered_default (8/8) ARE near-100% across all;
survivorship is near-100% only at flagship scale. Fixed both the new §5 note AND the pre-existing §11
"What a replication needs" paragraph (which carried the same overstatement from W3, undetected because
that fact-check wasn't given the per-size survivorship breakdown). Verified against recomputed per-model
numbers. Rebuilt clean (32pp); 4 reflexive gates PASS. This is the convergence pass: the inverted
evidentiary structure is now legible at first read, and the paper is done barring the powered efficacy
comparison it honestly defers.

## Trim cycle -- de-hedge after the W1-W5 honesty pass over-corrected (2026-06-21)

A fresh Gate-A judgment (ACCEPT-WITH-MINOR-REVISIONS) diagnosed that the W1-W5 honesty edits had
OVER-corrected into over-qualification: bloated ~520-word abstract, the barrier-outcome negative stated
5-6x, "we state this once" then repeated, "provider-invariant" overstating 3 providers, and a B
"wrong" vs "genuinely open" inconsistency. This is the pendulum from over-elevation (old R3) to
over-defensiveness; the fix is TRIM, not add. Implemented all five:
- Abstract halved (~520 -> ~280 prose words): one concise barrier-negative mention, dropped the
  same-provider-casts detail + reflexive-defects sentence + duplicate scope (all still in the body),
  "provider-invariant" -> "reproduced across a three-provider panel".
- Barrier-negative consolidated: now ~4 justified homes (abstract brief, contribution (i), §7 experiment,
  §10 conclusion); tightened contribution (i)'s "anxiety-managing" paragraph.
- "provider-invariant" -> "reproduced across the (three-provider) panel" in §6 and §10 (+ "three
  providers, not invariance in a broader sense").
- "We state this once, here" -> "We state our scope plainly" (it wasn't once); removed the conclusion's
  duplicate existence-demonstration restatement.
- B rescope: delivered_default "wrong 8/8" -> "diverges from the authored archive 8/8", with a caveat
  (on B the archive shares the policy-owner's provenance, so this is underspecification SURFACED, not
  detection vs an independent oracle) -- reconciling the floor prose with §7's "we do not say the model
  is wrong"; also fixed the matching loose end in §eval (line ~1379).

DISJOINT Sonnet faithfulness check of the trimmed abstract + B rescope: faithful, correctly calibrated,
no load-bearing claim dropped (same-provider-casts is the closest but the conclusion still stands).
Caught + fixed two items: abstract "never sees the implementation it judges" (ambiguous -> "a judging
actor never sees the implementation it grades", matching C3) and the pre-existing §eval B
"coherent-and-wrong" without caveat. Rebuilt clean (31pp); 4 reflexive gates PASS. Net: same honesty,
less repetition -- the positive contribution is now easier to see.

## Global-story coherence sweep -- thread the soft->hard arc through section closers (2026-06-21)

Paper-cycle consistency read against the global story (the implicit upper bound): "a generic framework
for how to use AI to link a SOFT truth to the concrete/HARD-truth world." Disjoint Sonnet structural
read of the full 31pp: verdict = substantially coherent; the arc is loud at section OPENERS but goes
quiet at section CLOSERS (which tend to end on a measurement, a table, or a mechanism). Five surgical
connective edits (no new claims -- each restates the paper's own established framing), all proposed by
the disjoint reviewer:
- §6 (underspec) close: added a sentence tying the powered scaling result back to the arc -- the soft
  bound is genuinely ambiguous, capability doesn't resolve it, the disjoint oracle is the only thing
  that pins soft truth to a hard verdict.
- §7 (Stabilizers) close: section ended on Table 3 with no prose; added a closing sentence -- each
  stabilizer blocks a route by which the soft-intent->hard-verdict chain is severed.
- §8 (Reflexive) close: ended on "n=1 / rest no load-bearing claim"; added "the reflexive case is the
  global story turned inward" -- coherent-and-wrong hits soft-side editorial claims too, caught only by
  re-derivation from the source's hard truth.
- §5 Archetype B opener: made the soft<->hard provenance-sharing explicit at first contact (B's link
  reduces to author independence, not an external oracle).
- §2.3 (pipelines) close: swapped the method-ending clause for an arc-ending one (applies where the
  soft-to-hard link is hardest to forge: normative soft truth, no trainable verifier, no oracle).
Reviewer confirmed the strong sections (abstract, intro, §3 strategy, §10 limitations, conclusion) are
already well-threaded -- left untouched (no churn). Rebuilt clean (31pp); 4 reflexive gates PASS.

## §6 note: why D is deterministic / why the live floor is A,B,C only (2026-06-21)

Reader question: why did the powered/cross-provider live floor cover only A,B,C, not D? Verified against
the repo: only src/{A,B,C}/ground-truth/probe_cases.py define build_cases(); src/D has no probe -- by
design. Added a note in sec:underspec (right where A and C get re-armed as soft truths but proofs do
not): D (the deductive Rocq instance) has no SOFT upper bound to contradict -- its bound is a formal
spec, its gate the Rocq kernel + axiom audit (Print Assumptions) + code-blind mutations (the deductive
cousin of lace's strip-and-recompile), so coherent-and-wrong on D is a fabricated/vacuous proof rejected
DETERMINISTICALLY -- a yes/no construction check, not a stochastic divergence with a capability/provider
rate. D's evidence is the gate firing by construction; no capability curve to draw. Caught + fixed a
mechanism error mid-edit: first draft wrongly attributed strip-and-recompile (lace's Rust/Creusot
mechanism) to D; corrected to the Rocq kernel + axiom audit per sec:caseG. Rebuilt clean (31pp); 4
reflexive gates PASS.

## Gate-A judgment + implement W1-W5 (honesty/scoping pass) (2026-06-21)

Ran a paper cycle: a disjoint Sonnet Gate-A judgment on the full 31pp manuscript (verdict
ACCEPT-WITH-MINOR-REVISIONS), then implemented all five of its weaknesses. The recurring critique
(R3-style over-elevation, now at the abstract level): the context barrier is framed as a centerpiece
but its measured OUTCOME effect is zero (the §10 isolation experiment, ~504 draws); the honest reading
lived only in §10. Edits:
- W1: promoted the barrier's honest outcome status into the abstract + contribution (i) -- the oracle is
  the empirical catcher; the barrier's contribution is the STRUCTURAL guarantee (anchoring impossible in
  principle), its outcome effect undetectable in every condition we could cleanly test (§eval).
- W2: abstract "by construction" now carves out the oracle-free terrain -- by construction wherever an
  author-independent oracle exists (Archetypes A, C, D); B + soft side close by nesting to a human.
- W3: §11 now has a consolidated "What a replication needs" path (lace: rustc 1.96.0 + Creusot +
  faithfulness gate, deterministic; live: build_cases probes vs the oracle; the reproducible target is
  the FLOOR not the per-draw decimal; providers/tiers listed).
- W4: "no improvement with capability" -> "no monotone improvement with capability" everywhere (true
  umbrella for non-monotone A + flat B); "mid tier the lowest".
- W5: Table 1 caption notes the Barrier checkmark is the STRUCTURAL property; §10 saw no outcome effect.

All edits are scoping/honesty (no new claims). DISJOINT Sonnet fact-check of the five edits: all
faithful; two minor over-corrections fixed ("any capable model" -> "the models we ran"; "mid tier often
lowest" -> "the lowest" -- single aggregate obs). Confirmed no internal contradiction with §10 (which
already closes with "the oracle and the authority, not the context barrier, carry the load"). Rebuilt
clean (31pp); 4 reflexive gates PASS.

## Powered MULTI-PROVIDER replication -- gemma + llama at power (2026-06-20)

Powered the cross-provider axis: ran A/B/C at 8 draws/case, cap 512, on Google gemma4:31b and Meta
llama4:16x17b (784 draws), to pair with the powered qwen ladder -> three genuinely-independent
pretraining lineages (Alibaba/Google/Meta, none sharing pretraining w/ each other or the Anthropic
author). Slow non-MLX models (~85s gemma, ~63-130s llama, ~24h); gemma banked first. 18/784 UNPARSED
(llama C), excluded. Both passed controls. New report:
verify/reports/live/qwen-repeated-xprov-powered-2026-06-20.md. Runner: run_qwen_repeated.py --cap 512.

RESULT (vs powered qwen flagship 3.6:27b):
- PROVIDER-INVARIANT FLOOR on the genuinely-balanced forks: active 24/24, survivorship 24/24, B
  delivered_default 8/8 -- ALL THREE providers, 100%, at powered n. The "owed cross-provider
  replication" delivered.
- The softer/weaker-side forks SPREAD OUT (gemma most override-compliant, llama least): net qwen/gemma
  24/24 vs llama 16/24; patch-null gemma 16/16 > qwen 12/16 > llama 7/16; window qwen 14/24 < llama
  19/24 < gemma 22/22. So diversity decorrelates on the decidable forks but NOT on the genuine
  contradictions -- exactly where the oracle is the only adjudicator. NOT a generic compliance bias.

Paper: abstract + §6 + §10 upgraded from "preliminary / reps=1" to POWERED across three lineages,
scoped to the genuinely-balanced forks (no blanket cross-provider-100% claim).

DISJOINT Sonnet fact-check caught FIVE issues (all fixed): (1) verb "fall 24/24" misleading (24/24 =
err/comply with override) -> "err 24/24"; (2) "diverge in both directions" implied non-monotone but it's
monotone gemma>=qwen>=llama -> "spread out (gemma most compliant, llama least)"; (3) "decorrelates
exactly where decidable / fails exactly where contradiction" too crisp (utc complicates) -> softened;
(4) utc/window omitted from prose though it has the largest spread -> added with numbers; (5) hidden N
(gemma utc 22/22 not 24, 2 truncations) -> exposed via the added numbers + parenthetical. Process
working hard: caught a verb that inverted the meaning and a selective-reporting omission. Rebuilt clean
(31pp); 4 reflexive gates PASS.

## Powered qwen ladder -- add instance B (all three instances now powered) (2026-06-20)

Extended the powered qwen ladder to instance B (underspecified refund agent), so all three instances
A/B/C now have the full 4-size, 8-draw, cap-512 treatment. B run: 4 models x 16 cases x 8 reps = 512
draws, 0 UNPARSED (cap 512 clean). Merged into verify/reports/live/qwen-repeated-powered-2026-06-20.md
(B section added; A/C unchanged). B raw: qwen-repeated-powered-B-2026-06-20.jsonl.

RESULT: B overall error flat-ish across the ladder (0.20/0.14/0.20/0.14, non-monotone, CIs overlap) ->
no improvement with capability, matching §6's ~25%. The pure unstated-default fork delivered_default is
8/8=100% wrong at EVERY size -- a clean capability-invariant point mirroring A's active fork. 7 of 16
forks 0/8 on all sizes (competence intact); error concentrates on a few unstated-default/precedence
forks (precedence_fraud_transit, fraud_flag -- high but noisy/size-variable at n=8). So underspecification
shows the same capability-invariance as contradiction on its hardest fork.

Paper: §6 + §10 now state the powered qwen result covers all THREE instances (A contradiction floor flat
+ survivorship deepens with capability; B underspecification -- delivered_default 8/8 every size; C
patch-null 0.50-0.75).

DISJOINT Sonnet fact-check of the B numbers caught TWO overclaims (both FIXED): (1) "flat across the
ladder" overstated a non-monotone alternating aggregate -> "no improvement with capability
(non-monotone)"; (2) "narrow, capability-invariant floor like A's" / "capability-invariance holds for
underspecification" implied ALL of B is invariant, but only delivered_default is (precedence_fraud_transit
8/3/8/3 and fraud_flag 7/5/7/4 are noisy/size-variable) -> scoped the invariance to delivered_default +
the aggregate-no-trend, flagged the other forks as noisy. Process working: caught an over-tidy
"capability-invariant" generalisation from one clean fork to the whole instance. Rebuilt clean (31pp);
4 reflexive gates PASS.

## Powered qwen ladder -- full 4-size, high-cap, the size gradient settled (2026-06-20)

The powered version the prior cycle flagged as future work: full 4-size qwen ladder (qwen3.6:27b,
qwen3.5:27b/9b/4b) x A,C x 8 draws/case at temp 0.7, answer cap raised 160->512. 1056 draws,
control-gated. New flag eval/live/run_qwen_repeated.py --cap; report
verify/reports/live/qwen-repeated-powered-2026-06-20.md.

Cap-512 fix VALIDATED the truncation hypothesis: C UNPARSED 59% (cap 160) -> ~6% (cap 512), so C
finally has real powered data. All UNPARSED excluded as INSUFFICIENT; all 4 models passed controls.

RESULT (n=24 per contested fork):
- Floor survives across the FULL ladder: A active 24/24,24/24,24/24,22/24 (>=0.92 every size); net
  ~0.96-1.00; C patch-null fools all four sizes 0.50-0.75. Aggregate A flat 0.67-0.72 (no improvement
  with capability at the aggregate).
- THE SIZE GRADIENT: survivorship error RISES monotonically with size -- 4b 0.54, 9b 0.83, both 27b
  1.00. Capability makes that contradiction WORSE, not better. active/net flat. So nowhere does scaling
  help on the contested forks; on survivorship it actively hurts.
- Competence: both 27b score 0 on ALL decidable forks while at the floor (unambiguously
  coherent-and-wrong); 9b minor slips (aov 2/15, 404 1/16); 4b larger (aov 5/15) -> don't over-read the
  4b's low survivorship as principled resistance.

Paper: §6 qwen text + §10 updated single-draw/reps-3 -> powered full-ladder result (active/net flat,
survivorship deepens with capability, C no longer truncation-limited).

DISJOINT Sonnet fact-check caught TWO real errors (both FIXED): (1) "larger models score zero on the
decidable forks ... 4b alone slips" -- WRONG, the 9b also slips (aov 2/15, 404 1/16); scoped clean-
decidable to the two 27b's. (2) "n=24 per fork" overgeneralised (true only for contested floor forks;
aov/distinct/C differ) -> "n=24 per contested fork". Also tightened "flat near 100%" -> ">=0.92".
Process working yet again: the disjoint check caught an over-tidy "competence intact" claim that erased
the 9b's nonzero decidable cells. Rebuilt clean (31pp); 4 reflexive gates PASS.

## Repeated qwen draws -- does the contradiction floor survive sampling? (§6 follow-up) (2026-06-19)

§6 reported the qwen contradiction ladder at ONE deterministic (temp-0) draw per case, hedging "a
repeated qwen version is future work." Ran it: instances A and C, 3 draws/case at temperature 0.7, two
qwen sizes (qwen3.6:27b-mlx, qwen3.5:4b-mlx), control-gated, scored vs the executable oracle.
New runner eval/live/run_qwen_repeated.py; report verify/reports/live/qwen-repeated-2026-06-19.md.

RESULT (UNPARSED excluded as INSUFFICIENT throughout):
- A FLOOR SURVIVES SAMPLING: legitimate-authority forks net 9/9 (both sizes), active 27b 9/9, survivorship
  27b 9/9 -- at or near 100% over repeated temp-0.7 draws, not a temp-0 artifact.
- NO improvement with capability: the larger 27b is no better on active/survivorship (9/9 vs 4b 7/9,
  6/9); no clean size ordering (tie at 9/9 on net; 4b errs MORE on the decidable utc/window fork) ->
  non-monotone, like the Claude ladder.
- Floor is the defect not incompetence: both ~0 on decidable forks (27b 0/9, 4b 1/8), controls passed.
- C truncation-limited: at temp 0.7 the long API prompts ran past the 160-token answer cap -> 32/54
  (27b) and 25/54 (4b) UNPARSED, excluded. Parsed-only patch-null override 100% wrong on both sizes but
  small-n (3/3, 3/3, 1/1) -- corroborates, does not establish.

Paper edits: §6 qwen-ladder caveat ("single draw ... repeated qwen version is future work" -> repeated
on two sizes: floor survives, no improvement with capability, C truncation-limited, fine size-gradient
+ higher cap still future work); §10 strengthened the resistance-to-capability claim from single to
repeated draws.

DISJOINT Sonnet fact-check against the run data caught THREE imprecisions (all FIXED): (1) "larger errs
more on the contested forks" overgeneralised -- true for active/survivorship but net TIES at 1.00 and on
utc the SMALLER errs more; rephrased to "no better there ... no clean size ordering." (2)/(3) "~0 / near
zero on the decidable forks" erased the 4b's aov 1/5; replaced with explicit 27b 0/9, 4b 1/8. Process
working: the disjoint check caught selective/over-tidy reporting of a no-improvement result. Rebuilt
clean (31pp); 4 reflexive gates PASS.

## Cross-provider §6 replication -- the "owed" experiment, answered (preliminary) (2026-06-19)

List item #3: replicate §6's contradiction/underspecification finding across GENUINELY independent
providers (the abstract/§4.4/§10 had it as "owed"). Found the standing ollama host serves multiple
independent pretraining lineages, so #3 was NOT blocked. New runner eval/live/run_xprovider_six.py
(reuses run_underspec load_probe/score -> byte-identical cases/scoring to §6). Report:
verify/reports/live/xprovider-six-2026-06-19.md.

What ran (honest scope -- this is the discipline, not a footnote):
- Alibaba qwen3.6:35b (MLX, fast): FULL A/B/C, 0 unparsed. A 11/15=.73, B 2/16=.12, C 4/15=.27.
- Google gemma4:31b: A 11/15=.73 and B 1/16 clean; C INCOMPLETE (host degraded mid-run) -> excluded.
- Four-lineage SPOT CHECK (smoke, 1 case/instance): Alibaba, DeepSeek, Google, Meta.
- EXCLUSIONS as INSUFFICIENT infra (NOT scored as coherent-and-wrong, per the paper's own control):
  OpenAI gpt-oss:120b (unloadable model blob); DeepSeek-r1:70b (reasoning, ~200s/draw, full run
  infeasible -- it stalled the first attempt); Meta llama4 (too slow for a full run). UNPARSED/timeout
  responses excluded from rates throughout.

RESULT (the load-bearing convergence): on archetype A, two independent non-Anthropic lineages (qwen,
gemma) err at the IDENTICAL .73 and, on all 10 both-wrong cases, pick the SAME wrong reading (10/10),
fork-for-fork in lockstep (active 3/3 & 3/3, net 3/3 & 3/3, survivorship 3/3 & 3/3, window 2/2 & 2/2).
B: identical answer 15/16. Four-lineage spot check: same wrong reading on 2/3 sampled cases (A,B); on
C, qwen+gemma erred alike but Meta+DeepSeek read it correctly (convergence strong, NOT total). So
genuine model diversity largely does not decorrelate the contradiction blind spot -> it lives in the
task, not the weights -> corroborates "disjointness of EVIDENCE, not model weights, carries the gate."

Paper edits: abstract ("owed a cross-provider replication" -> "preliminary cross-provider replication
... two independent lineages ... same wrong reading"); §6 contradiction paragraph (added the
multi-provider replication + convergence after the qwen-ladder floor); §10 Shared priors ("not yet
run / claim ... and no more" -> "begun and pointing the predicted way ... preliminary, not powered").

DISJOINT Sonnet fact-check against the run data caught TWO of my overclaims (both FIXED): (1) I wrote
the four-lineage spot check was "unanimous"/"all four on the identical wrong reading" -- FALSE, on C
Meta+DeepSeek were right; corrected to "2 of 3 sampled cases, split on C." (2) §10 said "three full
lineages" -- only TWO providers ran in full here (Claude is the separate §6 anchor); corrected to "two
independent lineages run in full." Process working as designed: the disjoint check caught a coherent
over-reach in my own write-up of an anti-over-reach experiment. Rebuilt clean (30pp); 4 reflexive
gates PASS.

## Lean the framing onto the oracle -- disjoint review said "keep title, don't churn", one surgical fix (2026-06-19)

Goal: lean the framing further onto the executable oracle (make the oracle the empirical
protagonist, disjointness the structural precondition) -- candidate moves were a title change and a
contribution reorder. Ran it as a paper cycle with a DISJOINT Sonnet reviewer given only the framing
surfaces (abstract/intro/contributions/conclusion) and the established evidence facts.

Reviewer verdict (disciplined, anti-churn):
- TITLE: KEEP. Foregrounding the oracle in the title would collapse the paper into prior-art
  "verifier-in-the-loop / just run tests" and erase the squeeze's actual novelty (the construction:
  upper+lower bound + disjoint authority pairs + nesting to a human). The oracle-as-protagonist
  belongs in abstract/contributions, not the title.
- ABSTRACT REORDER: DECLINED (my call, against the reviewer's Edit 1). All three surfaces (abstract,
  contributions, conclusion) deliberately lead with the concrete real-world UEFI hook and frame the
  coherent-and-wrong/oracle finding as the one that "earns the architecture" (conclusion says so
  verbatim). Reordering only the abstract desyncs the three and demotes the external-codebase result.
- The reviewer flagged contribution (i)'s "the executable oracle catches the residual" as inverting
  the hierarchy (reads as the oracle mopping up disjointness's leftovers). Checking the BODY
  (§4.4, line ~717) it already says precisely "catches the residual CORRELATED ERROR ... the
  shared-pretraining blind spot model-disjointness leaves standing" -- the oracle is the primary
  catcher of the error class the barrier provably cannot remove. The contribution had abbreviated
  "correlated error" away, creating the ambiguity. So the reviewer's diagnosis was right but the fix
  is body-grounded, not the weakening it assumed.

ONE surgical edit: contribution (i) "catches the residual" -> "catches the residual correlated error
the barrier provably cannot --- the shared-pretraining blind spot model-disjointness leaves
standing." This both removes the ambiguity AND leans hardest onto the oracle (it catches exactly what
the structural barrier cannot), matching the body. Rebuilt clean (30pp); 4 reflexive gates PASS.
Honest outcome of the cycle: the framing was already well-leaned onto the oracle; the disciplined move
was to NOT change the title or reorder, and to make the single precision fix.

## Section 6 repeated-draws -- strengthen the live finding + CORRECT the C inversion (2026-06-19)

review14 #3 / the Gate-A "next experiment": repeat §6's contradiction/underspecification ladders with
many draws. Ran 735 Claude draws (build_cases A/B/C, 5 reps x 3 tiers, scored vs the executable
oracle; workflow wf_d6e4148b-cad; logged to verify/reports/live/six-repeated-draws-2026-06-19.md). 0
failures. A and C are the SAME case sets as §6 (15 and 18 cases; n = 5x), so they are clean repeated
updates; B's build_cases probe is 16 cases, NOT the §6 "balanced 12-case gap pool" -- so B was NOT
substituted (case-set mismatch caught before committing).

RESULT -- two things:
1. STRENGTHENED "no improvement with capability." A is non-monotone (46/75, 25/75, 40/75 = .61/.33/.53;
   mid lowest, strongest climbs back near weakest), with a hard floor: the GA4 active fork is wrong
   15/15 = 100% at EVERY tier incl. opus (survivorship 15/15 at haiku & opus, sonnet outlier 4/15). B
   (12-pool) and C are flat. So capability brings no monotone gain, and none at all on the
   both-authorities-legitimate forks.
2. CORRECTED the C "inversion." Single-draw had C 0/18,2/18,2/18, read as a capability-INVERSION
   (weakest right). Over 5 reps C is flat ~0.12 (11/90, 12/90, 10/90) -- NO inversion; the single-draw
   "weakest right" was an artifact. §6 now states the correction explicitly. The qwen "larger fooled
   more" (§6 ladder, §10 shared-priors) softened accordingly -- single-draw on qwen; floor reproduction
   kept (consistent), size-ordering claim dropped.

Paper edits: §6 contradiction paragraph rewritten (A repeated/non-monotone + sharp active floor; C
flat, inversion corrected); §9 recap A/C -> repeated figures (B left at 3/12); abstract/contribution
(iii)/conclusion dropped the draw-count claim (qualitative "no monotone trend" -- A/C repeated, B
12-pool still single). B 12-pool sentences left UNCHANGED (case-set integrity).

Disjoint Sonnet verification (given the log + changed sections): caught two of MY drafting slips --
(a) a leftover "one draw per case" contradicting the new "five draws"; (b) "survivorship nearly so"
imprecise vs sonnet's 4/15 outlier -- both FIXED. Confirmed A/C numbers match the log, the C
correction is faithful and not buried, no 16-case B leaked into the 12-pool, qwen size-ordering
removed, draw-count claims honest, no residual "invert"/"falls weak-to-strong". Applied (sha
b1f52902f16629b87fd727b9d51e86acf7e2a1a99450b3f0a750682bddc72a9f); rebuilt clean (30pp); 4 reflexive
gates PASS. This is the repeated-draws experiment doing exactly its job: it solidified the headline
and caught a single-draw over-claim (the C inversion) that the paper had shipped.

## reflexive-squeeze self-run -- recompute harness caught two apparatus defects (2026-06-19)

"run a paper cycle and share the judgment on the paper itself" (the README's canonical prompt). Ran
the full reflexive squeeze (src/paper/ground-truth/verify_ground_truth.py), which the recent
edit-cycles had not exercised -- and it caught two real coherent-and-wrong defects in the paper's OWN
apparatus:
1. DETERMINISM: tex/macros/gates.tex committed \ResGateSFlagged{1} but the generator
   (verify/gate_s_measures.py, reading the committed skill stores) recomputes 2 -- a stale macro. The
   value is generated-but-UNUSED in the prose, so no manuscript claim was wrong, but the recompute
   harness rightly failed on the byte-identical check. FIXED: regenerated gates.tex (-> 2).
2. READING RECORDS: every \cite must resolve to a bib/records/ entry; two were MISSING --
   denis2022creusot (Creusot) and gleirscher2023manifesto (the applicable-FM manifesto). FIXED: read
   both sources (Creusot ICFEM-2022 PDF; the manifesto via ar5iv) and wrote faithful reading records
   (claim cards + method + limitations + why-cited, VERDICT SUPPORTED each), matching the repo format.
   Adding them bumped \ResReflexRecords 49 -> 51 (regenerated reflexive.tex; also unused in prose;
   \ResReflexRecordsFull stays 43, correct -- both new records are partial reads, not FULL).

paper.tex UNCHANGED (sha 848f8d1e...) -- the fixes are macros (unused) + reading records + the
ledger, so the manuscript content and the disjoint review on file carry forward; 4 reflexive gates
PASS, editorial gate PASS, build clean (29pp). After committing the regenerations,
verify_ground_truth.py is green (determinism + cites-resolve + build all PASS). This is the reflexive
point working as intended: an edit-cycle run of the four lightweight gates is not the full squeeze;
the recompute harness is what catches stale generated numbers and unrecorded citations.

## barrier-isolation: weaker, cross-provider arm (qwen ladder) -- fourth negative (2026-06-19)

Ran the one condition the Claude tiers could not rule out: a genuinely WEAKER judge. Re-ran two seeds
(well-specified anchoring; soft-side persuasion) on the qwen ladder (4B/9B/27B, Alibaba -- weaker than
Claude haiku, cross-provider), control-gated, 10 draws/cell, via Ollama (runner
eval/live/run_barrier_isolation_qwen.py; NOT the Agent/Workflow path, which is Claude-only). Logged to
verify/reports/live/barrier-isolation-weakmodel-2026-06-19.{md,json}.

RESULT: fourth clean negative. All three qwen models PASSED the control probes, and escape (judge
ratifies the artifact's reading) = 0/10 in EVERY cell, both seeds, all arms. Even qwen 4B (weaker than
haiku) followed the explicit authority over the code and over the fluent justification. (Only non-zero
"other": qwen-27B anchoring/B had 3 unparsed figures, 0 escapes.)

FOUR-REGIME / SIX-MODEL PICTURE: 504 draws total (324 Claude + 180 qwen), three regimes, two provider
families, 4B->Opus range. escape with the artifact in context = 0 in every condition. The honest
refinement of the scope: where the failure WOULD bind -- a judge that follows the artifact over an
EXPLICIT authority -- is a regime a clean isolation excludes (a model that cannot hold the authority
fails the control gate = incompetence, not coherent-and-wrong; and the experiment must use an explicit
authority, the very condition under which a competent judge does not need the barrier). So isolating
the barrier and exhibiting it are in tension; the result stands as "the oracle and the authority, not
the barrier, carry the load in every condition we could CLEANLY test."

Paper: extended the §9 "Isolating the barrier" passage (now split into two paragraphs for readability)
with the qwen extension + the isolation-vs-exhibition tension. Disjoint Sonnet verification: CLEAN --
numbers match the log, 504 total correct, negative honestly bounded ("cleanly" is load-bearing),
consistent with the reframe, qwen properly framed as opt-in cross-provider corroboration. Applied (sha
848f8d1e66a490535fe08a8e522f4b87026b73ba482a06ac08510717bebc3571); rebuilt clean (29pp); 4 reflexive
gates PASS. The barrier-isolation program (anchoring x2, persuasion, weak/cross-provider) is now as
complete as a clean design allows.

## barrier-isolation: soft-side persuasion arm -- three-arm program complete (2026-06-19)

Ran the third and last barrier-isolation arm: the SOFT side, mechanism = persuasion (not anchoring).
Live, Claude sub-agents (workflow wf_41878cef-b14). Binding refund policy (REIMBURSE only within 30
days, absolute); clear violation (90-day request reimbursed); LLM compliance-judge rules
compliant/violation given the bare decision / + the agent's fluent self-justification / + a
length-matched neutral note. escape = judge accepts the violation. 3 arms x 3 tiers x 12 = 108.
Logged to verify/reports/live/barrier-isolation-softside-2026-06-19.md.

RESULT: third clean negative -- escape 0/12 in EVERY cell, all tiers, all arms. The fluent
justification swayed no judge; every tier held the absolute policy and rejected the reimbursement
(several explicitly said the rationale was irrelevant). Persuasion did not bind any more than
anchoring did.

THREE-ARM PICTURE (324 draws total): in all three regimes -- well-specified hard side, underspecified
hard side, soft side -- escape with the artifact-side material in context (Arm B) was 0/12 at every
tier, never above barrier-on. The barrier's outcome-effect is undemonstrated in every condition, for
one consistent reason: given an EXPLICIT authority a capable model follows it (or escalates the gap)
regardless of what artifact-side material (code or a persuasive rationale) is in its context, so the
failure the barrier removes did not reproduce. NOT read as "barrier useless" -- the anchoring/
sycophancy failures it targets are documented (Sec sota) and plausibly bind in weaker models / under
less explicit authorities; read as the honest scope: the executable oracle and the authority itself,
not the context barrier, carry the load in every condition we could test. This is the strongest
possible empirical backing for the review13/review14 reframe (oracle = protagonist, barrier =
structural precondition), produced by a pre-specified experiment that ran TOWARD the negative.

Paper: §9 "Isolating the barrier" paragraph now reports all three arms + the synthesis (324 draws).
Disjoint Sonnet verification: CLEAN -- soft-side numbers match the log, 324 total correct, negative
honestly scoped (not "useless"), consistent with the abstract/Contribution (i) reframe, no surviving
barrier overclaim in abstract/contributions. Applied (sha
e96372fe674ba1059296d39e2054b8fcb890addb69ab1b899279f3d542c6971a); rebuilt clean (29pp); 4 reflexive
gates PASS. The full review14 #2/#3 experimental program (all three barrier arms) is now complete.

## barrier-isolation: underspecified arm (2026-06-19)

Ran the next arm I had named as open: the UNDERSPECIFIED-spec barrier arm (where the barrier should
bind, the §6 regime). Live, Claude sub-agents (workflow wf_0dfe1e5c-304). Seed: handbook asks for
"active users" but is silent on whether a login-only user counts; fixture 1000 authenticated / 300
login-only / 700 substantive; defective code counts all authenticated (1000) vs exclude-login (700).
Judge asserts a figure OR escalates. escape = asserts 1000 (ratifies the code's reading). 3 arms x 3
tiers x 12 = 108. Logged to verify/reports/live/barrier-isolation-underspec-2026-06-19.md.

RESULT: another clean negative for anchoring, PLUS a positive for the squeeze's soft-side design.
- No anchoring: escape(B, code in context) = 0/12 at every tier, <= escape(A) (haiku A 4/12, B 0/12,
  B' 5/12; sonnet & opus 0 escape everywhere). Seeing the code did NOT make judges ratify it.
- Dominant response = ESCALATE to the policy-owner (the squeeze-correct move): sonnet & opus 12/12 in
  every arm; haiku escalated most of the time. NOT caused by the barrier (holds in all arms).
- Weakest tier (haiku) sometimes CONFABULATED handbook authority (invented "METRIC_002", a
  "product-council directive", "GA4 standard" -- none in the prompt) to fill the gap, a
  coherent-and-wrong of its own; it did this LESS, not more, with the real code present.

Paper: extended the §9 "Isolating the barrier" paragraph to report this arm. Disjoint Sonnet
verification flagged one real issue -- the escalation result appears to contradict §6's "no
improvement with capability / capable models fill the gap" unless the design difference is stated.
FIXED: noted that escalation was an EXPLICIT offered option here, unlike the §6 probe where the agent
had no escalation path. (Honest reconciliation; does not rewrite §6.) Only the soft-side persuasion
arm now remains untested. Applied (sha
2b056d3705fd12105ba90533482c2eec4e5bbead5c8dfeb4c837f8f2ad1326ba); rebuilt clean (29pp); 4 reflexive
gates PASS.

## review14 cycle 2 of 2 -- ran the barrier-isolation experiment (Archetype A) (2026-06-19)

Ran the experiment review14 #2/#3 asked for (the one item that adds new evidence, not reframing).
Live, with Claude sub-agents (workflow wf_9d664c98-afb): the Archetype A gross-vs-net seed (handbook
mandates net = gross - refunds; fixture gross $1,000,000, refunds $250,000, net $750,000; defective
impl returns gross). Judge writes the acceptance figure; escape = its test passes the defective gross
impl. Three arms (spec-only / spec+code / placebo) x three tiers (haiku/sonnet/opus) x 12 draws =
108 draws. Logged to verify/reports/live/barrier-isolation-archetypeA-2026-06-19.md.

RESULT: a CLEAN NEGATIVE -- escape 0/12 in EVERY cell, all arms, all tiers. Every judge, including
those shown the defective code (Arm B), derived the spec's net figure and caught the defect; several
(all tiers, incl. haiku) explicitly named the code buggy. The barrier moved nothing. On a
well-specified spec a capable judge follows the authority over the artifact whether or not it can see
it, so the executable spec-derived oracle -- not the context barrier -- is what catches. This is the
negative §9 pre-specified; it empirically backs the cycle-1 reframe (oracle = protagonist) and is
consistent with the boundary-condition framing (the failure lives on contested specs, not clear ones).

Paper updated: §9 paragraph rewritten from "the experiment we owe" to "Isolating the barrier: a clean
negative", reporting the run (108 draws, 0/12 all cells), scoping the negative (it does NOT settle the
underspecified-spec or soft-side arms -- the natural next experiments), and letting the negative
stand. This is the reflexive discipline working: the paper pre-specified the negative and now reports
it against itself.

Disjoint Sonnet verification (given the log + the §9 paragraph): CLEAN -- numbers/design/result match
the log exactly, the negative is correctly scoped (not over-generalized), consistent with the
abstract/Contribution (i) reframe, and the §1 "tests tuned to the code" tension is handled honestly
(capable models did not anchor on a clear spec; the active regime is underspecified specs). Applied
(sha 49076832a447e300e233561c17ef66f5ea5e82682fd91ed4c6662a16a5401391); rebuilt clean (29pp); 4
reflexive gates PASS.

## review14 cycle 1 of 2 -- reframe (disjoint Sonnet) (2026-06-19)

Eighth+ external review (review14.md), the most substantial: 6 major concerns + smaller points + a
proposed tighter abstract + a detailed barrier-isolation experiment design. The reviewer's bottom
line gives the in-scope path: "short of running the barrier experiment, reframe disjointness as a
structural precondition and let the executable oracle be the empirical protagonist." Cycle 1 does
that reframe + the in-paper fixes; Cycle 2 (running the barrier-isolation live experiment) is offered
separately as a large live-model undertaking.

Addressed:
- #1 (centerpiece vs evidence): ABSTRACT REWRITTEN (~430 -> tighter) -- disjointness of evidence is now
  the structural PRECONDITION, the executable oracle the CATCHER/protagonist; lace leads with the
  faithfulness gate and states the defect-finding is the verifier's, not squeeze-specific. Contribution
  (i) header aligned ("structural precondition ... and the executable oracle as the catcher").
- #4 (cross-provider not a headline result): abstract now says the diversity claim "is owed a
  cross-provider replication, and we do not rest on it" (removed the "made measurable" overclaim).
- #6 (abstract density): cut "we claim only this", "design aspiration not a proven universal", the
  duplicate "of evidence not weights", "made measurable rather than asserted"; caveats stated once.
- #6-concern (reflexive defects relabel): "coherent-and-wrong OR over-claim defects" now consistent at
  all six sites (abstract, contribution, conclusion, appendix title + caption, §8/§9, intro).
- #2 (barrier never shown to bind): added a §9 paragraph "Isolating the barrier (the experiment we
  owe)" -- diagnoses why the pilot nulled (both arms spec-derived), gives the corrected design (Arm A
  spec-only vs Arm B spec+code test-writer, length-matched placebo, agreement-with-code mediator, many
  draws), concedes it is un-run, and pre-specifies the clean negative that would collapse the
  contribution to "the oracle is the whole story." (Honest resolution of #2 in the reframe direction;
  RUNNING it is Cycle 2.)
- smaller (lace headline): faithfulness-gate-is-the-squeeze-specific-part moved up front in the
  abstract; (strip-and-recompile novelty): §4.1 now distinguishes it from "ordinary annotation
  hygiene" -- a disjoint mechanical check, not the prover's self-discipline.
Declined/deferred (noted): #5 (compress §5 -- already framed as existence demos; further compression
risks the terrain-taxonomy contribution); #3 (repeated §6 draws -- needs the experiment, Cycle 2);
checkpoint pinning (needs re-run); A/D-both-archetype-A rename (churn across many sites for a "small
irritant"); venue framing (strategic, no clean edit).

Disjoint Sonnet verification: flagged 3 issues, all fixed -- (1) abstract "casts ship identically"
unhedged vs the body's CONSENSUS-reading scope -> "ship identically as one model-consensus reading";
(2) a §9 reflexive restatement still said only "coherent-and-wrong defects" -> added "or over-claim";
(3) Contribution (i) "complementary pair" discontinuity with the abstract -> header reworded to the
precondition/catcher framing. Applied (sha
586e4e20019cef6232daa6942c0e2837f12e8961e656fe6f0255f7c2793a1248); rebuilt clean (29pp; +1 from the
§9 barrier-isolation paragraph); 4 reflexive gates PASS.

## full-paper consistency read #9 -- CONVERGED, no changes (disjoint Sonnet) (2026-06-19)

Cycle requested as "read the full paper once more for consistency using the paper cycle." Disjoint
Sonnet full read at sha aa8bdc58 (the post-review13 narrative-audit state): verdict **CONVERGED,
nothing actionable**. Verified the prior cycle's §9 edits (deleted "Where capable models err
(pointer)" paragraph; reworded the closer to "powered comparison as specified-but-unrun") integrated
cleanly -- no dangling transition, no orphaned cross-reference, the deleted content still available in
Contribution (i)/§3.4/§underspec, closer accurate. Re-confirmed all numerics (lace 25=8+17, 4=3+1,
corpus 241, disposition 37/36; seeded 15; reflexive 4+4=8 w/ 1 external; hyps 1+3=4; §6 fractions
12/15,9/15,6/15 and 0/18,2/18,2/18; qwen 3/12), cross-refs, scope qualifiers, term introduction, and
front-matter consistent. NO paper edit -- paper-sha unchanged (aa8bdc58...), verdict carries forward,
prior cross-provider AUTHORITATIVE result stands. Third clean consistency read (#6, #8, #9); the
intervening items were self-induced by review12/review13 edits and are closed.

## narrative-coherence re-audit post-review13 (disjoint Sonnet) (2026-06-19)

Re-ran the global-story narrative sweep (the README prompt) after review13's substantial edits.
Disjoint Sonnet: COHERENT overall --- all five review13 loci (Contribution (i) pair reframe, the new
§10 worst-first dual-failure limitation, the §6/§9 raw fractions, the abstract trim+cross-provider
clause, the §10 cost/irony additions) integrate cleanly and serve the soft↔hard-truth thread; the
arc holds; the motif is at the right density (the new §10 limitation strengthens it by naming the
case the construction cannot link). Three PRE-EXISTING local-logic items flagged (none from review13);
acted on two, declined one:
- B2 (APPLY): the §9 "Where capable models err (pointer)" paragraph was a pure pointer to §underspec
  with covered content and an awkward "cast that measures ... casts" phrasing -> DELETED. (Reverses an
  earlier cycle's "keep"; a fresh disjoint read judged it redundant, and on re-read the
  comparative-baseline paragraph above it already carries the content. No reference broke
  -- self_contained PASS; the disjointness pointer survives in Contribution (i) and §3.4.)
- B3 (APPLY): the §9 closer called the whole section "a protocol sketch", underselling the
  exploratory pieces that WERE run -> reworded to "present the powered comparison as
  specified-but-unrun --- the exploratory pieces above were run".
- B1 (DECLINE): §underspec's two-beat opener ("Manipulation is a wall ... underspecified is not")
  judged a defensible sharpening contrast, not a competing opener worth restructuring a converged
  section.

Applied (sha aa8bdc58ef1c650f4f6ac9deb0759cbb8318f998c855b8e909f6937885f9fae8); rebuilt clean (28pp);
4 reflexive gates PASS.

## review13 cycle (disjoint Sonnet) (2026-06-19)

Seventh+ external review (review13.md): praise + 5 major concerns + 5 smaller. Addressed:
- #1 (headline mechanism vs evidence): reframed Contribution (i) as "Disjointness of evidence AND the
  executable oracle, as a complementary pair", explicit about attribution -- disjointness removes the
  POSSIBILITY of anchoring, the oracle CATCHES the residual, and the live evidence lands on the
  oracle; the barrier's distinct value is a structural guarantee concentrated where a judge would
  otherwise anchor. (The §3.4 two-jobs resolution already existed; this surfaces it in the
  contributions.)
- #2 (the scarier failure the structure handles least): added a WORST-FIRST §10 limitation -- "The
  harder failure is the one the oracle cannot see": the dual of coherent-and-wrong (satisfies the
  hard check, betrays soft intent, §3.1) passes the oracle and falls to the un-squeezed Gate~A;
  by-construction covers only the catchable half. Opener reworded so "worst first" leads with it.
- #3 (sample sizes): replaced §6/§9 percentages with raw k/n -- A 12/15,9/15,6/15; C 0/18,2/18,2/18;
  refund ~3/12 per tier -- matching the live reports; added "we report raw k/n, since each cell is a
  single draw."
- #4 (distinctive claim awaits replication): added to the abstract that the Knight--Leveson core
  (disjoint evidence beats model diversity) still awaits a genuinely cross-provider replication.
- #5 (Table 1 No-auth overstates): caption now notes the squeeze-loop checkmark is for HAVING a
  construction (Archetype B), not an oracle-backed guarantee, which B lacks (reduces to author
  independence). Kept the checkmark (the column = "has a construction"); did not mis-downgrade.
- smaller: #6 trimmed the abstract capability parenthetical ("no monotone trend;" dropped); #8 added
  the reproducibility-irony sentence (the deterministic harness regenerates the seeded NON-load-bearing
  numbers; the load-bearing §4/§6 findings are non-deterministic/unpinned); #9 made the cost
  back-of-envelope concrete as a STRUCTURAL count (a handful of role-invocations + 2 docs/item, low
  single-digit multiple, not measured tokens).
Already covered / not added: #10 (null-as-finding) was done in the review12 boundary-condition edit;
#7 (by-construction vs stabilizers split) is now carried by the new §10 dual-failure paragraph + the
existing hard-side scoping of "by construction".

Disjoint Sonnet verification of all edits: arithmetic and fractions confirmed against the live
reports; §10 dual-failure consistent with §3.1/§3.3; Contribution (i) consistent with §3.4; abstract
trim/clause consistent with §10; irony + Table-1 caption consistent. One issue: the §10 cost
parenthetical said "four role-invocations", clashing with the three actors named and the pipeline
(coordinator acts twice) -> reworded to "a handful of role-invocations (coordinator delegation + gate
approval, implementer, exerciser)". Noted (not changed): "disjointness of evidence not weights" now
appears ~7x -- each in a distinct structural role; it is the paper's centerpiece. Applied (sha
8b20d1a79c156c92076239e65d5c3c0d21ff4a39c9d8a3cf6cc50bd9f1154931); rebuilt clean (28pp); 4 reflexive
gates PASS.

## full-paper consistency read #8 -- CONVERGED, no changes (disjoint Sonnet) (2026-06-19)

Cycle requested as "read the full paper once more for consistency using the paper cycle." Disjoint
Sonnet full read at sha 7078cb32 (the consistency-#7 state): verdict **CONVERGED, nothing actionable**.
Verified the consistency-#7 §5.2 table reword (intro "gives each role a different slice of the truth";
role-neutral "Holds in context / Withheld" headers) reads cleanly and fits all three rows incl. the
Gate; re-confirmed all numerics (lace 25=8+17, 4=3+1, corpus 241, disposition 37/36; seeded 15;
reflexive 4+4=8 w/ 1 external; hyps 1+3=4; qwen 3/12=25%), cross-refs, scope qualifiers, term
introduction, and front-matter consistent. NO paper edit -- paper-sha unchanged (7078cb32...), verdict
carries forward, prior cross-provider AUTHORITATIVE result stands. Recorded as provenance of an
independent clean pass. (Two consecutive clean reads now: #6 and #8 found nothing; the one item in
#7 was self-induced by review12's new table and is closed.)

## full-paper consistency read #7 (disjoint Sonnet, review12-edit focus) (2026-06-19)

Cycle requested as "read the full paper once more for consistency using the paper cycle," focused on
whether the review12 additions integrated cleanly. Disjoint Sonnet: 1 ACTIONABLE ISSUE (low),
otherwise CONVERGED -- the §9 opener/Protocol-status split is non-duplicative and consistent, the
§3.3 human-interface sentence is consistent with §8/§10 and does not overclaim, and all numerics /
cross-refs / scope qualifiers / terms check out.
- The one issue: the new §5.2 context-barrier table used "Prompt holds / Prompt withholds" headers and
  an "each actor's prompt" intro, but its third row is the Gate -- a mechanism with no prompt. FIXED:
  intro -> "gives each role a different slice of the truth"; headers -> "Holds in context / Withheld"
  (role-neutral, so the Gate row reads naturally). Cell content was already accurate vs the prose,
  tab:cast, and §3.4.

Applied (sha 7078cb327d3aef29aad6f23c0811fce3fe74b1dac1a55e4c4c01972fd2e51e4b); rebuilt clean (28pp);
4 reflexive gates PASS. (Self-induced again: the only issue was a header-framing slip in last cycle's
new table, caught and closed.)

## review12 cycle (disjoint Sonnet) (2026-06-19)

Sixth+ external review (review12.md): mostly praise + three refinements + minor notes. Addressed the
three actionable refinements:
- #1 (Sec 9 "evaluation tension"): reframe the nulls as a NON-LINEAR efficacy / BOUNDARY CONDITION,
  stated EARLIER (the Sec 9 opener) per the review. Added the boundary-condition sentence to the
  opener ("efficacy is non-linear, so these null pilots are a boundary condition, not a shortfall ...
  strictly necessary only on contested soft specs") and RELOCATED there from the Protocol-status
  paragraph (the review11 "diagnostic, not disappointing" sentence was trimmed to a short transition
  to avoid duplication).
- #2 (human-in-the-loop regress -- how does the human avoid corruption/overwhelm?): added to Sec 3.3
  the human terminus's operational interface -- "bounded ... the human does not re-verify from
  scratch (the hard gates settled the executable side) but adjudicates only the soft-side residual,
  the delta between what U claims and what L established, holding U and the gate record without having
  produced the work they judge." Bounded scope answers overwhelm; disjoint (holds U, didn't produce
  the artifact) answers corruption; does not claim the human guarantees correctness.
- #3 (visual scannability of the context barrier): added a compact 3-row inline table to Sec 5.2
  (Archetype B) -- Role | Prompt holds | Prompt withholds -- making the disjointness concrete
  (implementer holds policy+conversation, withholds the archive; exerciser holds policy alone,
  withholds the implementation; gate sees both decisions via the lockpoint). Verified against the
  prose, tab:cast, and Sec 3.4; complementary, not a duplicate of tab:cast.
Declined (defensible): the "organizational invariant, not an algorithmic fine-tune" emphasis at the
Sec 1 asymmetric-guarantee sentence -- Sec 2.2 already makes that point in its proper place; adding
it at Sec 1 would conflate two distinct asymmetries. (Minor notes -- Sec 6 "organize the logs", the
closing question -- need no paper edit.)

Disjoint Sonnet verification of the three edits: flagged one overstatement -- the Sec 9 opener's
"capable models reliably diverge" overstates Sec 6's hedge -> softened to "diverge and added
capability does not fix it". Edits 2 and 3 clean; the Sec 1 decline judged defensible. Applied (sha
f479e2c46d255689d0f2008607ff5704d71f522c0a33b7053a1994db4cb4e3b0); rebuilt clean (28pp; no margin
overflow); 4 reflexive gates PASS.

## full-paper consistency read #6 -- CONVERGED, no changes (disjoint Sonnet) (2026-06-19)

Cycle requested as "read the full paper once more for consistency using the paper cycle." Disjoint
Sonnet full read at sha ada179f1 (the consistency-#5 state): verdict **CONVERGED, nothing
actionable**. Verified the consistency-#5 Sec 8 clause ("a narrow framing probe ... separate from the
live cross-provider cast of Sec underspec") reads cleanly, resolves correctly, and is consistent with
Sec 6/Sec 10's experimental-qwen treatment; and re-confirmed numerics (lace 25=8+17, 4=3+1, corpus
241, disposition 37/36; seeded 15; reflexive 4+4=8 w/ 1 external; hyps 1+3=4), cross-references,
scope qualifiers, term introduction, and front-matter all consistent. NO paper edit made -- paper-sha
unchanged (ada179f1...), so this verdict carries forward and the prior cross-provider AUTHORITATIVE
result stands. Recorded as provenance that an independent pass at this exact sha found nothing.

## full-paper consistency read #5 (disjoint Sonnet, recent-edit focus) (2026-06-19)

Cycle requested as "read the full paper once more for consistency using the paper cycle," focused on
whether the just-added Sec 8 nesting sentence integrated cleanly. Disjoint Sonnet: 1 ACTIONABLE
ISSUE; everything else clean (numerics, cross-refs incl. sec:mechanics, the "same provider family, so
partial" usage, the n=1 framing and the "no load-bearing claim" parenthetical all consistent).
- The new Sec 8 sentence introduced a use of the cross-provider judge -- corroborating the
  MANUSCRIPT's framing -- that no other section scopes (Sec 6/Sec 10 discuss the qwen only as the
  experimental cast; an earlier Sec 10 mention of the cross-provider EDITORIAL judge had been trimmed
  in a later cycle, so this deployment now appeared only once, unscoped). FIXED: made Sec 8
  self-contained with a disambiguating clause -- "a narrow framing probe that passes its controls,
  separate from the live cross-provider cast of Sec underspec" -- so a reader cannot conflate it with
  the experimental qwen or over-read it as a full review/replication. (Chose the in-place caveat over
  re-expanding Sec 10, to avoid re-inflating the reflexive apparatus.)

Applied (sha ada179f1141933545475b676b1c0d91caa4ea3eee05987267352dbfaeff15e5f); rebuilt clean (28pp);
4 reflexive gates PASS.

## incorporate edit.md into Sec 8 (reflexive case study) (disjoint Sonnet) (2026-06-19)

User asked whether material synthesized in edit.md (a one-paragraph synthesis of THIS file -- the
standing disjoint editorial-review history) could be incorporated into Sec 8 (the reflexive case
study). Disjoint Sonnet scoping verdict: a genuine, NARROW under-sell. Sec 8 said its gate's
independence "was only approximated --- by separating the verifying pass from the writing pass, and by
external challenge", but the actual process used the construction's own nesting (a different-model
disjoint judge + a cross-provider qwen framing-consistency judge + a human peer-reviewer terminus) ---
and Sec 3.3 already CITES Sec 8 as the exemplar of that human terminus working, while Sec 8 never
described the stack. ADDED one sentence after "external challenge": "That approximation used the
construction's own nesting: each revision cycle was reviewed by a disjoint model (a different-model
sub-agent reading the authored draft; same provider family, so partial), corroborated on framing
consistency by a genuinely cross-provider judge (a second provider family), with the human peer
reviewer as the mandatory terminus that closes the un-squeezed Gate~A (Sec mechanics)."

Kept honest and un-inflated per the standing over-elevation caution (circle 124): scoped the Sonnet
judge as same-family/partial, scoped the qwen judge to framing-consistency, left "only approximated"
and the n=1 framing intact, and the "we rest no load-bearing claim" parenthetical untouched.
DELIBERATELY EXCLUDED (disjoint reviewer's do-not-add list): the convergence claim (defects shrank
over cycles -- an efficacy framing for n=1), any "it worked / caught more" claim, any appendix
expansion, any positioning of the qwen corroboration as a Sec 10 replication result.

Applied (sha b1b112f5620f5dce47ef3a9e8e44156bfbff96255dd193a6bc3254f78bd762ed); rebuilt clean (28pp);
4 reflexive gates PASS.

## narrative-coherence re-audit (disjoint Sonnet) (2026-06-19)

Re-ran the global-story narrative sweep (the README prompt) because the review11 cycle reworked
several openers/closers (§3.3, §5 opener, §5.2, §9, §10). Disjoint Sonnet verdict: COHERENT --- all
five recently-edited sections cohere, every section's opener/closer still links to the global story
at the right density, NO missing links, and the end-to-end arc (framework -> why hard -> how forged
-> evidence) holds. Only two over-link/trim candidates, both minor:
- §3.4: the evidence-not-weights distinction restated closely back-to-back, with an empty
  editorializing tag "This distinction is load-bearing." -> TRIMMED that tag (the paragraph proves
  it; the sharp concrete statement and the "two distinct jobs / complementary not competing"
  resolution, both flagged valuable by the earlier framing panel, were KEPT).
- §5.5: forward-pointer to §eval at the synthesis close -> DECLINED: it is a specific caveat that the
  coupling figures are illustrative, not a duplicate of §6's apparatus pointer (different purposes).

Applied (sha d6323a4b2e28d0e2afb071968be0c5617452d7f6e721a1e1d1eb84ad7a4cc066); rebuilt clean (28pp);
4 reflexive gates PASS. The narrative dimension is converged: the motif is threaded, not a refrain.

## review11 cycle + nesting-terminus directive (disjoint Sonnet) (2026-06-19)

Fifth+ external review (review11.md), plus a user directive overriding its point #2. review11's three
High-Risk Vulnerabilities + a structural suggestion, all addressed:
- #1 ("mostly-null pilots" framing in Sec 9): added a framing sentence to Protocol status -- the nulls
  are "diagnostic, not disappointing" (seeded tasks too easy; capable models already right on small
  well-specified code), and the strategy targets CONTESTED soft specs (Sec underspec), where the
  barrier earns its keep. Sets up the "comparative baseline on defective soft specs" paragraph rather
  than duplicating it.
- #2 (nesting regression / "who squeezes the squeezer?"): USER DIRECTIVE overrides review11's
  "quantify the depth (n=2)" suggestion -> instead state plainly that a HUMAN MUST END THE NESTING,
  full stop. Sec 3.3 rewritten: "the recursion MUST terminate in a human ... a stack of automated
  monitors only relocates the un-squeezed judgment one level up --- it can never close it ... A human
  must end the nesting, full stop." Aligned Sec 10 to match ("must terminate at a human (an external
  reviewer) ... automation alone never closes it") after the disjoint check flagged Sec 10's looser
  "human or external reviewer" as a precision loose end vs the new categorical Sec 3.3.
- #3 (Knight-Leveson / Archetype B): added the ASYMMETRIC-guarantee statement to Sec 5.2 -- on
  Archetype B the squeeze removes conversational anchoring (a NECESSARY condition for correctness) but,
  lacking an external oracle, cannot supply sufficiency; reduces to author independence (Fagan/
  Cleanroom) plus that anchoring guarantee, and no more. Consistent with Sec 2.6 novelty + Sec 10.
- structural (A/B/C/D alphabet soup): added an inline instance<->archetype mapping at the Sec 5 opener
  (A & D = transcription, B = authored authority, C = split planes; four instances over three
  archetypes) instead of a third table -- tab:archetypes and tab:synthesis already exist; trimmed the
  now-redundant reconciliation sentence from Sec 5.5 (avoiding the duplication a third matrix or a
  repeated sentence would create). review11's closing scaling question (multi-file repos) is discussion,
  not a required edit; SWE-bench wiring (Sec 9) + cost limitation (Sec 10) already gesture at it.

Disjoint Sonnet verification of all five edits: CLEAN -- each accurate, in-voice, non-contradictory;
flagged the Sec 3.3-vs-Sec 10 phrasing asymmetry -> fixed. Applied (sha
2e755411b37d3fc1a500efb5629a75ce36d3172b76c62090fccb58c7e1595aae); rebuilt clean (28pp; +1 page from
the additions); 4 reflexive gates PASS.

## holistic readiness pass (disjoint Sonnet) (2026-06-19)

Cycle requested as "read the full paper once more for consistency using the paper cycle." Having
rotated through every standing dimension (consistency, terms, summary-vs-body, narrative, numeric,
redundancy, citations), ran a HOLISTIC readiness pass instead of re-running one dimension: verify the
recent edits integrated cleanly + one disciplined full hunt for any remaining actionable issue, with
license to conclude CONVERGED. Build clean (0 overfull boxes / no margin overflow), 4 reflexive gates
PASS, editorial gate PASS on entry.

Disjoint Sonnet: recent edits (citation fixes, redundancy cuts, relocated terminology note, abstract
trim) ALL integrated cleanly. One actionable issue:
- l.685: "Gate~S is the no-blend rule of Section~\ref{sec:disjoint}" -- but the no-blend rule is
  Gate~C, defined in Sec 3.3 (sec:mechanics), not Sec 3.4 (sec:disjoint). FIXED -> \ref{sec:mechanics}.
(Same defect class as consistency-read #4's l.365 fix: a cross-ref target that drifted as content
moved between the §3.3 mechanics and §3.4 disjointness subsections.)

Applied (sha f0bdf484886bb800ba389678bb4d581a8cb67ed9827ee367fbffc9c1e06453ab); rebuilt clean (27pp);
4 reflexive gates PASS. The paper is converging: the last several cycles have each found a single
localized cross-ref or hygiene item, no substantive defects.

## citation-attribution sweep (3 web-enabled disjoint Sonnet agents) (2026-06-19)

User directive: citation-attribution sweep -- does each cited CLAIM match what the source actually
says (Principle 5; the one honesty dimension this cycle-run had not yet checked). Ran THREE
web-enabled disjoint Sonnet agents in parallel, split by section, each extracting the claim attached
to every \cite in its range and verifying against the real source via web. ~62 citation-claim pairs
checked. (One agent garbled its first run by trying to fan out per-paper; re-run inline cleanly.)
NO sources were un-downloadable -- the four older works (Avizienis 1985, Knight-Leveson 1986, Fagan
1976, Saltzer-Schroeder 1975) were confirmed via authoritative secondary sources. Build clean, 4
reflexive gates PASS, editorial gate PASS on entry.

5 attribution issues found; fixed 3, declined 2:
- cemri2025why (l.323): "placing weak verification and inter-agent misalignment among the COMMONEST
  breakdowns" -- but in the MAST taxonomy task/weak verification is the LEAST common of the three top
  categories (~21%; spec/design 42%, inter-agent misalignment 37%). FIXED -> "counts weak
  verification and inter-agent misalignment among its three top failure categories" (true; drops the
  false frequency claim).
- anil2021pvg + kirchner2024pvg (l.316-318): the "sneaky prover rewarded for plausible wrong answers"
  + capability-gap sweep are Kirchner 2024 specifics, and "co-trained" overstates the alternating-round
  procedure. FIXED -> "trained against each other", and attributed the sneaky-prover reward to
  \citep{kirchner2024pvg} specifically.
- atlidakis2019restler (l.956): characterized as "spec/runtime drift detection", but RESTler is
  stateful REST API fuzzing from the spec. FIXED -> "the established practice of exercising a live API
  against tests derived from its specification" (accurate to RESTler, drops the wrong label).
Declined: qian2023chatdev "software-company simulation" (matches ChatDev's own "virtual software
company" framing -- within paraphrase); sun2023clover "passing all checks implies correctness"
(already hedged as "on the hypothesis that" and previously addressed as reflexive defect D7).

All other ~57 pairs FAITHFUL; metadata (venue/year/authors) correct where checked; the four named
external standards (RFC 7396 null-deletes, ASC 606 net-vs-gross, GA4 active-user, GDPR Art. 17) all
FAITHFUL. Applied (sha 099c1d07841345775fd02398c17e10f7591aa47548b3c1585680eb70d2fdda23); rebuilt
clean (27pp, 0 undefined citations); 4 reflexive gates PASS.

## redundancy & local-logic sweep (disjoint Sonnet) (2026-06-19)

Cycle requested as "read the full paper once more for consistency using the paper cycle." Rotated to
the freshest unswept dimension (per the write-a-paper standing-sweeps menu): "say it once"
(redundancy) + local paragraph logic. Build clean, 4 reflexive gates PASS, editorial gate PASS on
entry. Disjoint Sonnet returned 11 candidate items (4 high, 4 medium, 3 optional); applied 4, declined
the rest with reasons:
- R5 (abstract): the "disjointness of evidence, not weights" distinction stated twice in the abstract
  (l.85-86 and l.99-101) -> trimmed the second to "the load-bearing distinction --- of evidence, not
  weights --- made measurable rather than asserted" (keeps the NEW point, drops the verbatim restate;
  the "implementation absent from judge's context" gloss already appears at l.79).
- R6 (Sec 4): the strip-and-recompile mechanism described in full in both the Sec 4 opener and Sec 4.2
  -> trimmed the opener to "cannot survive its strip-and-recompile check", leaving the full mechanism
  to Sec 4.2 where the result is reported.
- R1 (Sec 9): "near-zero rate" appeared 5x in the eval section, with two consecutive paragraphs both
  OPENING "The near-zero rate is [a property of thin tasks / specific to small tasks]" -> dropped the
  redundant opener of "Toward a real-bug study" (the point is made in the preceding "comparative
  baseline" paragraph; "nonzero" carries the contrast).
- L5 (orphan): the "Terminology: role names are organizational, not cognitive" sentence dangled at the
  end of Sec 10 (Limitations) with no structural home -> relocated to Sec 3.2 (cast), where the role
  names are first assigned.
Declined: R2 (tab:synthesis caption repeats the "existence demonstration / no detection rate"
qualifier -- JUSTIFIED: tables are read independently of prose, so the caveat belongs on the table at
its highest-misread point); R3 (abstract/contributions parenthetical -- structurally motivated);
L1/L2 (paragraph restructures in Sec 3 disjointness / Sec 5 synthesis -- modest gain, churn risk on a
converging paper); L4 (Sec 9 "pointer" paragraph -- serves a real connecting job); L3/L6 (optional
polish).

Applied (sha 8f3ea7a08123ea405e56679bbc696d4735b14433c8a3199f74ebbc71e7189ff0); rebuilt clean (27pp);
4 reflexive gates PASS.

## full-paper consistency read #4 (disjoint Sonnet, numeric/cross-ref focus) (2026-06-19)

Cycle requested as "read the full paper once more for consistency using the paper cycle." Rotated the
emphasis (per the write-a-paper standing-sweeps menu) to the least-recently-swept dimensions:
NUMERIC/ARITHMETIC and CROSS-REFERENCE integrity, plus a recent-edit check on last cycle's 7
narrative-link additions. Build clean, 4 reflexive gates PASS, editorial gate PASS on entry.

Disjoint Sonnet verdict: INCONSISTENT -- 1 issue. ALL numerics re-verified independently (lace 25=8+17,
4=3+1, corpus 241, disposition 37 slots/36 fns, seeded 15, reflexive 4+4=8 with 1 external, hyps
1+3=4, ladders A 80/60/40 + C 0/11/11, qwen 3/12=25%); all macro/prose/table triples agree; the 7
narrative additions introduce no contradiction and broke no count or reference.
- The one issue: a MISMATCHED CROSS-REFERENCE at l.365 (Sec 2.5, mutation-testing antecedent) --
  "the seeded falsifications of Section~\ref{sec:mechanics}" pointed at Sec 3.3, which defines the
  GATE but contains no seeded instances; the seeded falsifications live in Sec 5 (the four case
  studies). FIXED -> \ref{sec:archetypes}.

Applied (sha 5a3dd4955c5b08d3512ce2b76ec696fa62a35d1d97f4cf929a4e2ec2b17a30db); rebuilt clean (27pp);
4 reflexive gates PASS; 0 undefined references.

## narrative-coherence sweep against the global story (disjoint Sonnet) (2026-06-19)

User directive: read for paragraph-level coherence and "why each paragraph is here, like a small
part of a global story," changing section openers/closers where a link to the global story is
missing. The GLOBAL STORY (the implicit upper bound of the cycle): the paper is a generic framework
for forging a link between a SOFT TRUTH (normative authority) and the CONCRETE/HARD WORLD (executable
ground truth). (New standing sweep; belongs under write-a-paper Principle 3/14.)

Disjoint Sonnet narrative audit returned NEEDS-WORK (13 sections weak/missing link, 12 paragraph
issues). Applied 7 high-value link additions, each adding a DISTINCT local point (not a stamped
refrain), declined the rest:
- §2 SOTA opener: prior work forges part of the link but leaves the per-actor evidence base
  unspecified.
- §2.5 antecedents opener: the setting is new -- antecedents drew independence from separate
  people/teams; the squeeze must construct it among agents sharing one model's priors. (First draft
  duplicated the §2 opener; the disjoint re-check flagged it -> rewritten to this local point.)
- §5.2 Archetype B opener: the hardest terrain for the link (no external authority; lower bound
  built from within).
- §5.3 Archetype C closer: the terrain where the truth itself is split across two planes; the link
  is forged by holding them independent.
- §5.4 Rocq opener: the link does not require a runnable oracle -- here the concrete truth is
  type-checking itself.
- §7 Stabilizers opener: a collapse severs, at one node, the link between the soft authority and the
  executable ground truth.
- §10 Limitations opener: each limitation is a place the link is still incomplete -- hard side, soft
  side, or evidence reach.
Declined (with reason): §4.2 (the "squeeze, not Creusot, earns its keep" lede is already the crisp
2nd paragraph); §8 reflexive (opener already maps the construction onto the paper); §3.2/§3.3 (§3
already carries the link strongly -- adding would be a refrain); plus the level-1 buried-lede/orphan
flags judged not worth churning given the openers now orient each section.

Disjoint Sonnet RE-VERIFICATION (second agent): all 7 accurate, in-voice, non-breaking; flagged §2.5
as a near-duplicate of §2 -> rewritten (above); judged the motif now at the right density (middle
sections deliberately not re-annotated, so it reads as one story, not a refrain). Applied (sha
603b4d9f53ace2414717acf67f8723309b4dc4a3c8f5d093d2a710cf0c0658ed); rebuilt clean (27pp); 4 reflexive
gates PASS (claim_consistency clean -- the threaded motif did not trip the uniqueness caps).

## term-definition & introduction sweep (disjoint Sonnet) (2026-06-19)

User directive: "read the full paper for consistency ... make sure each term is well defined and
introduced before being used." Ran a disjoint Sonnet term-hygiene audit (full inventory of coined
terms, acronyms, symbols, gate/role names, labels; each checked for defined-somewhere +
introduced-before-use). Build clean, 4 reflexive gates PASS, editorial gate PASS on entry. (This is
now a STANDING sweep recorded in the write-a-paper skill, Principle 2 + the standing-sweeps menu.)

Audit returned ISSUES (24); fixed the genuine ones, declined the universal/cosmetic:
- "existence demonstration" (coined, used 7x, never glossed) -> inline gloss at first use (l.190):
  "single end-to-end runs showing the construction instantiates and its gate fires on each terrain,
  not measurements of how often it helps".
- "no-blend" (used in glossary/figure before "blending" defined) -> glossed in the Gate C glossary
  row: "the no-blend rule --- one plane's check may not stand in for another's".
- H1--H4 (referenced as "H2", "H1, H3, H4" but NEVER stated in the body; defined only in
  verify/eval_protocol.py) -> enumerated all four in Sec eval before first reference, copied verbatim
  from the harness (the source of truth).
- "formalizer"/"prover" (Rocq roles not in the canonical cast) -> mapped inline: "the cast's
  property author and implementer, respectively, specialized for the deductive terrain".
- "standing invariant" (bare in cast table before its Sec mechanics definition) -> inline gloss +
  forward pointer: "(a property re-checked after every item, defined in Sec mechanics)".
- A/B/C/D DUAL LABELLING (letters label both 3 archetypes AND 4 instances; D = 2nd archetype-A) ->
  removed the premature "four A/B/C/D instances" in Sec 3.3 (now "four seeded instances, Sec
  caseD--caseG"), and added an explicit reconciliation at the synthesis opening: "A, B, C reuse the
  letter of the archetype each instantiates ... D is a second instance of archetype A ... four
  instances span three archetypes, with A and D sharing archetype A". Verified consistent with
  tab:synthesis, tab:archetypes, "instance B", and ResNTerrains=4 / ResNArchetypes=3.
- Acronyms expanded at first use: UEFI (at first BODY use, Contribution ii, not the abstract),
  PE, ESP, DoS, SMT, MBR, TPM, FFI, ASC 606, GA4, GDPR, RFC. Disjoint re-check confirmed each
  expanded exactly once, no double-expansion.

Declined (documented): universal acronyms (API, LLM already done) left bare; "prover" cast-role vs
"prover--verifier games" collision left -- the latter is a fixed compound proper-noun (cited ML
paradigm), the former is glossed at use as "the cast's implementer", different registers.

Disjoint Sonnet RE-VERIFICATION (second agent, post-fix): confirmed all fixes correct and the
A/B/C/D reconciliation introduces no contradiction; caught one residue (UEFI expanded after its
first body use) -> moved expansion to Contribution (ii), de-duplicated the Sec realworld one.
Applied (sha 3b9812fc89eb4d01a19700a28c6f4e714ed8e2e486f91d0a21341fc6906973e3); rebuilt clean
(27pp); 4 reflexive gates PASS (incl. self_contained).

## summary-vs-body faithfulness sweep (two disjoint Sonnet agents) (2026-06-19)

User directive: dedicated summary-vs-body faithfulness sweep -- check every claim in the summary
surfaces against its precise body statement (the residual drift the last 3 cycles kept finding lived
there). Ran TWO disjoint Sonnet agents IN PARALLEL, each decomposing its surfaces into atomic claims
and matching each to a body line with a FAITHFUL/OVERSTATED/UNDERSTATED/UNSUPPORTED/CONTRADICTED
verdict: agent 1 = abstract + contributions (29 claims, 1 issue); agent 2 = conclusion + all tables
+ figure captions (~80 claims, 6 issues). Build clean, 4 reflexive gates PASS, editorial gate PASS on
entry (sha 0f5a4de6).

Fixed 5 of the 7 flags (2 declined, with reasons):
- B10 (Contribution iii) -- a verb the PREVIOUS cycle (consistency #3) introduced now read wrong:
  "model-consensus core ... reduce but do not catch" applied "reduce" uniformly, but the body says
  cross-model casts ship the consensus core IDENTICALLY (zero reduction) while only critics reduce
  the non-consensus errors. FIXED -> "whose model-consensus core every model-based check reproduces
  --- self-critique, same-context critics, and same- and same-provider cross-model casts alike ---",
  matching Sec 6 "what every model-based check passes ... is the model-consensus reading". (Note: the
  prior cycle over-corrected an over-claim into a different over-claim; this is the accurate union.)
- tab:positioning, AlphaCodium "Barrier" cell: "(\checkmark)" UNSUPPORTED -- the body describes only
  "a flow against public and AI-generated tests" (supports the Gate mark, not "physically enforced
  context separation"). FIXED -> "---".
- tab:synthesis, D "Lower bound made of": "the Rocq kernel + a signed proof registry" -- "signed
  proof registry" appears NOWHERE in Sec caseG (lower bound = "the Rocq kernel"; gate = axiom audit).
  FIXED -> "the Rocq kernel + axiom-audited proofs".
- Conclusion dropped two headline counts the body/abstract give: "proved functions robust" (no 25)
  beside "surfaced 4 defects" -> added \ResRWRobust{} (25); "caught coherent-and-wrong defects" (no
  count) -> added \ResReflexDefects{} (8) + "(1 only by external review)".
- tab:cast Coordinator row presented the coordinator as squeezed above/below with no marker, while
  the body makes the un-squeezed editorial judgment (Gate A) load-bearing. FIXED -> added inline
  caveat "(but its editorial judgment, Gate A, is itself un-squeezed within the loop; Sec strategy)".

Declined (with reason):
- Conclusion "same- and same-provider cross-model casts ship identically" lacks an extra "within one
  provider family" prose clause: the noun-phrase "same-provider" IS the scope signal; stacking a
  second clause over-qualifies a summary callback (same adjudication as the qualifier-uniformity
  cycle).
- Appendix D-label ordering (D1-D2-D3-D7 / D4-D5-D6-D8): cosmetic, deliberate plane ordering, counts
  correct, D8 reference load-bearing.

All other ~100 atomic claims across both agents verified FAITHFUL. Applied (sha
85baa5fe4cee0968b0ce30e1b89b5dd23db6212f8b6395df5937a064636f4fa3); rebuilt clean (27pp); 4 reflexive
gates PASS.

## full-paper consistency read #3 (disjoint Sonnet, table/definition focus) (2026-06-19)

Cycle requested as "read the full paper once more for consistency using the paper cycle." Done
DISJOINTLY (Sonnet subagent, full read), this pass steered at the lower-yield-but-overlooked areas:
definitions, figures, TABLES + captions, eval/limitations caveats, quantifiers, recomputable
arithmetic. Build clean, 4 reflexive gates PASS, editorial gate PASS on entry (sha c98fac63).
Arithmetic all re-verified (corpus 241; lace 37 slots/36 fns; seeded 15; reflexive 4+4=8;
hypotheses 1+3=4; robust 8+17=25; runnable+pending eval configs 2+3=5).

Disjoint Sonnet verdict: INCONSISTENT -- 3 substantive + 1 cosmetic. Fixed the three:
- I1 (Contribution iii, line ~213) -- LOAD-BEARING: the intro said the divergence was "missed by
  self-critique, same-context critics, and both same- and same-provider cross-model casts", but the
  body (Sec 6, lines ~1064-1067) shows self-critique HALVES it and a same-context critic + LLM-judge
  cut it to ~a sixth -- they reduce, they don't miss. What every model-based check misses is the
  model-CONSENSUS core specifically. FIXED -> "whose model-consensus core self-critique, same-context
  critics, and both same- and same-provider cross-model casts reduce but do not catch, and which is
  surfaced only by the executable lower bound", matching Sec 6's "what every model-based check passes
  ... is the model-consensus reading".
- I2 (tab:cast Implementer row, line ~573): canonical cast table listed the terrain-specific
  "\emph{total additivity}" as the implementer's lower bound, while Sec mechanics (line ~657) and the
  pipeline figure use the general term "standing invariant" ("in our instances total additivity").
  FIXED -> "a \emph{standing invariant}" in the general table.
- I3 (tab:collapse, coherent-and-wrong row, line ~1190): defense listed as "13 + Gate~C", but
  stabilizer 13 is explicitly scoped to the authored-authority case ("Where authority is authored
  ..."), while Gate~C is the general defense. FIXED -> "Gate~C; 13 where authored" (general defense
  first, 13 scoped).
- I4 (appendix defect table, cosmetic): D-labels ordered D1-D2-D3-D7 then D4-D5-D6-D8 (by plane:
  literature then evidence), not numerically. LEFT AS-IS -- deliberate plane ordering; counts correct
  (4+4=8); renumbering would disturb the load-bearing D8 = sole-external-catch reference.

Applied (sha 0f5a4de625716752b3a74a8152f56200c947b4ef401731a062c14b7f8687684e); rebuilt clean (27pp);
4 reflexive gates PASS.

## full-paper consistency read #2 (disjoint Sonnet) (2026-06-19)

Cycle requested as "read the full paper once more for consistency using the paper cycle." Done
DISJOINTLY (Sonnet subagent, full end-to-end read; not the Opus author). Build clean, 4 reflexive
gates PASS, editorial gate PASS on entry (sha bc5afaa7 unchanged from the qualifier-uniformity
cycle). Numerics all reconciled again (corpus 241; lace 37 slots / 36 fns; robust 8+17=25; defects
3+1=4; reflexive 4+4=8, D8 sole external; seeded 5+4+4+2=15; qwen 3/12=25%; A 80/60/40, C 0/11/11);
cross-refs and "by construction"/nesting/capability framing all consistent.

Disjoint Sonnet verdict: INCONSISTENT -- 2 issues, both fixed:
- I1 (Contribution iii, line ~214): the contributions list read "same-provider cross-model casts",
  DROPPING the "same-" (same-model) component that every other occurrence of the identical-error
  finding carries ("same- and same-provider cross-model casts"). FIXED -> "both same- and
  same-provider cross-model casts" (the "both" keeps the list grammar clean against the list's own
  "and").
- I2 (sec:caseD, lines ~902/904): a lone terminology drift -- "(coherent but wrong)" and
  "coherent-but-wrong number" where the paper's load-bearing term is "coherent-and-wrong"
  (used 40+ times). FIXED both to "coherent-and-wrong".

Applied (sha c98fac637599d204a97b7025a99037ce270b906ecadb0dd7fa3a64d6f1cbe8a9); rebuilt clean (27pp);
4 reflexive gates PASS; residual greps for "coherent-but-wrong" and bare "same- and cross-model"
both empty.

## "same-provider" qualifier made uniform (disjoint Sonnet) (2026-06-19)

User directive: make the "same-provider" qualifier consistent everywhere it appears. The prior
consistency cycle had scoped only the abstract + conclusion; the qualifier still appeared in three
forms across the paper: adjectival "same-provider cross-model casts" (abstract/intro/conclusion),
and the fuller clause "within one provider family" / "within the family" in the discussion sections
(Sec 3.4, Sec 6, Sec 7/eval, Sec 10) -- with the identical-error NOUN PHRASE itself still reading
bare "same- and cross-model casts" at those four discussion sites (and at Sec 3.4 the scope clause
TRAILED the claim, so it read unscoped first).

Standardized on the adjectival form fused into the noun phrase at EVERY identical-error claim site:
"same- and same-provider cross-model casts" (plain, not \emph -- emphasis stays on "identically").
Dropped the \emph from the abstract/conclusion adjective (was "\emph{same-provider}") to match the
plain intro form. At the four discussion sites, fused "same-provider" into the noun phrase and
removed the now-redundant adjacent scope clause where one existed (Sec 7 dropped "\emph{within one
provider family}"; Sec 10 dropped the leading "within one provider family," keeping the load-bearing
"that measurement is itself within one provider family" in the next sentence). The genuine
cross-provider Qwen corroboration stays labelled "cross-provider" everywhere (verified not
over-corrected).

Disjoint Sonnet verification (two passes): pass 1 found NOT UNIFORM (4 discussion sites bare) ->
all four fused. Pass 2 confirmed every claim's noun phrase now carries "same-provider", Qwen still
"cross-provider", no over-correction; flagged two MARGINAL residues -- (1) Sec 3.4 mild double-scope
("same-provider ..." + "in the one provider family we could test") -> TRIMMED to "in the only family
we could test"; (2) the conclusion noun phrase carries "same-provider" but no extra prose scope
clause -> LEFT AS-IS by editorial judgment (the noun-phrase qualifier IS the scope signal; stacking
a second clause onto a summary callback would over-qualify, and the earlier defect -- conclusion
lacking ANY qualifier -- is fixed). Applied (sha
bc5afaa750f926b50200b811fa32457543e474b9c595b9398a5ee7105fef1e41); rebuilt clean (27pp); 4 reflexive
gates PASS.

## full-paper consistency read (disjoint Sonnet) (2026-06-19)

Cycle requested as "read the full paper once more for consistency using the paper cycle." No new
edit directive -- a whole-document internal-consistency pass, done DISJOINTLY (a Sonnet subagent
read the full manuscript end to end, not the Opus author). Build clean, 4 reflexive gates PASS,
editorial gate PASS on entry (sha 674f3d9f unchanged from the review10 cycle).

Disjoint Sonnet full-read verdict: INCONSISTENT -- 1 genuine issue. Numerics all reconciled
(warm-up 74+8+6+153=241; lace 25+4+2+6=37 slots / 36 fns with ISSUE-4 double-counted; robust
8+17=25; defects 3 VC + 1 call-graph = 4; reflexive 4 lit + 4 evid = 8, D8 sole external catch;
qwen 3/12=25%); cross-refs, terminology, and the D1/D2/D3 reframing all consistent. The one
issue: the abstract (line ~97) and conclusion (line ~1449) said "same- and cross-model casts
ship identically" WITHOUT the "same-provider / within one provider family" qualifier that the
body (Sec 6) and Limitations (Sec 10) take care to include -- the abstract/conclusion asserting a
broader scope than the data support. FIXED: both now read "same- and \emph{same-provider}
cross-model casts ship identically," matching the convention used elsewhere (cross-PROVIDER =
qwen, called out separately). Applied (sha
5e206e2baa6b145a75990361b6061872e3d12659d7fa80c1f9c1f4ab708f273a); rebuilt clean (27pp); 4
reflexive gates PASS. (Two non-issues noted, not changed: the \ResNTerrains macro name counts
instances not terrains -- prose says "4 instances over 3 archetypes" correctly; the appendix
defect table orders D1-D2-D3-D7-D4-D5-D6-D8 by plane not numerically -- counts correct.)

## review10 cycle + user directives D1/D2/D3 + Gate C (2026-06-19)

Fifth external review (review10.md) plus three author directives that partly OVERRIDE it.
The review's core: the evidentiary structure reads heavier than it is; almost everything
load-bearing collapses to two live findings (the lace faithfulness gate; the §6
underspecification result), the rest being wiring checks the paper itself disowns as efficacy.

DIRECTIVES (override review10 where they conflict):
- D1 (remove the 15/15): the aggregate "15/15 seeded caught / 0/15 barrier-off" headline is
  REMOVED ENTIRELY (not merely demoted). Author: "I do not see the point." Done across the
  abstract, Contribution list, §5.1-§5.5, Table 5 (the "seeded caught" row dropped, replaced by
  a "load-bearing gate" row; caption now "existence demonstrations ... no barrier-on/off
  detection rate"), §9, and §1 Scope. The four seeded instances are now framed only as
  existence/wiring demonstrations that the gate FIRES, with NO detection rate reported anywhere.
- D2 (remove the 10 fabricated proofs): the "10 fabrications caught/reverted" RESULT is removed
  ("it was just to train the skill"). KEPT: the faithfulness-gate MECHANISM (strip annotations,
  require a byte-identical recompile => a fabricated proof cannot survive -- "trustworthy by
  construction"). The \ResRWFabCaught=10 macro was RETIRED (commented out in realworld.tex) to
  prevent future drift. The lace headline now leads with the mechanism + 25 robust / 4 defects,
  with "finding the defects is a result the underlying verifier delivers, not squeeze-specific."
- D3 (nesting CLOSES the Gate-A hole): overrides review10 #5's "nesting doesn't close it."
  Synthesis honoring both: the HARD/executable side is closed "by construction" (mechanical,
  judge-free); the SOFT side's Gate-A hole is closed by NESTING -- each inner coordinator
  squeezed from outside by its monitor -- terminating at a HUMAN / external reviewer as the
  outermost squeeze (D8 = that terminal squeeze working). "By construction" is now scoped to the
  hard side at every appearance (abstract, §1 thesis, §3.3, §10). §3.3 rewritten ("Nesting
  closes the inner loop's Gate~A ... the recursion terminates at a human/external reviewer");
  §10 "single point of judgment" reconciled; both SKILL.md files (sl-monitoring-sl, sl-builder)
  reconciled from "relocates, does not abolish" to "closes by disjoint authority, terminating in
  a human."

Other review10 points applied: #3 "capability-invariant" WEAKENED consistently to "no
improvement with capability across the tiers we ran (one draw per cell, not a measured
invariance)" -- bare word eliminated everywhere (abstract, Contribution iii, §5, §10 x2,
Limitations); #6 a plain statement added in §10 that the distinctive claim over prover-verifier
games rests on the un-run cross-provider replication (where an oracle exists the gate rests on
the executable lower bound regardless).

Disjoint Gate C (sonnet vs opus author): ACCEPT-WITH-FIXES. Verified D1/D2/D3 carried through
consistently (no lingering 15/15, 0/15, or "10 fabrications" result; no "relocates/does not
abolish" residue; "by construction" scoped to the hard side throughout). Caught two item-#3
residues the first pass missed: Contribution (iii) and the Conclusion still stated the
capability result without "not a measured invariance" -- both FIXED. Also flagged the dead
\ResRWFabCaught macro -> retired. Applied (sha
674f3d9f6f99d5f576fdf4e2bb8378902a5b4ff802701279d598bc53ed8436b3); rebuilt clean (27pp); 4
reflexive gates PASS.

## nesting (why squeeze loops are monitored by squeeze loops) + Gate C (2026-06-19)

User point on the review9 un-squeezed-Gate-A fix: the un-squeezed coordinator is precisely WHY a
squeeze loop is nested inside an outer one (SL A/B/C/D monitored by the paper loop; lace's two
nested loops creusot-sl under creusot-monitoring). Extended the Sec 3.3 Gate-A passage: the
soft-side hole is not closed at a single level; the remedy is to NEST -- an outer squeeze whose
monitor holds a disjoint (U,L) pair over the inner loop's coordinator/soft outputs (Gate S
generalized from one skill to the whole loop, the squeeze-monitoring-a-squeeze pattern). Both
applications are built this way: the four A/B/C/D instances squeezed by the outer paper loop
(Sec 8); lace nests creusot-sl inside creusot-monitoring (Sec 4). Honest terminus kept: nesting
pushes the hole up one level, the OUTERMOST coordinator stays un-squeezed, closable only by
external review/human (D8). Also tagged Gate S as "the per-skill case of the nesting just
described".

Disjoint Gate C (sonnet vs opus): **ACCEPT, no fixes.** Verified both nesting examples match their
source sections (Sec 8 lower bound = the 4 instances; Sec 4 = creusot-monitoring drives creusot-sl,
"a loop monitoring a loop, the Gate S pattern"), the terminus does not overclaim (nesting relocates,
does not close, the hole; consistent with Sec 10), Gate S framing consistent, no numeric drift, no
contradiction with the abstract or Contribution (i). Applied (sha
eac4426a20163fc10b8e515ce338d3823d7c8b84e25553af2170b8d40f698dff); rebuilt clean (26pp); 4 reflexive
gates PASS.

## review9 cycle + Gate C (2026-06-19)

Fourth+ external review (review9.md). HEADLINE FIX (the reviewer's #1, an actual coherent-and-wrong
in our own front matter): the "10 fabricated proofs" were MISATTRIBUTED to lace; they were on the
Creusot WARM-UP CORPUS (Creusot's own 241-file test suite), while lace yields 25 robust + 4
defects. Separated cleanly in all four places (abstract, Contribution (ii), Sec 4 opener,
Conclusion): warm-up = 10 fabrications reverted; lace = 25 robust + 4 defects. Also softened
"would likely have shipped" -> "a floor on what a lone verifier would ship" (abstract + Sec 4),
matching the Sec 4.2 floor framing; and glossed "lace" (Canonical's) on first mention.

Supporting points applied: (#2) Sec 3.4 now distinguishes the two jobs -- disjointness removes the
POSSIBILITY of anchoring (structural; only defense where no oracle, Archetype B) vs the executable
oracle CATCHES the residual in measured cases -- "complementary, not competing", reconciling
Contribution (i)'s centerpiece with Sec 6's "the oracle does the catching"; (#3) Sec 2.6 states
plainly that Archetype B is the WEAKEST guarantee (lower bound shares the property author's
provenance -> reduces to author independence, the Fagan/Cleanroom move; novelty is the construction
not a stronger guarantee); (#4) Sec 3.3 surfaces the un-squeezed Gate A (the coordinator's
editorial judgment is the one actor not itself squeezed -- a soft-side structural hole, with D8 as
the demonstrated failure); (#5) Table 5 DROPPED the modeled barrier-off column (3 reviews flagged
it as inviting an efficacy misread) -> shows only measured barrier-on; the load-bearing pilot fact
(in the one real-agent pilot the exerciser caught the defect regardless, so the modeled 0/15
overstates the barrier's effect) promoted to Sec 5.5 main text; (#7) Sec 6 now states the
capability profile is flat-but-not-strictly-monotone ("capability-invariant" = no downward trend,
not identical rates). Presentation #8/#9 (hedge/aphorism density): deliberately not gutted -- this
cycle ADDS load-bearing caveats, so trimming hedges would degrade the honesty the reviewer praised;
noted as a trade-off.

Disjoint Gate C (sonnet vs opus): **ACCEPT, no fixes.** Verified the misattribution fix is complete
in all four locations (10 -> warm-up corpus; lace -> 25 robust + 4 defects; no residual telescoping),
counterfactual softened, the four framing additions accurate and consistent with Contribution (i)
and the artifacts, Table 5 column dropped + pilot fact in main text, non-monotonicity explicit, and
arithmetic intact (warm-up 74+8+6+153=241; lace 25/4/~6/2 over ~36; "two live findings" preserved).
Applied (sha d2d507b77ab569a18a18531c74923fcc83932bff7be84fb1e4fc39cb033b4a8e); rebuilt clean (26pp);
4 reflexive gates PASS.

## cross-provider qwen ladder folded into Sec 6 + Sec 10 + Gate C (2026-06-18)

Ran the A/C/B defect probes through a control-gated qwen ladder (Alibaba; 4B/9B/27B over gens
3.5 and 3.6) to test whether the capability-invariant floor (A) and inversion (C) are
Claude-specific. All four models PASSED the control gate (known-contradiction + known-consistent
+ parseable), so their errors are coherent-and-wrong, not incompetence. Recorded in
verify/reports/live/defect-upperbound-ABC-2026-06-18.md ("Cross-provider qwen capability ladder")
+ qwen-ladder-controls.md + answers_*_qwen*.json; runner eval/live/run_qwen_ladder.py.

Results (error vs oracle): A = 80/67/87/67% (4b/9b/27b-3.5/27b-3.6); C = 11/17/17/33%; B(enriched)
= 12.5/19/19/38%. REPRODUCTION VERDICT: (i) A capability-invariant floor reproduces and is now
provider- AND scale-invariant -- the `active` fork is wrong 3/3 for EVERY qwen size and opus;
survivorship 3/3 for three qwens + opus, 2/3 for the 9B. (ii) C inversion reproduces -- patch-null
(governance-override vs RFC 7396) wrong 2/2 for BOTH 27B qwens (matching sonnet+opus), 1/2 for
9B/4B, 0/2 for haiku: larger/more-capable models more fooled by the authoritative-sounding
override, second provider.

Folded into Sec 6 ("Contradiction, not only silence": both patterns reproduce on the qwen ladder)
and Sec 10 ("Shared priors": the ladder advances the cross-provider replication of the
Knight-Leveson limitation -- floor + inversion reproduce on a second family). Caveats stated: one
second provider family across sizes/generations (NOT many independent providers); qwen errs more
overall (competence gap); one draw per cell; control-gated.

Disjoint Gate C (sonnet vs opus): ACCEPT-WITH-FIXES. It RECOMPUTED every per-model number
(A active 3/3 all sizes; survivorship 3/3 except 9B 2/3; C patch-null 2/2 both 27B, 1/2 for
9B/4B), confirmed control-gate 4/4 PASS, caveats present, no overreach, Sec 10 consistent. One
MODERATE fix: Sec 6 "while sparing the smallest" overstated (the 4B is 1/2 on patch-null, not 0/2;
only haiku is 0/2) -> changed to "more than the smaller ones (1/2 for the 9B and 4B)". Applied
(sha 307a55542a92f3169cf80356898bdf2adb435a9b95aab868bd9827e73d82ff7e); rebuilt clean (26pp); 4
reflexive gates PASS.

## defect-based authority-vs-authority result folded into Sec 6 + Sec 9 + Gate C (2026-06-18)

New live result folded in (user direction). Background: the "near-zero error rate" reviewer
concern was that on thin/well-specified tasks capable models don't err. We rebuilt the A
(analytics) and C (API) upper bounds as genuine SOFT truths carrying DEFECTS -- authority-vs-
authority contradictions (A: ASC 606 net vs a finance directive=gross; GA4 active-user vs a
product-council directive excluding logins; point-in-time vs GDPR Art.17 erasure. C: RFC 7396
null-deletes vs a Zalando "governance override" that ignores null). Ran them with CLAUDE
SUBAGENTS as weak/mid/strong tiers (haiku/sonnet/opus; one draw per case; logged, not gated),
oracle = executable lower bound (metrics.py / reference_server). Results (recorded in
verify/reports/live/defect-upperbound-ABC-2026-06-18.md + answers_*.json, scored by
eval/live/subagent_eval.py):
- A: 12/15=80%, 9/15=60%, 6/15=40% -- opus retains a 40% capability-INVARIANT floor on the two
  forks where both authorities are legitimate (active=self-defined; survivorship=GDPR).
- C: 0/18=0%, 2/18=11%, 2/18=11% -- capability-INVERTING: haiku trusts the RFC and is right;
  sonnet+opus defer to the "governance override" and are wrong (the patch-null fork).
A methodological fix en route: A v2 had a PROMPT LEAK ("the value the executable definition
intends" telegraphed the oracle) -> neutralized to "resolve the conflict and report the figure
you would"; C had a predict-the-server framing + authority-annotated options -> reframed to
implementer-commit + bare options, so A and C are measured identically.

Folded into Sec 6 (retitled "Underspecification and Contradiction"; scoped the old "three
surfaces vanish" to THIN specs; new para "Contradiction, not only silence") and Sec 9 (new para
"A comparative baseline on defective soft specs"). Numbers in prose (logged-not-gated, like the
existing Sec 6 live numbers), with caveats: constructed defects, one draw per tier, existence
demonstration not a real-world frequency, powered version future work.

Disjoint web/exec-enabled Gate C (sonnet vs opus author): **ACCEPT**, no fixes required. It
RECOMPUTED every number with the scorer (A 12/15,9/15,6/15; opus floor = active(3)+survivor(3);
C 0/18,2/18,2/18; patch-null capability-inversion), confirmed the named authority pairs match
the probe system texts, confirmed all honesty caveats present with no overreach, and confirmed
consistency with the abstract ("two live findings" intact; "near-zero on well-specified" not
contradicted; "three surfaces vanish" now scoped to thin specs). One cosmetic precision note
(name Zalando alongside "governance override") -> applied. sha
d7e0deaf74a9f81b04411895171c95eb61ceb62e0291416c723d1fb6b71e310f; rebuilt clean (25pp); 4
reflexive gates PASS.

## bibliography-venues + drop "working draft" cycle + Gate C (2026-06-18)

Literature-plane cycle: convert arXiv-preprint citations to their peer-reviewed venues, and
remove the title-page "working draft" mention. A lit-agent (WebSearch/WebFetch) verified each
of the 28 arXiv-preprint entries against authoritative sources (DBLP first, then
proceedings/OpenReview/ACL Anthology/Springer/PMLR), updating 20 to their venues and KEEPING 8
as arXiv (no peer-reviewed version exists): bai2022constitutional, amodei2016concrete,
manheim2018goodhart, irving2018debate, bowman2022scalable, ridnik2024alphacodium, anil2021pvg,
kirchner2024pvg. Every bibkey preserved (manuscript \cite's them); every arXiv id preserved as
note=. `\date` -> "June 2026" (no "working draft"); the only remaining "DRAFT" tokens are the
\code{DRAFT} status-handshake states (legitimate mechanics).

Disjoint Gate C (sonnet, WEB-enabled, vs opus author): **ACCEPT**, no misattributions. It
independently re-derived the riskiest not-yet-DBLP-indexed venues -- wu2023autogen=COLM 2024
(OpenReview BAakY1hNKS), cemri2025why=NeurIPS 2025 D&B Track, sun2023clover=SAIV 2024 (LNCS
14846, pp.134-155, DOI 10.1007/978-3-031-65112-0_7), zheng2023judging + yang2024sweagent at
NeurIPS -- plus spot-checks (yao2022react=ICLR2023, hong2023metagpt=ICLR2024 oral,
du2023debate=ICML2024, qian2023chatdev=ACL2024 pp.15174-15186, burns2023weak=ICML2024,
jimenez2023swebench=ICLR2024), and confirmed all 8 arXiv-only entries genuinely lack a venue
(anil2021pvg and kirchner2024pvg are submitted-but-unpublished; not conflated with related
papers). Build clean (25pp; 0 undefined citations); 4 reflexive gates PASS. sha
a8b0eb36b02d622ace62fd2a7a595b2143d4e092ae11cfd065027f1ecfe031d8.

## review8 cycle + Gate C (2026-06-18)

Fourth external review (review8.md). User chose: attempt the real cross-provider run (#3),
aggressive -15-20% restructure (#7), add a compact appendix (#8).

NEW EXPERIMENT (#3, the headline): wired an Ollama backend into eval/live/model_client.py and
ran a genuinely cross-provider cast on instance B (refund) -- qwen3.6:27b-mlx (Alibaba) on the
remote host, same balanced 12-case gap pool (seed 7) as the within-family study. Result
(frozen in verify/reports/live/report-B-crossprovider-2026-06-18.md + transcripts): qwen errs
3/12 = 25% (stable 9/36 over 3 reps at temp 0), SHARES the blind spot on the pure
unstated-default cases (DELIVERED-default, REFUNDED/AUTHORITY) that every Claude tier also
missed, but PARTIALLY decorrelates -- fixes IN_TRANSIT/AUTHORITY (right where Claude escalated)
and newly caves on NEW_HIGH/URGENT. Honest, nuanced: corroborates the surface is not
Anthropic-specific AND gives direct evidence for the §10 caveat that within-family measurement
overstates cross-provider correlation. Integrated into §6, §3.4, §10; the old §10 "framing
probe" parenthetical (review8 flagged it as gesturing at evidence it isn't) was REPLACED by
this real experiment.

OTHER review8 points applied: #1 grounded the UEFI counterfactual in the measured production
count (10 fabrications produced-then-reverted; fresh lone-agent ablation noted as not-run, no
toolchain) -> stated as a floor not a rate; #2 Table 5 header relabels barrier-off as
\emph{modeled}; #4 §4.2 lace disposition now reconciles (25 robust + 4 defect + ~6 blocked + 2
partial over ~36 distinct functions, recursion/blocked overlap named; firm counts exact,
blocked marked ~ per its artifact); #5 §6 named "latent-underspecification surfacing", not the
correctness story; #6 abstract claims "only" contextual producibility, catchability = design
aspiration; #8 NEW Appendix A enumerates the 8 caught defects (D1-D8 from
verify/manuscript_defects.tsv) as claim->correction, making §8 falsifiable; novelty (§2.6) now
leads with disjoint authority PAIRS vs the binary author/inspector split; McNemar marked
vacuous. #7 aggressive compression: two density-pass subagents (one over the body, one hard on
§9 + §2.5) -- §9's three mechanism-demo paragraphs (level-up / caught-then-consolidate / Gate~S)
merged to one, dropping 17 illustrative §9 macros (still defined, unused); 26pp -> 24pp,
preserving all 65 cites, 86 distinct macros, 35 labels.

Fresh model-disjoint Gate C (sonnet vs opus author), given the raw cross-provider transcripts +
artifacts. **ACCEPT-WITH-FIXES.** Verified the cross-provider claims part-by-part against the
transcripts (3/12, stable; shared cases 10/11; decorrelation cases 5/1 -- all accurate), the
lace arithmetic reconciles, the appendix matches the TSV (4 lit + 4 evid, D8 external), the
load-bearing numbers survived compression, abstract<->C2 align, §6 framing clean. Two FIXES
applied: [MED] §6+§10 "same rate as the Anthropic casts" -> "same 25% rate as haiku and opus
(Sonnet ran higher at 33%)"; [LOW] §4.2/§4.3 "6 blocked" -> "~6" with reason (source uses ~6;
false precision avoided). The self_contained gate also caught the density pass silently dropping
the Gate~A forward-\ref{sec:mechanics} signpost -> restored. Applied (sha
17e733c15d799c2dc8aec542be01258a4eb557cff44e0af35c945e74889263b1); rebuilt clean (24pp); 4
reflexive gates PASS; cross-provider framing judge (qwen3.6:27b-mlx) re-confirmed AUTHORITATIVE
(both controls OK, live probe CONSISTENT). Could-not-run: the fresh UEFI lone-agent ablation
(#1, no Creusot toolchain) and a powered multi-provider replication remain future work.

## §10 cross-provider fix + Gate C (2026-06-18)

The standing review's cross-provider judge is now AUTHORITATIVE (qwen3.6:27b-mlx; see header),
so the paper's "(we lack a capable cross-provider judge)" in Sec 10 was stale. Fixed Sec 10
"Shared priors" + the Sec 9 "infrastructure we did not have" list to distinguish the two senses:
the cross-provider EXPERIMENT replication (re-running the underspecification instance across
genuinely independent providers) remains future work; the cross-provider EDITORIAL judge now
exists (a narrow framing-consistency probe that passed its controls, recorded in
cross_provider_review.md). All four cross-provider mentions (Sec 3.4, Sec 9, Sec 10 x2) are now
mutually consistent; the old "we lack a capable judge" phrasing is gone.

Fresh model-disjoint Gate C (sonnet), given the real cross-provider-judge fact:
ACCEPT-WITH-FIXES. It confirmed all four mentions consistent and the experiment/editorial
distinction correctly drawn; flagged [HIGH] that "a reflexive check that concurs" overclaimed a
narrow 3-probe check -> tightened to "reviewed this paper's framing on three consistency probes
and passed them all --- a narrow check, not a full review, and not a re-run of the casts."
Applied (sha df52f701883a634892abfec1c607b1352a0fcc48da96b3926313a3ae68351d2e); rebuilt clean (25pp); 4 reflexive gates PASS.

## manifesto citation cycle + Gate C (2026-06-18)

Bounded cycle: cite the "Applicable Formal Methods" manifesto (Gleirscher, van de Pol,
Woodcock, SoSyM 2023; arXiv:2112.12758) in Sec 2.6 and map the paper's evaluation to its
Evaluation + case-study principles, making the partial conformance explicit. Added a positioning
paragraph + the bib entry. Fresh model-disjoint Gate C (sonnet) on the new passage, with the
manifesto's principle text supplied for faithfulness checking: **ACCEPT-WITH-FIXES**; the cited
principles are faithfully characterized and the partial-conformance concession honest. Two fixes
applied:
- [HIGH] the "re-runnable harnesses and artifacts" parenthetical bundled Sec 9 (a mostly-null
  protocol proposal, not completed runnable evidence) -> rescoped to Sec 4 (lace) + the four
  instance sections (sec:caseD--caseG), dropping sec:eval from that claim.
- [MED] case-study conflation -> distinguished: the lace application is a "case study" in the
  manifesto's sense; the four seeded instances are "existence demonstrations" (intensive but
  constructed), matching the term the paper uses elsewhere.
All applied (sha b438df50fc5d87107d6b3d637246b1c853d94b9492145db2f55087ab08c3d963); rebuilt clean (25pp); 4 reflexive gates PASS. The authoritative
cross-provider judge (qwen3.6:27b-mlx) re-confirmed the framing CONSISTENT on the updated paper.

## review7 cycle + Gate C (2026-06-18)

Third external review (review7.md), honesty-focused; much overlapped review5/6. Applied (one
commit, "review7 cycle"): #1 dagger-flagged Table 5's barrier-off column as modeled-not-measured
+ cut the coupling row (#8); #2 LED the abstract/contribution (ii)/Sec 4 with the faithfulness
gate (10 fabricated proofs reverted) and demoted the 4 bugs to a verifier-surfaced bonus; #3 Sec
6 "surfaces a latent divergence" not "the model errs" (+ dropped "production discrepancy");
#4 named the Archetype-B archive author + its residual dependence (Sec 5.2); #5 softened the
Knight-Leveson claim to within-one-provider-family in Sec 3.4 + Sec 6; #6 stated hard=structural
/ soft=procedural(Gate A) once in the scope para; #9 consolidated a Sec 9 paragraph to a pointer;
#10 contributions 8 -> 4 + "we also provide"; #11 reframed Sec 7 stabilizers as "operational
lore, not theorems"; minor Rocq=Coq footnote, abstract reproducibility caveat, conclusion n=1
modesty. (#7 "(100%)" already gone from the review6 compression.) Could-not-run items (#3
multi-provider experiment, #7 run SWE-bench) remain out of reach.

Fresh model-disjoint Gate C (sonnet vs opus author). **ACCEPT-WITH-FIXES**; confirmed the UEFI
reframe is consistent across abstract/contribution/Sec 4, the Table 5 dagger accurate, numbers
intact (ResRWFabCaught=10, ResRWBugsNum=4, barrier-off all 0). Two HIGH artifacts FIXED -- the
reframe had not propagated to (a) the Sec 4 title ("Finding Bugs ..." -> "Trustworthy Proofs
(and Real Bugs) ...") or (b) the conclusion (still led with the 4 bugs -> now leads with the
faithfulness gate, bugs as bonus); + MED Table 5 footnote made precise ("the exerciser tested
the spec, not the code" rather than "no difference"). MED on Sec 3.4 was a mislabel (the cited
passage is the Sec 2.5 inherited-limitation statement, already cautious). All applied (sha 743f2bb32cf2fa3e09c2de66aeaecf92597fd24509790fce1b0a694f556069db);
rebuilt clean (24pp); 4 reflexive gates PASS.

## review6 cycle + Gate C (2026-06-18)

Second large external review (review6.md). Overlapped review5 (already applied) but pushed
further. Stage A (concrete, committed): #2 UEFI counterfactual (faithfulness gate / 10
reverted fabrications is the squeeze-specific value vs "just Creusot"); #6 same-provider as a
first-order Knight-Leveson threat; #10 C2 scoped to a design aspiration; #11 "lower bound can
be coherent-and-wrong"; #12 model-family/dates reproducibility note; #13 crisp
disjointness-of-evidence opener in Sec 3. Stage B (structural, committed): #8 compressed Sec 8
to two paragraphs + CUT Appendix A + removed generativity/strange-loop from the body (8
reflexive scripts reclassified described->internal); #1 compressed the four seeded-instance
subsections (~36%); #9 reframed as "protocol sketch, not run" (cut the IOU lists) + #5
Monte-Carlo to one line; #4 dropped bigram precise % from prose. Could NOT run: the
multi-provider underspecification experiment (#3) or SWE-bench (#7) -- no keys/Docker/endpoint;
handled #7 by reframing rather than promising. Length 28 -> 24 pp.

Fresh model-disjoint Gate C (sonnet vs opus author). **ACCEPT-WITH-FIXES**; confirmed the cuts
are clean (no dangling generativity/strange-loop/Appendix refs; numbers consistent with
artifacts: UEFI 4/5/25 + 10 fabrications, 15/15, reflexive 8+1). Revision artifacts found and
FIXED:
- [HIGH] the post-(C1-C4) Remark asserted a universal "cannot propagate silently" guarantee
  that contradicted the newly-scoped C2 -> scoped it to the failure classes C2 covers.
- [HIGH] the hard/soft-truth Remark still introduced "reflexive Gate C / reflexive Gate S"
  terminology (orphaned when Appendix A was cut) -> deleted the sentence.
- [MED] UEFI counterfactual "would have shipped" -> "would likely have shipped" (it is an
  inference, not a measurement).
- [MED] Sec 9 "efficacy evidence ... of two kinds" inflated the reflexive n=1 -> reframed as
  "one live result and one reflexive illustration".
- [MED] removed 7 now-dead macro-file preamble loads (strangeloop/selfmodel/closure/etc.).
- [LOW] scope paragraph: "N executable instances" -> "... over N terrain archetypes".
All applied (sha 128f306119f432bf35cdba7d6b35a969b99386c285d8948b5873305328abce48); rebuilt clean (24pp); all 4 reflexive gates PASS.

Post-Gate-C consistency read (2026-06-18, full 24-page re-read): mechanical scans clean (no
doubled words, no sentence-initial macros, no dangling generativity/strange-loop/Appendix
refs; references renumbered 1-48, the dropped Hofstadter cite leaving no dangling ref). One
minor cross-ref fixed: Sec 3.4 said "Section 10 measures ..." for the cross-model /
Knight-Leveson result, but that measurement is reported in Sec 6 (the Sec 3 opener already
said "Section 6 measures"); repointed Sec 3.4 to sec:underspec. No claim/number changed;
verdict carries forward (sha f631e80f).

## review5 cycle, Stage 2 + Gate C (2026-06-18)

Large revision incorporating review5.md. Stage 1 (committed earlier): framing restructure
(consolidate hedging into one Scope paragraph; demote generativity/strange-loop out of
abstract/contributions/conclusion; state the guarantee at true precision -- contextual
producibility, not correlated error; disjointness-OF-EVIDENCE not model weights; worked
example; glossary; eval labelled a proposal). Stage 2 (this entry):
- #3 full reorder: UEFI moved up to Section 4 (ahead of the seeded archetypes); instance-B's
  underspecification extracted to a new Section 6 "A Live-Model Failure Mode".
- #5 full density pass over ALL sections (per-section copy-edit subagents, sonnet): shortened
  sentences, capped em-dashes. Verified preservation: citations 70, \Res macros 187, \code 67
  all unchanged across the pass; build clean; all four reflexive gates PASS.
- gate-letter clash: disambiguated the meta-gates by the "reflexive Gate X" qualifier
  (reflexive Gate C in the closure figure) + updated the disambiguating remark, rather than a
  risky rename of the core A/B/C/S.

Fresh model-disjoint Gate C (claude-sonnet-4-6 vs claude-opus-4-8) on the fully revised
manuscript. **ACCEPT-WITH-FIXES.** It confirmed NO claim drift from the density rewrite (5
load-bearing spot-checks all pass: UEFI 4/5/25, 15/15 seeded, reflexive 8+1, underspecification,
barrier-off-as-model) and a coherent reorder. Revision artifacts found and FIXED:
- [HIGH] conclusion's "controlled comparison still owed" ref pointed to sec:realworld (the UEFI
  section itself) -> sec:eval.
- [HIGH] conclusion omitted the second live finding (underspecification) the abstract promises
  -> added a sentence pointing to sec:underspec.
- [MED] limitations dropped the "same-provider" scope on the Knight-Leveson consensus claim ->
  "within one provider family, same- and cross-model casts ...".
- [MED] intro pointed only to sec:eval for the underspecification finding -> also points to the
  new sec:underspec.
- [LOW] abstract "in its own draft" -> "in its own claims" (matches the body).
All applied (sha 57abee40); rebuilt clean; gates PASS. (refs 120 -> 122: two new cross-refs to
sec:underspec, intentional.)

Post-Gate-C consistency read (2026-06-18, full 28-page re-read): found three sentence-initial
numerals introduced by the density pass (a sentence split just before a \Res macro, beginning
"4 of ..."/"3 of ..." in Sec 8 + Appendix A) -- fixed by colon / "of which" rewrites. Same
typo class as prior cycles; no claim/number/framing changed, so the ACCEPT-WITH-FIXES verdict
carries forward (sha 2816697e). All reflexive gates + build re-confirmed.

## Fresh disjoint pass (2026-06-17) -- re-review of carried-forward edits

The prior verdict (below) was carried forward through three edit rounds (MED reconciliation,
exploratory tag, "process caught" reframing) that no judge had actually re-read. Ran a fresh
model-disjoint pass (claude-sonnet-4-6 vs claude-opus-4-8 author) on the current manuscript.
**ACCEPT-WITH-FIXES.** It confirmed the carried-forward edits are sound and internally
consistent, and found two residual framing inconsistencies + one clarity gap:

- [MED] contribution (vi) still said "this paper's own GATES caught coherent-and-wrong
  defects" while abstract/Sec 6/Sec 7 had all moved to "PROCESS caught (1 only by external
  review)" -- the one spot the previous cycle's uniform-reframe missed (it was judged a
  "general uncounted statement" and left; the fresh judge correctly flagged it as the lone
  inconsistent occurrence). FIXED: "gates" -> "process".
- [MED] abstract said "cross-model casts do not catch" -- could be misread as a CROSS-PROVIDER
  result, whereas the probe was within one provider family (Sec 7 + Limitations make the
  shared-pretraining point). FIXED: "(an exploratory probe), ... \emph{same-provider}
  cross-model casts do not catch" (provider scope moved inline onto the casts, removing the
  redundant parenthetical "one provider family").
- [LOW] "applied unchanged" (Sec 5 intro) sat unreconciled with "two specializations" (Sec
  5.1). FIXED: Sec 5.1 now says "'Applied unchanged' means the loop topology and the squeeze
  are unchanged; the gate materials are rebuilt per terrain, as Sec 4 prescribes".
- [LOW, NOT APPLIED] abstract "every number regenerated by a harness" could be over-read to
  cover the (transcribed) Sec 5 numbers. Left as-is: it is grammatically bound to "each [of
  the four] instances"; the Sec 5 numbers appear in later sentences and are not claimed
  harness-generated. Noted, no change.

Weakest point (judge): the barrier's empirical effect on real agent behavior is undemonstrated
beyond one exploratory probe on one instance (the lace case study is the only non-seeded
positive evidence); honestly acknowledged, defensible at the paper's stated methods-paper
scope. All must-fix items applied (sha e8bf56d3). Verdict ACCEPT-WITH-FIXES.

## Real-world cycle (2026-06-17) -- Section 5 (lace UEFI) added; full disjoint re-review

The paper changed substantially since circle 127 (new Section 5 "A Real-World Application",
macros/realworld.tex, Creusot citation, conclusion + abstract integration, two
sentence-initial-macro typo fixes), so the standing review went STALE (editorial_gate.py
flagged recorded sha != current). Re-ran the disjoint Gate A on the new manuscript.

Two passes, increasing disjointness:
- Pre-pass (context-disjoint, author-model): caught the bug-count framing -- the artifacts
  describe FIVE distinct hazards filed as FOUR issues (ISSUE-2 = div-by-zero + u32 mul
  overflow), while the paper said "four defects" everywhere. FIXED in Sec 5.2: "four ...
  (five distinct hazards, the PE section-alignment site carrying two)".
- Authoritative pass (model-disjoint: judge claude-sonnet-4-6, author claude-opus-4-8):
  **ACCEPT-WITH-FIXES**. Findings and disposition:
  - [HIGH] cross-section inconsistency: scope para said "one model" while the eval (Sec 7)
    says "one provider family" (weak->strong tier gradient + cross-model casts) for the same
    exploratory comparison. FIXED: scope para -> "one provider family".
  - [HIGH] abstract over-credited the internal gates: "this paper's gates caught 8 such
    defects" with no qualifier, while Sec 7 + appendix record ResCalibExternalCatches=1 caught
    only by external review -- ironically the self-overcredit this paper warns against. FIXED:
    abstract -> "... in its own draft (1 only by external review)", matching Sec 7's phrasing.
  - [LOW] "annotator" used in Sec 5.1 is the implementer role instantiated on this terrain but
    not in the cast table. FIXED: added "(Table~\ref{tab:cast})".
  - [MED, RECONCILED] Sec 6 prose said external challenge happened "in at least two
    instances" while the macro counts 1 "external review" -- a challenge-vs-review accounting
    gap. FIXED: the two are distinct mechanisms and the prose now says so -- the
    execution-environment reality check is reframed as "the executable lower bound refuting a
    claim, the squeeze's own mechanism rather than a reviewer", and only the peer-review
    figure-caption catch is the "single defect (1 of 8) ... only external review caught",
    matching ResCalibExternalCatches=1 across the abstract, Sec 7, and the appendix. No
    re-count of the macro; the prose now distinguishes lower-bound catches from external
    review. (Small change implementing this review's own finding; verdict carries forward.)
  - [LOW, APPLIED] abstract cross-model finding ("cross-model casts do not catch") not tagged
    "exploratory". FIXED: added "(an exploratory probe, one provider family)" after "On a live
    model", matching the eval's "Exploratory (... one provider family)" scoping.
  Weakest point (judge): under-evidence, not overclaim -- no powered efficacy comparison
  exists (pilots null, p=1.000), so the payoff rests on a structural guarantee + existence
  demonstrations. The paper defends this honestly and explicitly; a venue may still reject on
  empirical payoff, but cannot charge dishonesty.

Verdict recorded ACCEPT-WITH-FIXES; ALL findings now applied (the MED challenge-vs-review gap
reconciled, sha e44c435b; the last [LOW] exploratory-tag applied, sha 73b270a7; then the
"gates caught 8" phrasing refined to "process caught" -- sharpening the [HIGH] honesty fix and
resolving an internal Sec 6 tension the MED reconciliation introduced (Sec 6 line 1200 "the
gates caught 8" contradicted the new "1 of 8 our own gates missed"). Applied uniformly:
abstract + Sec 6 -> "the process caught", Sec 7 -> "caught before submission", each keeping
"(1 only by external review)". Line 197 (contribution vi) left as a general uncounted statement.
sha b865c296). Nothing from this review remains open. Cross-provider gold standard still
pending a key (see below).

## Circle 127 -- fix two PDF margin overflows + Markdown flowchart in paper-impl.md

User reported seeing something off in the PDF (screenshot did not transmit). Proactive
inspection found two real margin-overflow defects, both fixed:
- the per-item pipeline TikZ figure (fig:pipeline) was 14pt wider than the text block (the
  probe + right-side arrow pushed the bounding box into the margin) -> narrowed the boxes and
  side extents; the divergence label's "(N:=N+1)" was briefly dropped in the narrowing and
  restored (fidelity);
- the Protocol-status line had an unbreakable \texttt path (verify/eval_protocol.py) jutting
  31pt into the margin -> \allowbreak after the slash + \emergencystretch=4.5em globally.
apparatus_described.py's path extractor was made robust to typographic break hints
(\allowbreak/whitespace) so the gate still recognises the script. Remaining overfulls are
<=7pt (a pre-existing table cell).
Also (review4 Markdown-flowchart option): converted the per-item pipeline ASCII in
paper-impl.md to a Mermaid flowchart (renders on GitHub etc.).

Disjoint pass: ACCEPT, findings none (changes strictly typographic; all eight pipeline
stages, both loop-backs, "positives pass", and "(N:=N+1)" intact).

## Circle 126 -- convert both ASCII figures to TikZ vector flowcharts (review4 minor)

review4.md minor: convert the ASCII diagrams to clean vector graphics for scannability.
Converted Figure~1 (per-item pipeline, fig:pipeline) and the reflexive-cycle figure
(fig:closure) from verbatim ASCII to TikZ. Added \usetikzlibrary{arrows.meta,positioning}.

Pass 1 (sha 052ff1c7...): ACCEPT-WITH-FIXES. The disjoint pass caught two fidelity losses in
my pipeline conversion (I over-simplified): (1) the probe's distinct PRE-spec loop-back to the
coordinator was collapsed into a parenthetical and merged with the Gate B divergence arrow;
(2) "positives pass" was dropped from Gate B. (The closure figure was faithful.) FIXED: probe
restored as a distinct left side-branch with its own dashed loop-back; "positives pass"
restored; Gate B divergence kept as a separate right-side loop-back.

Pass 2 (sha 5e9ffe1a..., this record): ACCEPT, findings none -- all eight pipeline stages,
both loop-backs, and the four-node closure cycle faithful to the original ASCII.

## Circle 125 -- incorporate review4.md feedback

review4.md (external review): three refinement asks + minors. Triage and action:
- Point 2 (keep strange-loop out of the SE-grounded body): already satisfied -- zero
  Hofstadter/philosophical terms in Sections 1-5 (R9 + circle 124). No edit.
- Point 3 (quantify efficiency overhead H4): no token/latency telemetry exists, so a measured
  multiplier table would be fabrication. Instead added the STRUCTURAL per-item overhead (fixed
  by the cast: coordinator + implementer + exerciser + gates + documents = a small constant
  multiple of a single-agent pass) and explicitly deferred the token/wall-clock numbers to
  uninstrumented telemetry / H4. No fabricated numbers.
- Point 1 (finish SWE-bench): cannot run in-sandbox (infra-blocked). Sharpened the blocker to
  answer the reviewer's closing question concretely -- the minimum infrastructure is the
  per-repo Docker images that build+test each project and a patch-generating model endpoint.
- Minors: Section-1 multi-citations already render uniformly (natbib sort&compress, spaced);
  Figure 1 ASCII kept deliberately (byte-reproducible artifact). No change.

Disjoint pass: ACCEPT, findings none (verified the structural-overhead claim is a design fact
not a measured number, and the SWE-bench edit does not imply the study was run).

## Circle 124 -- reflexive appendix trimmed (over-elevation course-correction)

Gate-A judgment found the reflexive material (App. A 143 + body 62 = 205 lines) had grown to
rival the core strategy section -- the self-indulgence risk review3 #7 named. Trimmed App. A
~143 -> ~96 lines: compressed the generativity paragraph (self-model + level-crossing detail
and the feedback/quine controls moved to paper-impl.md; self_model_check.py reclassified
internal in the apparatus manifest) and the flag-rate longitudinal-log detail. The
apparatus_described gate confirmed the reclassification is consistent (no code-vs-prose drift).

The disjoint pass then caught two follow-on inconsistencies from the trim: (1) the strange-loop
"exhibited but not met" clause implied in-paper exhibition of the self-model, now moved out ->
fixed to locate each condition (category-generation "above", self-model in paper-impl.md); (2)
the body's "discharge status" promise over-stated in-appendix content -> narrowed. Final
disjoint pass: ACCEPT, findings none.

## Circle 122 -- §reflexive apparatus updated to match the gates built in 119-121

The Gate-A editorial pass found the manuscript's self-description had gone stale: it described
a 4-member reflexive-monitor family and framed the disjoint reviewer as a limit it "cannot
engineer away", while circles 119-121 had actually added the claim-consistency gate, the
standing editorial gate, and the cross-provider judge. The §reflexive apparatus paragraph was
rewritten to (a) add the claim-consistency monitor to the family, (b) reframe the limit as
"mechanize the bookkeeping, cannot eliminate the disjoint judge" with the standing editorial
gate + cross-provider judge named, carrying the partial-disjoint / non-authoritative caveats,
and (c) fold in the word-order catch as the latest reminder.

- Pass 1 (sha 585e8107...): ACCEPT-WITH-FIXES. (1) "(R3)" leaked the internal roadmap label
  into the manuscript -- undefined to a reader (a self-containment miss the term registry did
  not cover). FIXED: replaced with an inline reference to the cross-model casts of the eval
  section. (2) count mismatch -- the family lists 5 members but flag-rate calibration covers 3
  planes, unexplained. FIXED: planes marked "rate-producing"; an explicit clause notes the
  perturbation gate and consistency linter are pass/fail, outside the count.
- Pass 2 (sha 63d6e7df..., this record): ACCEPT, findings none.

## Circle 120 -- abstract halved (~43 -> 23 lines), short high-impact sentences

The abstract was compressed to roughly half length. Compression is exactly where overclaim
and dropped caveats creep in, so the disjoint Gate A was re-run on the new abstract:

1. Pass A (sha 244c1915...): ACCEPT-WITH-FIXES. Found a compression-induced overclaim --- the
   generativity sentence said "an agent must invent new distinctions to escape" as a general
   claim, dropping the Limitations caveat that generativity is shown for PROGRAMMATIC learners,
   not live models. FIXED: scoped to "shown here for programmatic learners, not yet live
   models" (verbatim match to the Limitations section).

2. Pass B (sha d968e491..., this record): ACCEPT, findings none. The compressed abstract is
   faithful across all checked dimensions --- coherent-and-wrong, disjointness, four instances
   over three terrains, the live instance-B result ("only the executable lower bound does"),
   the reflexive n=1 catch, the two-coordinate-strands framing (no ranking superlative), the
   "existence demonstrations not a benchmark" and "powered study is future work" qualifiers,
   and the now-scoped generativity claim.

## Prior history (circle 119, sha c29ad665...): three framing defects caught + fixed

H2 over-claim in Protocol status -> "partially demonstrated"; contribution (vi)'s "strongest
on real, non-seeded" ranking removed (had ESCAPED claim_consistency on word order -> ledger
gained a reverse-order MAX rule); conclusion's ambiguous "measured it" -> "measured defect
detection". Final pass that circle: ACCEPT.

## Why this gate is necessary (not redundant with claim_consistency.py)

The compression overclaim (Pass A above) is the latest proof: a brand-new framing defect that
no invariant anticipated, caught only by the disjoint judge. `claim_consistency.py` mechanizes
the KNOWN defects (coverage is a floor); this gate covers the residual. Each editorial catch is
then folded back into `claims/framing_invariants.tsv` so it becomes mechanical next time.
