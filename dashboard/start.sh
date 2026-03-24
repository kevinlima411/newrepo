#!/bin/bash
# Run Kevin Bot Dashboard
# Usage: GITHUB_TOKEN=your_token ./start.sh

if [ -z "$GITHUB_TOKEN" ]; then
  echo "ERROR: GITHUB_TOKEN is not set."
  echo "Usage: GITHUB_TOKEN=ghp_xxx ./start.sh"
  exit 1
fi

cd "$(dirname "$0")"

# Install deps if needed
pip install -q -r requirements.txt

export PORT=${PORT:-5555}
echo "Starting dashboard on http://192.168.1.239:$PORT"
python app.py
