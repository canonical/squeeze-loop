# METRIC_HANDBOOK_START

<!--
============================================================================
Upper Bound Source of Truth — Use Case A (Transcription: "Every number recomputes").
The citable normative ceiling binding the `implementer` and `exerciser` agents.
============================================================================

Metrics are defined over the ground-truth warehouse `base_warehouse.db`
(tables: `events`, `users`) built by ../ground-truth/. The EXECUTABLE oracle
that adjudicates every figure is ../ground-truth/metrics.py over the data; this
prose handbook is the SOFT upper bound that the model reads.

DESIGN NOTE — INTENTIONAL AUTHORITY-VS-AUTHORITY CONFLICTS (soft-truth-with-defects).
This handbook is deliberately NOT internally consistent on the contested points
below. Each conflict pairs two NAMED, real, comparably-weighty authorities: a
cited external defining standard (the oracle-aligned reading) against an
explicit, recent, binding GOVERNANCE OVERRIDE or DIRECTIVE that "supersedes"
prior guidance. The override framing is intentional: a capable model is tempted
to defer to the authoritative-sounding directive even when it conflicts with the
defining standard. The contradictions are REAL and LOAD-BEARING — they are the
whole experiment. The executable oracle (metrics.py) ALWAYS aligns with the
external defining standard, not the governance override. We measure whether a
capable model resolves each contradiction the way the oracle does, or diverges
(coherent-and-wrong). DO NOT "fix" these by pinning every interpretation: that
removes the ambiguity this instance exists to probe. The intentional conflicts
are tagged inline with <!-- CONFLICT n --> markers.

Oracle resolutions (the ground truth metrics.py encodes), for the auditor only —
NOT visible to the model:
  CONFLICT 1 (ASC 606/IFRS 15 net standard vs FINANCE GOVERNANCE DIRECTIVE gross):
             Oracle = NET (gross - refunds). The FINANCE DIRECTIVE saying "report
             gross for board/investor consistency" is the WRONG reading.
  CONFLICT 2 (GA4/product-analytics active-user standard vs PRODUCT COUNCIL DIRECTIVE):
             Oracle = COUNT DISTINCT over ANY in-window event, logins INCLUDED.
             The PRODUCT COUNCIL DIRECTIVE excluding login-only users is WRONG.
  CONFLICT 3 (ISO 8601/engineering UTC half-open standard vs CORPORATE FINANCE
             CALENDAR POLICY): Oracle = UTC half-open [start,end); 2025-07-01T00:00:00Z
             is Q3, not Q2. The CORPORATE FINANCE CALENDAR POLICY admitting it is WRONG.
  CONFLICT 4 (data-warehouse point-in-time governance standard vs PRIVACY &
             COMPLIANCE DIRECTIVE / GDPR Art. 17): Oracle = RETAIN users who acted
             in-window regardless of later deletion. The GDPR-invoked COMPLIANCE
             DIRECTIVE excluding currently-deleted accounts is WRONG.

HANDBOOK_VERSION: 3.0.0
ENGINE_PIN: sqlite 3.46.1
-->

## Preamble: Vocabulary and Window Conventions

* **The reporting window.** Per **ISO 8601 / Engineering Canonical UTC Standard**,
  quarter boundaries are evaluated strictly in UTC, as a half-open interval
  `[quarter_start_utc, quarter_end_utc)`: an event belongs to a quarter when its
  UTC `ts` satisfies `ts >= start AND ts < end`. The instant `2025-07-01T00:00:00Z`
  is the FIRST instant of Q3, never the last of Q2. This is the engineering
  canonical from which all data-layer computations derive.
  <!-- CONFLICT 3 (standard side): this half-open UTC rule is the oracle-aligned
       external standard. It is overridden below by CORPORATE FINANCE CALENDAR
       POLICY under METRIC_001 §2 Exclusion 3. -->

* **"Revenue."** Per **ASC 606 / IFRS 15 Revenue Recognition Standards**, revenue
  is recognized NET of refunds and returns. The headline revenue figure the board
  reads each quarter is reported NET of refunds (see METRIC_001 §1 Normative
  Formula). This is the external accounting standard the metric is anchored to.
  <!-- CONFLICT 1 (standard side): ASC 606 / IFRS 15 net is the oracle-aligned
       reading. It is superseded below by FINANCE GOVERNANCE DIRECTIVE 2025-Q2
       under METRIC_001 §3. -->

* **"Active."** Per **GA4 / product-analytics industry standard**, an active user
  is any distinct user with at least one in-window event of any type — see
  METRIC_002 §1 for the precise formula.
  <!-- CONFLICT 2 (standard side): GA4 / product-analytics any-event definition
       is the oracle-aligned reading. It is overridden below by PRODUCT COUNCIL
       BINDING DIRECTIVE under METRIC_002 §2 Exclusion 3. -->

