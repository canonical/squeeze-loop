-- Storage schema (spec §2 Plane 2): the frozen runtime app state, app_state.db.
-- The runtime server (reference_server.py) opens this file strictly read-only
-- (?mode=ro) and keeps all mutations IN MEMORY, so the engine itself rejects any
-- attempt to write the ground truth -- the file stays immutable and the build
-- stays byte-deterministic. The file is deployed root:root 0444 by provision.sh.
--
-- The public API maps callers to user_uuid (TEXT), NEVER to the internal integer
-- id. The id column exists only as the primary key; it is never serialized onto
-- the wire (the "no integer id leak" invariant of Use Case C).

PRAGMA page_size = 4096;
PRAGMA journal_mode = DELETE;

CREATE TABLE users (
    id           INTEGER PRIMARY KEY,        -- internal id; NEVER serialized
    user_uuid    TEXT    UNIQUE NOT NULL,    -- public resource identifier
    display_name TEXT    NOT NULL,
    updated_at   TEXT    NOT NULL            -- ISO-8601 Z timestamp
);

CREATE TABLE api_keys (
    api_key   TEXT PRIMARY KEY,              -- bearer key presented as X-API-Key
    user_uuid TEXT NOT NULL REFERENCES users(user_uuid)
);
