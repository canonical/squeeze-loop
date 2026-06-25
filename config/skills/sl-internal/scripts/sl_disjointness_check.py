#!/usr/bin/env python3
"""
sl_disjointness_check.py — run the mechanical squeeze-loop checks over an SL JSON
instance (sl-schema-1.0). This is the executable lower bound an sl-auditor / the
sl-monitoring-sl monitor would call: it turns the disjointness contract (C1/C2/C3
+ endogeneity) into set operations over the source registry.

Usage:  python3 sl_disjointness_check.py <loop.sl.json>            # single-loop check
        python3 sl_disjointness_check.py <controlling> <base>     # cross-loop check
Exit code 0 = all checks PASS; 1 = at least one FAIL; 2 = usage error.

In two-file mode it runs the cross-loop source-of-truth check (sl-monitoring-sl):
the controlling/monitor loop must not bound itself on any base-internal source, and
any shared source id must be the same exogenous authority in both registries.

Dimension tags match sl-auditor's numbering:
  D1 disjointness (C1)  ·  D2 barrier (C3)  ·  C2 catchability  ·
  D6 cross-loop source-of-truth (two-file mode)  ·  D8 terminus / disjoint base.
REF (referential integrity), INT (authorship: produces vs produced_by) and ENDO
(endogenous upper bound) are integrity sub-checks feeding D1; D3 (oracle existence/
immutability), D4 (gates/done) and D5/D7 are not mechanized here — they stay manual
in the audit. A checker PASS is the floor of these dimensions, never the ceiling.
"""
import json, sys


def load(path):
    with open(path) as f:
        return json.load(f)


def bound_sources(actor):
    """Every source id this actor reads from (U + L)."""
    return set(actor["upper_bound"]["sources"]) | set(actor["lower_bound"]["sources"])


