-- Storage Plane schema (spec §2 Step 1): the frozen customer runtime state.
-- The runtime app (app.py) opens this file strictly read-only (?mode=ro), so
-- the engine itself rejects any attempt to "adjust user histories to satisfy a
-- flawed decision track" (spec §2 Step 1 enforcement). The file is deployed
-- root:root 0444 by provision.sh.
--
-- Monetary values are stored as integer USD (no floats) so the refund-threshold
-- comparison (MAX_REFUND_THRESHOLD_USD = 500) is exact and recomputable.

PRAGMA page_size = 4096;
PRAGMA journal_mode = DELETE;

CREATE TABLE customers (
    customer_id            TEXT    PRIMARY KEY,
    registration_age_hours INTEGER NOT NULL,   -- account age at session time, hours
    lifetime_orders        INTEGER NOT NULL,   -- count of orders ever placed
    return_velocity        REAL    NOT NULL,   -- fraction of orders returned (0..1)
    fraud_flag             INTEGER NOT NULL     -- 0 = clean, 1 = flagged
                           CHECK (fraud_flag IN (0, 1))
);

CREATE TABLE orders (
    order_id    TEXT    PRIMARY KEY,
    customer_id TEXT    NOT NULL REFERENCES customers(customer_id),
    value_usd   INTEGER NOT NULL                -- integer USD, no floats
                CHECK (value_usd >= 0),
    status      TEXT    NOT NULL
                CHECK (status IN ('DELIVERED', 'IN_TRANSIT', 'REFUNDED'))
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
