#!/usr/bin/env python3
"""
CLI wrapper for sms_classifier.classify.

  python agents/cleaning/classify_sms.py --message "can we do friday" --history history.json
  echo '{"message": "ok thanks", "thread_history": []}' | python agents/cleaning/classify_sms.py

history.json: a JSON list of strings or {"role", "text"} objects, oldest first.
Prints the JSON result to stdout. Exit code 0 even on API failure (check "error").
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sms_classifier import classify  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="Classify an inbound DK SMS.")
    parser.add_argument("--message", help="SMS text. If omitted, reads a JSON payload from stdin.")
    parser.add_argument("--history", help="Path to a JSON file with the thread history.")
    args = parser.parse_args()

    if args.message is not None:
        message = args.message
        history = json.loads(Path(args.history).read_text()) if args.history else []
    else:
        payload = json.load(sys.stdin)
        message = payload.get("message", "")
        history = payload.get("thread_history", [])

    print(json.dumps(classify(message, history)))


if __name__ == "__main__":
    main()
