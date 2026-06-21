#!/usr/bin/env python3
"""Control-gated cross-provider capability ladder: run the A/C/B probes through a
range of qwen models (Alibaba) on the Ollama host, to test whether the
capability-invariant floor (A) and capability-inversion (C) reproduce across a
SECOND, independent provider family and a wide size/generation span.

CONTROL GATE: before a model's answers count, it must pass two control probes (a
known-CONTRADICTION pair and a known-CONSISTENT pair) and emit parseable answers.
A model that fails is recorded INSUFFICIENT -- its errors would be incompetence,
not coherent-and-wrong, so they must not be read as a capability-invariant floor.

This is the opt-in CROSS-PROVIDER corroboration axis (the primary measurement stays
Claude subagents). Non-deterministic in principle; observed deterministic at temp 0.
Writes answers_<X>_<tag>.json (scored by subagent_eval.py) + a ladder report.
"""
import json
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_underspec as RU  # parse_categorical

OUT = REPO / "verify" / "reports" / "live"
HOST = "http://localhost:11434"
MODELS = ["qwen3.6:27b-mlx", "qwen3.5:27b-mlx", "qwen3.5:9b-mlx", "qwen3.5:4b-mlx"]
INSTANCES = ["A", "C", "B"]

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


def call(model, prompt, num_predict=320, timeout=300):
    payload = {"model": model, "prompt": prompt, "stream": False, "think": False,
               "options": {"temperature": 0, "num_predict": num_predict}}
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
    lines = []
    ok = True
    for expect, a, b in CONTROLS:
        p = (f'Two sentences from a paper.\nA: "{a}"\nB: "{b}"\n'
             "Do A and B contradict each other? Answer exactly CONTRADICT or CONSISTENT, "
             "then one short reason.\nAnswer:")
        got = verdict_token(call(model, p, num_predict=64, timeout=120))
        good = got == expect
        ok = ok and good
        lines.append(f"control expected {expect} got {got} -> {'OK' if good else 'FAIL'}")
    return ok, lines


def load_public(x):
    return json.loads((OUT / f"cases_{x}.json").read_text())


def main():
    report = ["# Cross-provider qwen capability ladder (control-gated) — A/C/B probes\n",
              f"host: {HOST}\n"]
    for model in MODELS:
        tag = tag_of(model)
        ok, clines = control_check(model)
        status = "PASS" if ok else "INSUFFICIENT"
        print(f"=== {model}  controls: {status} ===")
        for l in clines:
            print("   ", l)
        report.append(f"\n## {model}  ({tag})\ncontrols: {status}\n- " + "\n- ".join(clines))
        if not ok:
            report.append("  -> INSUFFICIENT: answers not collected (incompetence != coherent-and-wrong).")
            print("    -> skipping case runs (INSUFFICIENT)")
            continue
        for x in INSTANCES:
            cases = load_public(x)
            ans = {}
            unparsed = 0
            for c in cases:
                raw = call(model, c["system"] + "\n\n" + c["user"])
                pred = RU.parse_categorical(raw, c["options"])
                if pred is None:
                    pred = "UNPARSED"
                    unparsed += 1
                ans[c["id"]] = pred
            (OUT / f"answers_{x}_{tag}.json").write_text(json.dumps(ans, indent=2))
            print(f"    [{x}] {len(cases)} cases answered ({unparsed} unparsed) -> answers_{x}_{tag}.json")
            report.append(f"  - {x}: {len(cases)} cases, {unparsed} unparsed -> answers_{x}_{tag}.json")
    (OUT / "qwen-ladder-controls.md").write_text("\n".join(report) + "\n")
    print(f"\nreport -> {OUT / 'qwen-ladder-controls.md'}")


if __name__ == "__main__":
    main()
