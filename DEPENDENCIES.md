# Dependencies — TGS Mapper Agent

## crew/requirements.txt

```
# --- Core ---
crewai>=0.80.0
crewai-tools>=0.20.0

# --- Web framework ---
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
pydantic>=2.9.0
python-multipart>=0.0.12

# --- LLM via OpenRouter (OpenAI-compatible) ---
litellm>=1.50.0
openai>=1.50.0

# --- Document/media processing ---
pypdf>=5.0.0
pdfplumber>=0.11.0
pillow>=11.0.0
beautifulsoup4>=4.12.0
httpx>=0.27.0
requests>=2.32.0

# --- Utils ---
python-dotenv>=1.0.0
loguru>=0.7.0
tenacity>=9.0.0  # retries for LLM calls
```

## crew/Dockerfile (skeleton)

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# System deps for pdf/image processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    libgl1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Services in docker-compose.yml

| Service | Image | Local port | Function |
|---|---|---|---|
| n8n | docker.n8n.io/n8nio/n8n:latest | 5678 | Orchestration |
| crewai | build ./crew | 8000 | Multi-agent service |

OpenClaw runs separately (already on the VPS), n8n calls it via HTTP.

## External services used

- **OpenRouter** — `https://openrouter.ai/api/v1` (API key required, free signup with $5 credit)
- **Telegram Bot API** — `https://api.telegram.org` (token from @BotFather)
- **Reddit API** — via OpenClaw, "script" app credentials
- **Mermaid render** — `https://kroki.io` or `https://mermaid.ink` (render diagrams to PNG without local install)
- **Hostinger VPS** — where everything runs
- **Cloudflare / Hostinger DNS** — for subdomains `n8n.qyvos.com` and `api.qyvos.com`

## Accounts created by the team (data to receive before coding)

```
OpenRouter API Key:    sk-or-v1-...
Telegram bot username: @...
Telegram bot token:    ...
Reddit username:       ...
Reddit password:       ...
Reddit client_id:      ...
Reddit client_secret:  ...
```

## n8n — community nodes

No community packages needed for the MVP. Everything works with built-in nodes:
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.code`

## Recommended versions

- **Python:** 3.12
- **Node (for n8n):** whatever ships with the official image (not managed manually)
- **Docker Engine:** 24+
- **Docker Compose:** v2 plugin (`docker compose`, not `docker-compose`)
