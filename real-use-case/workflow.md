# Running `creusot-monitoring` as a Workflow

This explains how to drive the `creusot-monitoring` loop with the **Workflow** tool so
it runs **unsupervised** — processing the `annotate/` corpus in batches of 10
`creusot-sl` sub-agents, monitor-gating each, and committing every batch — without
filling the main conversation's context window.

## Why a Workflow (the one idea that matters)

When I run `creusot-sl` sub-agents *inline* (via the Agent tool), the **coordinator is
the chat itself**, so every sub-agent's returned summary piles up in my context and the
run caps out after ~3 batches.

A Workflow moves the **coordinator into deterministic JavaScript**:

| | inline (Agent tool) | Workflow |
|---|---|---|
| `creusot-sl` instance | isolated context | isolated context (same) |
| `creusot-monitoring` coordinator | **the chat (my context)** | **plain JS — zero LLM context** |
| per-file results land in | my context (accumulate) | JS variables |
| scale | ~3 batches | the whole queue |
| runs | foreground, blocks | **background**, notifies on completion |

The sub-agents don't change; the *coordinator* stops competing for my window. That's
what lets it finish all 169 remaining files.

## Mental model

```
Workflow script (JS coordinator — not an LLM)
  chunk the file list into batches of 10
  for each batch (sequential, so commits are ordered):
     pipeline over its 10 files (concurrent, capped ~10-16):
        stage 1  agent creusot-sl   -> annotate + cargo creusot   (isolated context)
        stage 2  agent monitor      -> faithfulness gate, revert if fabricated
     agent committer -> update verdict log + git commit this batch
```

- `agent(...)` = one isolated sub-agent. With a `schema` it returns a validated object.
- `pipeline(items, s1, s2)` = each file flows s1→s2 independently, no barrier; the call
  resolves when all 10 are done — *then* the batch commit runs.
- The script has **no filesystem access**, so the file queue is passed in via `args`.

## Preparing the queue (passed as `args`)

The script can't scan directories, so compute the remaining real-code files first and
pass them as a real JSON array (not a string):

```sh
# remaining files NOT yet in the verdict log, that contain real code
comm -23 \
  <(find annotate -name '*.rs' | sort) \
  <(cut -f1 annotate/.verdicts.tsv | sort) > /tmp/remaining.txt
# (optionally filter to real-code via the classifier; trivial stubs can be a fast batch)
```

Then invoke the Workflow tool with:

```json
{
  "script": "<the script below>",
  "args": { "repo": "/path/to/use-creusot",
            "batch": 10,
            "files": ["annotate/bug/691.rs", "annotate/bug/922.rs", "..."] }
}
```

`args.files` is the verbatim queue; `args.batch` is the batch size (10).

## The workflow script

```javascript
export const meta = {
  name: 'creusot-monitoring',
  description: 'Drive creusot-sl over annotate/: annotate+prove each file, monitor-gate, commit per batch of 10',
  phases: [
    { title: 'Prove',   detail: 'creusot-sl: annotate + cargo creusot' },
    { title: 'Monitor', detail: 'faithfulness gate (strip == original), revert fabrications' },
    { title: 'Commit',  detail: 'update verdict log + git commit per batch' },
  ],
}

const REPO  = (args && args.repo)  || '/path/to/use-creusot'
const BATCH = (args && args.batch) || 10
const FILES = (args && args.files) || []

// --- structured outputs (agents are forced to return these) ---
const VERDICT = {
  type: 'object', additionalProperties: false,
  required: ['file', 'verdict'],
  properties: {
    file:    { type: 'string' },
    verdict: { type: 'string', enum: ['PROVED', 'PARTIAL', 'FAILED', 'TRIVIAL'] },
    spec:    { type: 'string' },
    learned: { type: 'string' },
    bug:     { type: 'string' },
  },
}
const GATE = {
  type: 'object', additionalProperties: false,
  required: ['file', 'faithful', 'finalVerdict'],
  properties: {
    file:         { type: 'string' },
    faithful:     { type: 'boolean' },                 // monitor-check.sh == ACCEPT
    finalVerdict: { type: 'string' },                  // downgraded to TRIVIAL/FAILED if not faithful
    note:         { type: 'string' },
  },
}

function chunk(a, n) { const o = []; for (let i = 0; i < a.length; i += n) o.push(a.slice(i, i + n)); return o }
function name(f) { return f.replace(/[^A-Za-z0-9_]/g, '_') }

// --- the creusot-sl sub-agent (annotate + prove ONE file) ---
function provePrompt(f) {
  return `You are a creusot-sl sub-agent. Add Pearlite specs to ONE Rust file and prove it with Creusot.
TARGET: ${REPO}/${f}

