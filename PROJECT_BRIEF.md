# TGS Mapper Agent — Project Brief

> This document contains ALL the design decisions already made for the project.
> Read this file COMPLETELY before writing any code.
> If something is not defined here, ask before inventing.

---

## 1. Context

**Author:** Santiago Valencia León — Systems Engineering student, UTP (with a group of 5 other teammates).
**Course:** General Systems Theory (GST / TGS in Spanish).
**Delivery:** TODAY. Live demo + GitHub repo + architecture document.

## 2. What the agent does

Receives an arbitrary input (text, PDF, image, URL) via **Telegram bot** or via **HTTP API** and returns a **structured analysis under the lens of General Systems Theory (TGS)**: system, purpose, boundary, environment, suprasystem, elements, subsystems, relationships, couplings (strong/weak/sequential/reciprocal), inputs-processes-outputs, feedback, states and transitions, system type, and complexity. Includes a Mermaid diagram of the analyzed system.

**Example use case:** if a TGS exam PDF is passed in, the agent identifies each topic of the exam as a subsystem of the system "exam knowledge" and relates them.

**Extra command:** if after the analysis the user sends `/publish`, the system publishes the analysis to Reddit (own profile `r/u_<username>`) via OpenClaw.

**IMPORTANT — Language rule:**
- All code, comments, variable names, function names, technical documentation: **English**.
- All strings shown to the end user (Telegram messages, error messages, Reddit posts): **Spanish (Colombia)**.
- All LLM outputs (analysis content): **Spanish (Colombia)**.

## 3. Tech stack (CLOSED, do not change)

| Component | Technology | Role |
|---|---|---|
| External orchestration | **n8n** (self-hosted, Docker) | Receives Telegram, routes, calls CrewAI, responds |
| Multi-agent brain | **CrewAI** (Python, FastAPI) | 4 agents with roles, sequential process |
| User channel | **Telegram Bot API** | Main I/O |
| Distribution | **OpenClaw → Reddit** (already running on VPS) | Publishes the analysis to `r/u_<username>` when the user sends `/publish`. Reddit only in MVP. |
| LLM | **OpenRouter + DeepSeek V4** (open source via API) | Brain of the agents |
| Demo frontend (alternative) | Static HTML + Tailwind + Mermaid.js | For demos without Telegram |
| Infrastructure | Docker Compose on Hostinger VPS + Nginx + Let's Encrypt | Everything starts with `docker compose up -d` |

## 4. The 4 agents (CrewAI)

Process: **`Process.sequential`** — the 4 tasks run in order (extraction -> analysis -> diagram -> coordination); the Manager runs the final coordination task. (Originally hierarchical; switched to sequential for latency, commit 40ed33d.)

All agent prompts (role, goal, backstory) must be written in **Spanish**, because the LLM must respond in Spanish to the end user. Code identifiers stay in English.

### Agent 1 — Content Extractor (`extractor.py`)
- **role:** "Extractor y comprensor de contenido"
- **goal:** "Leer cualquier input (texto, PDF transcrito, descripción de imagen, contenido web) e identificar: el tema central, los conceptos clave mencionados, las relaciones implícitas entre conceptos, y el dominio al que pertenece (académico, empresarial, técnico, etc)."
- **backstory:** "Eres un investigador con doctorado en análisis de texto. Tu única misión es destilar el input: no interpretas, no analizas bajo ningún marco teórico, solo extraes el qué del contenido. Eres el sensor del sistema."
- **Output schema (Pydantic):** `tema_central: str, conceptos: list[str], relaciones_implicitas: list[dict], dominio: str, resumen_objetivo: str`

### Agent 2 — TGS Analyst (`analista_tgs.py`)
- **role:** "Analista experto en Teoría General de Sistemas"
- **goal:** "Aplicar el marco completo de TGS al contenido extraído. Identificar: sistema, propósito, frontera, entorno, suprasistema, elementos, subsistemas, relaciones, acoplamientos (fuerte/débil/secuencial/recíproco), entradas-procesos-salidas, retroalimentación, estados y transiciones, tipo de sistema (abierto/cerrado, deterministico/estocástico, continuo/discreto) y nivel de complejidad."
- **backstory:** "Eres profesor titular de TGS con 20 años aplicando los conceptos de Bertalanffy a cualquier dominio: biología, software, negocios, sociedad. No confundes elemento con subsistema, ni frontera con entorno, y siempre justificas cada clasificación."
- **Output schema (Pydantic):** see `schemas/tgs_output.py` — must match `TGSAnalysis` EXACTLY (section 7).

