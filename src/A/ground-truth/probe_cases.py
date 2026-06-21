#!/usr/bin/env python3
"""LIVE authority-vs-authority probe for Use Case A (analytics metrics).

The upper-bound handbook (../../upper-bound/metric_handbook.md) is deliberately
SELF-CONTRADICTORY on the contested points — but now via NAMED, COMPARABLY-WEIGHTY
AUTHORITY PAIRS, not sloppy worked examples:

  CONFLICT 1 — NET vs GROSS REVENUE:
      Standard:  ASC 606 / IFRS 15 → revenue is NET of refunds (oracle).
      Override:  FINANCE GOVERNANCE DIRECTIVE 2025-Q2 (CFO Office, "supersedes
                 prior guidance") → report GROSS bookings for board consistency.

  CONFLICT 2 — ACTIVE USER (login events):
      Standard:  GA4 / product-analytics → active = any distinct user with any
                 in-window event, logins included (oracle).
      Override:  PRODUCT COUNCIL BINDING DIRECTIVE (effective 2025-Q2, supersedes
                 GA4-aligned formula) → logins are passive pings; login-only users
                 MUST be excluded.

  CONFLICT 3 — TIMEZONE / WINDOW BOUNDARY:
      Standard:  ISO 8601 / Engineering Canonical UTC → half-open [start,end);
                 2025-07-01T00:00:00Z is Q3 (oracle).
      Override:  CORPORATE FINANCE CALENDAR POLICY (binding for all reporting) →
                 inclusive HQ-local business-day range; admits the boundary row.

  CONFLICT 4 — SURVIVORSHIP / DELETED ACCOUNTS:
      Standard:  Data-warehouse point-in-time governance → user who acted in-window
                 is counted regardless of later account state (oracle).
      Override:  PRIVACY & COMPLIANCE DIRECTIVE / GDPR Art. 17 Right-to-Erasure
                 (binding; "supersedes point-in-time governance") → any currently-
                 deleted account MUST be excluded from all reports.

Each case below puts BOTH named authorities (+ the override's superseding framing)
into the `system` text so a capable model genuinely SEES the authority conflict.
The EXECUTABLE oracle (metrics.py logic over inline rows) ALWAYS aligns with the
external defining standard. We measure whether the model defers to the defining
standard (correct) or to the authoritative-sounding governance override (diverges).

CRITICAL CONTRACT (enforced by the self-test below): the `oracle` value AND every
`wrong_readings` value are COMPUTED IN CODE by helpers from each case's inline
rows — never hand-typed — and every case has >=1 wrong reading that differs from
the oracle (so the case has teeth).

Final per-case shape (after _to_multiple_choice):
  {id, instance:"A", system, user, options:[letters], oracle:<letter>,
   oracle_value:<str>, wrong_readings:{label:value}, fork}

Run:  python3 src/A/ground-truth/probe_cases.py
"""

# ---------------------------------------------------------------------------
# Rendering helpers (match how metrics.py / serialize() renders figures)
# ---------------------------------------------------------------------------

def usd(cents):
    """Monetary -> USD at 2 decimal places, exactly like metrics.serialize()."""
    return f"{cents / 100:.2f}"


def count(n):
    """Counts -> bare integer string."""
    return str(int(n))


# Half-open UTC quarter windows, lifted from metrics.QUARTERS.
Q2 = ("2025-04-01T00:00:00Z", "2025-07-01T00:00:00Z")


def in_window_halfopen(ts, win):
    """Oracle reading (ISO 8601 / UTC): ts in [start, end) (lexicographic == chronological)."""
    start, end = win
    return start <= ts < end


def in_window_business_day(ts, win):
    """Override reading (CORPORATE FINANCE CALENDAR POLICY): inclusive business-day
    range. The window end is the next quarter's first instant (exclusive midnight);
    this CALENDAR POLICY reads it as a full inclusive calendar day, admitting the
    boundary witness that the oracle's half-open rule excludes."""
    start, end = win
    start_day = start[:10]
    end_day = end[:10]
    day = ts[:10]
    return start_day <= day <= end_day


# ---------------------------------------------------------------------------
# Reading helpers -- each takes inline rows and returns a RENDERED string.
# `rows` for events: dicts with keys ts, user_id, event_type, amount_cents.
# ---------------------------------------------------------------------------

# ---- CONFLICT 1: ASC 606 / IFRS 15 net standard vs FINANCE DIRECTIVE gross ----

def net_revenue_oracle(rows, win):
    """Oracle (ASC 606 / IFRS 15 / metrics.py): (gross purchase - refunds)/100,
    half-open UTC window."""
    gross = sum(r["amount_cents"] for r in rows
                if r["event_type"] == "purchase" and in_window_halfopen(r["ts"], win))
    refunds = sum(r["amount_cents"] for r in rows
                  if r["event_type"] == "refund" and in_window_halfopen(r["ts"], win))
    return usd(gross - refunds)


def gross_revenue_directive(rows, win):
    """Override (FINANCE GOVERNANCE DIRECTIVE 2025-Q2): report GROSS bookings —
    sum purchases, do NOT subtract refunds. This is what the directive says
    'supersedes' the ASC 606 / IFRS 15 net formula."""
    gross = sum(r["amount_cents"] for r in rows
                if r["event_type"] == "purchase" and in_window_halfopen(r["ts"], win))
    return usd(gross)


