---
name: use-case-paper
description: The reflexive Squeeze Loop instance for the paper — the manuscript produced under the strategy it describes AND a monitor over the four object instances A–D, spanning terrains A/B/C. Its verifier re-derives every ledgered claim (including claims about A–D's results) from the hard ground truth, never from the writer's prose; the four sub_loop bridge rows link down to instance-a..d by their returned results (not their internals). The dominant failure is a manuscript whose prose reads as faithful while a reported number does not recompute or overclaims. The reflexive soft-side claim (selfhood / faithful reading of the literature) has no executable refuter and is closed at the human/external reviewer terminus. Use when working on src/paper — the paper-spec, the manuscript, the claim ledger, the recompute/build harness, the read-before-cite literature guard, the verifier's re-derivation, the A–D bridges, or the reflexive case study. Trigger phrasings: "use case paper", "instance paper", "the reflexive instance", "monitor over A–D", "re-derive from ground truth not prose", "every number recomputes", "who squeezes the coordinator", "human reviewer terminus".
---

# Use Case Paper — the reflexive instance (a monitor over A–D)

Use Case Paper is the **reflexive** squeeze loop (`instance-paper`, **`kind: monitor`**,
terrains **A/B/C**): the paper is *produced under the strategy it describes*, and the same
loop *monitors the four object instances A–D*. Its SL-1.0 self-description is
[`src/paper/instance-paper.sl.json`](../../../instance-paper.sl.json); the companion
write-up with the diagram is
[`src/paper/docs/use-case-paper.md`](../../../docs/use-case-paper.md).

## The dominant failure it guards

**Coherent-and-wrong here = a manuscript whose prose reads as faithful to the literature
while a reported number does not recompute or overclaims a result** — including a claim
*about* one of the instances A–D. Fluent, citable, and wrong.

## Two roles in one loop

1. **The deliverable.** The manuscript (`tex/paper.tex`) + the claim ledger, written by the
   writer agent.
2. **The monitor over A–D.** The verifier re-derives each ledgered claim — including every
   claimed result of instances A–D — **from the hard ground truth and the instances'
   returned results, never from the writer's prose.** The four `sub_loop` bridge rows link
   down to `instance-a..d` by their **returned results** (the mediated channel), *never*
   their internal sources — so the monitor never bounds itself on an instance-internal
   artifact (the cross-loop disjointness rule).

## The bounds

- **Upper bound `U`** — the **read literature** (every cite has an archived read record) +
  the **paper-spec** (the authored normative ceiling).
- **Lower bound `L`** — the **recompute + build harness** (every number recomputes from a
  generator, the manuscript compiles, every cite resolves) over the **raw repository ground
  truth** and the instances' returned results.

## The cast (ten actors)

| Actor | Role | Builds | Must not see |
|---|---|---|---|
| **Main-thread coordinator** (the only judge) | coordinator | approvals, gate verdicts, ledger reconciliation, the `.sl.json` | — |
| **Literature agent** | property author | the paper-spec + the read-before-cite guard | the manuscript, the ledger |
| **Writer agent** | implementer | the manuscript + the claim ledger | the verifier's re-derivation |
| **Verifier agent** | exerciser | the independent re-derivation of every ledgered claim | the manuscript, the ledger |
| **Bench agent** | probe | the recompute/build harness that pins every number to its generator | the manuscript, the ledger |
| **Bridges → instance-a..d** | sub_loop | each object instance collapsed to one row; returns its machine-verdicted results | — |
| **External / human reviewer** | human terminus | the terminal editorial judgment closing the reflexive soft side | — |

## The barrier and the terminus

The verifier (and bench) **never see the writer's manuscript/ledger** and re-derive
independently; the monitor reads only the instances' **returned results** via the bridges,
never their internals. The coordinator's editorial judgment — *is the paper a faithful
reading of the literature?* — is the **one soft-side hole**, and it is closed at the
**human/external reviewer terminus**, by disjoint authority, not mechanically. A claim that
the automation alone closed the soft side would itself be the coherent-and-wrong this loop
exists to catch.

## The gates

- **Gate A (editorial).** The coordinator judges each bridge / item before accepting it.
- **Gate B (machine).** Every number recomputes from its generator; the manuscript builds;
  every cite resolves to bib + an archived read record.
- **Gate C (coverage / no-blend).** The claim ledger reconciles with the reflexive macros
  (no ledgered claim silently skipped); prose never stands in for a recomputed number.

## Disjointness

The reflexive cast holds disjoint bases: lit holds the literature (never the manuscript);
writer holds the spec + literature + the build (never the verifier's evidence); verifier
re-derives from the hard truth and the instances' returned results (never the writer's
prose); bench pins the hard truth from raw repo data (never the writer's claims). The four
bridges link to A–D by returned results, not internals. The coordinator's editorial
judgment is closed at the human reviewer terminus.

```sh
python config/skills/sl-internal/scripts/sl_disjointness_check.py src/paper/instance-paper.sl.json
```

(0 FAIL / 31 checks.)