### Agent 3 — Diagrammer (`diagramador.py`)
- **role:** "Diagramador de sistemas complejos"
- **goal:** "Convertir el análisis TGS en un diagrama Mermaid claro y legible. Subsistemas como nodos, relaciones como aristas, tipo de acoplamiento como estilo de línea, frontera como subgraph. Máximo 12 nodos para legibilidad."
- **backstory:** "Eres diseñador de información especializado en visualización de sistemas complejos. Conoces Mermaid al dedillo. Tu mayor habilidad es decidir qué dejar afuera para que el diagrama comunique sin saturar."
- **Output schema (Pydantic):** `mermaid_code: str, leyenda: str`

### Agent 4 — Coordinator Manager (`manager.py`)
- **role:** "Director del análisis TGS"
- **goal:** "Validar la coherencia entre el contenido extraído, el análisis TGS y el diagrama generado. Detectar inconsistencias (ej: el diagrama menciona un subsistema que no está en el análisis) y corregirlas directamente en el JSON final integrado de tipo TGSAnalysis."
- **backstory:** "Eres editor en jefe y arquitecto de sistemas. Tu superpoder es ver el bosque mientras los demás ven el árbol. Nunca entregas un producto a medias: si detectas un problema, mandas a corregirlo antes de cerrar."
- **Special:** the Manager runs the **final coordination task** of the sequential Crew, after the Extractor, Analyst and Diagrammer. It validates the three prior outputs (passed as task context) and assembles the final `TGSAnalysis` directly, without re-delegating.

## 5. TGS analysis of the project itself (include in docs/)

Each agent is a subsystem of the "TGS Mapper Agent" system:

| Agent | TGS Role | Justification |
|---|---|---|
| Extractor | Sensor / input subsystem | Converts external reality into processable internal data |
| TGS Analyst | Processor / core subsystem | Applies the rules of the TGS framework; where emergent behavior occurs |
| Diagrammer | Output / transduction subsystem | Converts internal information into a visual representation |
| Manager | Control / feedback subsystem | Compares the assembled output with purpose, adjusts by correcting inconsistencies directly (negative feedback) |

Couplings:
- Manager ↔ Extractor: **strong** (Manager depends directly on Extractor output)
- Manager ↔ Analyst: **strong** (core of the product)
- Manager ↔ Diagrammer: **weak** (if the diagram fails, the textual analysis is still useful)
- Extractor → Analyst: **sequential**
- Analyst → Diagrammer: **sequential**
- Manager ↔ all: **reciprocal** (can return and request corrections)

## 6. Folder structure

```
tgs-mapper-agent/
├── README.md
├── CLAUDE.md                          # persistent memory for Claude Code
├── PROJECT_BRIEF.md                   # this file
├── DEPENDENCIES.md                    # project dependencies
├── docker-compose.yml
├── .env.example
├── .gitignore
├── Makefile                           # make up, make logs, make test, make down
│
├── n8n/
│   ├── workflows/
│   │   ├── 01-telegram-to-crew.json
│   │   └── 02-openclaw-publish-reddit.json
│   └── README.md
│
├── crew/
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── main.py                        # FastAPI app
│   ├── crew_setup.py                  # Defines the Crew
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── extractor.py
│   │   ├── analista_tgs.py
│   │   ├── diagramador.py
│   │   └── manager.py
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── extraction.py
│   │   ├── analysis.py
│   │   ├── diagram.py
│   │   └── coordination.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── pdf_reader.py
│   │   ├── image_reader.py
│   │   └── url_fetcher.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── input.py                   # AnalyzeRequest
│   │   └── tgs_output.py              # TGSAnalysis (Pydantic)
│   └── config/
│       ├── __init__.py
│       └── llm.py                     # OpenRouter config
│
├── frontend/
│   └── index.html
│
├── docs/
│   ├── architecture.md
│   ├── tgs-analysis-of-itself.md
│   ├── agents-design.md
│   └── demo-script.md
│
└── examples/
    ├── input-text.json
    ├── input-pdf.json
    └── output-sample.json
```

## 7. Final output JSON schema (Pydantic in schemas/tgs_output.py)

Field names stay in Spanish because the LLM output uses Spanish terminology that matches the course materials. Class names are in English (`TGSAnalysis`, `Subsystem`, etc) — Python style.

