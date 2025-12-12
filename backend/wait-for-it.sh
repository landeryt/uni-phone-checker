#!/usr/bin/env sh
# Simple wait-for-it script for the backend container
# Usage: ./wait-for-it.sh host port timeout [-- command args]

HOST=${1:-db}
PORT=${2:-3306}
TIMEOUT=${3:-30}

# shift past the first three args if any command follows
shift 3 || true

if [ -z "$HOST" ] || [ -z "$PORT" ]; then
  echo "Usage: $0 host port [timeout] [-- command args]" 1>&2
  exit 2
fi

echo "Waiting for $HOST:$PORT with timeout ${TIMEOUT}s..."
START=$(date +%s)

while :; do
  if command -v nc >/dev/null 2>&1; then
    nc -z "$HOST" "$PORT" >/dev/null 2>&1 && break
  else
    # fallback to /dev/tcp (may not exist in some shells)
    (echo > /dev/tcp/"$HOST"/"$PORT") >/dev/null 2>&1 && break
  fi

  NOW=$(date +%s)
  if [ $((NOW - START)) -ge "$TIMEOUT" ]; then
    echo "Timeout after ${TIMEOUT}s waiting for ${HOST}:${PORT}" 1>&2
    exit 1
  fi
  sleep 1
done

echo "$HOST:$PORT is available"

# If a command is provided, execute it
if [ "$#" -gt 0 ]; then
  echo "Executing: $@"
  exec "$@"
fi

exit 0
