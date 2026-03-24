# Kevin Bot

An AI agent system that automates client communication and business operations for DK Organizing & Cleaning and beyond.

## Architecture

One **Operator** routes all incoming tasks to four specialized agents:

| Agent | Domain | Status |
|---|---|---|
| Cleaning Agent | DK client SMS automation | Phase 1 — Active Build |
| Flooring Intel Agent | Contractor leads & pricing intel | Phase 2 — Not started |
| Finance Agent | Personal & business finance | Phase 3 — Not started |
| Personal Agent | Life, family, scheduling | Phase 4 — Not started |

## Stack

- **Automation:** Twilio + Make.com + Claude API
- **Database:** Google Sheets
- **Scheduling:** Calendly
- **Messaging:** Wassenger (WhatsApp via HTTP MCP)
- **Models:** Haiku (classification), Sonnet (customer-facing), Opus (architecture)

## Repo Structure

```
├── CLAUDE.md              # Global context for AI assistants
├── learned_routes.md      # Operator routing decisions log
├── operator/
│   ├── CLAUDE.md          # Operator agent context & rules
│   └── SKILLS.md          # Operator capabilities
├── agents/
│   ├── cleaning/SKILLS.md
│   ├── finance/SKILLS.md
│   ├── flooring/SKILLS.md
│   └── personal/SKILLS.md
├── shared/
│   ├── errors.md          # Known errors log
│   ├── schemas.md         # Data shapes
│   └── tools.md           # Tool registry
└── infrastructure/        # Per-tool setup details
```

## Getting Started

See `CLAUDE.md` for full context, stack decisions, and what not to touch without asking.
