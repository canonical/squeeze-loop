# 12-4200-paper-spec-46 — paper-impl loop, circle 46: polish the reflexive case study

STATUS: APPROVED
Polish of sec:reflexive that closes a traceability gap between the generated defect
counts and the prose. The macros (from verify/manuscript_defects.tsv) report
ResReflexDefects 8 = ResReflexDefectsLit 4 + ResReflexDefectsEvid 4, but the prose
names only 3 examples per plane. Audit of the 8 tsv rows against the text:
  literature: D1 (comparative overstated), D2 (misattributed finding), D7
    (hypothesis-as-fact) are named; D3 (Constitutional AI shared-context claim not
    scoped to the self-critique stage) is named NOWHERE.
  evidence: D4 (figure mis-credit), D5 (cross-section self-inconsistency), D6
    (abridged-as-verbatim) are named in the list; D8 (Figure 1 caption Gate-A
    mischaracterization) is already described separately as the external-review
    catch.
So D3 is the single gate-caught defect invisible in the prose despite being
counted. Add it to the literature-plane example list, making the literature
enumeration complete (4/4) and every one of the 8 defects traceable in the text.

## Changes
- tex/paper.tex sec:reflexive literature-plane sentence (~line 982-983): insert a
  fourth literature example for D3 -- "a shared-context claim not scoped to the one
  stage where it holds" -- between the D2 ("wrong paper") and D7 ("conjecture as
  result") items. Keeps "included" (evidence list still gives 3, with D8 covered
  separately).
- Regenerate reflexive.tex (ResReflexSpecDocs 45->46 for this new spec doc).

## Gates
- Gate B: build green; no new \cite/number/macro/CLM (the example is a prose
  description of an already-ledgered defect, D3 in manuscript_defects.tsv);
  previously-SUPPORTED text byte-stable outside the one sentence; literature
  examples now number ResReflexDefectsLit (4).
- Gate C: ledger unchanged (CITE 46 + RESULT 28); reflexive macros reconcile;
  reflexive re-run byte-identical; defect count macros (8/4/4) unchanged.

## Note
Accuracy completion: D3 is a real, FIXED, ledgered defect
(verify/manuscript_defects.tsv) that the prose had been silently dropping. After
this, all 8 gate-caught defects are referenced in the section (D1-D3,D7 in the
literature list; D4-D6 in the evidence list; D8 in the external-challenge
sentence). The generated counts are the source of truth and are unchanged.
