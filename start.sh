#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# Activate virtual environment
if [ ! -d "venv" ]; then
  echo "No venv found. Creating one..."
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
else
  source venv/bin/activate
fi

# Drop and reload database
echo "Dropping and reloading database..."
python seed.py

PORT="${PORT:-5050}"
if lsof -ti :"$PORT" &>/dev/null; then
  echo "Killing existing process on port $PORT..."
  kill -9 $(lsof -ti :"$PORT")
  sleep 1
fi

echo "Starting Flask server on port $PORT..."
PORT="$PORT" python run.py
