---
name: use-case-c
description: The Squeeze Loop instance for Use Case C — an HTTP API where the document plane (OpenAPI contract) and the runtime plane (live server) are forced into exact lockstep, on terrain C (split planes). The dominant failure is blending — a clean schema masking broken runtime behaviour (id leaks, tracebacks, missing auth), or a clean runtime escaping stale documentation. The exerciser RUNS the live server over HTTP but is physically denied the server source and the published schema (the load-bearing "run, don't read" channel). Use when working on src/C — the API governance policy, the canonical OpenAPI contract, the schema linter, the live server, the conformance test matrix, the legacy route-signature regression oracle, or the no-blend cross-check. Trigger phrasings: "use case C", "instance C", "split planes", "document vs runtime plane", "no-blend", "run don't read", "OpenAPI conformance squeeze", "id leak / missing auth on an untested route".
---

# Use Case C — the split-planes API squeeze loop

Use Case C is a **base** squeeze loop (`instance-c`, terrain **C**): an API whose
**document plane** (the published OpenAPI schema) and **runtime plane** (the live HTTP
server) are forced into exact lockstep so neither can mask the other. Its SL-1.0
self-description is [`src/C/instance-c.sl.json`](../../../instance-c.sl.json); the companion
write-up is [`src/C/docs/use-case-c.md`](../../../docs/use-case-c.md).

## The dominant failure it guards

**Coherent-and-wrong here = blending** — one plane's weak check standing in for the other's
strong claim: a clean schema masking broken runtime behaviour (id leaks, tracebacks,
missing auth on an untested route), or a clean runtime escaping stale documentation.

## Terrain C — split planes

Correctness divides across **two planes, each with its own authority**:

- **Runtime plane** — the API governance policy `API_POLICY_081` (`CLAUSE_1` auth,
  `CLAUSE_2` uuid-only ids, `CLAUSE_3` clean errors).
- **Document plane** — the canonical OpenAPI contract `base_schema.json` (`0444`), read
  independently by both bands.

The soundness load rests on a **no-blend cross-check**: each plane is verified *separately*
and the planes must *agree*.

## The bounds

- **Upper bound `U`** — *both* plane authorities (governance policy + canonical contract),
  which the sentinel refuses to let blend.
- **Lower bound `L`** — the schema linter (document plane), the frozen app-state DB, the
  legacy route-signature regression oracle (`ty0_baseline`), and — for the exerciser — the
  **live server observed over HTTP**.

## The cast (three actors) and the run-vs-read channel

| Actor | Builds | `U` | `L` | Must not see |
|---|---|---|---|---|
| **Gate sentinel / no-blend referee** (coordinator) | the gate sequence + the `.sl.json` | both plane authorities | linter + runtime HTTP + frozen DB + legacy-signature regression + both bands | — |
| **API implementer** | the HTTP server + its published OpenAPI schema | policy + canonical contract | the frozen DB it serves; the linter its schema must pass | the conformance matrix |
| **Conformance exerciser** | the conformance test matrix | policy + canonical contract, read independently | **what the live server returns when RUN over HTTP** | the server source + the implementer's `openapi.json` |

The load-bearing subtlety: the implementer *produces* the running server
(`runtime_oracle`), but the exerciser **runs** it over HTTP as its lower bound — it never
**reads** the source. A judge may *run* an oracle over an artifact it is barriered from; it
may never *read* that artifact. That run-vs-read distinction is what keeps the barrier
physical rather than honorary.

## The gates

- **Gate A / isolation.** The exerciser has zero import/path linkage to the server source.
- **Gate B (runtime).** Status codes, exact response keys, no forbidden patterns (no id
  leaks, no tracebacks) on every tested route; plus the document-plane route cross-check.
- **Gate C (coverage / no-blend).** Every clause maps to a passing check on *its* plane,
  seeded coherent-and-wrong negatives fire, and a clean check on one plane never stands in
  for the other; the legacy `ty0` signature hash re-verifies (no regression).

## Disjointness

The implementer is bound by both plane authorities but reads only the frozen DB and the
linter below; the exerciser is bound by the same authorities but its lower bound is the
**running server observed over HTTP** — it runs the implementation without ever reading its
source. The sentinel certifies only when both planes pass separately and agree, so neither
plane's check can mask the other. Catchability: an implementer blend (clean schema/happy
path hiding an id leak or missing auth) is caught by the exerciser's runtime assertions +
route cross-check; a weak happy-path matrix is caught by the sentinel (Gate C coverage +
seeded negatives).

```sh
python config/skills/sl-internal/scripts/sl_disjointness_check.py src/C/instance-c.sl.json
```

(0 FAIL / 8 checks.)
