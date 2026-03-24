# CLAUDE.md — Kevin's Global Context

## Who I Am
- Name: Kevin. 31. Married, one young daughter.
- I co-own **DK Organizing & Cleaning** with my wife (she runs day-to-day ops).
- Day job: RW Supply and Design (flooring wholesaler) — direct daily contact with flooring contractors.
- Long-term goal: financial freedom, leave the day job, be home full-time.

## How I Work
- I have ADHD. Give me **small, concrete steps** over broad plans.
- My build window is **4:00–6:30am daily**. I'm often moving fast with limited time.
- Be **blunt and direct**. No padding, no softening, no excessive caveats.
- If something I'm doing is wrong or inefficient, say so immediately.
- Prefer **one thing at a time** — don't stack multiple tasks in one response unless I ask.
- I learn best by doing. Vibe coding with Opus is my primary mode for complex builds.

## My Stack & Infrastructure
- **Main machine:** Ubuntu Linux, basement, IP `192.168.1.239`, username `kevin`
- **This machine runs 24/7** and is the foundation for autonomous agent operation.
- **OpenRouter** is active on this machine.
- **Claude Pro** is separate from API access — API goes through the Anthropic Console.
- **Knowledge vault:** Obsidian (local markdown files)
- **Automation stack:** Twilio + Make.com + Claude API + Google Sheets + Calendly (~$95/month)

## Kevin Bot — The Main Project
This is my primary build. An AI agent system that automates client communication and business ops.

**Agent architecture (4 specialists):**
1. Cleaning Agent — Phase 1, proof of concept on DK Cleaning (sellable product)
2. Flooring Intel Agent — Phase 2, sell to flooring contractors
3. Finance Agent — personal only
4. Personal Agent — life/family

**Model routing:**
- Haiku → RAG, classification, cheap/fast tasks
- Sonnet → customer-facing content, standard agent responses
- Opus → hard reasoning, architecture decisions, complex builds
- Almost never use Opus in production

**System prompt rule:** ~250 tokens max. Scripts and brand voice fetched on demand from Google Drive/Notion, not baked in.

**10-file markdown architecture (stored in Obsidian):**
`Agents.md`, `Soul.md`, `Me.md`, `Bootstrap.md`, `Tools.md`, `Scratchpad.md`, `Knowledge.md`, `Errors.md`, `Goals.md`, `Changelog.md`

## DK Cleaning Business Context
- ~40 recurring + ~20 one-off customers
- My wife handles training and quality; **appointment volume is the bottleneck**, not labor
- Real SMS conversation datasets from DK and two other cleaning companies — competitive advantage
- Cleaning Agent handles: inbound SMS classification, auto-replies, complaint escalation (WhatsApp to wife), reschedule via Calendly, post-job review requests (2hrs post), referral asks (triggered by 5-star reviews), 45-day win-back sequences, review-to-SEO pipeline

## Business Goals & Phases
- **Phase 1:** Cleaning Agent live on DK → proof of concept
- **Phase 2:** Clone and sell to flooring contractors → target $1K/month per client, 5 clients = financial freedom pace
- **Phase 3+:** Flooring Intel Agent, contractor matching service (KC area)
- **Phase 4+:** Personal trading/copy-trading agent — do NOT prioritize before core revenue

## What Not to Touch Without Asking
- Any live Twilio SMS flows
- Production Google Sheets that clients or my wife interact with
- Make.com scenarios that are active
- Wassenger/WhatsApp routing to my wife

## Key Decisions Already Made (Don't Relitigate)
- Flask over FastAPI for the bot control panel — keep it
- Twilio MCP requires API Key + API Secret pair, NOT Auth Token
- Wassenger runs as a remote HTTP MCP server (`claude mcp add --transport http`)
- Google Sheets is the database — not moving to a real DB for now
- Brazilian Portuguese required for spouse-facing and some client-facing materials

## Communication
- I speak English and Brazilian Portuguese
- When drafting client or partner materials, ask me which language unless context is obvious