```python
from pydantic import BaseModel
from typing import Literal

class TipoSistema(BaseModel):
    abierto_o_cerrado: Literal["abierto", "cerrado", "mixto"]
    natural_o_artificial: Literal["natural", "artificial", "sociotecnico"]
    deterministico_o_estocastico: Literal["deterministico", "estocastico", "mixto"]
    continuo_o_discreto: Literal["continuo", "discreto", "hibrido"]
    justificacion: str

class Frontera(BaseModel):
    descripcion: str
    elementos_dentro: list[str]
    elementos_fuera: list[str]

class Entorno(BaseModel):
    descripcion: str
    variables_externas: list[str]

class Elemento(BaseModel):
    nombre: str
    rol: str

class Subsistema(BaseModel):
    nombre: str
    proposito: str
    elementos_clave: list[str]

class Relacion(BaseModel):
    origen: str
    destino: str
    tipo_acoplamiento: Literal["fuerte", "debil", "secuencial", "reciproco"]
    descripcion: str

class CajaNegra(BaseModel):
    entradas: list[str]
    procesos: list[str]
    salidas: list[str]

class Retroalimentacion(BaseModel):
    tipo: Literal["positiva", "negativa"]
    descripcion: str

class Transicion(BaseModel):
    hacia: str
    disparador: str

class EstadoTransicion(BaseModel):
    estado: str
    transiciones: list[Transicion]

class Complejidad(BaseModel):
    nivel: Literal["simple", "complicado", "complejo", "caotico"]
    justificacion: str

class TGSAnalysis(BaseModel):
    tema: str
    resumen: str
    proposito: str
    tipo_de_sistema: TipoSistema
    frontera: Frontera
    entorno: Entorno
    suprasistema: str
    elementos: list[Elemento]
    subsistemas: list[Subsistema]
    relaciones: list[Relacion]
    caja_negra: CajaNegra
    retroalimentacion: list[Retroalimentacion]
    estados_y_transiciones: list[EstadoTransicion]
    complejidad: Complejidad
    diagrama_mermaid: str
    supuestos: list[str]
    preguntas_para_profundizar: list[str]
```

## 8. API contract of the CrewAI service

### POST /analyze

**Request:**
```json
{
  "input_type": "text" | "url" | "pdf" | "image",
  "content": "plain text | URL | base64",
  "user_id": "optional_telegram_chat_id"
}
```

**Response (200):**
```json
{
  "ok": true,
  "analysis": { /* full TGSAnalysis */ },
  "markdown": "# ... human-readable rendering",
  "mermaid": "graph TD ...",
  "metadata": {
    "duration_seconds": 12.4,
    "model_used": "deepseek/deepseek-chat-v4",
    "validated_by_manager": true,
    "corrections_applied": []
  }
}
```

**Response (error):**
```json
{ "ok": false, "error": "message", "stage": "extractor|analista|diagramador|manager" }
```

### GET /health
```json
{ "ok": true, "version": "0.1.0" }
```

## 9. LLM configuration (config/llm.py)

```python
from crewai import LLM
import os

def get_llm() -> LLM:
    return LLM(
        model="openrouter/deepseek/deepseek-chat-v4",  # adjust to exact OpenRouter slug
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        temperature=0.3,  # structured, not creative
        max_tokens=8000,
    )
```

## 10. Environment variables (.env.example)

```
# --- LLM ---
OPENROUTER_API_KEY=sk-or-v1-...
LLM_MODEL=deepseek/deepseek-chat-v4

# --- Telegram ---
TELEGRAM_BOT_TOKEN=8000000000:AAAA...
TELEGRAM_WEBHOOK_URL=https://n8n.qyvos.com/webhook/telegram

# --- n8n ---
N8N_BASIC_AUTH_USER=santiago
N8N_BASIC_AUTH_PASSWORD=change_me
N8N_ENCRYPTION_KEY=generate_with_openssl_rand_hex_32
N8N_HOST=n8n.qyvos.com
WEBHOOK_URL=https://n8n.qyvos.com/

# --- CrewAI service ---
CREW_API_PORT=8000
CREW_API_URL=http://crewai:8000

# --- OpenClaw + Reddit ---
OPENCLAW_URL=http://localhost:<openclaw_port>
OPENCLAW_API_KEY=
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USERNAME=
REDDIT_PASSWORD=
REDDIT_TARGET=u_<reddit_username>   # own profile, no karma restrictions
```

## 11. docker-compose.yml — services

```yaml
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    ports: ["5678:5678"]
    env_file: .env
    volumes: [n8n_data:/home/node/.n8n]
    depends_on: [crewai]
    restart: unless-stopped

  crewai:
    build: ./crew
    ports: ["8000:8000"]
    env_file: .env
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
    restart: unless-stopped

  # OpenClaw runs separately on the VPS, n8n calls it via HTTP.

volumes:
  n8n_data:
```

