#!/usr/bin/env python3
"""Cross-provider §6 replication across GENUINELY INDEPENDENT providers.

§6's load-bearing finding is that model-based casts ship the SAME coherent-and-wrong
reading on contradiction/underspecification cases (shared blind spot), and only the
executable oracle catches it. The paper states (abstract, §4.4, §10) that the stronger
claim -- "the evidence barrier beats genuine model DIVERSITY" -- is "owed a cross-provider
replication". This runner is that replication.

It runs the SAME build_cases() A/B/C cases used in §6 across several models from
INDEPENDENT pretraining lineages reachable on one ollama host:

    anthropic  -> (anchor; supplied separately from the Claude §6 repeated-draws run)
    alibaba    -> qwen3.6:35b
    deepseek   -> deepseek-r1:70b
    google     -> gemma4:31b
    openai     -> gpt-oss:120b
    meta       -> llama4:16x17b

For each provider it scores answer-vs-executable-oracle (the SAME oracle for everyone), and
records per-case the chosen option. The deliverable is two things §6 cannot get from one
provider:
  (1) per-provider error rates on the contradiction/underspecification ladders, and
  (2) CONVERGENCE: on each case, do the providers that ERR pick the SAME wrong reading?
      High cross-provider convergence on the wrong fork == the blind spot is in the TASK,
      not the weights -> genuine model diversity does NOT decorrelate it -> corroborates
      "disjointness of evidence, not model diversity, carries the gate."

Non-deterministic; logged under verify/reports/live/, NEVER gated. Reuses load_probe()/
score() from run_underspec so the cases and scoring are byte-identical to §6's runner.

Usage:
  OLLAMA_HOST=http://localhost:11434 python3 eval/live/run_xprovider_six.py \
      --reps 3 --stamp 2026-06-19 [--instances A,B,C] [--limit 0] [--providers alibaba,deepseek,...]
"""
import argparse
import json
import os
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_underspec as RU  # reuse load_probe, score, wilson, _tail_after_answer

OUTDIR = REPO / "verify" / "reports" / "live"
OLLAMA_HOST = (os.environ.get("OLLAMA_HOST") or "").rstrip("/")

# provider lineage -> ollama model id. Each is an INDEPENDENT pretraining lineage.
PROVIDERS = {
    "alibaba":  "qwen3.6:35b",
    "deepseek": "deepseek-r1:70b",
    "google":   "gemma4:31b",
    "openai":   "gpt-oss:120b",
    "meta":     "llama4:16x17b",
}


