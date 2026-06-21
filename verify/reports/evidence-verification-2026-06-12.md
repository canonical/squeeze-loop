# Evidence-plane verification (Gate C) — 2026-06-12

Sources now archived under `bib/archive/` with `SHA256SUMS`:

- `pycsl-prereqs-impl.md`  sha256 9ec3e509…140f4  (277 lines)
- `happy-roadmap-impl.md`  sha256 e92a5468…2344b  (305 lines)
- `typing-global-impl.md`  sha256 b8c391ba…40ae  (370 lines)

Method: each `\begin{extract}` / `\begin{verbatim}` block in `tex/paper.tex`
re-opened at its claimed anchor in the archived source; verbatim fidelity,
anchor correctness, and surrounding prose claims checked.

## Verbatim blocks

| paper line | anchor claimed | verdict |
|---|---|---|
| 391 extract | pycsl §1 rule 2 | SUPPORTED — verbatim; anchor correct |
| ~402 figure | "adapted from P-series guide" | **UNSUPPORTED→fixed** — fig has Gate C; P-series §4 has only Gates A–B. Caption corrected: Gates A–B from P-series, Gate C from HAPPY/typing |
| 524 extract | pycsl §6 (DoD) | SUPPORTED — verbatim; legitimately truncated before "— the same discipline that closed os" |
| 537 extract | happy §0 | SUPPORTED — verbatim (math rendered to LaTeX); anchor correct |
| 554 extract | happy §4 (Gate C) | SUPPORTED — verbatim from "There, faithfulness…"; anchor correct |
| 584 extract | typing §0 | SUPPORTED — verbatim minus inline (S1)/(S3/S4) codes; anchor correct |
| 599 extract | typing §4 (Gate C) | SUPPORTED — faithful; S5→"conformance subset", S4→"CPython", S3→"the reference" glosses, all defined in body |
| 855 verbatim | pseries-driver-agent (full def) | SUPPORTED — exactly verbatim (line-wrap only) |
| 886 verbatim | happy-threat-agent | **OVERCLAIMED→fixed** — abridged (examples, file paths, milestone list dropped; §9→S9), presented as verbatim. Intro now marks it "(lightly abridged)" |

## Prose claims about the guides (spot-check)

| paper loc | claim | verdict |
|---|---|---|
| §4.1 510 | ACSL binder grammar + \at semantics + internal prereqs spec | SUPPORTED (pycsl §3) |
| §4.1 517 | P-4 "verdict forks the item" quote w/ bracketed subs | SUPPORTED — subs honest ([emitter]=Module 6, [item]=P-4, [implementer]=core-agent) (pycsl §5) |
| §4.2 564 | H-R trap (appended vs immutable); H-S trap (callee vs call-site) | SUPPORTED — verbatim from happy §3 table |
| §4.3 576 | two-plane split; "central sentence is negative" quote; CPython resolves runtime | SUPPORTED (typing §0) |
| §4.3 609 | "no unspecified behaviour" quote; transcription verified by prediction | SUPPORTED (typing §0 + §5 TY0) |
| stab. 6 649 | typing: single monomorphized instantiation end-to-end before machinery | SUPPORTED — verbatim (typing §2 probe-agent) |
| stab. 3 640 | "all three guides end with this sentence" | **F6→fixed** — three *different* closing sentences (same rule). Changed to "close on this rule"; App. B "same sentence"→"same closing rule" |
| §4 472 | three PyCSL engagements; subagents cannot spawn subagents → main thread coordinator | SUPPORTED (all three guides §1) |

## Outcome

- 3 defects fixed in `tex/paper.tex` (figure provenance F2; "same sentence" F6;
  abridged-block honesty). Build green, all refs resolve, no other verified text
  touched.
- All extract quotes confirmed verbatim-faithful at their anchors. Evidence
  plane is sound.
- GP1 (gap-2) closed: sources obtained, archived, hashed.

## Residual

- The archived guides are local working copies, not yet a public/anonymized
  supplement (intersects manuscript TODO line ~143). Decision still open: attach
  as supplementary material or cut the dependency. Coordinator will not decide
  unilaterally.
