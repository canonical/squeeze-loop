# Literature-plane verification report — 2026-06-12

Scope: every `\cite` in `tex/paper.tex`. Each source was located online and the
manuscript's sentence about it judged against what the source actually says.

**Access caveat (honest scope, per §3 key rule).** This pass verified sources
at **abstract + key-section level** (arXiv abstract pages, HTML/ar5iv mirrors,
and authoritative secondary descriptions for paywalled classics). It is **not**
the §3 `read: FULL` reading-record standard — no full PDFs were archived under
`bib/archive/` with SHA-256 hashes. Treat every verdict below as
"abstract-corroborated"; promoting a `\cite` to camera-ready requires the
full-text reading record. Two verdicts that turn on body content
(CRITIC's tool-vs-intrinsic ablation; CAI's two-phase critic identity) are
flagged as such.

## Verdict table

| bibkey | manuscript claim (gist) | verdict | note |
|---|---|---|---|
| yao2022react | observations feed back; external feedback | SUPPORTED | |
| wang2023voyager | iterates skills vs embodied env | SUPPORTED | |
| madaan2023selfrefine | loop closed by model's own critique | SUPPORTED | |
| shinn2023reflexion | self-critique, optionally test-grounded | SUPPORTED | "optionally" hedge correct |
| bai2022constitutional | critiques vs normative doc; shared weights | SUPPORTED→tightened | shared-weights true only of self-critique stage; qualified in text |
| gou2023critic | external-tool critique > intrinsic | **OVERCLAIMED→fixed** | F3-a; see gap-1 |
| lightman2023verify | process supervision: outcomes→steps | SUPPORTED | |
| huang2023cannot | no self-correct w/o external; can degrade | SUPPORTED | both halves verbatim in abstract |
| panickssery2024llm | linear corr. self-recognition↔self-preference | SUPPORTED | "linear correlation" is the paper's own word; established via fine-tuning |
| zheng2023judging | position + verbosity biases | SUPPORTED | abstract lists position, verbosity, self-enhancement |
| sharma2023sycophancy | yields to user position over evidence | SUPPORTED | |
| li2023camel | role-play communicative agents > single-agent | SUPPORTED | baseline = single-shot |
| wu2023autogen | conversation programming | SUPPORTED | AutoGen's own term |
| hong2023metagpt | SOP pipelines; typed documents not chat | SUPPORTED | structured outputs via shared message pool |
| qian2023chatdev | software-company simulation | SUPPORTED | |
| du2023debate | shares full context across rounds | SUPPORTED | |
| irving2018debate | (was) shares full context | **OVERCLAIMED→fixed** | F3-b; judge-mediated, length-limited — not full context; see gap-1 |
| bowman2022scalable | weak judges supervise strong workers | SUPPORTED | |
| burns2023weak | weak supervision of stronger model | SUPPORTED | weak-to-strong is training-time, same family |
| jimenez2023swebench | held-out PR tests as ground truth | SUPPORTED | FAIL_TO_PASS / PASS_TO_PASS |
| yang2024sweagent | held-out tests as ground truth | SUPPORTED | inherits SWE-bench harness; methodology is SWE-bench's |
| ridnik2024alphacodium | flow vs public + AI-generated tests | SUPPORTED | verbatim from full text |
| kambhampati2024position | pair LLM gen with external sound verifiers | SUPPORTED | |
| sun2023clover | consistency: code/docstring/annotations | SUPPORTED | CloverBench confirmed real (Dafny benchmark) |
| filliatre2013why3 | deductive platform; obligations discharge | SUPPORTED | |
| avizienis1985nversion | reliability via independent versions | SUPPORTED | metadata correct |
| knight1986independence | independence cannot be assumed; correlated failures | SUPPORTED | primary abstract: correlated failures, H0 rejected |
| fagan1976inspections | author–inspector separation | SUPPORTED | title is "...in Program Development" (correct in bib) |
| mills1987cleanroom | devs forbidden to execute own code; separate cert team | SUPPORTED | prohibition is on developer execution/debugging/unit-test |
| beck2003tdd | specs made executable | SUPPORTED | |
| meyer1992contract | specs made executable (DbC) | SUPPORTED | |
| clark1987comparison | separation of duties / integrity model | SUPPORTED | certifier ≠ implementer |
| saltzer1975protection | separation-of-privilege principle | SUPPORTED | |
| popper1959logic | trust by surviving refutation (Popperian) | SUPPORTED | |
| baudin_acsl | ACSL binder grammar + \at semantics | SUPPORTED | acsl-language repo has at.tex, binders.tex |

## Outcome

- 2 OVERCLAIMED (F3) → fixed in `tex/paper.tex`, recorded in
  `docs/12-0930-paper-gap-1.md`.
- 1 precision tightening (CAI), applied.
- 0 phantom, 0 misattributed metadata, 0 unsupported. Bibliographic metadata
  correct for all entries.

## Residual (GP) ledger

- **GP-FULLTEXT** — no source has a `read: FULL` reading record with archived
  full text + hash. Required before camera-ready per §6. This is the largest
  open item on the literature plane.
- Minor: `baudin_acsl` has an empty `year` (bibtex warning). A year was *not*
  invented (a hand-typed fact with no verified source is F4); resolve by
  recording the actual manual version/date when the full text is archived.
