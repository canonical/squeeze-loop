"""A pool of 100 metric tasks of varying subtlety for the A diversity test.

Diversity, not determinism. Each task carries the INTENDED SQL (the handbook
reading) and the NAIVE SQL a fixed weak implementer would write -- "the obvious
query". On simple metrics naive == intended (the implementer is right); on subtle
metrics the naive reading is a wrong fork (gross-not-net, grain, activity
definition, survivorship) that returns a plausible number. The implementer ERRS
when naive != intended on the real warehouse. Sampling tasks randomly each cycle
yields a varying error rate -- an actual trial.
"""
Q = {
    "Q1": ("2025-01-01T00:00:00Z", "2025-04-01T00:00:00Z"),
    "Q2": ("2025-04-01T00:00:00Z", "2025-07-01T00:00:00Z"),
    "Q3": ("2025-07-01T00:00:00Z", "2025-10-01T00:00:00Z"),
    "Q4": ("2025-10-01T00:00:00Z", "2026-01-01T00:00:00Z"),
}
REGIONS = ["UTC", "US/Pacific", "Europe/Paris", "Asia/Tokyo"]

_simple, _subtle = [], []


def S(dst, tier, kind, intended, naive):
    dst.append({"tier": tier, "kind": kind, "intended": intended, "naive": naive})


def same(dst, tier, kind, sql):
    S(dst, tier, kind, sql, sql)


# --- SIMPLE: the obvious query is correct (naive == intended) ----------------
same(_simple, "trivial", "count_events", "SELECT COUNT(*) FROM events")
same(_simple, "trivial", "count_users", "SELECT COUNT(DISTINCT user_id) FROM events")
for t in ("purchase", "refund", "login"):
    same(_simple, "trivial", f"count_{t}", f"SELECT COUNT(*) FROM events WHERE event_type='{t}'")
for r in REGIONS:
    same(_simple, "easy", f"count_region_{r}", f"SELECT COUNT(*) FROM events WHERE region='{r}'")
    same(_simple, "easy", f"count_login_{r}", f"SELECT COUNT(*) FROM events WHERE event_type='login' AND region='{r}'")
    same(_simple, "easy", f"sum_purchase_{r}", f"SELECT COALESCE(SUM(amount_cents),0) FROM events WHERE event_type='purchase' AND region='{r}'")
    same(_simple, "easy", f"sum_refund_{r}", f"SELECT COALESCE(SUM(amount_cents),0) FROM events WHERE event_type='refund' AND region='{r}'")
for q, (lo, hi) in Q.items():
    same(_simple, "easy", f"count_{q}", f"SELECT COUNT(*) FROM events WHERE ts>='{lo}' AND ts<'{hi}'")
    same(_simple, "easy", f"gross_{q}", f"SELECT COALESCE(SUM(amount_cents),0) FROM events WHERE event_type='purchase' AND ts>='{lo}' AND ts<'{hi}'")
    same(_simple, "easy", f"refunds_{q}", f"SELECT COALESCE(SUM(amount_cents),0) FROM events WHERE event_type='refund' AND ts>='{lo}' AND ts<'{hi}'")
    same(_simple, "easy", f"purchasers_{q}", f"SELECT COUNT(DISTINCT user_id) FROM events WHERE event_type='purchase' AND ts>='{lo}' AND ts<'{hi}'")
    for r in REGIONS:
        same(_simple, "easy", f"count_{q}_{r}", f"SELECT COUNT(*) FROM events WHERE region='{r}' AND ts>='{lo}' AND ts<'{hi}'")
        same(_simple, "easy", f"gross_{q}_{r}", f"SELECT COALESCE(SUM(amount_cents),0) FROM events WHERE event_type='purchase' AND region='{r}' AND ts>='{lo}' AND ts<'{hi}'")
for r in REGIONS:
    same(_simple, "easy", f"users_region_{r}", f"SELECT COUNT(DISTINCT user_id) FROM events WHERE region='{r}'")

# --- SUBTLE: the obvious query is a WRONG fork (naive != intended) -----------
for q, (lo, hi) in Q.items():
    S(_subtle, "medium", f"net_rev_{q}",
      (f"SELECT (SELECT COALESCE(SUM(amount_cents),0) FROM events WHERE event_type='purchase' AND ts>='{lo}' AND ts<'{hi}')"
       f" - (SELECT COALESCE(SUM(amount_cents),0) FROM events WHERE event_type='refund' AND ts>='{lo}' AND ts<'{hi}')"),
      f"SELECT COALESCE(SUM(amount_cents),0) FROM events WHERE ts>='{lo}' AND ts<'{hi}'")
    S(_subtle, "hard", f"dau_grain_{q}",
      f"SELECT COUNT(DISTINCT user_id) FROM events WHERE ts>='{lo}' AND ts<'{hi}'",
      f"SELECT COUNT(*) FROM events WHERE ts>='{lo}' AND ts<'{hi}'")
    S(_subtle, "hard", f"active_customer_{q}",
      f"SELECT COUNT(DISTINCT user_id) FROM events WHERE event_type='purchase' AND ts>='{lo}' AND ts<'{hi}'",
      f"SELECT COUNT(DISTINCT user_id) FROM events WHERE ts>='{lo}' AND ts<'{hi}'")
    S(_subtle, "very_hard", f"survivorship_{q}",
      f"SELECT COUNT(DISTINCT user_id) FROM events WHERE ts>='{lo}' AND ts<'{hi}'",
      (f"SELECT COUNT(DISTINCT e.user_id) FROM events e JOIN users u ON u.user_id=e.user_id"
       f" WHERE u.deleted_ts IS NULL AND e.ts>='{lo}' AND e.ts<'{hi}'"))
S(_subtle, "medium", "net_rev_all",
  ("SELECT (SELECT COALESCE(SUM(amount_cents),0) FROM events WHERE event_type='purchase')"
   " - (SELECT COALESCE(SUM(amount_cents),0) FROM events WHERE event_type='refund')"),
  "SELECT COALESCE(SUM(amount_cents),0) FROM events")
S(_subtle, "hard", "dau_grain_all", "SELECT COUNT(DISTINCT user_id) FROM events", "SELECT COUNT(*) FROM events")
S(_subtle, "hard", "active_customer_all",
  "SELECT COUNT(DISTINCT user_id) FROM events WHERE event_type='purchase'",
  "SELECT COUNT(DISTINCT user_id) FROM events")
for r in REGIONS:
    S(_subtle, "medium", f"net_rev_region_{r}",
      (f"SELECT (SELECT COALESCE(SUM(amount_cents),0) FROM events WHERE event_type='purchase' AND region='{r}')"
       f" - (SELECT COALESCE(SUM(amount_cents),0) FROM events WHERE event_type='refund' AND region='{r}')"),
      f"SELECT COALESCE(SUM(amount_cents),0) FROM events WHERE region='{r}'")
    S(_subtle, "hard", f"dau_grain_region_{r}",
      f"SELECT COUNT(DISTINCT user_id) FROM events WHERE region='{r}'",
      f"SELECT COUNT(*) FROM events WHERE region='{r}'")
    S(_subtle, "hard", f"active_customer_region_{r}",
      f"SELECT COUNT(DISTINCT user_id) FROM events WHERE event_type='purchase' AND region='{r}'",
      f"SELECT COUNT(DISTINCT user_id) FROM events WHERE region='{r}'")

assert len(_simple) >= 70 and len(_subtle) >= 30, (len(_simple), len(_subtle))
POOL = [{"id": f"M_{i:03d}", **t} for i, t in enumerate(_simple[:70] + _subtle[:30])]
assert len(POOL) == 100, len(POOL)
