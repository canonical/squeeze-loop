-- Storage Plane schema (spec §2 Step 1): the raw transaction event log.
-- Timestamps are canonical ISO-8601 UTC ("...Z"); lexicographic order on these
-- strings equals chronological order, so quarter windows are plain range scans.
-- Monetary values are integer cents (no floats in the warehouse) so every
-- derived figure is exact and recomputable.

PRAGMA page_size = 4096;
PRAGMA journal_mode = DELETE;

CREATE TABLE users (
    user_id     INTEGER PRIMARY KEY,
    signup_ts   TEXT    NOT NULL,            -- ISO-8601 UTC
    deleted_ts  TEXT,                        -- NULL = still active; row is KEPT
                                             --   even after deletion (survivorship)
    home_region TEXT    NOT NULL
);

CREATE TABLE events (
    event_id     INTEGER PRIMARY KEY,
    ts           TEXT    NOT NULL,           -- ISO-8601 UTC (canonical)
    user_id      INTEGER NOT NULL REFERENCES users(user_id),
    event_type   TEXT    NOT NULL CHECK (event_type IN ('login','purchase','refund')),
    amount_cents INTEGER NOT NULL DEFAULT 0  -- 0 for login; > 0 for purchase/refund
                 CHECK (amount_cents >= 0),
    region       TEXT    NOT NULL            -- region the event was observed from
);

CREATE INDEX idx_events_ts   ON events(ts);
CREATE INDEX idx_events_type ON events(event_type, ts);