def ollama_call(model, prompt, temperature=0.0, num_predict=320):
    payload = {"model": model, "prompt": prompt, "stream": False, "think": False,
               "options": {"temperature": temperature, "num_predict": num_predict}}
    url = f"{OLLAMA_HOST}/api/generate"
    for body in (payload, {k: v for k, v in payload.items() if k != "think"}):
        try:
            data = json.dumps(body).encode()
            req = urllib.request.Request(url, data=data,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=600) as r:
                return json.loads(r.read()).get("response", "")
        except Exception as e:
            last = e
            continue
    return f"__ERROR__ {last}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instances", default="A,B,C")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--stamp", default="UNSTAMPED")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--providers", default=",".join(PROVIDERS))
    args = ap.parse_args()

    if not OLLAMA_HOST:
        print("=== Cross-provider §6 replication: SKIPPED (OLLAMA_HOST unset) ===")
        return 3
    try:
        with urllib.request.urlopen(f"{OLLAMA_HOST}/api/tags", timeout=8):
            pass
    except Exception as e:
        print(f"=== Cross-provider §6 replication: SKIPPED (ollama unreachable: {e}) ===")
        return 3

    provs = [p.strip() for p in args.providers.split(",") if p.strip()]
    instances = [s.strip() for s in args.instances.split(",") if s.strip()]
    cases_by_inst = {}
    for x in instances:
        cs = RU.load_probe(x)
        if args.limit:
            cs = cs[:args.limit]
        cases_by_inst[x] = cs

    OUTDIR.mkdir(parents=True, exist_ok=True)
    tpath = OUTDIR / f"xprovider-six-{args.stamp}.jsonl"

    # results[provider][instance] = {n, errors}
    results = defaultdict(lambda: defaultdict(lambda: {"n": 0, "errors": 0, "forks_wrong": defaultdict(int)}))
    # per-case predictions for convergence: preds[(inst,id)][provider] = [pred,...]
    preds = defaultdict(lambda: defaultdict(list))
    oracle_of = {}

    with tpath.open("w", buffering=1) as tr:
        for prov in provs:
            model = PROVIDERS.get(prov, prov)
            print(f"\n### provider={prov}  model={model}", flush=True)
            for x in instances:
                for rep in range(args.reps):
                    for c in cases_by_inst[x]:
                        prompt = c["system"] + "\n\n" + c["user"]
                        raw = ollama_call(model, prompt)
                        good, pred = RU.score(c, raw)
                        cell = results[prov][x]
                        cell["n"] += 1
                        if not good:
                            cell["errors"] += 1
                            cell["forks_wrong"][c["fork"]] += 1
                        key = (x, c["id"])
                        preds[key][prov].append(pred)
                        oracle_of[key] = c["oracle"]
                        tr.write(json.dumps({
                            "provider": prov, "model": model, "instance": x, "id": c["id"],
                            "fork": c["fork"], "rep": rep, "oracle": c["oracle"],
                            "pred": pred, "correct": good,
                            "raw_tail": RU._tail_after_answer(raw).strip().replace("\n", " ")[:120],
                        }) + "\n")
                cell = results[prov][x]
                print(f"  [{prov}/{x}] error {cell['errors']}/{cell['n']}", flush=True)

    # ---- convergence analysis: per case, the MAJORITY wrong reading across providers ----
    # For each case, take each provider's modal prediction; among providers that ERR, how
    # concentrated are they on a single wrong option? (shared blind spot vs decorrelated)
    def modal(lst):
        if not lst:
            return None
        return max(set(lst), key=lst.count)

    convergence = []
    for key, by_prov in sorted(preds.items()):
        oracle = oracle_of[key]
        prov_modal = {p: modal(v) for p, v in by_prov.items()}
        wrong = {p: m for p, m in prov_modal.items() if m is not None and m != oracle}
        if not wrong:
            continue
        # most common single wrong option among the erring providers
        vals = list(wrong.values())
        top = modal(vals)
        share = vals.count(top) / len(vals)
        convergence.append({
            "case": f"{key[0]}/{key[1]}", "oracle": oracle,
            "n_providers_err": len(wrong), "n_providers_total": len(prov_modal),
            "top_wrong_reading": top, "convergence_on_top": round(share, 2),
            "per_provider": prov_modal,
        })

    # summary numbers
    summary = {}
    for prov in provs:
        tot_n = sum(results[prov][x]["n"] for x in instances)
        tot_e = sum(results[prov][x]["errors"] for x in instances)
        summary[prov] = {
            "model": PROVIDERS.get(prov, prov),
            "by_instance": {x: {"errors": results[prov][x]["errors"], "n": results[prov][x]["n"],
                                "forks_wrong": dict(results[prov][x]["forks_wrong"])}
                            for x in instances},
            "total": {"errors": tot_e, "n": tot_n,
                      "rate": RU.wilson(tot_e, tot_n)[0] if tot_n else None},
        }

    out = {
        "stamp": args.stamp, "reps": args.reps, "instances": instances,
        "providers": {p: PROVIDERS.get(p, p) for p in provs},
        "summary": summary, "convergence": convergence,
    }
    rpath = OUTDIR / f"xprovider-six-{args.stamp}.json"
    rpath.write_text(json.dumps(out, indent=2))
    print(f"\n  transcript -> {tpath}\n  results -> {rpath}")
    # headline convergence: among cases where >=2 providers err, mean convergence-on-top
    multi = [c for c in convergence if c["n_providers_err"] >= 2]
    if multi:
        mean_conv = sum(c["convergence_on_top"] for c in multi) / len(multi)
        print(f"  cases with >=2 providers erring: {len(multi)}; "
              f"mean convergence on a single wrong reading = {round(mean_conv, 2)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
