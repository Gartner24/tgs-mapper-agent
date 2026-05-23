# TGS Mapper Agent

Multi-agent system that analyzes any input (text, PDF, image, URL) under the
**General Systems Theory (TGS)** framework and returns a structured JSON
analysis with a Mermaid diagram.

Built for the General Systems Theory course at Universidad Tecnologica de
Pereira (UTP) — Systems Engineering.

---

## What it does

Send any of the following to the Telegram bot:
- A text description of any system
- A URL to an article or webpage
- A PDF document
- An image

The bot replies with a full TGS analysis: system type, boundary, environment,
suprasystem, elements, subsystems, couplings, feedback, states, complexity level,
and a Mermaid diagram of the system.

Send `/publish` after an analysis to post it to Reddit.

---

## Stack

| Component | Technology |
|---|---|
| Orchestration | n8n (Docker) |
| Multi-agent brain | CrewAI + FastAPI (Python 3.12, Docker) |
| User channel | Telegram Bot API |
| LLM | OpenRouter + DeepSeek V4 |
| Reddit publishing | OpenClaw (separate VPS process) |
| Reverse proxy | Nginx + Certbot (centralized, `vps-proxy`) |
| Infrastructure | Docker Compose on Hostinger VPS |

---

## Prerequisites

- Docker Engine 24+ with Compose v2 plugin (`docker compose`)
- External Docker network `web` created on the VPS:
  ```bash
  docker network create web
  ```
- Centralized proxy stack running at `/opt/projects/proxy/` (see
  [vps-proxy](https://github.com/Gartner24/vps-proxy))
- DNS record: `n8n.qyvos.com` pointing to the VPS IP
- Accounts: OpenRouter API key, Telegram bot token, Reddit API credentials

---

## Quick start

### 1. Clone and configure

```bash
git clone https://github.com/Gartner24/tgs-mapper-agent /opt/projects/tgs-mapper-agent
cd /opt/projects/tgs-mapper-agent
cp .env.example .env
```

Edit `.env` and fill in all values:

```
OPENROUTER_API_KEY=sk-or-v1-...
LLM_MODEL=deepseek/deepseek-chat      # verify slug at openrouter.ai/models
TELEGRAM_BOT_TOKEN=...
N8N_BASIC_AUTH_USER=santiago
N8N_BASIC_AUTH_PASSWORD=<strong-password>
N8N_ENCRYPTION_KEY=<openssl rand -hex 32>
N8N_HOST=n8n.qyvos.com
WEBHOOK_URL=https://n8n.qyvos.com/
OPENCLAW_URL=http://...
OPENCLAW_API_KEY=...
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
REDDIT_USERNAME=...
REDDIT_PASSWORD=...
REDDIT_TARGET=u_<your-reddit-username>
```

### 2. Install the nginx vhost

```bash
sudo cp deploy/proxy/n8n.qyvos.com.conf \
  /opt/projects/proxy/conf.d/active/
```

Issue the TLS certificate (first deploy only):

```bash
cd /opt/projects/proxy
docker compose exec certbot certbot certonly \
  --dns-cloudflare \
  --dns-cloudflare-credentials /run/secrets/cloudflare.ini \
  -d n8n.qyvos.com
docker compose exec nginx nginx -s reload
```

### 3. Start the services

```bash
just up
```

Or without `just`:
```bash
docker compose up -d
```

Verify CrewAI is healthy:
```bash
curl http://localhost:8000/health   # requires temporary port exposure
# OR from inside the container:
docker compose exec crewai curl -s http://localhost:8000/health
```

### 4. Configure n8n

1. Open `https://n8n.qyvos.com` (use the credentials from `.env`)
2. Go to **Credentials** -> **New** -> **Telegram API**, enter your bot token,
   name it `Telegram Bot`
3. **Workflows** -> **Import from file**:
   - `n8n/workflows/01-telegram-to-crew.json`
   - `n8n/workflows/02-openclaw-publish-reddit.json`
4. Open each workflow, assign the `Telegram Bot` credential to every Telegram
   node, and toggle both workflows to **Active**

### 5. Register the Telegram webhook

```bash
curl "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  -d "url=https://n8n.qyvos.com/webhook/telegram"
```

### 6. Send a message to the bot

The bot is ready. Send any text to the Telegram bot and wait 20-60 seconds
for the analysis.

---

## Common commands (just)

```bash
just up        # start all services
just down      # stop all services
just logs      # stream logs
just rebuild   # rebuild and restart crewai only
just shell     # open shell in crewai container
just health    # check /health endpoint
just test      # run smoke test with examples/input-text.json
```

Install `just`: `cargo install just` or `apt install just`

---

## API reference

### POST /analyze

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "input_type": "text",
    "content": "Describe your system here...",
    "user_id": "optional"
  }'
```

`input_type`: `text` | `url` | `pdf` | `image`
`content`: plain text, URL string, or base64-encoded binary

**Response:**
```json
{
  "ok": true,
  "analysis": { },
  "markdown": "# Analisis TGS...",
  "mermaid": "graph TD ...",
  "metadata": {
    "duration_seconds": 18.4,
    "model_used": "openrouter/deepseek/deepseek-chat",
    "validated_by_manager": true,
    "corrections_applied": []
  }
}
```

### GET /health

```json
{ "ok": true, "version": "0.1.0" }
```

Interactive docs: `http://localhost:8000/docs`

---

## Alternative demo (no Telegram)

Open `frontend/index.html` directly in a browser. Set the API URL to
`http://localhost:8000` (or the VPS URL) and submit any text.

---

## Project structure

```
tgs-mapper-agent/
├── compose.yml                  # Docker Compose (web network, no public ports)
├── justfile                     # Task runner
├── .env.example                 # Environment variables template
├── crew/                        # CrewAI service (Python 3.12)
│   ├── main.py                  # FastAPI app (/analyze, /health)
│   ├── crew_setup.py            # Hierarchical Crew assembly
│   ├── agents/                  # 4 agent definitions
│   ├── tasks/                   # 4 task definitions
│   ├── tools/                   # PDF, image, URL tools
│   ├── schemas/                 # Pydantic v2 models (TGSAnalysis, etc.)
│   └── config/llm.py            # OpenRouter LLM config
├── n8n/workflows/               # n8n workflow JSON (import into n8n UI)
├── frontend/index.html          # Static demo frontend
├── deploy/proxy/                # Nginx vhost config for the VPS proxy
├── docs/                        # Architecture, agent design, TGS self-analysis
└── examples/                    # Sample inputs and expected output
```

---

## Documentation

| Document | Description |
|---|---|
| `docs/architecture.md` | System architecture, component diagram, request lifecycle |
| `docs/tgs-analysis-of-itself.md` | TGS analysis of the project itself (course requirement) |
| `docs/agents-design.md` | Agent roles, tools, schemas, task dependency chain |
| `docs/demo-script.md` | Presentation script for the live demo |
| `n8n/README.md` | n8n workflow import and configuration guide |
| `deploy/proxy/README.md` | Nginx vhost installation on the VPS |

---

## Done criteria

- [ ] `just up` brings up n8n + crewai with no errors
- [ ] `GET /health` returns `{ok: true}`
- [ ] `POST /analyze` with text input returns a valid `TGSAnalysis`
- [ ] Telegram workflow imports into n8n and responds to a message
- [ ] Bot returns markdown text + diagram image
- [ ] `/publish` command posts to Reddit
- [ ] `docs/tgs-analysis-of-itself.md` contains the TGS self-analysis