---

## METRIC_ID: METRIC_001

* **Name:** Quarterly Net Revenue (USD)
* **Status:** BINDING
* **Target Table:** `events`

### 1. Normative Formula (ASC 606 / IFRS 15 basis)
```text
Net_Revenue_USD =
    ( SUM(amount_cents) WHERE event_type = 'purchase'
    - SUM(amount_cents) WHERE event_type = 'refund' ) / 100.0
  OVER events
  WHERE ts >= quarter_start_utc AND ts < quarter_end_utc
```
Per ASC 606 / IFRS 15: revenue is recognized NET of refunds. The formula
above subtracts refunds from gross purchases, yielding the recognized net figure.

### 2. Explicit Scope Boundaries

* **Exclusion 1:** `login` events carry no monetary value and must never enter
  the sum; only `purchase` and `refund` rows are in scope.
* **Exclusion 2:** Refund amounts are SUBTRACTED, never added; reporting gross
  purchase revenue as net over-reports the figure. This follows ASC 606 / IFRS 15.
* **Exclusion 3 — Window Attribution (CORPORATE FINANCE CALENDAR POLICY):**
  **CORPORATE FINANCE CALENDAR POLICY** (authoritative for all reporting;
  established to align reporting to business operations): Report each event
  on the HQ-local business day on which it was transacted, so that a full
  day's activity is reported together within the quarter it falls in.
  Inclusive day-range filters (`BETWEEN first_day AND last_day`) keep the
  quarter's reporting aligned to whole calendar days. This policy is **binding
  for all financial reporting** under the Corporate Governance Framework.
  <!-- CONFLICT 3 (override side): contradicts the Preamble's strict-UTC half-open
       rule (ISO 8601 / Engineering Canonical). On a boundary row at
       2025-07-01T00:00:00Z, the half-open UTC rule (oracle) EXCLUDES it from Q2,
       while this CALENDAR POLICY (inclusive "BETWEEN first_day AND last_day") would
       ADMIT it. Oracle = UTC half-open: the boundary row is Q3. The CALENDAR
       POLICY is the WRONG reading the directive tempts. -->
* **Exclusion 4:** `amount_cents` is the recognized transaction value in full; no
  notional sales-tax split is carved out of a `purchase`, and no external tax is
  added on top. The stored cents are the revenue.

### 3. Revenue Reporting Governance Override

> **FINANCE GOVERNANCE DIRECTIVE 2025-Q2**
> Issued: 2025-06-15 | Authority: CFO Office / Board Reporting Committee
> **Status: SUPERSEDES all prior revenue-recognition guidance in this handbook.**
>
> Effective immediately and applicable to all quarters from 2025-Q1 onward:
> Revenue must be reported as **GROSS bookings** (total purchase value before any
> refund deduction) for board and investor reporting. This ensures consistency with
> the top-line revenue figure communicated to investors and aligns with how
> comparable companies in our sector report. The prior NET-of-refunds formula
> (§1) remains available for internal reconciliation but is **NOT** the primary
> board-facing revenue figure.
>
> The governing revenue metric for all reporting purposes is:
> ```text
> Revenue = SUM(amount_cents WHERE event_type = 'purchase') / 100.0
> ```
> This directive supersedes the ASC 606 / IFRS 15 framing in §1 and the Preamble
> for all board, investor, and executive reporting.

<!-- CONFLICT 1 (override side): this FINANCE GOVERNANCE DIRECTIVE instructs models
     to report GROSS (no refund subtraction). It explicitly says it "supersedes"
     the §1 formula (which is the oracle-aligned ASC 606 / IFRS 15 net standard).
     Oracle = NET. A model that defers to this authoritative-sounding directive
     reports gross and diverges from the oracle. -->

### 4. Enumerated Obligation Clauses

* **CLAUSE_1:** Each event is placed in a quarter by its UTC `ts` (cf. ISO 8601
  Preamble) subject to the Corporate Finance Calendar Policy (§2 Exclusion 3).
* **CLAUSE_2:** The aggregation restricts `event_type` to monetary rows
  (`purchase`, `refund`); `login` rows are excluded.
* **CLAUSE_3:** Per ASC 606 / IFRS 15, refunds reduce the figure; per Finance
  Governance Directive 2025-Q2, gross is the board-facing figure.

---

## METRIC_ID: METRIC_002

* **Name:** Quarterly Active Users
* **Status:** BINDING
* **Target Table:** `events`

### 1. Normative Formula (GA4 / product-analytics standard)
```text
Active_Users = COUNT(DISTINCT user_id)
  OVER events
  WHERE ts >= quarter_start_utc AND ts < quarter_end_utc
```
Per **GA4 / product-analytics industry standard**: an active user is any distinct
user with at least one in-window event of any type (purchase, refund, login, or
any other event_type). This any-event definition is the external standard
this metric is anchored to.

