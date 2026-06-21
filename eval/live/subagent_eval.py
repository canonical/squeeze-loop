#!/usr/bin/env python3
"""Helper for running the A/B/C underspecification probes with CLAUDE SUBAGENTS as
the model (not the Ollama/qwen backend).

  dump  <X..>             write verify/reports/live/cases_<X>.json  = [{id,system,user,options}]
                          (NO oracle -- safe to hand to a subagent acting as the model)
  score <X> <tier>        read answers_<X>_<tier>.json ({id: answer}) and score vs the
                          oracle in src/<X>/ground-truth/probe_cases.py (build_cases()).

A subagent reads cases_<X>.json, answers each case from the prompt ALONE (no oracle/
ground-truth files), and writes answers_<X>_<tier>.json. This script never calls a model.
"""
import importlib.util
import json
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "verify" / "reports" / "live"


def load_cases(x):
    gt = REPO / "src" / x / "ground-truth"
    sys.path.insert(0, str(gt))
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


def _norm(s):
    return str(s).strip().upper().replace("ANSWER:", "").strip()


def cmd_dump(xs):
    OUT.mkdir(parents=True, exist_ok=True)
    for x in xs:
        pub = [{"id": c["id"], "system": c["system"], "user": c["user"],
                "options": c.get("options")} for c in load_cases(x)]
        (OUT / f"cases_{x}.json").write_text(json.dumps(pub, indent=2))
        print(f"{x}: {len(pub)} cases -> {OUT / f'cases_{x}.json'}")


def cmd_score(x, tier):
    cases = {c["id"]: c for c in load_cases(x)}
    ans = json.loads((OUT / f"answers_{x}_{tier}.json").read_text())
    if isinstance(ans, list):  # some subagents emit [{"id":..,"answer":..}] instead of {id:ans}
        ans = {r["id"]: r.get("answer", r.get("letter", r.get("choice")))
               for r in ans if isinstance(r, dict) and "id" in r}
    n = errs = 0
    wrong = []
    forks = {}
    for cid, c in cases.items():
        pred = ans.get(cid)
        good = pred is not None and _norm(pred) == _norm(c["oracle"])
        n += 1
        if not good:
            errs += 1
            wrong.append((cid, c["fork"], c.get("oracle_value", c["oracle"]),
                          pred, c.get("oracle")))
            forks[c["fork"]] = forks.get(c["fork"], 0) + 1
    p, lo, hi = wilson(errs, n)
    print(f"[{x}/{tier}] error {errs}/{n} = {p} [{lo},{hi}]")
    for cid, fork, ov, pred, oletter in wrong:
        print(f"    WRONG {cid:<24} fork={fork:<28} oracle={oletter}({ov}) pred={pred}")
    print(f"    forks_wrong={forks}")
    return {"instance": x, "tier": tier, "n": n, "errors": errs,
            "error_rate": [p, lo, hi], "forks_wrong": forks}


if __name__ == "__main__":
    if sys.argv[1] == "dump":
        cmd_dump(sys.argv[2:] or ["A", "B", "C"])
    elif sys.argv[1] == "score":
        cmd_score(sys.argv[2], sys.argv[3])
