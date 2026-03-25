# SKILLS.md — Logos Agent

## Agent Name
Logos — Daily learning agent that sharpens critical and logical thinking through structured research, audio content, and active recall exercises.

---

## What I Can Do

### Daily Session Generation
- Produce a full 45–60 min structured learning session on demand
- Rotate across three domains: Philosophy & Logic (35%), Economics & Markets (30%), Science & Technology (35%)
- Execute a weekly difficulty arc: Mon=Foundational, Tue–Thu=Intermediate, Fri=Advanced/counterintuitive, Sat=Synthesis, Sun=Deep-dive
- Never repeat a topic within 30 days (tracked via local history)

### Phase 1 — Audio Script
- Write spoken-word-optimized prose for the day's topic (8 min target)
- Style: natural cadence, rhetorical questions, Socratic loop, concrete examples before abstractions
- Include [PAUSE] markers at genuine decision points
- Open with provocation or paradox; close with cliffhanger into Phase 2
- Optimized for listening without a screen

### Phase 2 — Concept Map
- ASCII/Markdown visual map: central concept → sub-concepts → real-world applications → common misconceptions
- Show directionality and causality with arrows and indentation

### Phase 3 — Interactive Gauntlet
- 5 progressively harder exercises using these types (at least 3 per session):
  - `[SOCRATIC]` — escalating chain of 3 questions, model answer at end
  - `[STEELMAN]` — strongest version of a position the user likely disagrees with
  - `[FALSIFY]` — generate 2 ways to disprove a claim, then reveal known counterarguments
  - `[APPLY]` — real-world scenario, apply today's concept to diagnose or predict
  - `[LOGICAL TRAP]` — argument with hidden fallacy, user names the flaw
- Each exercise has clear instructions, a `▶ YOUR TURN:` section, and a collapsible model answer

### Phase 4 — Synthesis & SRS Seeds
- 3-sentence synthesis of the core insight
- 1 cross-domain connector (philosophy ↔ econ ↔ science)
- 3 Anki-ready Q&A flashcard pairs
- 1 rabbit hole: book, paper, or thinker for deeper exploration

### Personalization
- On first run, ask: "What's a belief you hold confidently that you've never seriously tried to disprove?"
- Store answer in `history.json` and inject into STEELMAN/FALSIFY exercises going forward

---

## What I Need to Run

### Required Inputs
- Today's date (for weekly difficulty arc and 30-day dedup)
- `history.json` (auto-created on first run) — stores onboarding answer and session log
- `SYSTEM_PROMPT.md` — the Logos system prompt, loaded at runtime

### Tools & Integrations
| Tool | Purpose | Auth Method |
|---|---|---|
| OpenRouter API | Call Claude Opus for session generation | `OPENROUTER_API_KEY` env var |
| Anthropic API (optional) | Direct Claude Opus access | `ANTHROPIC_API_KEY` env var |

### Context Files
- `agents/logos/SYSTEM_PROMPT.md` — full Logos system prompt
- `agents/logos/history.json` — session log and onboarding answer (auto-created)
- `agents/logos/sessions/` — output directory for daily session markdown files (auto-created)

---

## What I Return

- A single structured Markdown file saved to `agents/logos/sessions/YYYY-MM-DD_logos.md`
- Printed file path to stdout on completion
- Updated `history.json` with the new session's topic and date

---

## Run Command

```bash
python agents/logos/logos.py

# Debug mode — prints assembled prompt, skips API call
python agents/logos/logos.py --dry-run
```

### Env Vars (set in shell profile)
| Variable | Required When | Default |
|---|---|---|
| `LOGOS_API` | Always | `openrouter` |
| `OPENROUTER_API_KEY` | When `LOGOS_API=openrouter` | — |
| `ANTHROPIC_API_KEY` | When `LOGOS_API=anthropic` | — |

---

## Critical Thinking Targets (per session, at least 2)

| Skill | How Logos targets it |
|---|---|
| Argument mapping | Identify premises and conclusions in exercises |
| Bayesian updating | Prior belief + new evidence → estimate shift |
| Causal vs. correlational reasoning | Data presented that could be misread |
| First-principles deconstruction | "What must be true for this to be true?" |
| Inductive/deductive distinction | Label and test argument types |
| Identifying cognitive biases | Availability heuristic, anchoring, etc. embedded in content |
| Falsifiability testing | Popper lens applied to claims |
| Systems thinking | Feedback loops, second-order effects, unintended consequences |

---

## What Logos Cannot Do (Route Instead)

| Task | Route To |
|---|---|
| Client communication or scheduling | Cleaning Agent |
| Flooring contractor inquiries | Flooring Intel Agent |
| Personal finances or trading | Finance Agent |
| Family/life scheduling | Personal Agent |

---

## Status
Phase: Independent utility — not part of the core Kevin Bot revenue pipeline
Last updated: March 2026
