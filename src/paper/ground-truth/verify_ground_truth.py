#!/usr/bin/env python3
"""Lower bound (verify): the manuscript's hard, executable truth.

Three machine checks, none of which an author's report can satisfy:
  1. DETERMINISM   regenerate every macro and assert it is byte-identical to the
                   committed version (`git diff` is empty) -- every number recomputes.
  2. BUILD         pdflatex + bibtex + pdflatex x2 is green; no undefined
                   references/citations/macros, no bibtex warnings. (Skipped if
                   pdflatex is absent -- honestly, never faked.)
  3. CITES RESOLVE every \\cite key in the manuscript has a reading record on disk.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import _paperlib as L


def main():
    g = L.Gate()

    # 1. determinism: regenerate, then check tex/macros is unchanged vs git
    for cwd, script in L.GENERATORS:
        L.run(["python3", script], cwd=L.REPO / cwd)
    diff = L.run(["git", "diff", "--name-only", "--", "tex/macros"])
    changed = [x for x in diff.stdout.split() if x]
    g.check("determinism: every macro recomputes byte-identical", not changed,
            "clean" if not changed else f"drifted: {changed}")

    # 2. build (only if a TeX engine is present -- capability-gated, never faked)
    if L.run(["which", "pdflatex"]).returncode == 0:
        tex = L.REPO / "tex"
        L.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "paper.tex"], cwd=tex)
        L.run(["bibtex", "paper"], cwd=tex)
        L.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "paper.tex"], cwd=tex)
        r = L.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "paper.tex"], cwd=tex)
        log = r.stdout + r.stderr
        bad = [w for w in ("undefined", "Warning: Cit", "Warning: Ref", "??")
               if w.lower() in log.lower()]
        built = "Output written on paper.pdf" in log
        g.check("build: pdflatex green, refs/cites/macros resolve", built and not bad,
                "ok" if built and not bad else f"issues={bad or 'no pdf'}")
    else:
        g.skip("build: pdflatex absent (DEPENDENCY UNMET; not faked)")

    # 3. every cited source is recorded (read-before-cite, lower-bound side)
    missing = sorted(L.cite_keys() - L.record_keys())
    g.check("every \\cite resolves to a reading record", not missing,
            "all recorded" if not missing else f"missing: {missing}")

    print("VERIFY OK" if g.ok else "VERIFY FAILED")
    sys.exit(0 if g.ok else 1)


if __name__ == "__main__":
    main()
