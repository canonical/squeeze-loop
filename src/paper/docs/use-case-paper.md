# Use Case Paper — the reflexive instance, a monitor over A–D

Use Case Paper is the **reflexive** squeeze loop (`id: instance-paper`, **`kind: monitor`**,
terrains **A/B/C**), encoded as
[`src/paper/instance-paper.sl.json`](../instance-paper.sl.json) and written up as the skill
[`src/paper/config/skills/use-case-paper`](../config/skills/use-case-paper/SKILL.md). It is
two things at once: **the paper produced under the strategy it describes, and the monitor
over the four object instances A–D.**

## Rationale — why this loop exists

The paper makes claims — about the literature, and about what instances A–D actually
demonstrated. The dominant failure is the fluent, citable falsehood:

> **Coherent-and-wrong = a manuscript whose prose reads as faithful to the literature while
> a reported number does not recompute or overclaims a result** — including a claim *about*
> A–D.

The loop guards this by re-deriving, never trusting prose:

- **Upper bound `U`** — the **read literature** (every cite has an archived read record) +
  the **paper-spec** (the authored ceiling).
- **Lower bound `L`** — the **recompute + build harness** over the **raw repository ground
  truth** and the instances' **returned results**: every number recomputes from a
  generator, the manuscript compiles, every cite resolves.

The verifier re-derives each ledgered claim — including every claimed result of A–D — **from
the hard ground truth, never from the writer's prose.** The four `sub_loop` bridges link
down to `instance-a..d` by their **returned results** (the mediated channel), never their
internals — so the monitor never bounds itself on an instance-internal artifact.

## Graphical representation

The diagram is rendered **top-to-bottom** (`--direction tb`) because the reflexive cast is
large (ten actors, four bridges); the SVG is the readable form (zoom-lossless).

![The `instance-paper` SL — the coordinator, literature/writer/verifier/bench agents, the
four A–D bridges, and the human-reviewer terminus (orange), squeezed between the read
literature + paper-spec (green, `U`) and the recompute harness + raw ground truth + the four
instances' returned results (pink, `L`)](img/use-case-paper.svg)

*Rendered from `instance-paper.sl.json` with `--direction tb --svg`. Solid edges are bounds
(`U` / `L`) and `produces`; red dashed edges are the `✗ must-not-see` barriers; blue edges
are the catchability ("catches") relation.*

| Actor | Role | Builds |
|---|---|---|
| **Main-thread coordinator** (the only judge) | coordinator | approvals, gate verdicts, ledger reconciliation, the `.sl.json` |
| **Literature agent** | property author | the paper-spec + the read-before-cite guard |
| **Writer agent** | implementer | the manuscript + the claim ledger |
| **Verifier agent** | exerciser | the independent re-derivation of every ledgered claim |
| **Bench agent** | probe | the recompute/build harness pinning every number to its generator |
| **Bridges → instance-a..d** | sub_loop | each object instance collapsed to one row; returns machine-verdicted results |
| **External / human reviewer** | human terminus | the terminal editorial judgment closing the reflexive soft side |

## Disjointness at a glance

> **The hypothesis.** The reflexive cast holds disjoint bases — lit holds the literature
> (never the manuscript), writer holds the spec + literature and the build (never the
> verifier's evidence), verifier re-derives from the hard truth and the instances' returned
> results (never the writer's prose), bench pins the hard truth from raw repo data (never
> the writer's claims). The four bridges link to A–D by their **returned results, not their
> internal sources**, so the monitor never bounds itself on an instance-internal artifact.
> The coordinator's editorial judgment — the one soft-side hole — is closed at the
> human/external reviewer terminus, by disjoint authority, not mechanically.

**Load-bearing barrier.** The verifier (and bench) never see the writer's manuscript/ledger
and re-derive independently; the monitor reads only the instances' returned results via the
bridges, never their internals.

**Catchability — each blind spot is caught by a different actor:**

| Actor | Characteristic blind spot | Caught by | Via |
|---|---|---|---|
| Coordinator | its own un-squeezed editorial judgment of whether the paper faithfully reads the literature | **Human reviewer** | external / human review — the terminus that closes the soft side |
| Literature agent | an over-broad reading: a cite that doesn't actually support the claim | **Verifier agent** | independent re-derivation requires each claim's source to actually support it |
| Writer agent | coherent-and-wrong prose: faithful-looking text whose number doesn't recompute or overclaims | **Verifier agent** | re-derivation from the hard ground truth; Gate B recompute mismatch |
| Verifier agent | a re-derivation that silently skips a ledgered claim | **Coordinator** | Gate C ledger ↔ reflexive-macro coverage reconciliation |
| Bench agent | a harness computing a consistent-but-wrong number not matching raw data | **Verifier agent** | the verifier re-derives from raw source independently of the harness build |
| Bridges → A / B / C / D | an instance reports a coherent-and-wrong result | **Verifier agent** | the verifier re-derives each instance's claimed result from its returned ground-truth outputs |

**The terminus is honest.** The reflexive soft-side claim (selfhood / faithful reading of
the literature) has **no executable refuter**, so the human-reviewer row carries **no**
lower bound — that absence is the point. Nesting closes the coordinator's hole by *disjoint
authority*, terminating at a human/external reviewer; claiming the automation alone closed
the soft side would be the coherent-and-wrong this loop is built to catch.

**Mechanical floor.** `sl_disjointness_check.py instance-paper.sl.json` returns
**0 FAIL / 31 checks** — every actor reads no source it produced (D1), every barrier is
consistent with its bounds (D2), the human terminus correctly carries no executable `L`
(D8), and each blind spot above is caught by a *different* actor (C2). The one
informational note (the terminus declares no blind spot of its own) is expected. A green
check certifies the **authorities are disjoint** — including across levels (the monitor
doesn't bound itself on instance internals) — never that the paper is *done*.

---

*Generated from [`src/paper/instance-paper.sl.json`](../instance-paper.sl.json). Regenerate
the diagrams with:*

```sh
python config/skills/sl-internal/scripts/sl2plantuml.py \
    src/paper/instance-paper.sl.json --direction tb -o src/paper/docs/img/use-case-paper.png
python config/skills/sl-internal/scripts/sl2plantuml.py \
    src/paper/instance-paper.sl.json --direction tb --svg -o src/paper/docs/img/use-case-paper.svg
```