CRITICAL FAITHFULNESS RULE: do NOT add/remove/rename/modify ANY executable code. ONLY add Pearlite
annotations (#[requires]/#[ensures]/#[invariant]/#[variant]/#[check(terminates)]), proof_assert!,
use creusot_std::prelude::*;, and #[logic] helpers. Stripped of #[...]/use/proof-macros/#[logic] items,
your file MUST be byte-identical to the original. If nothing can panic/overflow/index (empty/no-op/decl-only),
return verdict TRIVIAL and change NOTHING. Never use #[trusted]/assume!/axioms.

ENV: run '. "$HOME/.cargo/env"' in every bash block. Scaffold UNDER $HOME, never /tmp:
'mkdir -p $HOME/cwork && cd $HOME/cwork && cargo creusot new ${name(f)}'. Reference
${REPO}/config/skills/creusot/SKILL.md and .../references/learned-annotator.md.

STEPS: copy TARGET's code verbatim into the project's src/lib.rs, add only annotations, run 'cargo creusot',
iterate <=3 times. If ALL obligations Proved, overwrite TARGET with the annotated lib.rs. Return the verdict.`
}

// --- the monitor faithfulness gate for ONE file ---
function gatePrompt(f, v) {
  return `You are the creusot-monitoring base-SL monitor. Verify file ${f} (creusot-sl said: ${JSON.stringify(v)}).
Run: cd ${REPO} && ./monitor-check.sh ${f.replace(/^annotate\//, '')}
- If it prints ACCEPT: the annotation is faithful -> faithful=true, finalVerdict=the creusot-sl verdict.
- If it prints FABRICATED: the agent altered code -> revert it
  ('cp ${REPO}/training-data/${f.replace(/^annotate\//, '')} ${REPO}/${f}'), set faithful=false,
  and finalVerdict=TRIVIAL (no-op original) or FAILED (real original it failed to annotate faithfully).
Return the structured gate result.`
}

// --- the per-batch committer ---
function commitPrompt(n, results) {
  return `You are the creusot-monitoring committer for batch ${n}. In ${REPO}:
1. Append one TSV line per result to annotate/.verdicts.tsv as "<file>\\t<finalVerdict>\\t<note>" using: ${JSON.stringify(results)}.
2. Run ./gen-verdicts.sh to regenerate annotate/VERDICTS.md.
3. git add the batch files (${results.map(r => r.file).join(' ')}) + annotate/VERDICTS.md + annotate/.verdicts.tsv.
4. Commit: git commit -m "creusot-monitoring batch ${n}: $(...summary of PROVED/TRIVIAL/FAILED counts...)\\n\\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>".
Report the commit hash.`
}

const batches = chunk(FILES, BATCH)
const all = []
for (let b = 0; b < batches.length; b++) {
  phase('Prove')
  log(`Batch ${b + 1}/${batches.length} — ${batches[b].length} files`)

  // stage 1 (prove) -> stage 2 (monitor gate), pipelined per file, concurrent within the batch
  const gated = await pipeline(
    batches[b],
    (f)        => agent(provePrompt(f), { label: `sl:${f}`,  phase: 'Prove',   schema: VERDICT }),
    (v, f)     => agent(gatePrompt(f, v), { label: `mon:${f}`, phase: 'Monitor', schema: GATE }),
  )
  const results = gated.filter(Boolean)
  all.push(...results)

  phase('Commit')
  await agent(commitPrompt(b + 1, results), { label: `commit:b${b + 1}`, phase: 'Commit' })

  // optional: stop early if a token target was set
  if (budget.total && budget.remaining() < 60_000) { log('budget reached — stopping'); break }
}
return { processed: all.length, proved: all.filter(r => r.finalVerdict === 'PROVED').length }
```

## Bounding cost

Pass a token target with the run (e.g. prefix your request with `+800k`); then
`budget.total` is set and the `budget.remaining()` guard stops the loop cleanly before
it overruns. With no target, it runs the whole queue (169 files ≈ 17 batches).

## Running, watching, resuming

- **Launch:** call the Workflow tool with `{ script, args }` (or save the script to a
  file and pass `{ scriptPath, args }`). It returns a `runId` immediately and runs in
  the **background**; you get a notification when it finishes.
- **Watch live:** `/workflows` shows the phase tree (Prove / Monitor / Commit) and which
  files are in flight.
- **Resume after a stop/edit:** relaunch with `{ scriptPath, resumeFromRunId: "<runId>" }`
  — completed `agent()` calls return cached results instantly; only new/edited files
  re-run. (The verdict log on disk also means an interrupted run just re-queues the
  unprocessed files next time.)

## What stays true to the loop design

- **Isolated contexts:** each `creusot-sl` and each monitor check is its own agent — the
  coordinator (the JS script) holds only small structured results.
- **Monitor gate runs unattended:** the faithfulness check (`monitor-check.sh`: stripping
  the annotations must reproduce the original code) still rejects fabrications and
  reverts them — no human needed to catch a bad proof.
- **Gate-defined done & per-batch commits:** verdicts come from `cargo creusot` + the
  gate, and every batch is committed, exactly as in the inline run.
- **Capitalization:** to also accrue learned heuristics, add a stage (or a per-batch
  agent) that runs Gate S and appends PASS/CARVE-OUT entries to
  `config/skills/creusot/references/learned-*.md`; keep it disjoint (the monitor audits
  the annotator's skills, not its own).

## Caveat

Scripts run plain JavaScript (no TypeScript, no `Date.now()`/`Math.random()`), and have
no filesystem access — all inputs arrive through `args`, and all disk/git work happens
inside `agent()` calls. The concurrency cap is ~`min(16, cores-2)`, so a batch of 10
runs effectively in parallel.