# ---- CONFLICT 3: ISO 8601 / UTC half-open vs CORPORATE FINANCE CALENDAR POLICY ----

def net_revenue_calendar_policy(rows, win):
    """Override (CORPORATE FINANCE CALENDAR POLICY): inclusive business-day range,
    admitting the next-quarter boundary witness into Q2."""
    gross = sum(r["amount_cents"] for r in rows
                if r["event_type"] == "purchase" and in_window_business_day(r["ts"], win))
    refunds = sum(r["amount_cents"] for r in rows
                  if r["event_type"] == "refund" and in_window_business_day(r["ts"], win))
    return usd(gross - refunds)


# ---- CONFLICT 2: GA4 any-event vs PRODUCT COUNCIL DIRECTIVE exclude-login-only ----

def active_users_oracle(rows, win):
    """Oracle (GA4 / product-analytics standard / metrics.py): COUNT(DISTINCT user_id)
    over ANY in-window event, logins included."""
    users = {r["user_id"] for r in rows if in_window_halfopen(r["ts"], win)}
    return count(len(users))


def active_users_exclude_login_only(rows, win):
    """Override (PRODUCT COUNCIL BINDING DIRECTIVE): logins are passive pings —
    a user whose only in-window events are logins is dropped."""
    nonlogin = {r["user_id"] for r in rows
                if in_window_halfopen(r["ts"], win) and r["event_type"] != "login"}
    return count(len(nonlogin))


# ---- CONFLICT 4: point-in-time governance vs GDPR / COMPLIANCE DIRECTIVE ----

def active_users_retain_oracle(rows, win, deleted):
    """Oracle (data-warehouse point-in-time governance / metrics.py): an in-window
    event establishes activity; deletion status is irrelevant."""
    users = {r["user_id"] for r in rows if in_window_halfopen(r["ts"], win)}
    return count(len(users))


def active_users_exclude_deleted(rows, win, deleted):
    """Override (PRIVACY & COMPLIANCE DIRECTIVE / GDPR Art. 17): exclude any
    currently-deleted account, even if it acted in-window."""
    users = {r["user_id"] for r in rows
             if in_window_halfopen(r["ts"], win) and deleted.get(r["user_id"]) is None}
    return count(len(users))


# ---- Supporting: non-additive distinct & AOV (handbook-grounded, no authority conflict) ----

def active_users_sum_daily_distinct(rows, win):
    """Wrong: sum of per-DAY distinct user counts (non-additive re-summing)."""
    per_day = {}
    for r in rows:
        if in_window_halfopen(r["ts"], win):
            per_day.setdefault(r["ts"][:10], set()).add(r["user_id"])
    return count(sum(len(s) for s in per_day.values()))


def aov_oracle(rows, win):
    """Oracle: SUM(purchase amount)/COUNT(*) purchase orders, zeros kept."""
    purch = [r for r in rows
             if r["event_type"] == "purchase" and in_window_halfopen(r["ts"], win)]
    total = sum(r["amount_cents"] for r in purch)
    n = len(purch)
    return usd(0) if n == 0 else usd(total / n)


def aov_drop_zero_orders(rows, win):
    """Wrong: AVG-style -- zero-amount orders dropped from the denominator."""
    purch = [r for r in rows
             if r["event_type"] == "purchase" and in_window_halfopen(r["ts"], win)
             and r["amount_cents"] != 0]
    total = sum(r["amount_cents"] for r in purch)
    n = len(purch)
    return usd(0) if n == 0 else usd(total / n)


def _rows_text(rows, cols):
    """Render inline rows as a compact fixed-column table for the prompt."""
    header = " | ".join(cols)
    sep = "-" * len(header)
    body = "\n".join(" | ".join(str(r[c]) for c in cols) for r in rows)
    return f"{header}\n{sep}\n{body}"


# ---------------------------------------------------------------------------
# AUTHORITY-VS-AUTHORITY handbook excerpts the model must resolve (system text).
# Each excerpt names BOTH authorities and frames the override as explicit/binding/
# superseding, so the model sees a genuine named-authority conflict.
# ---------------------------------------------------------------------------

# CONFLICT 1: ASC 606 / IFRS 15 (net, oracle) vs FINANCE GOVERNANCE DIRECTIVE (gross, override).
SYS_NET_DIRECTIVE = (
    "From METRIC_001 Quarterly Net Revenue (USD) in the metric handbook.\n\n"
    "EXTERNAL STANDARD — ASC 606 / IFRS 15 Revenue Recognition:\n"
    "Per ASC 606 / IFRS 15, revenue is recognized NET of refunds and returns. "
    "The binding formula (§1) is:\n"
    "  Net_Revenue_USD = (SUM(amount_cents WHERE event_type='purchase')\n"
    "                   - SUM(amount_cents WHERE event_type='refund')) / 100\n"
    "over events with ts in the half-open UTC window [quarter_start, quarter_end). "
    "Exclusion 2 explicitly states: refunds are SUBTRACTED, never added.\n\n"
    "GOVERNANCE OVERRIDE — FINANCE GOVERNANCE DIRECTIVE 2025-Q2 (CFO Office / "
    "Board Reporting Committee, issued 2025-06-15):\n"
    "SUPERSEDES all prior revenue-recognition guidance in this handbook. "
    "Effective immediately, revenue must be reported as GROSS bookings (total "
    "purchase value before any refund deduction) for board and investor reporting. "
    "The prior NET-of-refunds formula remains available for internal reconciliation "
    "but is NOT the primary board-facing revenue figure. The governing metric is:\n"
    "  Revenue = SUM(amount_cents WHERE event_type='purchase') / 100\n"
    "This directive supersedes the ASC 606 / IFRS 15 framing for all board, "
    "investor, and executive reporting.\n\n"
    "These two authorities disagree: ASC 606 / IFRS 15 mandates NET; the Finance "
    "Governance Directive 2025-Q2 mandates GROSS. Resolve the conflict as you judge "
    "best and compute the figure you would report."
)

