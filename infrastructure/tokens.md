# infrastructure/tokens.md — API Token Setup

All tokens are stored as environment variables on the Ubuntu machine at `192.168.1.239`.
**Never hardcode tokens in code.** Never commit `.env` to git.

---

## Required Tokens

### GITHUB_TOKEN
- **Used by:** `dashboard/app.py` (read repo, browse files, list commits/issues)
- **Type:** GitHub Personal Access Token (classic)
- **Scopes needed:** `repo` (read access is sufficient for dashboard; write needed for file edits)
- **Where to create:** GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
- **Set via:** `export GITHUB_TOKEN=ghp_xxx` or in `.env`

### ANTHROPIC_API_KEY
- **Used by:** All Claude API calls (Haiku, Sonnet, Opus routing)
- **Where to create:** console.anthropic.com → API Keys
- **Set via:** `export ANTHROPIC_API_KEY=sk-ant-xxx`

### TWILIO_ACCOUNT_SID / TWILIO_AUTH_TOKEN
- **Used by:** Cleaning Agent SMS inbound/outbound
- **Note:** Twilio MCP requires API Key + API Secret, NOT Auth Token. See Twilio Console → API Keys.
- **Where to create:** console.twilio.com → Account → API Keys & Tokens
- **Set via:**
  ```
  export TWILIO_ACCOUNT_SID=ACxxx
  export TWILIO_API_KEY=SKxxx
  export TWILIO_API_SECRET=xxx
  ```

### WASSENGER_API_KEY
- **Used by:** WhatsApp escalation to wife (Cleaning Agent)
- **Type:** Wassenger API key (HTTP MCP server)
- **Where to create:** app.wassenger.com → Settings → API
- **Set via:** `export WASSENGER_API_KEY=xxx`

### OPENROUTER_API_KEY
- **Used by:** Model routing via OpenRouter (already active on this machine)
- **Where to create:** openrouter.ai → Keys
- **Set via:** `export OPENROUTER_API_KEY=sk-or-xxx`

### GOOGLE_SHEETS_CREDENTIALS
- **Used by:** All agents that read/write to Google Sheets (the DB)
- **Type:** Service account JSON key file
- **Where to create:** Google Cloud Console → IAM → Service Accounts → Create Key (JSON)
- **Set via:** `export GOOGLE_SHEETS_CREDENTIALS=/path/to/service-account.json`
- **Note:** Share the target Sheet with the service account email.

---

## Loading Tokens at Runtime

Copy `.env.example` to `.env` and fill in values:

```bash
cp .env.example .env
# edit .env with real values
```

Source before running any agent or the dashboard:

```bash
set -a && source .env && set +a
```

Or use the dashboard's start script:

```bash
GITHUB_TOKEN=ghp_xxx ./dashboard/start.sh
```

---

## Rotation Policy
- Rotate `GITHUB_TOKEN` every 90 days or immediately if exposed.
- Rotate `ANTHROPIC_API_KEY` immediately if committed to git or logged.
- Twilio API Keys can be revoked per-key without affecting the account SID.
