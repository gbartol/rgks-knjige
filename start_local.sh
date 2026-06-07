#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

set -a
source .env
set +a

echo "Starting backend..."
cd "$SCRIPT_DIR/backend"

source .venv/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py runserver &
BACKEND_PID=$!

echo "Starting frontend..."
cd "$SCRIPT_DIR/frontend"

npx vite &
FRONTEND_PID=$!

cleanup() {
  trap - EXIT INT TERM
  echo "Stopping..."
  kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
  wait $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
  echo "Done"
}
trap cleanup EXIT INT TERM

echo "Frontend: http://localhost:5173"
echo "Admin: http://localhost:8000/admin/"

wait
