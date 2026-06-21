"""Deterministic raw event-log generator for the Storage Plane (spec §2 Step 1).

No stdlib RNG is used: a small fixed LCG drives every choice, so the warehouse is
byte-for-byte reproducible across machines and Python versions. This is the data
half of the "frozen compute plane" / "every number recomputes" guarantee --
editing this file changes the ground truth, and therefore the baseline ledger,
on purpose.
"""

from datetime import datetime, timedelta, timezone

N_USERS = 50
YEAR = 2025

# Fixed linear congruential generator (glibc constants) -- portable & stable.
_A, _C, _M = 1103515245, 12345, 2 ** 31

REGIONS = ["UTC", "US/Pacific", "Europe/Paris", "Asia/Tokyo"]


def _lcg(state):
    return (_A * state + _C) % _M


def _iso(dt):
    # dt is tz-aware UTC; format the wall-clock fields and append literal Z.
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _jan1():
    return datetime(YEAR, 1, 1, tzinfo=timezone.utc)


def generate():
    """Return (users, events) as lists of tuples ready for executemany()."""
    users = []
    s = 7
    for uid in range(1, N_USERS + 1):
        s = _lcg(s)
        signup_doy = s % 300                       # signups taper off in late Oct
        signup = _jan1() + timedelta(days=signup_doy, hours=(s // 7) % 24)
        s = _lcg(s)
        deleted_iso = None
        if s % 5 == 0:                             # ~20% of users churn
            del_doy = signup_doy + 30 + (s % 120)
            if del_doy < 365:
                deleted_iso = _iso(_jan1() + timedelta(days=del_doy))
        region = REGIONS[uid % len(REGIONS)]
        users.append((uid, _iso(signup), deleted_iso, region))

    events = []
    s = 99
    for (uid, signup_iso, deleted_iso, region) in users:
        cur = datetime.strptime(signup_iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        s = _lcg(s)
        n_events = 3 + (s % 10)                    # 3..12 events per user
        for _ in range(n_events):
            s = _lcg(s)
            cur = cur + timedelta(days=1 + (s % 40),
                                  hours=(s // 11) % 24,
                                  minutes=(s // 3) % 60,
                                  seconds=s % 60)
            if cur.year != YEAR:                   # stay inside the calendar year
                break
            ts = _iso(cur)
            if deleted_iso is not None and ts >= deleted_iso:
                break                              # no events after deletion
            s = _lcg(s)
            r = s % 100
            if r < 60:
                etype, amt = "login", 0
            elif r < 92:
                s = _lcg(s)
                etype, amt = "purchase", 500 + (s % 49500)    # $5.00 .. $500.00
            else:
                s = _lcg(s)
                etype, amt = "refund", 100 + (s % 4900)       # $1.00 .. $50.00
            events.append((None, ts, uid, etype, amt, region))

    # Explicit boundary witnesses: quarter edges in UTC, observed from non-UTC
    # regions. These pin the timezone/quarter-boundary behaviour Gate C guards.
    boundary = [
        ("2025-03-31T23:59:59Z", 1, "purchase", 12345, "US/Pacific"),  # last sec of Q1
        ("2025-04-01T00:00:00Z", 1, "purchase", 67890, "US/Pacific"),  # first ns of Q2
        ("2025-06-30T23:59:59Z", 2, "refund",    5000, "Asia/Tokyo"),  # last sec of Q2
        ("2025-07-01T00:00:00Z", 2, "purchase", 10000, "Asia/Tokyo"),  # first ns of Q3
    ]
    for (ts, uid, etype, amt, reg) in boundary:
        events.append((None, ts, uid, etype, amt, reg))

    # Sort chronologically (stable) and assign contiguous event_ids.
    events.sort(key=lambda e: (e[1], e[2], e[3]))
    events = [(i + 1, ts, uid, et, amt, reg)
              for i, (_eid, ts, uid, et, amt, reg) in enumerate(events)]
    return users, events
