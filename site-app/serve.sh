#!/usr/bin/env bash
# AI Academy — build (if needed) and serve the site locally.
#
#   ./site-app/serve.sh                    # serve on :8000
#   ./site-app/serve.sh 9000               # serve on :9000
#   ./site-app/serve.sh --rebuild          # regenerate first
#
# Set your own passcodes:
#   AIA_STUDENT_PASS="..." AIA_TEACHER_PASS="..." ./site-app/serve.sh --rebuild
#
# Nothing is published. The server binds to localhost only.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT=8000
REBUILD=0

for arg in "$@"; do
  case "$arg" in
    --rebuild) REBUILD=1 ;;
    [0-9]*)    PORT="$arg" ;;
    *) echo "usage: serve.sh [port] [--rebuild]" >&2; exit 2 ;;
  esac
done

if [[ ! -d "$HERE/dist" || "$REBUILD" == 1 ]]; then
  echo "Building…"
  python3 "$HERE/build.py" --clean
fi

echo
echo "  AI Academy is running at  http://localhost:$PORT/"
echo
echo "    🎒 student passcode     ${AIA_STUDENT_PASS:-student1234}"
echo "    🧑‍🏫 teacher passcode     ${AIA_TEACHER_PASS:-teacher1234}"
echo
echo "  Only the home page opens without a passcode."

# serve.py resolves extensionless URLs the way Cloudflare Workers does; plain
# `http.server` would 404 on every generated link.
exec python3 "$HERE/serve.py" "$PORT"
