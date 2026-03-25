#!/usr/bin/env python3
"""
Logos — Daily Learning Agent
Run: python agents/logos/logos.py
Debug: python agents/logos/logos.py --dry-run
"""

import os
import sys
import json
import datetime
import requests
from pathlib import Path

BASE = Path(__file__).parent
HISTORY_FILE = BASE / "history.json"
SESSIONS_DIR = BASE / "sessions"
SYSTEM_PROMPT_FILE = BASE / "SYSTEM_PROMPT.md"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
OPUS_MODEL_OR = "anthropic/claude-opus-4-5"
OPUS_MODEL_AN = "claude-opus-4-5"


# ── History ──────────────────────────────────────────────────────────────────

def load_history():
    if HISTORY_FILE.exists():
        return json.loads(HISTORY_FILE.read_text())
    return {"first_run_answer": None, "sessions": []}


def save_history(history):
    HISTORY_FILE.write_text(json.dumps(history, indent=2))


def get_recent_topics(history, days=30):
    cutoff = datetime.date.today() - datetime.timedelta(days=days)
    recent = []
    for s in history["sessions"]:
        try:
            session_date = datetime.date.fromisoformat(s["date"])
            if session_date >= cutoff:
                recent.append(s["topic"])
        except (KeyError, ValueError):
            continue
    return recent


# ── First-run initialization ──────────────────────────────────────────────────

def run_onboarding(history):
    print("\n── LOGOS FIRST RUN ──────────────────────────────────────────")
    print("Before your first session, one question:\n")
    print("  What's a belief you hold confidently that you've never")
    print("  seriously tried to disprove?\n")
    answer = input("Your answer: ").strip()
    if not answer:
        answer = "(no answer provided)"
    history["first_run_answer"] = answer
    save_history(history)
    print("\nStored. This will personalize your STEELMAN and FALSIFY exercises.")
    print("─────────────────────────────────────────────────────────────\n")
    return history


# ── Prompt assembly ───────────────────────────────────────────────────────────

def build_prompt(history):
    system_prompt = SYSTEM_PROMPT_FILE.read_text()

    today = datetime.date.today()
    day_name = today.strftime("%A")  # e.g. "Wednesday"
    date_str = today.isoformat()

    recent_topics = get_recent_topics(history)
    topics_block = (
        "None yet — this is the first session."
        if not recent_topics
        else "\n".join(f"- {t}" for t in recent_topics)
    )

    onboarding_answer = history.get("first_run_answer") or "(not provided)"

    user_message = f"""Today is {day_name}, {date_str}.

RECENT TOPICS (do not repeat within 30 days):
{topics_block}

USER BELIEF (for personalized STEELMAN/FALSIFY exercises):
"{onboarding_answer}"

Generate today's Logos session. Follow the full session architecture exactly."""

    return system_prompt, user_message


# ── API call ──────────────────────────────────────────────────────────────────

def call_claude(system_prompt, user_message):
    api_mode = os.environ.get("LOGOS_API", "openrouter").lower()

    if api_mode == "anthropic":
        key = os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            sys.exit("Error: ANTHROPIC_API_KEY not set.")
        resp = requests.post(
            ANTHROPIC_URL,
            headers={
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": OPUS_MODEL_AN,
                "max_tokens": 8192,
                "system": system_prompt,
                "messages": [{"role": "user", "content": user_message}],
            },
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()["content"][0]["text"]

    else:  # openrouter (default)
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            sys.exit("Error: OPENROUTER_API_KEY not set.")
        resp = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {key}",
                "content-type": "application/json",
            },
            json={
                "model": OPUS_MODEL_OR,
                "max_tokens": 8192,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
            },
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


# ── Output saving ─────────────────────────────────────────────────────────────

def extract_topic(content):
    """Pull topic from the session header line: SESSION [DATE] — [TOPIC TITLE]"""
    for line in content.splitlines():
        if "SESSION" in line and "—" in line:
            parts = line.split("—", 1)
            if len(parts) == 2:
                return parts[1].strip().rstrip("═").strip()
    # Fallback: grab first ## heading
    for line in content.splitlines():
        if line.startswith("## "):
            return line[3:].strip()
    return "unknown-topic"


def save_output(content):
    SESSIONS_DIR.mkdir(exist_ok=True)
    date_str = datetime.date.today().isoformat()
    filename = SESSIONS_DIR / f"{date_str}_logos.md"
    filename.write_text(content)
    return filename, date_str


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    dry_run = "--dry-run" in sys.argv

    history = load_history()

    if history["first_run_answer"] is None:
        history = run_onboarding(history)

    system_prompt, user_message = build_prompt(history)

    if dry_run:
        print("── DRY RUN — SYSTEM PROMPT ──────────────────────────────────")
        print(system_prompt[:500], "...\n")
        print("── USER MESSAGE ─────────────────────────────────────────────")
        print(user_message)
        print("─────────────────────────────────────────────────────────────")
        print("No API call made.")
        return

    print("Generating today's Logos session...", flush=True)
    content = call_claude(system_prompt, user_message)

    output_file, date_str = save_output(content)

    topic = extract_topic(content)
    history["sessions"].append({
        "date": date_str,
        "topic": topic,
    })
    save_history(history)

    print(f"\nSession saved: {output_file}")
    print(f"Topic: {topic}")


if __name__ == "__main__":
    main()