def check(sl):
    src = {s["id"]: s for s in sl["sources"]}
    actors = sl["actors"]
    findings = []  # (dim, severity, status, message)

    def emit(dim, sev, status, msg):
        findings.append((dim, sev, status, msg))

    # ---- referential integrity: every referenced id exists -------------------
    for a in actors:
        for sid in bound_sources(a) | set(a["must_not_see"]) | set(a.get("produces", [])):
            if sid not in src:
                emit("REF", "CRITICAL", "FAIL", f"{a['id']} references unknown source '{sid}'")

    # ---- authorship: reconcile actor.produces with source.produced_by --------
    # Authorship is recorded on BOTH sides; they must agree, and the self-cert
    # check below must consult the UNION so neither side can hide it. A source
    # whose produced_by names an actor that does not list it in `produces` (or
    # vice versa) is an integrity gap that could otherwise mask self-judging.
    by_actor_from_pb = {}                       # actor id -> {source ids it produced_by}
    for s in sl["sources"]:
        pb = s.get("produced_by")
        if pb is not None:
            by_actor_from_pb.setdefault(pb, set()).add(s["id"])
            if pb not in {a["id"] for a in actors}:
                emit("INT", "MAJOR", "FAIL",
                     f"source '{s['id']}' produced_by unknown actor '{pb}'")
    for a in actors:
        declared = set(a.get("produces", []))
        from_pb = by_actor_from_pb.get(a["id"], set())
        mismatch = declared ^ from_pb           # symmetric difference
        if mismatch:
            emit("INT", "MAJOR", "FAIL",
                 f"{a['id']} authorship disagrees: produces={sorted(declared)} "
                 f"vs produced_by={sorted(from_pb)} (diff {sorted(mismatch)})")

    # ---- D1a self-certification: no actor judges against what it produced -----
    # Produced set = union of BOTH authorship records, so a loop cannot evade the
    # check by recording authorship only via source.produced_by.
    for a in actors:
        produced = set(a.get("produces", [])) | by_actor_from_pb.get(a["id"], set())
        overlap = produced & bound_sources(a)
        if overlap:
            emit("D1", "CRITICAL", "FAIL",
                 f"{a['id']} certifies its own work: bound reads self-produced {sorted(overlap)}")
        else:
            emit("D1", "-", "PASS", f"{a['id']} reads no source it produced")

    # ---- D1b pairwise-distinct (U-set, L-set) pairs --------------------------
    seen = {}
    for a in actors:
        key = (frozenset(a["upper_bound"]["sources"]), frozenset(a["lower_bound"]["sources"]))
        if key in seen and key != (frozenset(), frozenset()):
            emit("D1", "MAJOR", "FAIL",
                 f"{a['id']} and {seen[key]} hold an identical (U,L) pair (shared evidence)")
        seen.setdefault(key, a["id"])

    # ---- D1c single-pair-suffices (C1 subtle half, structural floor) ----------
    # C1 demands no single (U,L) certifies the deliverable. Fully deciding this is
    # semantic, but one structural necessary condition IS checkable: no substantive
    # certifying actor may read a SUPERSET of every other actor's evidence. If one
    # actor's bound sources contain every other actor's (strictly for at least one),
    # that actor alone reads all the evidence anyone holds — a single-pair-suffices
    # smell. Editorial / terminal roles are excluded: their reading legitimately
    # spans the spec but their certification is Gate A / human, not a hard verdict.
    # This is a floor, not a decision (see the skill).
    NON_CERTIFYING = ("coordinator", "auditor", "human_terminus", "disjoint_base", "sub_loop")
    bs = {a["id"]: bound_sources(a) for a in actors}
    for a in actors:
        if a["role"] in NON_CERTIFYING or not bs[a["id"]]:
            continue
        others = [b for b in actors if b["id"] != a["id"]]
        if (others and all(bs[b["id"]] <= bs[a["id"]] for b in others)
                and any(bs[b["id"]] < bs[a["id"]] for b in others)):
            emit("D1", "MAJOR", "FAIL",
                 f"{a['id']} reads a superset of every other actor's evidence "
                 f"{sorted(bs[a['id']])}: a single pair may suffice to certify (confirm manually)")

    # ---- D2 barrier consistency ----------------------------------------------
    # (a) no source is both must_not_see and a bound source (a contradiction)
    # (b) a judge must not READ an artifact it is barriered from. Running an
    #     executable_oracle over that artifact is allowed; reading it is not.
    for a in actors:
        barr = set(a["must_not_see"])
        leaked = barr & bound_sources(a)
        if leaked:
            emit("D2", "CRITICAL", "FAIL",
                 f"{a['id']} both bars and reads {sorted(leaked)} (honorary barrier / contradiction)")
        # judge reading a rationale source is always a barrier breach
        rationale_read = {s for s in bound_sources(a) if src[s]["type"] == "rationale"}
        if rationale_read:
            emit("D2", "CRITICAL", "FAIL",
                 f"{a['id']} reads a producer rationale {sorted(rationale_read)} as a bound")
        if not leaked and not rationale_read:
            emit("D2", "-", "PASS", f"{a['id']} barriers are consistent with its bounds")

    # ---- D2 missing-required barrier (honorary-by-omission) ------------------
    # The earlier check catches a *contradicted* barrier (bars-and-reads); this
    # catches a *missing* one. Role-keyed expectation: the actors who judge the
    # implementation must be physically denied it. Any artifact produced by an
    # `implementer` is an implementation artifact; every `property_author` and
    # `exerciser` must list it in must_not_see. The checker cannot credit a barrier
    # that is not declared, so an undeclared barrier on this load-bearing edge is
    # the honorary-by-omission collapse.
    impl_artifacts = {s["id"] for s in sl["sources"]
                      if s["type"] == "artifact"
                      and any(a["id"] == s.get("produced_by") and a["role"] == "implementer"
                              for a in actors)}
    JUDGE_ROLES = ("property_author", "exerciser")
    for a in actors:
        if a["role"] in JUDGE_ROLES and impl_artifacts:
            missing = impl_artifacts - set(a["must_not_see"])
            if missing:
                emit("D2", "MAJOR", "FAIL",
                     f"{a['id']} ({a['role']}) does not barrier the implementation "
                     f"{sorted(missing)} (honorary-by-omission; add to must_not_see)")

    # ---- Endogeneity: a soft_authority read off the artifact under test ------
    # Endogenous U is LEGITIMATE BUT MUST BE DECLARED. A PASS against an endogenous
    # upper bound certifies self-consistency, not conformance (an inferred spec /
    # architectural audit reads its U off the very artifact it will judge). So:
    #   declared (the source id OR the reading actor id is in endogeneity_flags)
    #     => acknowledged INFO; the PASS is recorded as self-consistency.
    #   undeclared => FAIL: the loop is silently passing self-consistency off as
    #     conformance, which is exactly what the flag exists to surface.
    declared = set(sl["disjointness"].get("endogeneity_flags", []))
    for a in actors:
        endo = {s for s in a["upper_bound"]["sources"]
                if src.get(s, {}).get("provenance") == "endogenous"}
        if not endo:
            continue
        undeclared = {s for s in endo if s not in declared and a["id"] not in declared}
        if undeclared:
            emit("ENDO", "MAJOR", "FAIL",
                 f"{a['id']} has UNDECLARED endogenous U {sorted(undeclared)}: a PASS is "
                 f"self-consistency, not conformance — declare it in endogeneity_flags")
        ack = endo - undeclared
        if ack:
            emit("ENDO", "-", "INFO",
                 f"{a['id']} endogenous U {sorted(ack)} declared: PASS certifies self-consistency, not conformance")
    # stale flags: an entry that names neither a known source nor a known actor
    known = set(src) | {a["id"] for a in actors}
    stale = {d for d in declared if d not in known}
    if stale:
        emit("ENDO", "MINOR", "INFO",
             f"endogeneity_flags has stale entries {sorted(stale)} (no such source/actor)")

    # ---- Terminus: a human_terminus / disjoint_base must carry NO runnable L --
    for a in actors:
        if a["role"] in ("human_terminus", "disjoint_base"):
            if a["lower_bound"]["sources"]:
                emit("D8", "MAJOR", "FAIL",
                     f"{a['id']} is a terminus but claims an executable L {a['lower_bound']['sources']}")
            else:
                emit("D8", "-", "PASS", f"{a['id']} terminus correctly carries no executable L")

    # ---- C2 catchability coverage: every blind spot caught by ANOTHER actor ---
    ids = {a["id"] for a in actors}
    catch_actors = {c["actor"] for c in sl["disjointness"]["catchability"]}
    for c in sl["disjointness"]["catchability"]:
        if c["caught_by"] == c["actor"]:
            emit("C2", "CRITICAL", "FAIL", f"{c['actor']} is its own catcher (self-judging)")
        elif c["caught_by"] not in ids and c["caught_by"] not in ("external", "human"):
            emit("C2", "MAJOR", "FAIL", f"{c['actor']} caught_by unknown actor '{c['caught_by']}'")
        else:
            emit("C2", "-", "PASS", f"{c['actor']}'s blind spot caught by {c['caught_by']}")
    # producing actors with no declared catcher are a coverage gap
    producers = {a["id"] for a in actors if a.get("produces")}
    for pid in sorted(producers - catch_actors):
        emit("C2", "MINOR", "INFO", f"{pid} produces artifacts but declares no characteristic blind spot")

    return findings


