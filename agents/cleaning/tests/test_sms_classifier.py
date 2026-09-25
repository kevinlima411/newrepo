"""Unit tests for sms_classifier — no API calls, uses a fake client."""

import json
from types import SimpleNamespace

import anthropic
import httpx2 as httpx
import pytest

import sms_classifier
from sms_classifier import classify


class FakeMessages:
    def __init__(self, text=None, stop_reason="end_turn", exc=None):
        self.text, self.stop_reason, self.exc = text, stop_reason, exc
        self.last_kwargs = None

    def create(self, **kwargs):
        self.last_kwargs = kwargs
        if self.exc:
            raise self.exc
        content = [SimpleNamespace(type="text", text=self.text)] if self.text is not None else []
        return SimpleNamespace(stop_reason=self.stop_reason, content=content)


def fake_client(**kwargs):
    return SimpleNamespace(messages=FakeMessages(**kwargs))


def reply(category, confidence):
    return fake_client(text=json.dumps({"category": category, "confidence": confidence}))


def test_confident_result_passes_through():
    assert classify("can we do thursday instead", client=reply("reschedule", 0.92)) == {
        "category": "reschedule", "confidence": 0.92, "flagged_for_review": False,
    }


def test_low_confidence_overrides_to_other_and_flags():
    result = classify("hmm", client=reply("question", 0.41))
    assert result["category"] == "other"
    assert result["confidence"] == 0.41
    assert result["flagged_for_review"] is True
    assert result["raw_category"] == "question"


def test_threshold_is_inclusive_and_configurable():
    assert classify("x", client=reply("question", 0.6))["flagged_for_review"] is False
    assert classify("x", client=reply("question", 0.7), threshold=0.8)["category"] == "other"


def test_low_confidence_complaint_still_escalates():
    result = classify("hmm the house smells kind of weird", client=reply("complaint", 0.45))
    assert result == {"category": "complaint", "confidence": 0.45, "flagged_for_review": True}


def test_confidence_clamped():
    assert classify("x", client=reply("question", 1.7))["confidence"] == 1.0


@pytest.mark.parametrize("client, error_prefix", [
    (fake_client(text="not json"), "malformed response"),
    (fake_client(text=json.dumps({"category": "reschedule"})), "malformed response"),
    (fake_client(text=json.dumps({"category": "spam", "confidence": 0.9})), "unknown category"),
    (fake_client(text=None), "malformed response"),
    (fake_client(text="{}", stop_reason="max_tokens"), "unexpected stop_reason"),
])
def test_bad_responses_fall_back(client, error_prefix):
    result = classify("hello", client=client)
    assert result["category"] == "other"
    assert result["confidence"] == 0.0
    assert result["flagged_for_review"] is True
    assert result["error"].startswith(error_prefix)


def test_api_errors_do_not_raise():
    req = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
    for exc in [
        anthropic.APIConnectionError(request=req),
        anthropic.InternalServerError("boom", response=httpx.Response(500, request=req), body=None),
        anthropic.RateLimitError("slow", response=httpx.Response(429, request=req), body=None),
    ]:
        result = classify("hello", client=fake_client(exc=exc))
        assert result["flagged_for_review"] is True
        assert "error" in result


def test_empty_message_skips_api():
    client = reply("question", 0.9)
    assert classify("   ", client=client)["error"] == "empty message"
    assert client.messages.last_kwargs is None


def test_history_window_and_formats():
    client = reply("reschedule", 0.9)
    history = ["m1", "m2", {"role": "dk", "text": "Does Thursday at 10 work?"}]
    classify("yes that works", history, history_window=2, client=client)
    content = client.messages.last_kwargs["messages"][0]["content"]
    assert "m1" not in content
    assert "[unknown] m2" in content
    assert "[dk] Does Thursday at 10 work?" in content
    assert content.index("thread_history") < content.index("new_message")


def test_request_uses_haiku_and_strict_schema():
    client = reply("question", 0.9)
    classify("do you bring supplies", client=client)
    kw = client.messages.last_kwargs
    assert kw["model"] == "claude-haiku-4-5"
    schema = kw["output_config"]["format"]["schema"]
    assert schema["properties"]["category"]["enum"] == sms_classifier.CATEGORIES


def test_missing_credentials_does_not_raise(monkeypatch):
    for var in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"):
        monkeypatch.delenv(var, raising=False)
    no_auth = anthropic.Anthropic(api_key=None, auth_token=None, max_retries=0)
    result = classify("hello", client=no_auth)
    assert result["flagged_for_review"] is True
    assert result["error"].startswith("client error")
