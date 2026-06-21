#!/usr/bin/env bash
# Runtime plane launcher (spec §2 Plane 2): boot the frozen profile API server
# bound to 127.0.0.1:8000. Mirrors /opt/squeeze/runtime_app/run_server.sh once
# deployed by provision.sh. Picks the deployed reference_server.py if present,
# else the local one.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"

if [ -f "/opt/squeeze/runtime_app/reference_server.py" ]; then
    SERVER="/opt/squeeze/runtime_app/reference_server.py"
else
    SERVER="$HERE/reference_server.py"
fi

exec python3 "$SERVER" --host 127.0.0.1 --port "${PORT:-8000}" "$@"
