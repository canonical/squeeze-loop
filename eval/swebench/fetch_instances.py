#!/usr/bin/env python3
"""Fetch real SWE-bench-Lite instances (metadata) via the HuggingFace
datasets-server REST API -- a genuine population of real GitHub bugs, each with
held-out FAIL_TO_PASS tests. Stores a slim record per instance to
eval/swebench/instances.json.

This is the real-bug population the synthetic studies (eval/study) lacked: every
instance is, by construction, a real defect whose gold tests currently fail.
Needs host internet ONCE; the run harness then operates on the stored file.
"""

import json
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "instances.json"
N = 15
URL = ("https://datasets-server.huggingface.co/rows?dataset=princeton-nlp%2F"
       "SWE-bench_Lite&config=default&split=test&offset=0&length=" + str(N))


def _loads(x):
    return json.loads(x) if isinstance(x, str) else x


def main():
    try:
        with urllib.request.urlopen(URL, timeout=60) as r:
            data = json.load(r)
    except Exception as e:
        print(f"FETCH FAILED ({e}); leaving any existing instances.json untouched")
        return 1
    out = []
    for item in data.get("rows", []):
        row = item["row"]
        ftp = _loads(row.get("FAIL_TO_PASS", "[]"))
        ptp = _loads(row.get("PASS_TO_PASS", "[]"))
        out.append({
            "instance_id": row["instance_id"],
            "repo": row["repo"],
            "base_commit": row["base_commit"],
            "problem_statement": row.get("problem_statement", ""),
            "fail_to_pass": ftp,
            "n_fail_to_pass": len(ftp),
            "n_pass_to_pass": len(ptp),
        })
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(f"fetched {len(out)} real SWE-bench-Lite instances -> {OUT}")
    for r in out[:5]:
        print(f"  {r['instance_id']:32s} {r['repo']:22s} "
              f"FAIL_TO_PASS={r['n_fail_to_pass']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
