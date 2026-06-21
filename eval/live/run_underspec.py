#!/usr/bin/env python3
"""Unified live underspecification probe for instances A, B, C.

Each instance's src/<X>/ground-truth/probe_cases.py exposes build_cases() -> [case],
where every `oracle` is DERIVED from that instance's executable ground truth (A: computed
from inline rows the metrics.py way; B: reference_policy.decide; C: reference_server
dispatch). This runner gives a capable model ONLY the prose upper bound + the case, lets it
reason, parses its ANSWER, and scores it against the oracle -- the §6 "does the richer upper
bound make a capable model err?" measurement, generalised from B to A and C.

Non-deterministic -> logged under verify/reports/live/, NEVER gated. No backend reachable
=> loud SKIP (exit 3); nothing fabricated. Backend selected by model_client (Ollama if
OLLAMA_HOST+CROSS_MODEL set -- the cross-provider capable model -- else Anthropic).
"""
import argparse
import importlib.util
import json
import math
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import model_client as MC

OUTDIR = REPO / "verify" / "reports" / "live"


def load_probe(x):
    gt = REPO / "src" / x / "ground-truth"
    sys.path.insert(0, str(gt))           # so its `import metrics`/`reference_policy` resolve
    spec = importlib.util.spec_from_file_location(f"probe_{x}", gt / "probe_cases.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.build_cases()


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (round(p, 3), round((c - h) / d, 3), round((c + h) / d, 3))


def _tail_after_answer(raw):
    up = (raw or "")
    i = up.upper().rfind("ANSWER:")
    return up[i + 7:] if i >= 0 else up


def parse_categorical(raw, options):
    """First option token to appear after the final ANSWER:, else last anywhere.
    Single-letter options (A/B/C...) are matched on word boundaries so a stray
    letter inside a word (e.g. the 'A' in 'Apparently') does not false-match."""
    single = all(len(o) == 1 for o in options)
    tail = _tail_after_answer(raw)
    if single:
        for tok in re.findall(r"\b([A-Za-z])\b", tail):
            if tok.upper() in [o.upper() for o in options]:
                return next(o for o in options if o.upper() == tok.upper())
        return None
    tU = tail.upper()
    hits = [(o, tU.find(o.upper())) for o in options if o.upper() in tU]
    if hits:
        return min(hits, key=lambda h: h[1])[0]
    whole = (raw or "").upper()
    hits = [(o, whole.rfind(o.upper())) for o in options if o.upper() in whole]
    return max(hits, key=lambda h: h[1])[0] if hits else None


_NUM = re.compile(r"-?\$?\s?\d[\d,]*(?:\.\d+)?")


def parse_numeric(raw):
    # require an explicit ANSWER: line -- never scrape a number out of the reasoning
    # (that mistakes a truncated/unfinished reply for a wrong answer).
    up = (raw or "")
    if "ANSWER:" not in up.upper():
        return None
    tail = up[up.upper().rfind("ANSWER:") + 7:]
    m = _NUM.search(tail)
    return m.group(0).replace("$", "").replace(",", "").strip() if m else None


def score(case, raw):
    if case.get("options"):
        pred = parse_categorical(raw, case["options"])
        ok = pred is not None and pred == case["oracle"]
        return ok, (pred if pred is not None else "UNPARSED")
    pred = parse_numeric(raw)
    if pred is None:
        return False, "UNPARSED"
    try:
        ok = abs(float(pred) - float(case["oracle"])) < 0.005
    except ValueError:
        return False, pred
    return ok, pred


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instances", default="A,B,C")
    ap.add_argument("--reps", type=int, default=1)
    ap.add_argument("--stamp", default="UNSTAMPED")
    ap.add_argument("--limit", type=int, default=0, help="cap cases per instance (0=all)")
    args = ap.parse_args()

    ok, reason = MC.available()
    if not ok:
        print("=== Underspecification probe: SKIPPED ===")
        print(f"  model client unavailable: {reason}")
        print("  Set OLLAMA_HOST+CROSS_MODEL (cross-provider) or ANTHROPIC_API_KEY. Nothing fabricated.")
        return 3
    model = MC.CROSS_MODEL if MC._backend() == "ollama" else "anthropic"
    print(f"=== Live underspecification probe (A/B/C) — {reason} ===")

    OUTDIR.mkdir(parents=True, exist_ok=True)
    tpath = OUTDIR / f"underspec-{args.stamp}.jsonl"
    results = {}
    with tpath.open("w", buffering=1) as tr:   # line-buffered: readable live
        for x in [s.strip() for s in args.instances.split(",") if s.strip()]:
            cases = load_probe(x)
            if args.limit:
                cases = cases[:args.limit]
            n = errs = 0
            forks_wrong = {}
            for rep in range(args.reps):
                for c in cases:
                    raw = MC.call_model(model, c["system"], c["user"])
                    good, pred = score(c, raw)
                    n += 1
                    # for A (numeric), classify a wrong answer: did it land on a KNOWN
                    # wrong-reading value (a genuine interpretation fork) or elsewhere?
                    matched = None
                    if not good and pred not in (None, "UNPARSED") and c.get("wrong_readings"):
                        for label, val in c["wrong_readings"].items():
                            try:
                                if abs(float(pred) - float(val)) < 0.005:
                                    matched = label
                                    break
                            except (ValueError, TypeError):
                                pass
                    if not good:
                        errs += 1
                        forks_wrong[c["fork"]] = forks_wrong.get(c["fork"], 0) + 1
                    tr.write(json.dumps({
                        "instance": x, "id": c["id"], "fork": c["fork"], "rep": rep,
                        "oracle": c["oracle"], "pred": pred, "correct": good,
                        "matched_wrong_reading": matched,
                        "raw_tail": _tail_after_answer(raw).strip().replace("\n", " ")[:120],
                    }) + "\n")
                    print(f"    {c['id']:<34} oracle={c['oracle']!s:<16} pred={pred!s:<16} "
                          f"{'OK' if good else 'WRONG'}", flush=True)
            rate = wilson(errs, n)
            results[x] = {"n": n, "errors": errs, "error_rate": rate, "forks_wrong": forks_wrong}
            p, lo, hi = rate
            print(f"  [{x}] error {errs}/{n} = {p} [{lo},{hi}]   forks_wrong={forks_wrong}")

    tot_n = sum(r["n"] for r in results.values())
    tot_e = sum(r["errors"] for r in results.values())
    print(f"  [ALL] error {tot_e}/{tot_n} = {wilson(tot_e, tot_n)[0]}")

    report = OUTDIR / f"underspec-{args.stamp}.md"
    report.write_text(
        f"# Live underspecification probe (A/B/C) — {args.stamp}\n\n"
        f"- model: {model} (backend {MC._backend()})\n- reps: {args.reps}\n"
        f"- transcript: `{tpath.name}`\n\n"
        "Capable model given ONLY the (enriched) prose upper bound + an underspecified case; "
        "error = its reading != the executable oracle (A computed from inline rows; B "
        "reference_policy.decide; C reference_server dispatch). Non-deterministic; logged, NOT "
        "gated.\n\n## Per-instance error rate (with Wilson 95% CI)\n\n```\n"
        + json.dumps(results, indent=2) + "\n```\n"
        f"\nAggregate: {tot_e}/{tot_n} = {wilson(tot_e, tot_n)[0]}.\n")
    print(f"\n  transcript -> {tpath}\n  report -> {report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
