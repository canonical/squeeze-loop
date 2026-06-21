# Full-text verification pass (read:FULL) — 2026-06-12

Upgrades the abstract-level pass (`lit-verification-2026-06-12.md`) to the §3
key-rule standard: full text obtained, read, archived, and each claim checked
against **body** content. Reading records: `bib/records/<bibkey>.md`.

## Archive

26 arXiv PDFs downloaded to `bib/archive/` and hashed in `SHA256SUMS`
(alongside the three companion guides). Classics obtained from open
author/university copies where possible; access level recorded honestly in each
record's header (`read: FULL | PARTIAL | SECONDARY`).

## Findings (delta vs the abstract pass)

**New overclaim caught only by reading the body:**
- **sun2023clover** — F3. "reducing correctness to cross-artifact consistency"
  stated a *reduction* as fact; the authors call it the **"Clover hypothesis"**
  (a conjecture) and name failure modes (edge-case omissions shared across all
  three artifacts go undetected). Body results: correct programs accepted
  75%@k=1 / 87%@k=10; incorrect 0% (no false positives) on CloverBench (60
  Dafny programs + 4 incorrect variants each). **Fixed** in `tex/paper.tex`:
  now "on the hypothesis that passing all checks implies correctness
  (empirically, no false positives on its CloverBench Dafny suite)."

**Body strengthened a prior softening (no change needed):**
- **gou2023critic** — the body's ablation supports even the *original* stronger
  comparative: "the model's own critiques contribute marginally… and even fall
  short compared to the initial output" (§4.1); "performance deterioration"
  without tool feedback (§4.2). Our softened wording is safely SUPPORTED.

**Confirmed at body level (special-scrutiny items):**
- **panickssery2024llm** — "linear" is the authors' own word (§3.2), established
  by controlled fine-tuning with three control tasks ruling out a generic
  fine-tuning confound. Flat manuscript phrasing is fair (if anything
  conservative).
- **knight1986independence** — read FULL (Leveson's MIT copy). 27 versions, 10^6
  tests, z=100.51 vs 2.33 critical, independence null rejected at 99%; up to
  8/27 versions fail one input. Manuscript "independence cannot be assumed" is
  faithful. (Scope note: authors reject the *independence-of-errors assumption*
  for this application, not N-version programming wholesale — the manuscript
  does not overstate this.)
- **hong2023metagpt** — body (§3.2) confirms "agents communicate through
  documents and diagrams (structured outputs) rather than dialogue" + shared
  message pool. "Typed documents not free chat" holds at body level.
- **bai2022constitutional** — two-phase structure confirmed; "self-critique
  stage" qualifier (added earlier) is accurate.
- **huang2023cannot**, **zheng2023judging**, **sharma2023sycophancy**,
  **jimenez2023swebench**, **ridnik2024alphacodium**, **kambhampati2024position**,
  **du2023debate**, **irving2018debate** (argue-before-judge, correctly excludes
  full-context), **li2023camel**, **lightman2023verify**, etc. — all SUPPORTED
  with body anchors in their records.

**Now-sourced fix:**
- **baudin_acsl** — empty `year` resolved from the actual manual (Version 1.23,
  © 2009–2026). bib updated (`year={2026}`, version in title); bibtex warning
  gone. Not invented — read from frama-c.com/download/acsl.pdf.

## Precision caveats recorded but NOT edited (fair characterizations, not quotes)

- **mills1987cleanroom** — "developers do not execute their own code" is verbatim
  1987 ("verification in place of program debugging"); the explicit "separate
  certification *team*" wording is from later Cleanroom/SEI literature, not the
  1987 paper. Substance ("concurrent fabrication and certification") supports
  the manuscript; the load-bearing gloss ("implementer never touches the
  acceptance evidence") is verbatim-backed. Left as-is.
- **meyer1992contract / beck2003tdd** — "made specifications executable" is a
  fair characterization; note Meyer frames runtime checking primarily as a
  debugging aid, and "specification" is not Beck's own word (the records flag
  this). Joint claim left as-is; revisit only if a reviewer presses.
- **li2023camel** — body baseline is single-shot gpt-3.5-turbo (GPT-4 is judge);
  manuscript already says "single-agent baselines" without naming GPT-4. OK.
- **clark1987comparison** — page range: text shows p.184; dblp lists 184–195 vs
  bib's 184–194. Minor; verify at camera-ready.

## State

- All cited sources have a reading record. read:FULL for the 26 arXiv +
  knight/avizienis/mills/fagan/clark/saltzer/meyer/filliatre/baudin; PARTIAL for
  beck (book) and popper (book, Ch.1 verbatim + SECONDARY).
- Residual: `manheim2018goodhart`, `krakovna2020specification` records pending
  (Goodhart co-cites; the claim is independently covered by the amodei record).
- GP-FULLTEXT (from the abstract pass) is now largely discharged.
