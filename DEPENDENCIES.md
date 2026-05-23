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
tenacity>=9.0.0  # retries para llamadas al LLM
```

## crew/Dockerfile (esqueleto)

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

## Servicios en docker-compose.yml

| Servicio | Imagen | Puerto local | Función |
|---|---|---|---|
| n8n | docker.n8n.io/n8nio/n8n:latest | 5678 | Orquestación |
| crewai | build ./crew | 8000 | Servicio multi-agente |

OpenClaw corre aparte (ya está en el VPS), n8n lo llama por HTTP.

## Servicios externos usados

- **OpenRouter** — `https://openrouter.ai/api/v1` (API key necesaria, registro gratis con $5 de crédito)
- **Telegram Bot API** — `https://api.telegram.org` (token de @BotFather)
- **Reddit API** — vía OpenClaw, credenciales tipo "script app"
- **Mermaid render** — `https://kroki.io` o `https://mermaid.ink` (renderizar diagramas a PNG sin instalación local)
- **Hostinger VPS** — donde corre todo
- **Cloudflare / Hostinger DNS** — para subdominios `n8n.gartnercodes.com` y `api.gartnercodes.com`

## Cuentas que crea el grupo (datos a recibir antes de programar)

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

No se necesitan community packages para el MVP. Todo se hace con nodos built-in:
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.code`

## Versiones recomendadas

- **Python:** 3.12
- **Node (para n8n):** lo que trae la imagen oficial (no se maneja manualmente)
- **Docker Engine:** 24+
- **Docker Compose:** plugin v2 (`docker compose`, no `docker-compose`)
