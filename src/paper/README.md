# src/paper — the reflexive instance (the paper as its own squeeze)

This directory packages the **reflexive case study** as a use case with the same
shape as `src/A`, `src/B`, `src/C`, `src/D`: a `ground-truth/` (lower bound), an
`upper-bound/`, and an `in-band-deliverable/`, plus `evidence/`. It makes the
paper's central reflexive claim *runnable*: **this paper is produced under the
strategy it describes.**

## The vision

**The squeeze loop strategy bridges the gap between two sources of truth** — a
*hard* truth (the executable lower bound: it runs, it compiles, the number
recomputes, the proof type-checks) and a *soft* truth (the normative upper bound:
the literature and the paper-spec — authoritative, but interpretation-laden). The
deliverable is *in-band* exactly when it is a reading of the soft truth that the
hard truth does not refute: never the upper bound alone (over-claiming) nor the
lower bound alone (faithful to nothing but itself).

The **coordinator** (the main thread) is the loop's only **judge**, and its
mission is to enforce this vision across every actor — `paper-lit-agent` (which
builds and guards the soft upper bound), `paper-bench-agent` (the hard lower
bound), `paper-writer-agent` (the deliverable that must be faithful to the soft
*and* consistent with the hard at once), and `paper-verifier-agent` (which checks
the bridge holds, re-deriving each claim from the hard ground truth and the raw
source). It approves no plan and accepts no item that does not hold that bridge.
The gates below are how the bridge is held mechanically.

## Not a sandboxed experiment

Unlike A–D, `src/paper` is **not** isolated in an LXC container and does **not**
run offline. Its actors must read and (re)generate the **real repository** —
`tex/paper.tex`, `bib/`, `claims/ledger.tsv`, `verify/`, `eval/`, `src/A..D` — and
that is deliberate: the in-band deliverable being squeezed *is this repo's paper*.
The agents change the repo; they are the paper cycle, not a separate experiment.

## The mapping (cf. `paper-impl.md`)

| Layer | In A–D | Here (reflexive) |
|-------|--------|------------------|
| **upper bound** | a written spec / policy / manifest | the **read literature** (every `\cite` has an archived, read record) + the paper-spec (`paper-impl.md`) |
| **lower bound** | a SQLite warehouse / REST app / OpenAPI+server / Rocq kernel | the **executable evidence + the build**: every number recomputes from a harness, the manuscript compiles, every `\cite` resolves |
| **in-band deliverable** | the implementer's artifact | the **manuscript** (`tex/paper.tex`) + the claim ledger |
| **exerciser** | independent tests | the **verifier**: re-derives each ledgered claim from the source/artifact, never from the writer's prose |

The cast that operates it is defined in `paper-impl.md` §2 (coordinator +
paper-lit/bench/writer/verifier agents).

## Layout

```
src/paper/
├── _paperlib.py                       # shared: repo discovery, generator list, ledger/cite helpers
├── ground-truth/                      # LOWER BOUND (the hard truth)
│   ├── build_ground_truth.py          #   regenerate all macro generators
│   └── verify_ground_truth.py         #   determinism + build + cites resolve
├── upper-bound/                       # UPPER BOUND (the normative ceiling)
│   ├── validate_handbook.py           #   read-before-cite: \cite ⊆ bib ∩ records
│   └── gate_checks.py                 #   Gate A (plan trail) + Gate C (ledger ↔ reflexive macros)
├── in-band-deliverable/               # THE MANUSCRIPT, squeezed
│   ├── implementer/                   #   the writer's deliverable -> tex/paper.tex (in the repo)
│   ├── exerciser/verify_claims.py     #   the verifier: each claim traces to a record/artifact
│   └── runner/execute_squeeze.py      #   run the whole reflexive squeeze
└── evidence/
    ├── measure_squeeze.py             #   emit results.json (self-application counts + verdict)
    └── results.json
```

## Run

```bash
python3 src/paper/in-band-deliverable/runner/execute_squeeze.py   # the full squeeze
python3 src/paper/evidence/measure_squeeze.py                     # + results.json
```

`src/D` is not yet wired into the manuscript's numbers, so it is absent from the
generator list in `_paperlib.py`; it joins when a paper-impl circle brings Use
Case D in.