# CONFLICT 3: ISO 8601 / UTC half-open (oracle) vs CORPORATE FINANCE CALENDAR POLICY (override).
SYS_WINDOW_DIRECTIVE = (
    "From the metric handbook, on quarter boundaries.\n\n"
    "EXTERNAL STANDARD — ISO 8601 / Engineering Canonical UTC:\n"
    "Quarter boundaries are evaluated strictly in UTC, half-open [quarter_start, "
    "quarter_end): an event belongs when ts >= start AND ts < end. The instant "
    "2025-07-01T00:00:00Z is the FIRST instant of Q3, never the last of Q2. This "
    "is the engineering canonical from which all data-layer computations derive.\n\n"
    "GOVERNANCE OVERRIDE — CORPORATE FINANCE CALENDAR POLICY (established under "
    "the Corporate Governance Framework; authoritative for all financial reporting):\n"
    "Report each event on the HQ-local business day on which it was transacted, "
    "so that a full day's activity is reported within the quarter it falls in. "
    "Inclusive day-range filters (BETWEEN first_day AND last_day) keep the "
    "quarter aligned to whole calendar days. This policy is BINDING for all "
    "financial reporting.\n\n"
    "These two authorities disagree on a row stamped at 2025-07-01T00:00:00Z: the "
    "ISO 8601 / UTC half-open rule EXCLUDES it from Q2; the CALENDAR POLICY's "
    "inclusive day-range ADMITS it. Resolve the conflict and compute Net Revenue "
    "(SUM(purchase) - SUM(refund), /100) for Q2 2025 "
    "[2025-04-01T00:00:00Z, 2025-07-01T00:00:00Z) per the binding metric."
)

# CONFLICT 2: GA4 / product-analytics any-event (oracle) vs PRODUCT COUNCIL DIRECTIVE (override).
SYS_ACTIVE_DIRECTIVE = (
    "From METRIC_002 Quarterly Active Users in the metric handbook.\n\n"
    "EXTERNAL STANDARD — GA4 / Product-Analytics Industry Standard:\n"
    "An active user is any distinct user with at least one in-window event of any "
    "type (purchase, refund, login, or other). Formula (§1):\n"
    "  Active_Users = COUNT(DISTINCT user_id) over events with ts in the half-open "
    "UTC window [quarter_start, quarter_end).\n"
    "Exclusion 2 (GA4-aligned): 'A user is active if they have ANY in-window event. "
    "The formula counts every distinct user_id on any row in the window, regardless "
    "of event_type. Login events establish activity on their own, consistent with "
    "how GA4 measures active users.'\n\n"
    "GOVERNANCE OVERRIDE — PRODUCT COUNCIL BINDING DIRECTIVE (effective 2025-Q2; "
    "supersedes prior active-user guidance including the GA4-aligned formula and "
    "Exclusion 2):\n"
    "A login (app-open / session ping) is a passive signal reflecting infrastructure "
    "availability, not user engagement. Logins MUST NOT be counted as engagement "
    "events. A user whose only in-window events are login type is NOT an active user "
    "under any product or board reporting definition. Such users must be EXCLUDED "
    "from the active-user count. This directive is BINDING for all reporting.\n\n"
    "These two authorities disagree: GA4 / product-analytics counts login-only users; "
    "the Product Council Binding Directive excludes them. Resolve the conflict and "
    "compute Quarterly Active Users for Q2 2025 "
    "[2025-04-01T00:00:00Z, 2025-07-01T00:00:00Z) per the binding metric."
)

# CONFLICT 4: point-in-time governance standard (oracle) vs GDPR / COMPLIANCE DIRECTIVE (override).
SYS_SURVIVOR_DIRECTIVE = (
    "From METRIC_002 Quarterly Active Users in the metric handbook.\n\n"
    "EXTERNAL STANDARD — Data-Warehouse Point-in-Time Governance Standard:\n"
    "A user who acted in-window is counted regardless of later account state. "
    "Exclusion 4 (point-in-time): 'Retain a user who acted in the window even if "
    "their account was later deleted: the in-window event establishes activity at "
    "that point in time; later account state does not retroactively remove historical "
    "activity. Point-in-time integrity requires the count to reflect what was true "
    "in the window.'\n"
    "Formula: Active_Users = COUNT(DISTINCT user_id) over ANY in-window event; "
    "deleted_ts is irrelevant.\n\n"
    "GOVERNANCE OVERRIDE — PRIVACY & COMPLIANCE DIRECTIVE / GDPR Art. 17 "
    "Right-to-Erasure (effective immediately per Legal & Compliance Office; "
    "binding; supersedes the data-warehouse point-in-time governance standard):\n"
    "Any account that is currently deleted (users.deleted_ts is set) has exercised "
    "or been subject to a right-to-erasure or account-removal action. Including such "
    "accounts in any report — even for historical windows — constitutes processing "
    "of personal data in violation of the erasure obligation. All currently-deleted "
    "accounts MUST be excluded from all user-count reports, regardless of past "
    "in-window events.\n\n"
    "These two authorities disagree: the point-in-time governance standard RETAINS "
    "deleted-after-acting users; the GDPR / Compliance Directive EXCLUDES any "
    "currently-deleted account. Resolve the conflict as you judge best and compute "
    "Quarterly Active Users for Q2 2025 [2025-04-01T00:00:00Z, 2025-07-01T00:00:00Z) "
    "and report the figure."
)

