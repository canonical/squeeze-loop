"""Deterministic seed for the storage plane (spec §2 Plane 2), app_state.db.

These are the CANONICAL FIXTURES the whole split-planes loop references. They are
hand-authored constants (not random) on purpose: the document plane
(base_schema.json), the implementer's runtime app, and the exerciser's conformance
scripts all reference these exact uuids/keys, so they must be fixed and named.
There is no RNG here -- the same tuples are emitted every build, so the on-disk DB
is byte-reproducible.

The configured API key `test_secure_token_abc123` identifies seeded user `u-0001`
(Ada Lovelace). Note that the public API only ever exposes user_uuid; the integer
`id` column is internal and is never serialized onto the wire.
"""

# (id, user_uuid, display_name, updated_at)
USERS = [
    (1, "u-0001", "Ada Lovelace", "2025-01-01T00:00:00Z"),
    (2, "u-0002", "Alan Turing",  "2025-01-02T00:00:00Z"),
    (3, "u-0003", "Grace Hopper", "2025-01-03T00:00:00Z"),
]

# (api_key, user_uuid)
API_KEYS = [
    ("test_secure_token_abc123", "u-0001"),
]


def generate():
    """Return (users, api_keys) as lists of tuples ready for executemany().

    Sorted by primary key so insertion order -- and therefore the on-disk DB --
    is deterministic regardless of how the literals above are ordered.
    """
    users = sorted(USERS, key=lambda u: u[0])
    api_keys = sorted(API_KEYS, key=lambda k: k[0])
    return users, api_keys
