#!/usr/bin/env python3
"""Run the adversary-strategy LADDER for Use Case B (level-up-B.md).

For each rung: compute the INTENDED action from the certified policy
(reference_policy.decide -- the answer key), then run each FORK (a vulnerable bot
that caves to that attack class). A fork is CAUGHT when its action diverges from
the intended action -- the coherent-and-wrong decision an independent exerciser
(deciding from the policy alone, immune to the manipulation) detects.

A "good bot" sanity (the reference policy itself) must AGREE with intended on every
rung -- the squeeze must not false-positive a correct bot.

Verdict per rung:
  PASS  every fork diverges from intended (all manipulations caught)
  GAP   some fork happens to land on the intended action (not separated) -- reported
        honestly, never hidden.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))            # reference_policy.py
sys.path.insert(0, str(HERE / "ladder"))  # ladder.py
import reference_policy as RP
import ladder as L


def main():
    print("=== Use Case B adversary-strategy ladder (level-up-B) ===")
    rows, gap = [], False
    for r in L.RUNGS:
        cust, orders, msgs = r["customer"], r["orders"], r["messages"]
        intended = RP.decide(cust, orders, msgs)
        good = RP.decide(cust, orders, msgs)            # the honest reimplementation
        good_ok = good == intended
        forks = []
        for f in r["forks"]:
            action = f["bot"](cust, orders, msgs)
            caught = action != intended
            forks.append({"name": f["name"], "action": action, "caught": caught, "why": f["why"]})
        all_caught = all(f["caught"] for f in forks)
        verdict = "PASS" if all_caught else "GAP"
        if verdict == "GAP":
            gap = True
        rows.append({"id": r["id"], "tier": r["tier"], "name": r["name"],
                     "intended": intended, "good_bot_agrees": good_ok,
                     "verdict": verdict, "forks": forks})
        nc = sum(f["caught"] for f in forks)
        mark = "[PASS]" if verdict == "PASS" else "[GAP ]"
        print(f"{mark} {r['tier']:<10} {r['name']:<42} policy={intended:<9} "
              f"forks caught {nc}/{len(forks)}")
        for f in forks:
            if not f["caught"]:
                print(f"        NOT CAUGHT: {f['name']} (= {intended}) -- {f['why']}")

    n_pass = sum(1 for r in rows if r["verdict"] == "PASS")
    good_all = all(r["good_bot_agrees"] for r in rows)
    print(f"\nladder: {n_pass}/{len(rows)} rungs with every manipulation caught; "
          f"good-bot agrees on all rungs: {good_all}")

    out = {
        "instance": "B-ladder",
        "rungs": len(rows),
        "rungs_all_forks_caught": n_pass,
        "good_bot_no_false_positive": good_all,
        "per_rung": [{"tier": r["tier"], "name": r["name"], "policy_action": r["intended"],
                      "verdict": r["verdict"],
                      "forks_caught": sum(f["caught"] for f in r["forks"]),
                      "forks_total": len(r["forks"])} for r in rows],
    }
    ev = HERE.parents[0] / "evidence" / "ladder_results.json"
    ev.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(f"results -> {ev}")
    # GAP is an honest coverage observation; only a good-bot false positive is a real failure.
    sys.exit(0 if good_all else 1)


if __name__ == "__main__":
    main()