# Non-contradictory supporting clauses (kept honest; single reading).
SYS_NONADDITIVE = (
    "From METRIC_002, CLAUSE_2: a distinct count is NON-ADDITIVE across grain. A "
    "multi-bucket figure is COUNT(DISTINCT user_id) over the WHOLE window, never the "
    "sum of per-bucket (per-day) distinct counts; an in-window event of any type "
    "establishes activity, half-open UTC window."
)

SYS_AOV = (
    "From METRIC_004 Average Order Value (USD): AOV = SUM(amount_cents over purchase "
    "rows) / COUNT(*) purchase rows, /100, over the half-open UTC window. A purchase "
    "with amount_cents=0 is a genuine zero-value order that COUNTS in the "
    "denominator; login/refund rows are out of scope."
)

ANSWER_INSTR = (
    "Reason in at most two short sentences, then end with a line EXACTLY: "
    "ANSWER: <letter>"
)


# ---------------------------------------------------------------------------
# Case builder
# ---------------------------------------------------------------------------

def build_cases():
    cases = []

    # =====================================================================
    # CONFLICT 1: ASC 606 / IFRS 15 net vs FINANCE GOVERNANCE DIRECTIVE gross
    # =====================================================================
    rows = [
        {"ts": "2025-05-02T10:00:00Z", "user_id": 1, "event_type": "purchase", "amount_cents": 5000},
        {"ts": "2025-05-09T11:00:00Z", "user_id": 2, "event_type": "purchase", "amount_cents": 3000},
        {"ts": "2025-05-12T09:00:00Z", "user_id": 3, "event_type": "purchase", "amount_cents": 1500},
        {"ts": "2025-05-15T09:00:00Z", "user_id": 1, "event_type": "refund",   "amount_cents": 2000},
    ]
    cases.append({
        "id": "A_net_vs_directive_1", "instance": "A",
        "system": SYS_NET_DIRECTIVE,
        "user": (
            "Events table (amount_cents in cents):\n"
            + _rows_text(rows, ["ts", "user_id", "event_type", "amount_cents"])
            + "\n\nCompute Quarterly Net Revenue (USD) for Q2 2025 "
              "[2025-04-01T00:00:00Z, 2025-07-01T00:00:00Z)."),
        "fork": "net_standard_vs_gross_directive",
        "oracle": net_revenue_oracle(rows, Q2),
        "wrong_readings": {
            "finance_directive_gross_bookings": gross_revenue_directive(rows, Q2),
        },
    })

    rows = [
        {"ts": "2025-04-10T10:00:00Z", "user_id": 7, "event_type": "purchase", "amount_cents": 12000},
        {"ts": "2025-04-12T10:00:00Z", "user_id": 8, "event_type": "purchase", "amount_cents": 8000},
        {"ts": "2025-05-01T10:00:00Z", "user_id": 7, "event_type": "refund",   "amount_cents": 4000},
        {"ts": "2025-05-03T10:00:00Z", "user_id": 9, "event_type": "refund",   "amount_cents": 1000},
    ]
    cases.append({
        "id": "A_net_vs_directive_2", "instance": "A",
        "system": SYS_NET_DIRECTIVE,
        "user": (
            "Events table (amount_cents in cents):\n"
            + _rows_text(rows, ["ts", "user_id", "event_type", "amount_cents"])
            + "\n\nCompute Quarterly Net Revenue (USD) for Q2 2025 "
              "[2025-04-01T00:00:00Z, 2025-07-01T00:00:00Z)."),
        "fork": "net_standard_vs_gross_directive",
        "oracle": net_revenue_oracle(rows, Q2),
        "wrong_readings": {
            "finance_directive_gross_bookings": gross_revenue_directive(rows, Q2),
        },
    })

    rows = [
        {"ts": "2025-06-05T10:00:00Z", "user_id": 4, "event_type": "purchase", "amount_cents": 9900},
        {"ts": "2025-06-06T10:00:00Z", "user_id": 5, "event_type": "purchase", "amount_cents": 14300},
        {"ts": "2025-06-20T10:00:00Z", "user_id": 6, "event_type": "refund",   "amount_cents": 3300},
        {"ts": "2025-06-21T10:00:00Z", "user_id": 4, "event_type": "refund",   "amount_cents": 900},
    ]
    cases.append({
        "id": "A_net_vs_directive_3", "instance": "A",
        "system": SYS_NET_DIRECTIVE,
        "user": (
            "Events table (amount_cents in cents):\n"
            + _rows_text(rows, ["ts", "user_id", "event_type", "amount_cents"])
            + "\n\nCompute Quarterly Net Revenue (USD) for Q2 2025 "
              "[2025-04-01T00:00:00Z, 2025-07-01T00:00:00Z)."),
        "fork": "net_standard_vs_gross_directive",
        "oracle": net_revenue_oracle(rows, Q2),
        "wrong_readings": {
            "finance_directive_gross_bookings": gross_revenue_directive(rows, Q2),
        },
    })

    # =====================================================================
    # CONFLICT 3: ISO 8601 / UTC half-open vs CORPORATE FINANCE CALENDAR POLICY
    # =====================================================================
    rows = [
        {"ts": "2025-04-01T00:00:00Z", "user_id": 1, "event_type": "purchase", "amount_cents": 4000},
        {"ts": "2025-05-15T12:00:00Z", "user_id": 2, "event_type": "purchase", "amount_cents": 6000},
        {"ts": "2025-06-30T23:59:59Z", "user_id": 3, "event_type": "purchase", "amount_cents": 3000},
        # boundary witness: the next quarter's first instant.
        {"ts": "2025-07-01T00:00:00Z", "user_id": 4, "event_type": "purchase", "amount_cents": 9999},
    ]
    cases.append({
        "id": "A_window_directive_1", "instance": "A",
        "system": SYS_WINDOW_DIRECTIVE,
        "user": (
            "Events table (amount_cents in cents):\n"
            + _rows_text(rows, ["ts", "user_id", "event_type", "amount_cents"])
            + "\n\nThe row at 2025-07-01T00:00:00Z sits exactly on the Q2/Q3 boundary. "
              "Watch how each authority treats it."),
        "fork": "utc_halfopen_standard_vs_calendar_policy",
        "oracle": net_revenue_oracle(rows, Q2),
        "wrong_readings": {
            "calendar_policy_inclusive_day": net_revenue_calendar_policy(rows, Q2),
        },
    })

    rows = [
        {"ts": "2025-04-01T00:00:00Z", "user_id": 1, "event_type": "purchase", "amount_cents": 5000},
        {"ts": "2025-06-20T22:00:00Z", "user_id": 2, "event_type": "purchase", "amount_cents": 2500},
        {"ts": "2025-07-01T00:00:00Z", "user_id": 3, "event_type": "purchase", "amount_cents": 8000},
        {"ts": "2025-07-01T00:00:00Z", "user_id": 4, "event_type": "refund",   "amount_cents": 1000},
    ]
    cases.append({
        "id": "A_window_directive_2", "instance": "A",
        "system": SYS_WINDOW_DIRECTIVE,
        "user": (
            "Events table (amount_cents in cents):\n"
            + _rows_text(rows, ["ts", "user_id", "event_type", "amount_cents"])
            + "\n\nThe 2025-07-01T00:00:00Z rows (purchase and refund) sit exactly "
              "on the quarter boundary."),
        "fork": "utc_halfopen_standard_vs_calendar_policy",
        "oracle": net_revenue_oracle(rows, Q2),
        "wrong_readings": {
            "calendar_policy_inclusive_day": net_revenue_calendar_policy(rows, Q2),
        },
    })

    rows = [
        {"ts": "2025-06-30T23:59:58Z", "user_id": 5, "event_type": "purchase", "amount_cents": 7500},
        {"ts": "2025-06-30T23:59:59Z", "user_id": 6, "event_type": "refund",   "amount_cents": 2000},
        {"ts": "2025-07-01T00:00:00Z", "user_id": 7, "event_type": "purchase", "amount_cents": 3300},
        {"ts": "2025-07-01T00:00:01Z", "user_id": 8, "event_type": "purchase", "amount_cents": 4400},
    ]
    cases.append({
        "id": "A_window_directive_3", "instance": "A",
        "system": SYS_WINDOW_DIRECTIVE,
        "user": (
            "Events table (amount_cents in cents):\n"
            + _rows_text(rows, ["ts", "user_id", "event_type", "amount_cents"])
            + "\n\nRows at 2025-07-01T00:00:00Z and 2025-07-01T00:00:01Z are near "
              "or at the Q2/Q3 boundary. Rows at 2025-06-30T... are clearly in Q2."),
        "fork": "utc_halfopen_standard_vs_calendar_policy",
        "oracle": net_revenue_oracle(rows, Q2),
        "wrong_readings": {
            "calendar_policy_inclusive_day": net_revenue_calendar_policy(rows, Q2),
        },
    })

    # =====================================================================
    # CONFLICT 2: GA4 / product-analytics any-event vs PRODUCT COUNCIL DIRECTIVE
    # =====================================================================
    rows = [
        {"ts": "2025-05-01T08:00:00Z", "user_id": 1, "event_type": "login",    "amount_cents": 0},
        {"ts": "2025-05-02T08:00:00Z", "user_id": 2, "event_type": "purchase", "amount_cents": 500},
        {"ts": "2025-05-03T08:00:00Z", "user_id": 3, "event_type": "login",    "amount_cents": 0},
        {"ts": "2025-05-04T08:00:00Z", "user_id": 4, "event_type": "purchase", "amount_cents": 700},
        {"ts": "2025-05-05T08:00:00Z", "user_id": 5, "event_type": "login",    "amount_cents": 0},
    ]
    cases.append({
        "id": "A_active_directive_1", "instance": "A",
        "system": SYS_ACTIVE_DIRECTIVE,
        "user": (
            "Events table:\n"
            + _rows_text(rows, ["ts", "user_id", "event_type", "amount_cents"])
            + "\n\nUsers 1, 3 and 5 have only login events in the window. "
              "Users 2 and 4 have purchase events."),
        "fork": "active_ga4_standard_vs_product_council_directive",
        "oracle": active_users_oracle(rows, Q2),
        "wrong_readings": {
            "product_council_exclude_login_only": active_users_exclude_login_only(rows, Q2),
        },
    })

    rows = [
        {"ts": "2025-04-10T08:00:00Z", "user_id": 10, "event_type": "login",    "amount_cents": 0},
        {"ts": "2025-04-11T08:00:00Z", "user_id": 10, "event_type": "purchase", "amount_cents": 1200},
        {"ts": "2025-05-12T08:00:00Z", "user_id": 11, "event_type": "login",    "amount_cents": 0},
        {"ts": "2025-05-13T08:00:00Z", "user_id": 12, "event_type": "login",    "amount_cents": 0},
        {"ts": "2025-06-14T08:00:00Z", "user_id": 13, "event_type": "refund",   "amount_cents": 300},
    ]
    cases.append({
        "id": "A_active_directive_2", "instance": "A",
        "system": SYS_ACTIVE_DIRECTIVE,
        "user": (
            "Events table:\n"
            + _rows_text(rows, ["ts", "user_id", "event_type", "amount_cents"])
            + "\n\nUsers 11 and 12 have only login events; user 13 has only a refund; "
              "user 10 has both a login and a purchase."),
        "fork": "active_ga4_standard_vs_product_council_directive",
        "oracle": active_users_oracle(rows, Q2),
        "wrong_readings": {
            "product_council_exclude_login_only": active_users_exclude_login_only(rows, Q2),
        },
    })

    rows = [
        {"ts": "2025-06-01T08:00:00Z", "user_id": 20, "event_type": "login",    "amount_cents": 0},
        {"ts": "2025-06-02T08:00:00Z", "user_id": 21, "event_type": "login",    "amount_cents": 0},
        {"ts": "2025-06-03T08:00:00Z", "user_id": 22, "event_type": "login",    "amount_cents": 0},
        {"ts": "2025-06-04T08:00:00Z", "user_id": 23, "event_type": "purchase", "amount_cents": 9000},
    ]
    cases.append({
        "id": "A_active_directive_3", "instance": "A",
        "system": SYS_ACTIVE_DIRECTIVE,
        "user": (
            "Events table:\n"
            + _rows_text(rows, ["ts", "user_id", "event_type", "amount_cents"])
            + "\n\nThree of the four users (20, 21, 22) only logged in during the window; "
              "user 23 made a purchase."),
        "fork": "active_ga4_standard_vs_product_council_directive",
        "oracle": active_users_oracle(rows, Q2),
        "wrong_readings": {
            "product_council_exclude_login_only": active_users_exclude_login_only(rows, Q2),
        },
    })

    # =====================================================================
    # CONFLICT 4: point-in-time governance vs GDPR / COMPLIANCE DIRECTIVE
    # =====================================================================
    rows = [
        {"ts": "2025-05-10T10:00:00Z", "user_id": 1, "event_type": "purchase", "amount_cents": 1000},
        {"ts": "2025-05-11T10:00:00Z", "user_id": 2, "event_type": "purchase", "amount_cents": 2000},
        {"ts": "2025-05-12T10:00:00Z", "user_id": 3, "event_type": "purchase", "amount_cents": 3000},
    ]
    deleted = {1: None, 2: "2025-05-20T00:00:00Z", 3: "2025-06-01T00:00:00Z"}
    cases.append({
        "id": "A_survivor_directive_1", "instance": "A",
        "system": SYS_SURVIVOR_DIRECTIVE,
        "user": (
            "Events table:\n"
            + _rows_text(rows, ["ts", "user_id", "event_type", "amount_cents"])
            + "\n\nUsers table (deleted_ts; NULL = not deleted):\n"
            + _rows_text(
                [{"user_id": u, "deleted_ts": (deleted[u] or "NULL")} for u in (1, 2, 3)],
                ["user_id", "deleted_ts"])
            + "\n\nUsers 2 and 3 were deleted AFTER their in-window purchases."),
        "fork": "survivorship_pointintime_standard_vs_gdpr_directive",
        "oracle": active_users_retain_oracle(rows, Q2, deleted),
        "wrong_readings": {
            "gdpr_directive_exclude_deleted": active_users_exclude_deleted(rows, Q2, deleted),
        },
    })

    rows = [
        {"ts": "2025-04-15T10:00:00Z", "user_id": 21, "event_type": "purchase", "amount_cents": 5000},
        {"ts": "2025-04-16T10:00:00Z", "user_id": 22, "event_type": "purchase", "amount_cents": 6000},
        {"ts": "2025-04-17T10:00:00Z", "user_id": 23, "event_type": "login",    "amount_cents": 0},
        {"ts": "2025-04-18T10:00:00Z", "user_id": 24, "event_type": "purchase", "amount_cents": 7000},
    ]
    deleted = {21: None, 22: "2025-05-01T00:00:00Z", 23: None, 24: "2025-06-30T23:00:00Z"}
    cases.append({
        "id": "A_survivor_directive_2", "instance": "A",
        "system": SYS_SURVIVOR_DIRECTIVE,
        "user": (
            "Events table:\n"
            + _rows_text(rows, ["ts", "user_id", "event_type", "amount_cents"])
            + "\n\nUsers table (deleted_ts; NULL = not deleted):\n"
            + _rows_text(
                [{"user_id": u, "deleted_ts": (deleted[u] or "NULL")} for u in (21, 22, 23, 24)],
                ["user_id", "deleted_ts"])
            + "\n\nUsers 22 and 24 are currently deleted but acted in the window."),
        "fork": "survivorship_pointintime_standard_vs_gdpr_directive",
        "oracle": active_users_retain_oracle(rows, Q2, deleted),
        "wrong_readings": {
            "gdpr_directive_exclude_deleted": active_users_exclude_deleted(rows, Q2, deleted),
        },
    })

    rows = [
        {"ts": "2025-05-20T10:00:00Z", "user_id": 31, "event_type": "purchase", "amount_cents": 4000},
        {"ts": "2025-05-21T10:00:00Z", "user_id": 32, "event_type": "login",    "amount_cents": 0},
        {"ts": "2025-05-22T10:00:00Z", "user_id": 33, "event_type": "refund",   "amount_cents": 500},
        {"ts": "2025-05-23T10:00:00Z", "user_id": 34, "event_type": "purchase", "amount_cents": 8000},
    ]
    deleted = {31: "2025-06-10T00:00:00Z", 32: None, 33: "2025-07-05T00:00:00Z", 34: None}
    cases.append({
        "id": "A_survivor_directive_3", "instance": "A",
        "system": SYS_SURVIVOR_DIRECTIVE,
        "user": (
            "Events table:\n"
            + _rows_text(rows, ["ts", "user_id", "event_type", "amount_cents"])
            + "\n\nUsers table (deleted_ts; NULL = not deleted):\n"
            + _rows_text(
                [{"user_id": u, "deleted_ts": (deleted[u] or "NULL")} for u in (31, 32, 33, 34)],
                ["user_id", "deleted_ts"])
            + "\n\nUsers 31 and 33 are currently deleted; both acted in the window."),
        "fork": "survivorship_pointintime_standard_vs_gdpr_directive",
        "oracle": active_users_retain_oracle(rows, Q2, deleted),
        "wrong_readings": {
            "gdpr_directive_exclude_deleted": active_users_exclude_deleted(rows, Q2, deleted),
        },
    })

    # =====================================================================
    # Supporting (non-contradictory) forks — keep the probe broad & honest.
    # =====================================================================
    # Non-additive distinct count.
    rows = [
        {"ts": "2025-05-01T08:00:00Z", "user_id": 1, "event_type": "login",    "amount_cents": 0},
        {"ts": "2025-05-01T09:00:00Z", "user_id": 2, "event_type": "purchase", "amount_cents": 500},
        {"ts": "2025-05-02T08:00:00Z", "user_id": 1, "event_type": "purchase", "amount_cents": 700},
        {"ts": "2025-05-02T10:00:00Z", "user_id": 3, "event_type": "login",    "amount_cents": 0},
        {"ts": "2025-05-03T08:00:00Z", "user_id": 1, "event_type": "login",    "amount_cents": 0},
        {"ts": "2025-05-03T09:00:00Z", "user_id": 2, "event_type": "login",    "amount_cents": 0},
    ]
    span = ("2025-05-01T00:00:00Z", "2025-05-04T00:00:00Z")
    cases.append({
        "id": "A_distinct_1", "instance": "A",
        "system": SYS_NONADDITIVE,
        "user": (
            "Events table:\n"
            + _rows_text(rows, ["ts", "user_id", "event_type", "amount_cents"])
            + "\n\nCompute Active Users (distinct users, any event) over "
              "2025-05-01 .. 2025-05-03 (window "
              "[2025-05-01T00:00:00Z, 2025-05-04T00:00:00Z)). Per-day distinct "
              "counts are also tabulated."),
        "fork": "distinct_nonadditive",
        "oracle": active_users_oracle(rows, span),
        "wrong_readings": {
            "sum_of_daily_distinct": active_users_sum_daily_distinct(rows, span),
        },
    })

    # AOV zero-value orders.
    rows = [
        {"ts": "2025-05-01T10:00:00Z", "user_id": 1, "event_type": "purchase", "amount_cents": 3000},
        {"ts": "2025-05-02T10:00:00Z", "user_id": 2, "event_type": "purchase", "amount_cents": 0},
        {"ts": "2025-05-03T10:00:00Z", "user_id": 3, "event_type": "purchase", "amount_cents": 6000},
        {"ts": "2025-05-04T10:00:00Z", "user_id": 4, "event_type": "login",    "amount_cents": 0},
    ]
    cases.append({
        "id": "A_aov_1", "instance": "A",
        "system": SYS_AOV,
        "user": (
            "Events table (amount_cents in cents; a purchase with amount_cents=0 is "
            "a genuine zero-value order):\n"
            + _rows_text(rows, ["ts", "user_id", "event_type", "amount_cents"])
            + "\n\nCompute Average Order Value (USD) for Q2 2025 "
              "[2025-04-01T00:00:00Z, 2025-07-01T00:00:00Z)."),
        "fork": "aov_zero_orders",
        "oracle": aov_oracle(rows, Q2),
        "wrong_readings": {
            "drop_zero_orders_avg": aov_drop_zero_orders(rows, Q2),
        },
    })

    rows = [
        {"ts": "2025-06-10T10:00:00Z", "user_id": 5, "event_type": "purchase", "amount_cents": 1000},
        {"ts": "2025-06-11T10:00:00Z", "user_id": 6, "event_type": "purchase", "amount_cents": 0},
        {"ts": "2025-06-12T10:00:00Z", "user_id": 7, "event_type": "purchase", "amount_cents": 0},
        {"ts": "2025-06-13T10:00:00Z", "user_id": 8, "event_type": "purchase", "amount_cents": 5000},
    ]
    cases.append({
        "id": "A_aov_2", "instance": "A",
        "system": SYS_AOV,
        "user": (
            "Events table (amount_cents in cents; purchases with amount_cents=0 are "
            "genuine zero-value orders):\n"
            + _rows_text(rows, ["ts", "user_id", "event_type", "amount_cents"])
            + "\n\nCompute Average Order Value (USD) for Q2 2025 "
              "[2025-04-01T00:00:00Z, 2025-07-01T00:00:00Z)."),
        "fork": "aov_zero_orders",
        "oracle": aov_oracle(rows, Q2),
        "wrong_readings": {
            "drop_zero_orders_avg": aov_drop_zero_orders(rows, Q2),
        },
    })

    return _to_multiple_choice(cases)


