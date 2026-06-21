"""Difficulty ladder for Use Case A (level-up-A.md): metric-definition subtlety.

The richness of the experiment comes from the richness of the upper bound. For A
that richness is the *interpretation surface* of a metric: how many plausible-but-
different SQL readings the English admits, of which only one matches intent. Each
rung pins one INTENDED computation (the handbook's reading) and a set of FORK
computations -- queries that RUN and return plausible numbers but encode a wrong
reading (gross vs net, grain, timezone/window, survivorship, what counts as
"active"). A fork is *caught* when its value diverges from the intended value: that
is the coherent-and-wrong the independent exerciser detects.

All SQL runs against the real ground-truth warehouse
(../shared/base_warehouse.db: tables events, users). Monetary values are integer
cents, so every figure is exact.

Q2_2025 = [2025-04-01T00:00:00Z, 2025-07-01T00:00:00Z)  (UTC, the canonical window)
"""

Q2_LO = "2025-04-01T00:00:00Z"
Q2_HI = "2025-07-01T00:00:00Z"

RUNGS = [
    {
        "id": "METRIC_L1", "tier": "trivial",
        "name": "Total event count",
        "english": "the number of rows in the event log",
        "clauses": ["CLAUSE_1: count every event row, no filter"],
        "intended": "SELECT COUNT(*) FROM events",
        "forks": [
            {"name": "count_distinct_users", "why": "counts users, not events (grain)",
             "sql": "SELECT COUNT(DISTINCT user_id) FROM events"},
        ],
    },
    {
        "id": "METRIC_L2", "tier": "easy",
        "name": "Gross purchase revenue (cents)",
        "english": "total purchase amount; refunds and logins are out of scope",
        "clauses": ["CLAUSE_1: only event_type='purchase' rows enter the sum"],
        "intended": "SELECT COALESCE(SUM(amount_cents),0) FROM events WHERE event_type='purchase'",
        "forks": [
            {"name": "sum_all_types", "why": "adds refunds (and logins=0) into gross",
             "sql": "SELECT COALESCE(SUM(amount_cents),0) FROM events"},
        ],
    },
    {
        "id": "METRIC_L3", "tier": "medium",
        "name": "Net revenue (cents)",
        "english": "gross purchases minus refunds",
        "clauses": ["CLAUSE_1: purchases summed", "CLAUSE_2: refunds SUBTRACTED, not added or ignored"],
        "intended": ("SELECT (SELECT COALESCE(SUM(amount_cents),0) FROM events WHERE event_type='purchase')"
                     " - (SELECT COALESCE(SUM(amount_cents),0) FROM events WHERE event_type='refund')"),
        "forks": [
            {"name": "add_refunds", "why": "sums all rows -> refunds ADDED instead of subtracted",
             "sql": "SELECT COALESCE(SUM(amount_cents),0) FROM events"},
            {"name": "ignore_refunds", "why": "gross only -> refunds ignored",
             "sql": "SELECT COALESCE(SUM(amount_cents),0) FROM events WHERE event_type='purchase'"},
        ],
    },
    {
        "id": "METRIC_L4", "tier": "hard",
        "name": "Active users in Q2 (UTC)",
        "english": "distinct users with at least one event whose UTC timestamp falls in Q2",
        "clauses": ["CLAUSE_1: bucket by UTC ts", "CLAUSE_2: dedup to distinct users (grain)",
                    "CLAUSE_3: any event type counts as active; survivorship-included"],
        "intended": f"SELECT COUNT(DISTINCT user_id) FROM events WHERE ts>='{Q2_LO}' AND ts<'{Q2_HI}'",
        "forks": [
            {"name": "count_events_grain", "why": "counts events, not distinct users (grain fork)",
             "sql": f"SELECT COUNT(*) FROM events WHERE ts>='{Q2_LO}' AND ts<'{Q2_HI}'"},
            {"name": "window_inclusive_hi", "why": "uses ts<=hi -> pulls the Q3 boundary event into Q2",
             "sql": f"SELECT COUNT(DISTINCT user_id) FROM events WHERE ts>='{Q2_LO}' AND ts<='{Q2_HI}'"},
            {"name": "purchases_only", "why": "treats only purchasers as active (activity-definition fork)",
             "sql": f"SELECT COUNT(DISTINCT user_id) FROM events WHERE event_type='purchase' AND ts>='{Q2_LO}' AND ts<'{Q2_HI}'"},
            {"name": "exclude_deleted", "why": "drops deleted users (survivorship fork)",
             "sql": (f"SELECT COUNT(DISTINCT e.user_id) FROM events e JOIN users u ON u.user_id=e.user_id"
                     f" WHERE u.deleted_ts IS NULL AND e.ts>='{Q2_LO}' AND e.ts<'{Q2_HI}'")},
        ],
    },
    {
        "id": "METRIC_L5", "tier": "very_hard",
        "name": "Active customers in Q2 (pinned)",
        "english": ("an 'active customer' is genuinely ambiguous; the handbook PINS it: a user with"
                    " >=1 PURCHASE in Q2 (UTC), deduped by user, survivorship-included"),
        "clauses": ["CLAUSE_1: 'active' = made a PURCHASE (not login, not refund)",
                    "CLAUSE_2: window Q2 in UTC", "CLAUSE_3: distinct users; deleted users still count"],
        "intended": f"SELECT COUNT(DISTINCT user_id) FROM events WHERE event_type='purchase' AND ts>='{Q2_LO}' AND ts<'{Q2_HI}'",
        "forks": [
            {"name": "login_counts_active", "why": "any event counts as active (incl. login)",
             "sql": f"SELECT COUNT(DISTINCT user_id) FROM events WHERE ts>='{Q2_LO}' AND ts<'{Q2_HI}'"},
            {"name": "refund_counts_active", "why": "refund-only users counted as active",
             "sql": f"SELECT COUNT(DISTINCT user_id) FROM events WHERE event_type IN ('purchase','refund') AND ts>='{Q2_LO}' AND ts<'{Q2_HI}'"},
            {"name": "all_time_window", "why": "drops the Q2 window (all-time purchasers)",
             "sql": "SELECT COUNT(DISTINCT user_id) FROM events WHERE event_type='purchase'"},
            {"name": "exclude_deleted", "why": "drops deleted purchasers (survivorship fork)",
             "sql": (f"SELECT COUNT(DISTINCT e.user_id) FROM events e JOIN users u ON u.user_id=e.user_id"
                     f" WHERE u.deleted_ts IS NULL AND e.event_type='purchase' AND e.ts>='{Q2_LO}' AND e.ts<'{Q2_HI}'")},
        ],
    },
]
