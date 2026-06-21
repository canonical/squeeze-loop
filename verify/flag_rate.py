#!/usr/bin/env python3
"""Flag-rate calibration monitor (self-improve.md, lesson #7).

A healthy monitor discriminates: it flags a STRICT, NONEMPTY subset of what it
audits. A permanent zero is a rubber stamp (the gate has stopped checking);
flagging everything is saturation (the monitor is over-claiming, or the audited
population is uniformly bad). This monitor reads the flag counts of the paper's
other monitoring planes and asserts each one is in the discriminating band
0 < flagged < total. It also records the external-catch datum: of the defects
the loop caught in its own claims, how many needed EXTERNAL review -- the standing
reminder that the internal flag-rate is not the whole story (a producer shares its
output's blind spot; some over-reach is only catchable from a disjoint base).

Deterministic: every input (skill oracles, category markers, claim ledger, defect
log) is committed. Emits tex/macros/calibration.tex. Loud-fails on a rubber-stamp
or saturated plane, or on a zero external-catch count (which would falsely imply the
internal gates are complete).
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "verify"))
DEFECTS = REPO / "verify" / "manuscript_defects.tsv"
HISTORY = REPO / "claims" / "flag_rate_history.tsv"
MACROS = REPO / "tex" / "macros" / "calibration.tex"


def gate_s_rate():
    import gate_s_measures  # noqa: F401  (re-import is harmless; deterministic)
    import skill_consistency as GS
    skills = flagged = 0
    for adapter in GS.ADAPTERS:
        _uc, _mode, verdicts = adapter()
        skills += len(verdicts)
        flagged += sum(1 for _s, ok, _d in verdicts if not ok)
    return "Gate S (skills)", flagged, skills


def overreach_rate():
    import category_overreach as CO
    carves = CO.carved_ids()
    over = 0
    for cid, _name, marker in CO.CATEGORIES:
        cover = [X for X in CO.INSTANCES if marker(X)]
        if len(cover) < len(CO.INSTANCES):  # over-reaches (carved or not)
            over += 1
    return "category audit (categories)", over, len(CO.CATEGORIES)


def reflexive_routing_rate():
    import reflexive_gate_s as RG
    total = interpretive = 0
    for r in RG.rows():
        total += 1
        if r["type"] in ("OPN", "DEFN", "MATH") or bool(RG.INTERPRETIVE_RE.search(r["binding"])):
            interpretive += 1
    return "reflexive Gate S (claims routed)", interpretive, total


def defect_catches():
    """(total defects caught in the paper's own claims, of which external-caught)."""
    total = external = 0
    for line in DEFECTS.read_text().splitlines():
        if not line.startswith("D"):
            continue
        total += 1
        if "EXTERNAL" in line.upper():
            external += 1
    return total, external


def history_rows():
    rows = []
    for line in HISTORY.read_text().splitlines():
        if not line.strip() or line.startswith("#") or line.startswith("circle"):
            continue
        rows.append(line.split("\t"))
    return rows


def trajectory_check(live, bad):
    """live = {plane: (flag, total)}. Verify the newest history row matches the live
    recomputation (the log is anchored to reality), and that no plane has been a
    permanent rubber-stamp or permanently saturated across the recorded window."""
    rows = history_rows()
    if not rows:
        bad.append("flag-rate history empty"); return 0
    # columns -> plane key; index pairs (flag, total) into each row
    PLANES = {"Gate S (skills)": (1, 2), "category audit (categories)": (3, 4),
              "reflexive Gate S (claims routed)": (5, 6)}
    print(f"\n=== Flag-rate trajectory ({len(rows)} circles tracked) ===")
    for name, (fi, ti) in PLANES.items():
        series = [(int(r[fi]), int(r[ti])) for r in rows if r[fi] != "-"]
        if not series:
            continue
        present = sum(1 for r in rows if r[fi] != "-")
        flags = [f for f, _ in series]
        tots = [t for _, t in series]
        circles = [r[0] for r in rows if r[fi] != "-"]
        print(f"  {name:36} {'->'.join(f'{f}/{t}' for f, t in series)}  (circles {circles[0]}-{circles[-1]})")
        if present >= 2 and all(f == 0 for f in flags):
            bad.append(f"{name}: permanent rubber-stamp across {present} circles")
        if present >= 2 and all(f == t for f, t in zip(flags, tots)):
            bad.append(f"{name}: permanently saturated across {present} circles")
    # anchor: newest recorded row must equal the live recomputation
    newest = rows[-1]
    for name, (fi, ti) in PLANES.items():
        if newest[fi] == "-":
            continue
        lf, lt = live[name]
        if (int(newest[fi]), int(newest[ti])) != (lf, lt):
            bad.append(f"{name}: newest history row {newest[fi]}/{newest[ti]} "
                       f"!= live {lf}/{lt} (append the current circle)")
    return len(rows)


def main():
    gs = gate_s_rate()
    over = overreach_rate()
    refl = reflexive_routing_rate()
    planes = [gs, over, refl]
    print("=== Flag-rate calibration (does each monitor discriminate?) ===")
    bad = []
    discriminating = 0
    for name, flagged, total in planes:
        if total == 0:
            verdict = "EMPTY (nothing audited)"
            bad.append(f"{name}: nothing audited")
        elif flagged == 0:
            verdict = "RUBBER-STAMP (flags 0)"
            bad.append(f"{name}: rubber-stamp (0/{total})")
        elif flagged == total:
            verdict = "SATURATED (flags all)"
            bad.append(f"{name}: saturated ({flagged}/{total})")
        else:
            verdict = "DISCRIMINATING"
            discriminating += 1
        print(f"  {name:36} {flagged}/{total}  {verdict}")

    d_total, d_external = defect_catches()
    print(f"\n  self-audit defects caught: {d_total}; of which external-only: {d_external} "
          f"(internal gates are NOT complete -- honest reminder)")
    if d_external == 0:
        bad.append("zero external-catch defects (would falsely imply internal gates complete)")

    live = {name: (flagged, total) for name, flagged, total in planes}
    tracked = trajectory_check(live, bad)

    MACROS.parent.mkdir(parents=True, exist_ok=True)
    MACROS.write_text(
        "% GENERATED by verify/flag_rate.py -- do not hand-edit.\n"
        f"\\newcommand{{\\ResCalibMonitors}}{{{discriminating}}}\n"
        f"\\newcommand{{\\ResCalibExternalCatches}}{{{d_external}}}\n"
        f"\\newcommand{{\\ResCalibDefects}}{{{d_total}}}\n"
        f"\\newcommand{{\\ResCalibRouted}}{{{refl[1]}}}\n"
        f"\\newcommand{{\\ResCalibClaims}}{{{refl[2]}}}\n"
        f"\\newcommand{{\\ResCalibHistory}}{{{tracked}}}\n"
    )
    ok = not bad
    print(f"\nFlag-rate calibration: {'PASS' if ok else 'FAIL'} "
          f"({discriminating}/{len(planes)} planes discriminating)")
    for b in bad:
        print("  [FAIL]", b)
    print("macros ->", MACROS)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
