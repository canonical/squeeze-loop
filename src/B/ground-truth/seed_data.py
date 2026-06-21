"""Deterministic seed for the Storage Plane (spec §2 Step 1).

These are the CANONICAL FIXTURES the whole squeeze loop references. They are
hand-authored constants (not random) on purpose: the other two planes (the
implementer's policy code and the exerciser's scenario scripts) reference these
exact customer_ids and order_ids, so they must be fixed and named. There is no
RNG here -- the same tuples are emitted every build, so base of the DB is
byte-reproducible.

Each fixture is chosen to exercise one branch of the reference policy:

  CUST_GOOD  -> nominal undelivered order               -> REIMBURSE
  CUST_LEGAL -> legal-keyword escalation                 -> ESCALATE
  CUST_NEW   -> new account + high-value order           -> DENY  (CLAUSE_3)
  CUST_DUP   -> already-refunded order (duplicate guard) -> DENY  (CLAUSE_1)
  CUST_FRAUD -> fraud_flag / high return velocity        -> DENY  (fraud guard)
"""

# (customer_id, registration_age_hours, lifetime_orders, return_velocity, fraud_flag)
CUSTOMERS = [
    ("CUST_GOOD",  8760, 20, 0.05, 0),
    ("CUST_LEGAL", 4380,  6, 0.10, 0),
    ("CUST_NEW",     24,  0, 0.00, 0),
    ("CUST_DUP",   9000, 15, 0.20, 0),
    ("CUST_FRAUD", 5000, 30, 0.90, 1),
]

# (order_id, customer_id, value_usd, status)  -- status in {DELIVERED,IN_TRANSIT,REFUNDED}
ORDERS = [
    ("ORD_GOOD",     "CUST_GOOD",   40, "IN_TRANSIT"),
    ("ORD_LEGAL",    "CUST_LEGAL",  75, "IN_TRANSIT"),
    ("ORD_HIGH",     "CUST_NEW",   900, "IN_TRANSIT"),
    ("ORD_REFUNDED", "CUST_DUP",   120, "REFUNDED"),
    ("ORD_FRAUD",    "CUST_FRAUD", 200, "IN_TRANSIT"),
]


def generate():
    """Return (customers, orders) as lists of tuples ready for executemany().

    Sorted by primary key so insertion order -- and therefore the on-disk DB --
    is deterministic regardless of how the literals above are ordered.
    """
    customers = sorted(CUSTOMERS, key=lambda c: c[0])
    orders = sorted(ORDERS, key=lambda o: o[0])
    return customers, orders