## 12. n8n workflows

### Workflow 1: `01-telegram-to-crew`
1. **Telegram Trigger** — listens to new messages from the bot
2. **Switch by type** — text / document (PDF) / photo / URL (detected via regex)
3. **Content extraction** based on type (download file from Telegram if applies, convert to base64 if binary)
4. **HTTP Request** → POST `http://crewai:8000/analyze`
5. **Format response** — markdown + render Mermaid to image (via kroki.io or mermaid.ink)
6. **Telegram: Send Message** (markdown) + **Telegram: Send Photo** (with diagram image)
7. **Stores the analysis** in n8n memory keyed by `chat_id` so `/publish` can retrieve it later

### Workflow 2: `02-openclaw-publish-reddit`
1. **Telegram Trigger** filtered by `/publish` command
2. **Retrieves the user's latest analysis** (n8n memory keyed by `chat_id`)
3. **Formats for Reddit:** catchy title (≤300 chars) + markdown body (summary + purpose + key subsystems) + link to rendered diagram
4. **HTTP Request** → OpenClaw API → publishes to `r/u_<REDDIT_USERNAME>` (own profile, no karma restrictions)
5. **Confirms to the user** in Telegram with the Reddit post link

**Reddit only in MVP.** Other social networks are out of scope due to cost/friction.

## 13. Golden rules for the code

1. **Language:** all code in English (variables, functions, technical comments). End-user strings in **Spanish**. LLM prompts in **Spanish**.
2. **Type hints mandatory** in all Python.
3. **Pydantic v2** for schemas. Use `BaseModel`, `Field`, `Literal`.
4. **FastAPI** with tags and descriptions on each endpoint (for auto docs at `/docs`).
5. **Logging** with `loguru`, NEVER `print()`.
6. **Explicit errors:** each agent can fail; catch and return `{ok: false, stage: "..."}`.
7. **No hardcoding:** everything configurable goes to `.env`.
8. **CrewAI 0.80+** (modern version with typed tools and `output_pydantic`).
9. **Async where it makes sense** in FastAPI (`async def` endpoints).
10. **Minimum tests:** one smoke test per agent, one e2e test with sample input.
11. **No emojis in code** (only in end-user strings if they fit).

## 14. Implementation plan (strict order)

1. Create folder structure + empty files
2. `pyproject.toml` + `requirements.txt` + crew `Dockerfile`
3. `schemas/` — Pydantic models
4. `config/llm.py` — OpenRouter config
5. `tools/` — pdf_reader, image_reader, url_fetcher
6. `agents/` — the 4 agents
7. `tasks/` — the 4 tasks
8. `crew_setup.py` — assemble the sequential Crew
9. `main.py` — FastAPI with `/analyze` and `/health`
10. `docker-compose.yml` + `.env.example` + `Makefile`
11. Local test with `examples/input-text.json`
12. n8n workflows (export JSON)
13. HTML frontend (alternative demo)
14. Documentation in `docs/`
15. Final README

## 15. What NOT to do

- ❌ Do NOT use OpenAI or Anthropic API as the agent LLM. Only open source via OpenRouter (DeepSeek V4).
- ❌ Do NOT invent additional agents beyond the 4 defined.
- ❌ Do NOT add a database. Ephemeral per-request memory is enough (n8n handles minimal persistence of the last analysis).
- ❌ Do NOT add complex authentication on the CrewAI API. It is an internal service, only exposed to n8n.
- ❌ Do NOT use `print()`.
- ❌ Do NOT generate Mermaid diagrams with more than 12 nodes.
- ❌ Do NOT return markdown inside the `mermaid` field (it must be pure Mermaid code).
- ❌ Do NOT publish to social networks other than Reddit.
- ❌ No emojis in code.

## 16. "Done" criteria

- [ ] `docker compose up -d` brings up n8n + crewai with no errors
- [ ] `curl http://localhost:8000/health` returns `{ok: true}`
- [ ] `curl POST /analyze` with a text input returns a valid `TGSAnalysis`
- [ ] The Telegram workflow imports into n8n and responds to a message
- [ ] The bot returns markdown + diagram image
- [ ] The `/publish` command posts to Reddit (`r/u_<username>`)
- [ ] The README explains how to run everything from scratch
- [ ] There is a TGS analysis of the project itself in `docs/tgs-analysis-of-itself.md`

---

> If something is not clear, ASK before inventing. If something in the plan no longer applies for a good reason, EXPLAIN before changing it.
