#!/usr/bin/env bash
set -euo pipefail

echo "[entrypoint] waiting for database at ${DB_HOST}:${DB_PORT}..."
python - <<'PY'
import os, socket, sys, time

host = os.environ.get("DB_HOST", "db")
port = int(os.environ.get("DB_PORT", "3306"))
deadline = time.time() + 60

while time.time() < deadline:
    try:
        with socket.create_connection((host, port), timeout=3):
            print(f"[entrypoint] database reachable at {host}:{port}")
            sys.exit(0)
    except OSError as e:
        print(f"[entrypoint] not ready ({e}); retrying...")
        time.sleep(2)

print(f"[entrypoint] timed out waiting for {host}:{port}", file=sys.stderr)
sys.exit(1)
PY

if [ "${RUN_MIGRATIONS:-1}" = "1" ]; then
    echo "[entrypoint] creating tables (idempotent)..."
    python create_tables.py
fi

echo "[entrypoint] launching: $*"
exec "$@"
