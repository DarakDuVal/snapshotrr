#!/usr/bin/env bash
set -e
source dev.env

run_backend() {
  echo "🔧 Starting backend on port $BACKEND_PORT"
  cd backend
  python app.py
}

run_frontend() {
  echo "🖥  Starting frontend on port $FRONTEND_PORT"
  cd frontend
  python app.py
}

run_all() {
  echo "🚀 Starting both backend and frontend..."
  tmux new-session -d -s dev './dev.sh backend' \; split-window -h './dev.sh frontend' \; attach
}

case "$1" in
  backend) run_backend ;;
  frontend) run_frontend ;;
  all) run_all ;;
  *)
    echo "Usage: ./dev.sh [backend|frontend|all]"
    exit 1
    ;;
esac
