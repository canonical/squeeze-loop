# 14-0845-paper-spec-67 — paper-impl loop, circle 67: build the live self-model (Artifact A, part 1)

STATUS: APPROVED
TARGET: G-O1O5

Step 3 of 14-0714-spec.md §5. Build the live self-model artifact + generator. No
discharge claim yet (that is circle 68's check). Honesty guard (spec §0/§6): the model
is DERIVED from the repo (a fixed point), never hand-authored.

## Changes
- New verify/self_model.py -> claims/self_model.json + tex/macros/selfmodel.tex.
  Derived: clause discharge from artifact presence; history from spec-doc TARGET
  headers; next_target = top open gap (pure function of clause status, not hand-set).
  Idempotent (re-run reproduces the JSON byte-identically).
- \input{macros/selfmodel}; self_model.py added to _paperlib GENERATORS.
- sec:reflexive: one modest, factual sentence -- the loop now maintains a derived
  self-model recording the obligation it targets per circle (ResSelfModelUpdates
  circles logged, currently ResSelfModelCircle). No O1/O5 discharge asserted here.

## Gates
- Gate B: build green; ResSelfModel* macros used (no orphan); self_model.json is a
  fixed point; no new ledger row this circle.
- Gate C: ledger unchanged (CITE 46 + RESULT 31) == regenerated reflexive macros
  (ResReflexSpecDocs 66->67); selfmodel/reflexive re-run byte-identical.

## Note
At this circle O1/O5 read "partial" in the model (the discharge check does not exist
yet); circle 68 adds verify/self_model_check.py, which flips them to discharged once
read->act + redirect are validated. Tier stays 2.
