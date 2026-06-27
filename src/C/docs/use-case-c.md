# Use Case C — document and runtime planes in lockstep

Use Case C is a **base** squeeze loop (`id: instance-c`, **`kind: base`**, terrain **C**),
encoded as [`src/C/instance-c.sl.json`](../instance-c.sl.json) and written up as the skill
[`src/C/config/skills/use-case-c`](../config/skills/use-case-c/SKILL.md). Its deliverable:
**an HTTP API whose published OpenAPI schema (document plane) and live server (runtime
plane) are forced into exact lockstep.**

## Rationale — why this loop exists

The terrain is **split planes**: correctness divides across two planes, each with its own
authority — the API governance policy `API_POLICY_081` (runtime) and the canonical OpenAPI
contract `base_schema.json` (document) — plus a precedence rule. The dominant failure is
therefore **blending**:

> **Coherent-and-wrong = blending** — one plane's weak check standing in for the other's
> strong claim: a clean schema masking broken runtime behaviour (id leaks, tracebacks,
> missing auth on an untested route), or a clean runtime escaping stale documentation.

The soundness load rests on a **no-blend cross-check**: each plane is verified separately
and the planes must agree.

- **Upper bound `U`** — *both* plane authorities (governance policy + canonical contract).
- **Lower bound `L`** — the schema linter, the frozen app-state DB, the legacy
  route-signature regression oracle, and the **live server observed over HTTP**.

## Graphical representation

![The `instance-c` SL — sentinel/no-blend referee, API implementer, and conformance
exerciser (orange) bound by both plane authorities (green, `U`) over the linter, frozen DB,
runtime oracle, and ty0 baseline (pink, `L`); the exerciser is barriered (red dashed) from
the server source and the published schema, yet RUNS the live server](img/use-case-c.svg)

*Rendered from `instance-c.sl.json`. Solid edges are bounds (`U` / `L`) and `produces`; red
dashed edges are the `✗ must-not-see` barriers.*

| Actor | Role | Builds | `U` | `L` |
|---|---|---|---|---|
| **Gate sentinel / no-blend referee** | coordinator | the gate sequence (isolation, coverage, runtime, document, ty0) | both plane authorities | linter + runtime HTTP + frozen DB + legacy-signature regression + both bands |
| **API implementer** | implementer | the HTTP server + its published OpenAPI schema | governance policy + canonical contract | the frozen DB it serves; the linter its schema must pass |
| **Conformance exerciser** | exerciser | the conformance test matrix | the same authorities, read independently | what the live server returns when **run** over HTTP |

## Disjointness at a glance

> **The hypothesis.** The implementer is bound by both plane authorities but reads only the
> frozen DB and the linter below; the exerciser is bound by the same authorities but its
> lower bound is the **running server observed over HTTP** — it RUNS the implementation
> without ever reading its source. The sentinel certifies only when both planes pass
> separately *and agree*, so neither plane's check can mask the other.

**Load-bearing barrier.** The exerciser runs the server (`runtime_oracle`) but is
physically denied the server source and the implementer's `openapi.json` (zero-import
isolation). **The run-vs-read distinction is what keeps the barrier physical:** a judge may
*run* an oracle over an artifact it is barriered from; it may never *read* that artifact.

**Catchability — each blind spot is caught by a different actor:**

| Actor | Characteristic blind spot | Caught by | Via |
|---|---|---|---|
| API implementer | a blend: a clean schema or happy-path runtime hiding an id leak / missing auth on an untested route | **Conformance exerciser** | Gate B runtime assertions (status, exact keys, no forbidden patterns) + the document-plane route cross-check |
| Conformance exerciser | a weak happy-path matrix that misses a clause corner | **Gate sentinel** | Gate C clause coverage + seeded coherent-and-wrong negative controls |

**No terminus.** Instance C is a fully **mechanical** loop (`terminus: null`): both planes
are settled by execution — the linter on the schema and live HTTP on the runtime — and the
no-blend cross-check is itself mechanical, so there is no soft-vs-soft residual.

**Mechanical floor.** `sl_disjointness_check.py instance-c.sl.json` returns
**0 FAIL / 8 checks** — every actor reads no source it produced (D1, incl. the exerciser
running but not reading the runtime oracle), every barrier is consistent with its bounds
(D2), and each blind spot above is caught by a *different* actor (C2). A green check
certifies the **authorities are disjoint**, never that any route is *done*.

---

*Generated from [`src/C/instance-c.sl.json`](../instance-c.sl.json). Regenerate the
diagrams with:*

```sh
python config/skills/sl-internal/scripts/sl2plantuml.py \
    src/C/instance-c.sl.json -o src/C/docs/img/use-case-c.png
python config/skills/sl-internal/scripts/sl2plantuml.py \
    src/C/instance-c.sl.json --svg -o src/C/docs/img/use-case-c.svg
```
