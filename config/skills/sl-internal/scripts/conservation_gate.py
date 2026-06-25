#!/usr/bin/env python3
"""conservation_gate.py — the conservative-transformation gate (addendum spec A6).

When a deliverable is meant to be a BOUNDED EXTENSION of its input — the producer may
only ADD content of kind X and must leave the rest Y untouched — the monitor gains a
cheap, sharp, mechanical check: strip X from the deliverable and require the
remainder to equal the original input. A mismatch means the producer altered or
fabricated Y, a coherent-and-wrong that content-level review routinely misses.

Two riders from the live run:
  * Separability precondition. The gate applies ONLY when X is mechanically separable
    from Y (the added lines are recoverable, e.g. by a marker/pattern). If the
    addition is interleaved with a reformat of Y, the strip cannot run -> DEP-UNMET,
    not a pass.
  * Trivial-input fabrication. A producer handed a trivial/empty input that returns a
    non-trivial deliverable has FABRICATED work to justify a result -> FAIL, and any
    skill/finding from that run is tainted provenance (discard it).

Domain-generic, line-based: "added X" lines are the ones matching `added_pattern`.

Usage:  conservation_gate.py <descriptor.json>   # run the gate
        conservation_gate.py --selftest          # calibrate
Exit 0 = conserved; 1 = mutation/fabrication; 2 = usage; 3 = DEP-UNMET (not separable).

Descriptor schema:
  {"original_input": "<text>",
   "deliverable":    "<text>",
   "added_pattern":  "<regex matching an ADDED (kind-X) line>"}   # required for separability
"""
import json
import re
import sys


def _is_trivial(text):
    return text.strip() == ""


def gate(original_input, deliverable, added_pattern):
    """Return (status, message). status in PASS|FAIL|DEP-UNMET."""
    # Separability precondition: need a recoverable boundary for the added content.
    if not added_pattern:
        return ("DEP-UNMET",
                "no added_pattern: X is not mechanically separable from Y — strip-and-diff "
                "cannot run; enforce conservation another way")
    rx = re.compile(added_pattern)

    # Trivial-input fabrication: empty/trivial in, non-trivial out.
    if _is_trivial(original_input) and not _is_trivial(deliverable):
        kept = [ln for ln in deliverable.splitlines() if not rx.search(ln)]
        if any(ln.strip() for ln in kept):
            return ("FAIL",
                    "trivial/empty input but the deliverable invents non-added (Y) content — "
                    "fabrication; tainted provenance: discard any skill/finding from this run")

    # Strip X, require the remainder to equal the original input.
    remainder = "\n".join(ln for ln in deliverable.splitlines() if not rx.search(ln))
    original = "\n".join(original_input.splitlines())
    if remainder == original:
        return ("PASS", "stripping added X leaves the original input unchanged (Y conserved)")
    return ("FAIL",
            "after stripping added X the remainder != original input — the producer altered or "
            "fabricated Y (a coherent-and-wrong content review misses); tainted provenance applies")


def report(title, status, msg):
    mark = {"PASS": "ok ", "FAIL": "XX ", "DEP-UNMET": " ? "}.get(status, "   ")
    print(f"\n{title}\n" + "=" * 64)
    print(f"  {mark}{status:<10} {msg}")
    print("=" * 64 + "\n")
    return {"PASS": 0, "FAIL": 1, "DEP-UNMET": 3}[status]


def selftest():
    cases = {
        "conserved":   ("a\nb",  "a\nb\n+X one\n+X two", r"^\+", "PASS"),
        "mutated-Y":   ("a\nb",  "a\nB_MUT\n+X one",     r"^\+", "FAIL"),
        "trivial-fab": ("",      "+X one\nINVENTED Y",   r"^\+", "FAIL"),
        "not-separable": ("a\nb", "a b +X (interleaved)", "",    "DEP-UNMET"),
        "empty-ok":    ("",      "+X one\n+X two",        r"^\+", "PASS"),
    }
    ok = True
    for name, (inp, deliv, pat, want) in cases.items():
        status, msg = gate(inp, deliv, pat)
        good = status == want
        ok = ok and good
        print(f"  {'ok ' if good else 'XX '}{name:<14} -> {status:<10} (want {want})")
    print("selftest:", "PASS — gate discriminates" if ok else "FAIL")
    return 0 if ok else 1


def main():
    args = sys.argv[1:]
    if args == ["--selftest"]:
        sys.exit(selftest())
    if len(args) != 1:
        print("usage: conservation_gate.py <descriptor.json> | --selftest")
        sys.exit(2)
    d = json.load(open(args[0]))
    status, msg = gate(d.get("original_input", ""), d.get("deliverable", ""), d.get("added_pattern", ""))
    sys.exit(report(f"CONSERVATION GATE — {args[0]}", status, msg))


if __name__ == "__main__":
    main()
