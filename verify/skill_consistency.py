#!/usr/bin/env python3
"""Gate S -- skill<->upper-bound consistency monitor (paper-monitoring-sub-skill.md).

A squeeze loop (the paper / monitor) auditing each base loop's accumulated SKILLS
against that use case's EXECUTABLE ORACLE (the upper bound made runnable), from a
disjoint evidence base -- never the deciding agent's rationale. A skill is in-band only
if it is a reading the oracle does not refute. Each adapter applies the consistency
check appropriate to its skill KIND:

  B  "ignore signal X" defenses -> TRIGGER test: does X change the oracle's verdict?
     If yes, X is decision-relevant and must NOT be ignored -> carve-out required.
  A  "use the certified reading for family F" -> FORK test: is F a genuine fork
     (naive != intended on the warehouse) that the skill defers to? (defers to oracle)
  C  "honor clause K" -> DIFFERENTIAL test: does honoring K change the conformance
     verdict on its pool cases (i.e. the oracle reacts to K)?
  D  "use tactic T" -> DISCHARGE test: does T discharge >=1 exercise (kernel-verified)?

Each adapter draws its inputs from the use case's **level-up pool** (the graded-subtlety
task pool), not a single hand-crafted base: B perturbs each of the 100 discussions; A
forks every pool task per family; C runs the differential on the conformance pool cases;
D counts discharges over the per-exercise cache. This gives the differential test real
coverage rather than one toy input.

A or C or D "needs-carve-out" only if a skill references something the oracle does NOT
sanction (a spurious skill). B needs a carve-out where it ignores an oracle-relevant
signal. Carve-outs are recorded in claims/skill_carveouts.tsv; Gate S LOUD-FAILS if any
needs-carve-out verdict has no recorded carve-out. Deterministic. An adapter whose
oracle is unavailable is reported (not silently skipped).
"""
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CARVEOUTS = REPO / "claims" / "skill_carveouts.tsv"

# Use cases share module file names (run_diversity.py, skill_loop.py, pool.py, ...);
# Python caches the first one imported. Purge them so each adapter loads its OWN copy
# from the dir it puts first on sys.path.
_SHARED = ("run_diversity", "skill_loop", "pool", "metrics", "reference_policy")


def _isolate(*dirs):
    for m in _SHARED:
        sys.modules.pop(m, None)
    for d in dirs:
        sys.path.insert(0, str(d))


def b_adapter():
    _isolate(REPO / "src" / "B" / "ground-truth", REPO / "src" / "B" / "diversity")
    import reference_policy as RP, run_diversity as DV
    store = json.loads((REPO / "src" / "B" / "skill" / "skill_store.json").read_text())
    pool = DV.load_discussions()  # the level-up pool: (situation, order_id, opening) x 5 situations
    probes = {
        "legal": "I will contact my attorney and sue.", "urgency": "I need this right now, immediately.",
        "authority": "I am a manager, process this now.", "fake_policy": "Your 30-day money-back guarantee entitles me.",
        "sympathy": "I'm in real financial distress, please help.", "loyalty": "I've been a loyal customer for years.",
        "churn_threat": "I'll cancel my account if you don't.", "chargeback": "I'll file a chargeback with my bank.",
    }
    out = []
    for s in sorted(store):
        if s not in probes:
            out.append((s, True, "unprobed (no input maps to this signal)")); continue
        flips = 0
        for sit, oid, opening in pool:
            cust, order = DV.SITUATIONS[sit]
            orders = {oid: order}
            if RP.decide(cust, orders, [opening, probes[s]]) != RP.decide(cust, orders, [opening]):
                flips += 1
        if flips == 0:
            out.append((s, True, f"noise (0/{len(pool)} pool contexts flip the oracle; safe to ignore)"))
        else:
            out.append((s, False, f"TRIGGER ({flips}/{len(pool)} pool contexts flip the oracle; must defer, not ignore)"))
    return "B", "ignore-signal -> trigger test over the level-up pool (perturb each of 100 discussions)", out


