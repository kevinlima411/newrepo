"""
SMS Intent Classifier — Cleaning Agent foundation.

Classifies an inbound DK SMS into one of five categories using Claude Haiku.
Import:  from sms_classifier import classify
CLI:     python agents/cleaning/classify_sms.py --message "can we do friday"
"""

import json

import anthropic

MODEL = "claude-haiku-4-5"
CATEGORIES = ["reschedule", "complaint", "new_booking", "question", "other"]
CONFIDENCE_THRESHOLD = 0.6  # below this → "other" + flagged_for_review (complaints excepted)
HISTORY_WINDOW = 5          # last N thread messages sent as context

SYSTEM_PROMPT = """You classify inbound SMS messages sent to DK Organizing & Cleaning, a home cleaning company.

Categories:
- reschedule: move, cancel, or confirm a change to an existing appointment
- complaint: unhappy about quality, a missed appointment, billing, or staff conduct
- new_booking: wants to start service or book a job that is not a change to an existing appointment
- question: asks for info (pricing, availability, policy, what's included) with no booking, reschedule, or complaint intent
- other: none of the above (thanks, acknowledgments, spam, unclear)

Use the thread history to resolve short replies like "yes that works".
If a message mixes a complaint with anything else, choose complaint.
confidence is your probability (0-1) that the category is correct. Be honest; use low values when the message is ambiguous."""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "category": {"type": "string", "enum": CATEGORIES},
        "confidence": {"type": "number"},
    },
    "required": ["category", "confidence"],
    "additionalProperties": False,
}

_client = None


def _get_client():
    global _client
    if _client is None:
        # SDK retries 429 / 5xx / connection errors once before raising.
        _client = anthropic.Anthropic(max_retries=1, timeout=30.0)
    return _client


def _format_history(thread_history, window):
    """Accepts a list of strings or {role, text[, timestamp]} dicts, oldest first."""
    lines = []
    for item in (thread_history or [])[-window:] if window > 0 else []:
        if isinstance(item, dict):
            role = item.get("role", "unknown")
            text = item.get("text", "")
        else:
            role, text = "unknown", str(item)
        lines.append(f"[{role}] {text}")
    return "\n".join(lines)


def _build_user_content(message, thread_history, window):
    history = _format_history(thread_history, window)
    parts = []
    if history:
        parts.append(f"<thread_history>\n{history}\n</thread_history>")
    parts.append(f"<new_message>\n{message}\n</new_message>")
    return "\n\n".join(parts)


def _fallback(error):
    return {
        "category": "other",
        "confidence": 0.0,
        "flagged_for_review": True,
        "error": error,
    }


def classify(message, thread_history=None, *, threshold=CONFIDENCE_THRESHOLD,
             history_window=HISTORY_WINDOW, client=None):
    """
    Classify one inbound SMS. Never raises on API problems.

    Returns {"category", "confidence", "flagged_for_review"} plus "error"
    when the call failed, and "raw_category" when a low-confidence result
    was overridden to "other". Low-confidence complaints are NOT overridden:
    they stay "complaint" (so escalation fires) with flagged_for_review=True.
    """
    if not message or not message.strip():
        return _fallback("empty message")

    client = client or _get_client()
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=200,
            system=SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": _build_user_content(message, thread_history, history_window),
            }],
            output_config={"format": {"type": "json_schema", "schema": OUTPUT_SCHEMA}},
        )
    except anthropic.AuthenticationError:
        return _fallback("auth error: check ANTHROPIC_API_KEY")
    except anthropic.RateLimitError:
        return _fallback("rate limited")
    except anthropic.APIStatusError as e:
        return _fallback(f"api error {e.status_code}: {e.message}")
    except anthropic.APIConnectionError:
        return _fallback("connection error")
    except TypeError as e:
        # SDK raises TypeError at request time when no credentials are configured.
        return _fallback(f"client error: {e}")

    if response.stop_reason != "end_turn":
        return _fallback(f"unexpected stop_reason: {response.stop_reason}")

    try:
        text = next(b.text for b in response.content if b.type == "text")
        data = json.loads(text)
        category = data["category"]
        confidence = max(0.0, min(1.0, float(data["confidence"])))
    except (StopIteration, ValueError, KeyError, TypeError) as e:
        return _fallback(f"malformed response: {e}")

    if category not in CATEGORIES:
        return _fallback(f"unknown category: {category}")

    if confidence < threshold and category == "complaint":
        # A missed complaint costs more than a false alarm: keep it routed to
        # escalation, but flag it so a human double-checks.
        return {"category": "complaint", "confidence": confidence, "flagged_for_review": True}
    if confidence < threshold:
        return {
            "category": "other",
            "confidence": confidence,
            "flagged_for_review": True,
            "raw_category": category,
        }
    return {"category": category, "confidence": confidence, "flagged_for_review": False}
