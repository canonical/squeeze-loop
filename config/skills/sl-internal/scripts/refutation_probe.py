#!/usr/bin/env python3
"""refutation_probe.py — the exemption-refutation gate (addendum spec A2).

The dominant live coherent-and-wrong is RELABELING: a producer meets a principle by
parking in-scope work in an exempt bucket (residual / out-of-scope / BLOCKED /
"tool limitation") instead of doing it. The fix is to attach, to every exemption,
the CONSTRUCTIVE NEGATION of its claim — supply the thing the exemption says is
impossible (the missing antecedent, the absent input, the unsupported construct) and
re-run the oracle:

  * an exemption with NO attached probe evidence  -> gate failure (say-so, not proof)
  * kind = non_entailed (something is MISSING from scope):
        supply it, re-run. If the verdict FLIPS to discharged -> the work was doable
        -> REJECT (unfinished, relabeled). If it does not flip -> genuine.
  * kind = incomplete (ENTAILED, nothing missing; this oracle just cannot close it):
        no probe can fire, so the default does not apply; settle ONLY by a positive
        disjoint witness (a stronger oracle that discharges it, or a human/proof).
        No witness -> treated as relabeling -> REJECT.

This is domain-generic: the oracle is not run here; the descriptor carries the
oracle's recorded verdicts, exactly as a gate consumes an oracle it does not own.

Usage:  refutation_probe.py <exemptions.json>     # gate a set of exemptions
        refutation_probe.py --selftest            # calibrate: catch fakes, pass genuine
Exit 0 = every exemption genuine; 1 = at least one REJECT/FAIL; 2 = usage error.

Descriptor schema (exemptions.json):
  {"exemptions": [
     {"id": "...",
      "kind": "non_entailed" | "incomplete",
      "probe_supplied": true|false,        # was the constructive negation attached?
      "oracle_with_probe": "discharged" | "refuted" | "unknown" | null,
      "witness": "<stronger-oracle|human|proof reference>" | null}]}
"""
import json
import sys


def gate(exemptions):
    """Return a list of (id, status, message). status in PASS|REJECT|FAIL."""
    out = []
    for e in exemptions:
        eid = e.get("id", "<unnamed>")
        kind = e.get("kind")
        if kind == "non_entailed":
            if not e.get("probe_supplied"):
                out.append((eid, "FAIL",
                            "non_entailed exemption with NO attached probe — say-so, not proof"))
                continue
            verdict = e.get("oracle_with_probe")
            if verdict == "discharged":
                out.append((eid, "REJECT",
                            "supplying the claimed-missing piece DISCHARGED the goal — "
                            "the work was doable; exemption false, unfinished"))
            elif verdict in ("refuted", "unknown"):
                out.append((eid, "PASS",
                            "probe supplied; verdict did not flip — genuine non-entailment"))
            else:
                out.append((eid, "FAIL",
                            f"non_entailed exemption missing oracle_with_probe verdict ({verdict!r})"))
        elif kind == "incomplete":
            if e.get("witness"):
                out.append((eid, "PASS",
                            f"entailed-but-unreachable, settled by disjoint witness: {e['witness']}"))
            else:
                out.append((eid, "REJECT",
                            "incomplete (entailed, nothing missing) with NO disjoint witness — "
                            "treated as relabeling until a stronger oracle or human/proof witnesses it"))
        else:
            out.append((eid, "FAIL", f"unknown exemption kind {kind!r}"))
    return out


def report(title, results):
    bad = [r for r in results if r[1] in ("REJECT", "FAIL")]
    mark = {"PASS": "ok ", "REJECT": "XX ", "FAIL": "XX "}
    print(f"\n{title}")
    print("=" * 64)
    for eid, status, msg in results:
        print(f"  {mark.get(status, '   ')}{status:<7} {eid}: {msg}")
    print("=" * 64)
    print(f"  {len(bad)} REJECT/FAIL / {len(results)} exemptions\n")
    return bool(bad)


def selftest():
    cases = [
        {"id": "fake-missing-hyp", "kind": "non_entailed", "probe_supplied": True,
         "oracle_with_probe": "discharged"},          # expect REJECT
        {"id": "genuine-non-entail", "kind": "non_entailed", "probe_supplied": True,
         "oracle_with_probe": "refuted"},              # expect PASS
        {"id": "no-probe", "kind": "non_entailed", "probe_supplied": False,
         "oracle_with_probe": None},                   # expect FAIL
        {"id": "incomplete-witnessed", "kind": "incomplete", "witness": "lean4 discharged it"},  # PASS
        {"id": "incomplete-bare", "kind": "incomplete", "witness": None},  # expect REJECT
    ]
    results = gate(cases)
    got = {eid: status for eid, status, _ in results}
    expect = {"fake-missing-hyp": "REJECT", "genuine-non-entail": "PASS", "no-probe": "FAIL",
              "incomplete-witnessed": "PASS", "incomplete-bare": "REJECT"}
    report("REFUTATION PROBE — selftest", results)
    ok = got == expect
    print("selftest:", "PASS — gate discriminates (catches fakes, passes genuine)" if ok
          else f"FAIL — got {got} expected {expect}")
    return 0 if ok else 1


def main():
    args = sys.argv[1:]
    if args == ["--selftest"]:
        sys.exit(selftest())
    if len(args) != 1:
        print("usage: refutation_probe.py <exemptions.json> | --selftest")
        sys.exit(2)
    doc = json.load(open(args[0]))
    failed = report(f"REFUTATION PROBE — {args[0]}", gate(doc.get("exemptions", [])))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
