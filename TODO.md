# TODO — Kevin Bot & DK Cleaning
_Last updated: 2026-03-24_

---

## PHASE 1 — Cleaning Agent Live (DO THIS FIRST)
> Goal: Automate DK client communication. Prove the system works. This is the product you'll sell.

### 1. Finish the Cleaning Agent core
- [ ] Create `agents/cleaning/CLAUDE.md` — DK brand voice, tone rules, approved scripts
- [ ] Build inbound SMS classifier (Haiku) — intents: new inquiry / reschedule / complaint / compliment / other
- [ ] Write auto-reply scripts for each intent (English + Brazilian Portuguese versions)
- [ ] Implement complaint escalation → Wassenger → wife's WhatsApp
- [ ] Build post-job follow-up trigger (2hrs after job completion → review request SMS)
- [ ] Build referral ask trigger (fires on 5-star review or explicit compliment)

### 2. Wire up the infrastructure
- [ ] Set up Twilio webhook → Make.com → Cleaning Agent pipeline
- [ ] Create Google Sheets client database (name, phone, job history, sequence status)
- [ ] Configure Make.com scenario: inbound SMS → classify → route → reply
- [ ] Configure Make.com trigger: job completion flag → post-job SMS
- [ ] Add Wassenger HTTP MCP server (`claude mcp add --transport http`)
- [ ] Store brand voice and approved scripts in Google Drive or Notion (not hardcoded)

### 3. Win-back sequence
- [ ] Build 45-day 3-touch SMS sequence for inactive recurring clients
- [ ] Track sequence status per client in Google Sheets
- [ ] Add stop logic: cancel sequence if client books or opts out

### 4. Review-to-SEO pipeline
- [ ] Detect 5-star review signal (GBP notification or manual flag)
- [ ] Extract key phrases via Claude (Haiku)
- [ ] Format as Google Business Profile post draft
- [ ] Route draft to Kevin for approval before posting
- [ ] Log review source + status in Sheets

### 5. Testing & Go-Live
- [ ] Run Cleaning Agent against real SMS dataset (DK + 2 other companies)
- [ ] Validate all auto-replies with wife before going live
- [ ] Flip one Twilio number to live routing
- [ ] Monitor for 2 weeks, log errors to `shared/errors.md`

---

## PHASE 2 — Productize & Sell to Cleaning Companies
> Goal: Clone the Cleaning Agent and sell it. Each client = recurring revenue toward financial freedom.

- [ ] Document the "Kevin Bot for Cleaning Businesses" offer (1-pager)
- [ ] Identify 3-5 cleaning business owners in KC area as first targets
- [ ] Build white-label version: swap out DK brand voice for client's voice
- [ ] Create onboarding checklist: what info you need from a new cleaning client
- [ ] Set pricing: suggest $300-500/month SaaS, or $1K setup + $200/month
- [ ] Pitch wife's friends who own cleaning businesses first — warm leads, easy trust

---

## PHASE 3 — Flooring Intel Agent (Path to $5K/Month)
> Goal: Sell to flooring contractors via your RW Supply relationships. 5 clients = financial freedom pace.

- [ ] Create `agents/flooring/CLAUDE.md` — contractor context, pain points, use cases
- [ ] Define Flooring Intel Agent skill set (pricing intel, lead tracking, product Q&A)
- [ ] List 10 contractors from RW Supply who are already warm relationships
- [ ] Build simple demo: contractor texts a product question → agent replies with pricing/availability
- [ ] Target price: $1K/month per contractor client
- [ ] Build sales deck or voice memo pitch for contractor calls

---

## INFRASTRUCTURE — Gaps to Close
- [ ] Populate `infrastructure/` directory with per-tool setup docs (Twilio, Make.com, Wassenger, Sheets)
- [ ] Add `agents/cleaning/CLAUDE.md` (referenced in SKILLS.md but missing)
- [ ] Add `agents/flooring/CLAUDE.md`, `agents/finance/CLAUDE.md`, `agents/personal/CLAUDE.md` stubs
- [ ] Flesh out `shared/tools.md` — currently empty, needs auth reference for all tools
- [ ] Set up error logging flow: automation failures → `shared/errors.md` automatically
- [ ] Confirm Twilio MCP uses API Key + API Secret (NOT Auth Token) — document in infrastructure/

---

## QUICK WINS (Do These Any Morning)
- [ ] Write `agents/cleaning/CLAUDE.md` brand voice doc — ask wife for 3 example SMS replies she's proud of
- [ ] Export real DK SMS history from Twilio for classifier training/testing
- [ ] Map out the Google Sheet columns you need before building any Make.com scenarios
- [ ] Send one test complaint through Wassenger to confirm wife receives it on WhatsApp

---

## ON HOLD — Don't Touch Yet
- Finance Agent — personal only, build after Phase 2 revenue is flowing
- Personal Agent — build after financial freedom is in sight
- Copy-trading / personal trading agent — explicitly deferred
- Any modifications to live Twilio flows or active Make.com scenarios
