# SMS Intent Classifier

Classifies an inbound DK SMS as `reschedule` / `complaint` / `new_booking` / `question` / `other` using Claude Haiku (`claude-haiku-4-5`).

## Run it (basement box)
```bash
pip install -r agents/cleaning/requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...          # from Anthropic Console
python agents/cleaning/classify_sms.py --message "can we do thursday instead"
python -m pytest agents/cleaning/tests       # free, no API calls
python agents/cleaning/eval/run_eval.py      # live, ~30 Haiku calls, < $0.05
```

## Output
```json
{"category": "reschedule", "confidence": 0.92, "flagged_for_review": false}
```
- Confidence below `CONFIDENCE_THRESHOLD` (0.6) → `category: "other"`, `flagged_for_review: true`, plus `raw_category` (what the model actually said).
- API failure, missing key, or bad response → `other` / `0.0` / flagged, plus `error`. Never raises.

## Decisions on PRD open questions
| Question | Decision |
|---|---|
| Enum casing | lowercase snake_case: `new_booking` |
| Threshold | 0.6 (`CONFIDENCE_THRESHOLD`), tune with `run_eval.py --threshold` |
| History window | 5 (`HISTORY_WINDOW`), tune with `run_eval.py --window` |
| History format | list of strings or `{role, text}` dicts, oldest first. Roles: `client` / `dk` |
| Retry policy | SDK retries 429/5xx/connection once, then falls back to flagged `other` |
| Tests | Unit tests use a fake client (free, CI-safe). Live accuracy lives in `eval/run_eval.py` |
| Accuracy target | Not set. Decide once the real DK export is in the eval CSV |
| Mixed complaint + other intent | Prompt says complaint wins, so escalation never gets missed |

## Eval data
`eval/labeled_sms.csv` is **synthetic** (30 rows written for the PRD's case types). Replace or extend it with the real DK export. Same columns, and `expected` can be `a|b` when two answers are acceptable.

## Known limitation
`confidence` is the model's self-reported confidence. It is not calibrated probability. Treat the threshold as a knob to tune against real data, not a guarantee.
