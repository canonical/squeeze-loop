# 12-4100-paper-spec-45 — paper-impl loop, circle 45: polish the stabilizers section (table completeness)

STATUS: APPROVED
Polish of sec:stabilizers / tab:collapse. The table is introduced as mapping
"collapse modes to the rules that block them", and 12 of the 13 stabilizers appear
in its "Blocked by" column (rules 1-10, 12, 13, plus the (C1) disjointness audit).
Stabilizer 11 ("Sequence by mechanism reuse; parallelize only across independence")
is the lone rule with no collapse-mode row -- a real completeness gap in the
catalogue. Add the collapse mode rule 11 blocks so every stabilizer is reachable
from the table.

## Changes
- tex/paper.tex tab:collapse (~between the "Scope blur ... & 9" and "Orphan change
  ... & 12" rows): add one row --
    Unsequenced parallelism & parallel chains share an evidence base or deliverable,
    or an item rides machinery a prior item had not hardened & 11 \\
  This is the failure stabilizer 11 prevents (sequential-by-mechanism-reuse;
  parallel-only-across-independence), stated in the same definitional register as
  the other rows.
- Regenerate reflexive.tex (ResReflexSpecDocs 44->45 for this new spec doc).

## Gates
- Gate B: build green; the new row is a DEFN-register description of the paper's own
  framework (like every other tab:collapse row), no new \cite/number/macro/CLM;
  table still references valid stabilizer numbers; previously-SUPPORTED text
  byte-stable outside the one table hunk; all 13 stabilizers now appear in the
  "Blocked by" column.
- Gate C: ledger unchanged (CITE 46 + RESULT 28); reflexive macros reconcile;
  reflexive re-run byte-identical.

## Note
Internal-consistency completion, not new content: stabilizer 11 already exists in
the enumerate; the new row names the collapse mode it blocks, matching the table's
stated purpose. The 13-rule catalogue and \ref{item:laststab}=13 are unchanged.
