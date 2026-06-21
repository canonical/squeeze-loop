# Metric-subtlety ladder (level-up-A)

The richness of Use Case A comes from the richness of its upper bound: metrics
whose English definition admits many plausible SQL readings, only one correct.
This implements `level-up-A.md`.

`ladder.py` defines the rungs (trivial -> very hard). Each rung pins ONE intended
computation (the handbook reading) and a set of FORKS -- queries that RUN against
the real warehouse but encode a wrong reading. `../ladder_runner.py` computes
intended + each fork against `../shared/base_warehouse.db`; a fork is **caught**
when its value diverges from intended (the coherent-and-wrong an independent
exerciser detects).

| Tier | Metric | Forks (wrong readings) |
|------|--------|------------------------|
| trivial | total event count | count distinct users (grain) |
| easy | gross purchase revenue | sum all types (refunds added) |
| medium | net revenue | add refunds; ignore refunds |
| hard | Q2 active users (UTC) | grain; window-inclusivity; purchases-only; exclude-deleted |
| very_hard | "active customer" (pinned) | login-counts; refund-counts; all-time; exclude-deleted |

Run: `python3 ../ladder_runner.py` (writes `../../evidence/ladder_results.json`).
Current data: 4/5 rungs catch every fork; the hard rung's window-inclusivity fork
is **NOT EXERCISED** because the Q3-boundary user is already in-window, so the
distinct-user count does not move -- reported honestly, never faked. That gap is
itself the level-up point: the experiment needs both a rich upper bound AND data
rich enough to separate every fork. The ladder is the scaffold for a live-implementer
run, where the wrong-fork rate is expected to rise from trivial to very hard.