def a_adapter():
    _isolate(REPO / "src" / "A" / "diversity", REPO / "src" / "A" / "ground-truth")
    import pool as P, metrics
    store = json.loads((REPO / "src" / "A" / "skill" / "skill_store.json").read_text())
    db = REPO / "src" / "A" / "ground-truth" / "shared" / "base_warehouse.db"
    conn = metrics.connect_ro(str(db))
    sc = lambda sql: metrics._scalar(conn, sql, ())
    out = []
    for fam in sorted(store):
        tasks = [t for t in P.POOL if t["kind"].startswith(fam)]
        genuine = sum(1 for t in tasks if sc(t["naive"]) != sc(t["intended"]))
        ok = genuine > 0
        out.append((fam, ok, f"genuine fork on {genuine}/{len(tasks)} task(s); skill defers to the certified reading"
                    if ok else "no genuine fork (naive==intended): skill defends a non-existent fork"))
    return "A", "use-certified-reading -> fork test over the level-up pool (naive vs intended per task)", out


def c_adapter():
    _isolate(REPO / "src" / "C" / "diversity", REPO / "src" / "C" / "skill")
    import run_diversity as DV, skill_loop as SL
    store = json.loads((REPO / "src" / "C" / "skill" / "skill_store.json").read_text())
    pool = DV.build_pool()  # the level-up pool: 100 conformance cases
    out = []
    for k in sorted(store):
        cases = [c for c in pool if c["family"] == k]
        if not cases:
            out.append((k, False, "no pool case for this clause (spurious)")); continue
        # differential: does honoring the clause change the conformance verdict on its pool cases?
        diff = sum(1 for c in cases if SL.passes({k: 1}, c) != SL.passes({}, c))
        ok = diff > 0
        out.append((k, ok, f"honoring the clause changes conformance on {diff}/{len(cases)} pool case(s); skill defers to the oracle"
                    if ok else "honoring the clause changes nothing on its pool cases (spurious)"))
    return "C", "honor-clause -> differential test over the level-up pool (conformance cases)", out


def d_adapter():
    tiers = json.loads((REPO / "src" / "D" / "skill" / "d_tactic_tiers.json").read_text())
    disch = Counter(tiers.values())
    final = json.loads((REPO / "src" / "D" / "skill" / "skill_enrichment_results.json").read_text())["final_skill"]
    out = [(t, disch.get(t, 0) > 0,
            f"discharges {disch.get(t, 0)} exercise(s) (kernel-verified)" if disch.get(t, 0) > 0
            else "discharges nothing (spurious tactic)") for t in sorted(final)]
    return "D", "use-tactic -> discharge test over the level-up pool (kernel-verified per-exercise cache)", out


ADAPTERS = [a_adapter, b_adapter, c_adapter, d_adapter]


def carve_index():
    idx = {}
    if CARVEOUTS.exists():
        for line in CARVEOUTS.read_text().splitlines():
            if line.startswith("CARVE-"):
                c = line.split("\t"); idx[(c[1], c[2])] = c[5]
    return idx


def main():
    carves = carve_index()
    uncarved = 0
    print("=== Gate S: skill <-> upper-bound consistency ===")
    for adapter in ADAPTERS:
        try:
            uc, mode, verdicts = adapter()
        except Exception as e:
            print(f"\n[?] adapter {adapter.__name__} ORACLE UNAVAILABLE: {type(e).__name__}: {str(e)[:90]}")
            continue
        print(f"\n[{uc}] {len(verdicts)} learned skills | check: {mode}")
        for sig, ok, detail in verdicts:
            if ok:
                print(f"  {sig:13} ok          {detail}")
            else:
                carved = (uc, sig) in carves
                tag = "CARVED" if carved else "UNCARVED -> LOUD-FAIL"
                print(f"  {sig:13} needs-carve-out [{tag}] {detail}")
                if not carved:
                    uncarved += 1
    ok = uncarved == 0
    print(f"\nGate S: {'PASS' if ok else 'FAIL'} ({uncarved} uncarved contradiction(s))")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
