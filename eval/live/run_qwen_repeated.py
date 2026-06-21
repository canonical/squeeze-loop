#!/usr/bin/env python3
"""Repeated-draws qwen capability ladder (control-gated) — the §6 follow-up.

§6 reports the qwen ladder as ONE draw per case (deterministic at temp 0), so it
"corroborates the floor but not finer size-ordering claims; a repeated qwen version is
future work." This is that version: each case is drawn REPS times at temperature>0 across
the qwen size/generation ladder, scored against the SAME executable oracle (build_cases),
to test whether (a) the capability-invariant FLOOR on A (active / survivorship forks) and
the C patch-null governance override survive sampling repetition, and (b) any finer
size-ordering stabilises or — as the corrected Claude C "inversion" warned — dissolves.

CONTROL GATE: before a model's draws count it must pass a known-CONTRADICTION and a
known-CONSISTENT probe (incompetence != coherent-and-wrong). A failing model is recorded
INSUFFICIENT and skipped.

Cross-provider (Alibaba), opt-in axis; the primary measurement stays Claude. All-MLX qwen
models only (fast + stable on the host; see the host-caveats memory). Non-deterministic ->
logged under verify/reports/live/, NEVER gated.

Usage:
  python3 eval/live/run_qwen_repeated.py --instances A,C,B --reps 5 --temp 0.7 --stamp 2026-06-19
"""
import argparse
import json
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_underspec as RU  # load_probe (build_cases w/ oracle+fork), score, wilson

OUT = REPO / "verify" / "reports" / "live"
HOST = "http://localhost:11434"
MODELS = ["qwen3.6:27b-mlx", "qwen3.5:27b-mlx", "qwen3.5:9b-mlx", "qwen3.5:4b-mlx"]

CONTROLS = [
    ("CONTRADICT",
     "in-house evidence comes in two coordinate strands, neither ranked above the other.",
     "the reflexive case study is the single strongest in-house evidence."),
    ("CONSISTENT",
     "the comparison is exploratory and small-n.",
     "a powered, multi-tier comparison remains future work."),
]


def tag_of(model):
    return model.replace(":", "-").replace(".", "")


def call(model, prompt, temperature, num_predict=160, timeout=300):
    payload = {"model": model, "prompt": prompt, "stream": False, "think": False,
               "options": {"temperature": temperature, "num_predict": num_predict}}
    for body in (payload, {k: v for k, v in payload.items() if k != "think"}):
        try:
            req = urllib.request.Request(f"{HOST}/api/generate",
                                         data=json.dumps(body).encode(),
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read()).get("response", "")
        except Exception:
            continue
    return ""


def verdict_token(text):
    up = (text or "").upper()
    ci, ki = up.find("CONTRADICT"), up.find("CONSISTENT")
    if ci < 0 and ki < 0:
        return "?"
    if ci < 0:
        return "CONSISTENT"
    if ki < 0:
        return "CONTRADICT"
    return "CONTRADICT" if ci < ki else "CONSISTENT"


def control_check(model):
    # controls at temp 0 (deterministic competence check)
    lines, ok = [], True
    for expect, a, b in CONTROLS:
        p = (f'Two sentences from a paper.\nA: "{a}"\nB: "{b}"\n'
             "Do A and B contradict each other? Answer exactly CONTRADICT or CONSISTENT, "
             "then one short reason.\nAnswer:")
        got = verdict_token(call(model, p, 0.0, num_predict=64, timeout=120))
        good = got == expect
        ok = ok and good
        lines.append(f"control expected {expect} got {got} -> {'OK' if good else 'FAIL'}")
    return ok, lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instances", default="A,C,B")
    ap.add_argument("--reps", type=int, default=5)
    ap.add_argument("--temp", type=float, default=0.7)
    ap.add_argument("--stamp", default="UNSTAMPED")
    ap.add_argument("--models", default=",".join(MODELS))
    ap.add_argument("--cap", type=int, default=160, help="num_predict answer cap for case draws")
    args = ap.parse_args()

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    instances = [s.strip() for s in args.instances.split(",") if s.strip()]
    cases_by = {x: RU.load_probe(x) for x in instances}
    OUT.mkdir(parents=True, exist_ok=True)
    tpath = OUT / f"qwen-repeated-{args.stamp}.jsonl"

    # results[model][inst] = {n, errors, unparsed, forks_wrong{fork:count}, fork_n{fork:count}}
    results = {}
    with tpath.open("w", buffering=1) as tr:
        for model in models:
            tag = tag_of(model)
            ok, clines = control_check(model)
            print(f"=== {model}  controls: {'PASS' if ok else 'INSUFFICIENT'} ===", flush=True)
            for l in clines:
                print("   ", l)
            if not ok:
                results[model] = {"controls": "INSUFFICIENT", "control_lines": clines}
                continue
            mres = {"controls": "PASS", "by_instance": {}}
            for x in instances:
                cell = {"n": 0, "errors": 0, "unparsed": 0,
                        "forks_wrong": defaultdict(int), "fork_n": defaultdict(int)}
                for rep in range(args.reps):
                    for c in cases_by[x]:
                        raw = call(model, c["system"] + "\n\n" + c["user"], args.temp,
                                   num_predict=args.cap)
                        good, pred = RU.score(c, raw)
                        cell["n"] += 1
                        cell["fork_n"][c["fork"]] += 1
                        if pred == "UNPARSED":
                            cell["unparsed"] += 1
                        if not good:
                            cell["errors"] += 1
                            cell["forks_wrong"][c["fork"]] += 1
                        tr.write(json.dumps({
                            "model": model, "instance": x, "id": c["id"], "fork": c["fork"],
                            "rep": rep, "oracle": c["oracle"], "pred": pred, "correct": good,
                        }) + "\n")
                p, lo, hi = RU.wilson(cell["errors"], cell["n"])
                cell["forks_wrong"] = dict(cell["forks_wrong"])
                cell["fork_n"] = dict(cell["fork_n"])
                cell["rate"] = [p, lo, hi]
                mres["by_instance"][x] = cell
                print(f"  [{x}] error {cell['errors']}/{cell['n']} = {p} "
                      f"({cell['unparsed']} unparsed)  forks_wrong={cell['forks_wrong']}", flush=True)
            results[model] = mres

    out = {"stamp": args.stamp, "reps": args.reps, "temp": args.temp,
           "models": models, "instances": instances, "results": results}
    (OUT / f"qwen-repeated-{args.stamp}.json").write_text(json.dumps(out, indent=2))
    print(f"\n  transcript -> {tpath}\n  results -> {OUT / f'qwen-repeated-{args.stamp}.json'}")


if __name__ == "__main__":
    main()