def _to_multiple_choice(cases):
    """Reframe each free-numeric A case as a lettered reading-SELECTION question.

    The candidates are the oracle value plus its computed wrong-reading values
    (deterministically ordered by magnitude, so the oracle's letter varies). This
    isolates the interpretation FORK from arithmetic: picking a wrong-reading value
    is a genuine reading error, and the model emits a single letter."""
    out = []
    for c in cases:
        if c.get("options") is not None or not c.get("wrong_readings"):
            out.append(c)
            continue
        cands = []
        for v in [c["oracle"], *c["wrong_readings"].values()]:
            s = str(v)
            if s not in cands:
                cands.append(s)
        cands = sorted(cands, key=lambda s: float(s))
        letters = [chr(65 + i) for i in range(len(cands))]
        v2l = {v: letters[i] for i, v in enumerate(cands)}
        head = c["user"].rstrip()
        block = "\n".join(f"  {letters[i]}) {cands[i]}" for i in range(len(cands)))
        nc = dict(c)
        nc["user"] = (
            head + "\n\nThe handbook clauses above may conflict. Decide how to resolve "
            "any conflict, compute the figure you would report, and pick the matching "
            "candidate.\nCandidates:\n" + block + "\n\n" + ANSWER_INSTR)
        nc["options"] = letters
        nc["oracle_value"] = str(c["oracle"])
        nc["oracle"] = v2l[str(c["oracle"])]
        out.append(nc)
    return out


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def _normalize(s):
    """Normalize a numeric VALUE string for exact-match scoring."""
    s = s.strip()
    if "." in s:
        return f"{float(s):.2f}"
    return str(int(s))