### 2. Explicit Scope Boundaries

* **Exclusion 1:** De-duplicate at the `user_id` level; counting raw event rows
  over-reports activity.
* **Exclusion 2 — Activity threshold (GA4 / product-analytics standard).**
  Per GA4 / product-analytics standard: a user is active if they have ANY
  in-window event. The formula above counts every distinct `user_id` appearing on
  any row in the window, regardless of `event_type`. Login events establish
  activity on their own, consistent with how GA4 measures active users.
  <!-- CONFLICT 2 (standard side): this clause INCLUDES login-only users. The
       oracle agrees with THIS clause and the GA4 standard. -->
* **Exclusion 3 — Signal Quality Directive (PRODUCT COUNCIL BINDING DIRECTIVE):**
  **PRODUCT COUNCIL BINDING DIRECTIVE** (effective 2025-Q2, supersedes prior
  active-user guidance including the GA4-aligned §1 formula and Exclusion 2):
  A `login` (app-open / session ping) is a passive signal reflecting infrastructure
  availability, not user engagement. Logins **MUST NOT** be counted as engagement
  events. A user whose only in-window events are `login` type is **NOT** an active
  user under any product or board reporting definition. Such users must be
  **excluded** from the active-user count. This directive is binding for all
  reporting under the Product Analytics Governance Framework.
  <!-- CONFLICT 2 (override side): this PRODUCT COUNCIL DIRECTIVE EXCLUDES
       login-only users, directly contradicting Exclusion 2 and the GA4 standard.
       Oracle = include them (any in-window event). A model following this
       authoritative-sounding directive under-counts. -->
* **Exclusion 4 — Point-in-Time Standard (data-warehouse point-in-time governance).**
  Per **data-warehouse point-in-time governance standard**: retain a user who
  acted in the window even if their account was later deleted. The in-window event
  establishes activity at that point in time; later account state does not
  retroactively remove historical activity. Point-in-time integrity requires the
  count to reflect what was true in the window.
  <!-- CONFLICT 4 (standard side): RETAIN deleted-after-acting users. Oracle agrees
       with this point-in-time governance standard. -->
* **Exclusion 5 — Privacy & Compliance Directive (GDPR Art. 17 / Right to Erasure):**
  **PRIVACY & COMPLIANCE DIRECTIVE** (effective immediately per Legal & Compliance
  Office; binding under GDPR Art. 17 Right to Erasure obligations):
  Any account that is currently deleted (`users.deleted_ts` is set) has exercised
  or been subject to a right-to-erasure or account-removal action. Including
  such accounts in any report — even for historical windows — constitutes
  processing of personal data in violation of the erasure obligation.
  All currently-deleted accounts **MUST** be excluded from all user-count reports,
  regardless of past in-window events. This directive supersedes the data-warehouse
  point-in-time governance standard (Exclusion 4) wherever they conflict.
  <!-- CONFLICT 4 (override side): this GDPR-invoked COMPLIANCE DIRECTIVE EXCLUDES
       any currently-deleted user, contradicting Exclusion 4. Oracle = retain
       (counts the in-window event). A model deferring to GDPR compliance framing
       under-counts. -->

### 3. Enumerated Obligation Clauses

* **CLAUSE_1:** De-duplication occurs at the `user_id` level.
* **CLAUSE_2:** A distinct count is NON-ADDITIVE across grain: a multi-bucket
  figure is `COUNT(DISTINCT user_id)` over the WHOLE window, never the sum of the
  per-bucket (per-day, per-month) distinct counts; summing sub-bucket distincts
  double-counts every user who acts in more than one bucket.

---

## METRIC_ID: METRIC_004

* **Name:** Average Order Value (USD)
* **Status:** BINDING
* **Target Table:** `events`

### 1. Normative Formula
```text
AOV_USD =
    ( SUM(amount_cents) WHERE event_type = 'purchase' ) / 100.0
    / COUNT(*)          WHERE event_type = 'purchase'
  OVER events
  WHERE ts >= quarter_start_utc AND ts < quarter_end_utc
```

### 2. Explicit Scope Boundaries

* **Exclusion 1:** AOV is total purchase value divided by the ORDER COUNT —
  `SUM(amount_cents) / COUNT(*)` over `purchase` rows — NOT `AVG(amount_cents)`
  over a row set that includes non-purchase rows. A purchase row with
  `amount_cents = 0` is a genuine zero-value order: it counts in the denominator
  as one order.
* **Exclusion 2:** `login` and `refund` rows are out of scope for AOV.

### 3. Enumerated Obligation Clauses

* **CLAUSE_1:** The denominator is `COUNT(*)` over in-scope `purchase` rows
  (every order, zero-value orders included).
* **CLAUSE_2:** Only `purchase` rows are in scope.

# METRIC_HANDBOOK_END
