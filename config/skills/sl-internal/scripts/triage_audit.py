#!/usr/bin/env python3
"""triage_audit.py — audit the coordinator's own triage rule (addendum spec B7).

A "skip the cheap inputs" fast-path triages by ONE signal and is exactly the
ignore-signal kind of heuristic (sl-monitoring-sl): it can systematically drop a
whole class of real work because it ignores a SECOND signal the input carries. The
monitor's remit therefore extends past the producers' learned skills to the
coordinator's own triage rule. The sharpest way to expose an over-broad triage is a
COMPARISON AGAINST GROUND TRUTH (a reference set): wherever the triage said "nothing
to do" but the reference shows real work, the rule dropped real work — carve it to
honor the missed signal, accepting the wider fan-out that buys back the coverage.

This is the ignore-signal -> trigger-test -> carve-out pattern (Gate S) applied to
the coordinator's triage instead of a producer's skill. It also reports the flag
rate so the audit itself is calibrated (discriminating: 0 < flagged < total).

Usage:  triage_audit.py <descriptor.json>   # audit a triage rule vs a reference set
        triage_audit.py --selftest          # calibrate
Exit 0 = no real work dropped; 1 = the rule drops real work (carve it); 2 = usage.

Descriptor schema:
  {"triage":    {"<item>": "skip" | "process", ...},
   "reference": {"<item>": true | false, ...}}     # true = the item carries real work
"""
import json
import sys


def gate(triage, reference):
    """Return (missed, processed_empty, flagged, total_skipped, messages)."""
    missed = sorted(i for i, d in triage.items()
                    if d == "skip" and reference.get(i) is True)
    skipped = [i for i, d in triage.items() if d == "skip"]
    # informational: processed an item with no real work (fan-out cost, not a defect)
    processed_empty = sorted(i for i, d in triage.items()
                             if d == "process" and reference.get(i) is False)
    return missed, processed_empty, len(missed), len(skipped)


def report(title, triage, reference):
    missed, processed_empty, flagged, total_skipped = gate(triage, reference)
    print(f"\n{title}\n" + "=" * 64)
    for i in missed:
        print(f"  XX DROPPED  triage skipped '{i}' but the reference shows real work — "
              f"carve the rule to honor the missed signal")
    if not missed:
        print("  ok          triage dropped no real work the reference reveals")
    band = "rubber-stamp/none" if (total_skipped and flagged == 0) else \
           ("saturated" if (total_skipped and flagged == total_skipped) else "discriminating")
    print("=" * 64)
    print(f"  dropped-real-work {flagged}/{total_skipped} skipped  (band: {band}); "
          f"processed-empty {len(processed_empty)} (fan-out cost)\n")
    return bool(missed)


def selftest():
    triage = {"big-1": "process", "cheap-2": "skip", "cheap-3": "skip", "cheap-4": "skip"}
    reference = {"big-1": True, "cheap-2": False, "cheap-3": True, "cheap-4": False}
    #            cheap-3 looks cheap by the one signal but carries a second-signal real work
    failed = report("TRIAGE AUDIT — selftest", triage, reference)
    missed, _, _, _ = gate(triage, reference)
    ok = (missed == ["cheap-3"]) and failed
    print("selftest:", "PASS — caught the dropped real-work class (cheap-3)" if ok else f"FAIL — missed={missed}")
    return 0 if ok else 1


def main():
    args = sys.argv[1:]
    if args == ["--selftest"]:
        sys.exit(selftest())
    if len(args) != 1:
        print("usage: triage_audit.py <descriptor.json> | --selftest")
        sys.exit(2)
    d = json.load(open(args[0]))
    failed = report(f"TRIAGE AUDIT — {args[0]}", d.get("triage", {}), d.get("reference", {}))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
