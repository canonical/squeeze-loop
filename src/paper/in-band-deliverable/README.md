# in-band-deliverable — the manuscript, squeezed

The deliverable is the paper itself, held between the literature (above) and the
executable evidence + build (below).

- `implementer/` — the writer's deliverable IS `tex/paper.tex` in the repo (see
  `implementer/README.md`); it is not duplicated here.
- `exerciser/verify_claims.py` — the verifier re-derives every ledgered claim from
  its source or artifact (a CITE row needs a reading record; a RESULT row needs an
  artifact on disk), never from the writer's prose.
- `runner/execute_squeeze.py` — runs the whole reflexive squeeze and passes iff
  every plane reconciles.