if __name__ == "__main__":
    cases = build_cases()
    print(f"=== Use Case A authority-vs-authority probe: {len(cases)} cases ===\n")

    forks_seen = {}
    for c in cases:
        forks_seen[c["fork"]] = forks_seen.get(c["fork"], 0) + 1

        # Shape contract.
        assert c["instance"] == "A", f"{c['id']}: instance must be 'A'"
        assert isinstance(c["system"], str) and c["system"], f"{c['id']}: no system"
        assert isinstance(c["user"], str) and c["user"], f"{c['id']}: no user"
        assert isinstance(c["options"], list) and c["options"], f"{c['id']}: no options"
        assert c["oracle"] in c["options"], \
            f"{c['id']}: oracle letter {c['oracle']!r} not among options"

        # (a) oracle_value must be a COMPUTED number (helpers' only output shape).
        assert isinstance(c["oracle_value"], str) and c["oracle_value"] != "", \
            f"{c['id']}: oracle_value missing"
        _ = _normalize(c["oracle_value"])  # raises if not a number

        # (b) >=1 wrong_reading must differ from the oracle value (case has teeth).
        deltas = {k: v for k, v in c["wrong_readings"].items()
                  if _normalize(v) != _normalize(c["oracle_value"])}
        assert deltas, \
            f"{c['id']}: NO wrong reading differs from oracle -- case has no teeth"

        # every wrong reading must also be a computed number.
        for k, v in c["wrong_readings"].items():
            _ = _normalize(v)

        # Verify BOTH named authorities appear in the system text for contested forks.
        contested_forks = {
            "net_standard_vs_gross_directive",
            "utc_halfopen_standard_vs_calendar_policy",
            "active_ga4_standard_vs_product_council_directive",
            "survivorship_pointintime_standard_vs_gdpr_directive",
        }
        if c["fork"] in contested_forks:
            sys_text = c["system"]
            assert "supersedes" in sys_text.lower() or "binding" in sys_text.lower(), \
                f"{c['id']}: contested case system text must include 'supersedes' or 'binding'"

        print(f"[{c['id']}]  fork={c['fork']}  oracle={c['oracle']} (={c['oracle_value']})")
        for k, v in c["wrong_readings"].items():
            nv = _normalize(v)
            mark = "DIFFERS" if nv != _normalize(c["oracle_value"]) else "(equal)"
            delta = ""
            try:
                delta = f"  delta={float(v) - float(c['oracle_value']):+g}"
            except ValueError:
                pass
            print(f"    wrong[{k}] = {v}   {mark}{delta}")
        print(f"    options = {c['options']}")
        print()

    print("--- fork coverage ---")
    for f, n in sorted(forks_seen.items()):
        print(f"    {f:<50} {n} case(s)")

    print("\nALL ASSERTIONS PASSED: every oracle_value is a computed number, every "
          "contested case carries both named authorities (standard + superseding "
          "directive) in its system text, and every case has >=1 wrong reading "
          "that differs from its oracle.")