def cross_loop_check(mon, base):
    """Cross-loop source-of-truth check: a controlling/monitor loop `mon` against the
    loop `base` it controls. Verifies (a) the monitor does not bound itself on any
    base-internal source (the cross-level form of self-certification / blend), and
    (b) any source id shared across the two registries is the genuinely-same
    exogenous authority — never an internal id reused with a different meaning.
    Convention: a shared source of truth carries the SAME id in both loops."""
    findings = []

    def emit(dim, sev, status, msg):
        findings.append((dim, sev, status, msg))

    msrc = {s["id"]: s for s in mon["sources"]}
    bsrc = {s["id"]: s for s in base["sources"]}

    if mon.get("monitors") not in (base["id"], None):
        emit("D6", "MINOR", "INFO",
             f"monitor.monitors='{mon.get('monitors')}' does not name base '{base['id']}'")

    # (a) the monitor must not bound itself on a base-internal source
    mbound = set()
    for a in mon["actors"]:
        mbound |= bound_sources(a)
    binternal = {s["id"] for s in base["sources"]
                 if s.get("produced_by") is not None
                 or s.get("provenance") in ("endogenous", "internal")}
    bleed = mbound & binternal
    if bleed:
        emit("D6", "CRITICAL", "FAIL",
             f"monitor bounds itself on base-internal source(s) {sorted(bleed)}: cross-level "
             f"self-certification / blend (only a sub_loop bridge row may link down)")
    else:
        emit("D6", "-", "PASS", "monitor reads no base-internal source as a bound")

    # (b) shared ids must denote the same exogenous authority
    shared = set(msrc) & set(bsrc)
    if not shared:
        emit("D6", "-", "INFO", "no shared source ids across the two registries")
    for sid in sorted(shared):
        m, b = msrc[sid], bsrc[sid]
        key_m = (m["type"], m.get("provenance"), m.get("produced_by"))
        key_b = (b["type"], b.get("provenance"), b.get("produced_by"))
        if key_m != key_b:
            emit("D6", "MAJOR", "FAIL",
                 f"shared id '{sid}' conflicts across loops: monitor {key_m} vs base {key_b}")
        elif not (m["type"] == "soft_authority" and m.get("provenance") == "exogenous"):
            emit("D6", "MAJOR", "FAIL",
                 f"shared id '{sid}' is shared but is not a same exogenous authority "
                 f"({m['type']}/{m.get('provenance')}): illegitimate cross-loop sharing")
        else:
            emit("D6", "-", "PASS", f"shared id '{sid}' is the same exogenous authority (ok)")

    return findings


def report(title, findings):
    """Print a findings table; return True iff any FAIL."""
    fails = [f for f in findings if f[2] == "FAIL"]
    width = max((len(f[0]) for f in findings), default=4)
    print(f"\n{title}")
    print("=" * 64)
    for dim, sev, status, msg in findings:
        mark = {"PASS": "ok ", "FAIL": "XX ", "INFO": " i "}.get(status, "   ")
        sevtag = f"[{sev}]" if sev not in ("-",) else ""
        print(f"  {mark}{dim:<{width}}  {sevtag:<10} {msg}")
    print("=" * 64)
    print(f"  {len(fails)} FAIL / {len(findings)} checks\n")
    return bool(fails)


def main():
    args = sys.argv[1:]
    if len(args) == 1:
        sl = load(args[0])
        failed = report(f"SL DISJOINTNESS CHECK — {sl['id']}  (kind={sl['kind']})", check(sl))
    elif len(args) == 2:
        mon, base = load(args[0]), load(args[1])
        failed = report(
            f"SL CROSS-LOOP SOURCE-OF-TRUTH CHECK — monitor '{mon['id']}' over base '{base['id']}'",
            cross_loop_check(mon, base))
    else:
        print("usage: python3 sl_disjointness_check.py <loop.sl.json> [<base.sl.json>]")
        print("  one file  -> single-loop disjointness check (C1/C2/C3 + endogeneity)")
        print("  two files -> cross-loop source-of-truth check (controlling, then base)")
        sys.exit(2)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
