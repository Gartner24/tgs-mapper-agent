# TGS Mapper Agent — Project Brief

> Este documento contiene TODAS las decisiones de diseño ya tomadas para el proyecto.
> Lee este archivo COMPLETO antes de escribir cualquier código.
> Si algo no está definido aquí, pregunta antes de inventar.

---

## 1. Contexto

**Autor:** Santiago Valencia León — Estudiante de Ingeniería de Sistemas, UTP (con grupo de 5 compañeros más).
**Curso:** Teoría General de Sistemas (TGS).
**Entrega:** HOY. Demo en vivo + repo en GitHub + documento de arquitectura.

## 2. Qué hace el agente

Recibe un input arbitrario (texto, PDF, imagen, URL) vía **Telegram bot** o vía **API HTTP** y devuelve un **análisis estructurado bajo la lente de la Teoría General de Sistemas**: sistema, propósito, frontera, entorno, suprasistema, elementos, subsistemas, relaciones, acoplamientos (fuerte/débil/secuencial/recíproco), entradas-procesos-salidas, retroalimentación, estados y transiciones, tipo de sistema y complejidad. Incluye un diagrama Mermaid del sistema analizado.

**Caso de uso ejemplo:** si se le pasa un PDF de un parcial de TGS, el agente identifica cada tema del parcial como un subsistema del sistema "conocimiento del parcial" y los relaciona.

**Comando extra:** si después del análisis el usuario manda `/publish`, el sistema publica el análisis en Reddit (perfil propio `r/u_<username>`) vía OpenClaw.

## 3. Stack tecnológico (CERRADO, no cambiar)

| Componente | Tecnología | Rol |
|---|---|---|
| Orquestación externa | **n8n** (self-hosted, Docker) | Recibe Telegram, route, llama CrewAI, responde |
| Cerebro multi-agente | **CrewAI** (Python, FastAPI) | 4 agentes con roles, proceso jerárquico |
| Canal de usuario | **Telegram Bot API** | Entrada/salida principal |
| Distribución | **OpenClaw → Reddit** (ya corre en el VPS) | Publica el análisis en `r/u_<username>` cuando el usuario manda `/publish`. Solo Reddit en el MVP. |
| LLM | **OpenRouter + DeepSeek V4** (open source vía API) | Cerebro de los agentes |
| Frontend demo (alternativo) | HTML estático + Tailwind + Mermaid.js | Para demos sin Telegram |
| Infraestructura | Docker Compose en VPS Hostinger + Nginx + Let's Encrypt | Todo arranca con `docker compose up -d` |

## 4. Los 4 agentes (CrewAI)

Proceso: **`Process.hierarchical`** con el Manager como `manager_agent`.

### Agente 1 — Extractor de Contenido
- **role:** "Extractor y comprensor de contenido"
- **goal:** "Leer cualquier input (texto, PDF transcrito, descripción de imagen, contenido web) e identificar: el tema central, los conceptos clave mencionados, las relaciones implícitas entre conceptos, y el dominio al que pertenece (académico, empresarial, técnico, etc)."
- **backstory:** "Eres un investigador con doctorado en análisis de texto. Tu única misión es destilar el input: no interpretas, no analizas bajo ningún marco teórico, solo extraes el qué del contenido. Eres el sensor del sistema."
- **Output schema (Pydantic):** `tema_central: str, conceptos: list[str], relaciones_implicitas: list[dict], dominio: str, resumen_objetivo: str`

### Agente 2 — Analista TGS
- **role:** "Analista experto en Teoría General de Sistemas"
- **goal:** "Aplicar el marco completo de TGS al contenido extraído. Identificar: sistema, propósito, frontera, entorno, suprasistema, elementos, subsistemas, relaciones, acoplamientos (fuerte/débil/secuencial/recíproco), entradas-procesos-salidas, retroalimentación, estados y transiciones, tipo de sistema (abierto/cerrado, deterministico/estocástico, continuo/discreto) y nivel de complejidad."
- **backstory:** "Eres profesor titular de TGS con 20 años aplicando los conceptos de Bertalanffy a cualquier dominio: biología, software, negocios, sociedad. No confundes elemento con subsistema, ni frontera con entorno, y siempre justificas cada clasificación."
- **Output schema (Pydantic):** ver `schemas/tgs_output.py` — debe coincidir EXACTAMENTE con `TGSAnalysis` (sección 7).

### Agente 3 — Diagramador
- **role:** "Diagramador de sistemas complejos"
- **goal:** "Convertir el análisis TGS en un diagrama Mermaid claro y legible. Subsistemas como nodos, relaciones como aristas, tipo de acoplamiento como estilo de línea, frontera como subgraph. Máximo 12 nodos para legibilidad."
- **backstory:** "Eres diseñador de información especializado en visualización de sistemas complejos. Conoces Mermaid al dedillo. Tu mayor habilidad es decidir qué dejar afuera para que el diagrama comunique sin saturar."
- **Output schema (Pydantic):** `mermaid_code: str, leyenda: str`

### Agente 4 — Manager Coordinador
- **role:** "Director del análisis TGS"
- **goal:** "Coordinar a los otros 3 agentes, validar la coherencia entre el contenido extraído, el análisis TGS y el diagrama generado. Detectar inconsistencias (ej: el diagrama menciona un subsistema que no está en el análisis), pedir correcciones, y producir el JSON final integrado. Si algo no cuadra, RE-DELEGA al agente correspondiente."
- **backstory:** "Eres editor en jefe y arquitecto de sistemas. Tu superpoder es ver el bosque mientras los demás ven el árbol. Nunca entregas un producto a medias: si detectas un problema, mandas a corregirlo antes de cerrar."
- **Especial:** este es el `manager_agent` del Crew jerárquico. NO se le asignan tasks directamente; CrewAI lo invoca automáticamente.

## 5. Análisis TGS del propio proyecto (incluir en docs/)

Cada agente es un subsistema del sistema "TGS Mapper Agent":

| Agente | Rol TGS | Justificación |
|---|---|---|
| Extractor | Subsistema sensor / entrada | Convierte realidad externa en datos internos procesables |
| Analista TGS | Subsistema procesador / núcleo | Aplica las reglas del marco TGS, donde ocurre el comportamiento emergente |
| Diagramador | Subsistema de salida / transducción | Convierte información interna en representación visual consumible |
| Manager | Subsistema de control / retroalimentación | Compara salida con propósito, ajusta enviando a corregir (feedback negativo) |

Acoplamientos:
- Manager ↔ Extractor: **fuerte** (Manager depende directo del output del Extractor)
- Manager ↔ Analista: **fuerte** (núcleo del producto)
- Manager ↔ Diagramador: **débil** (si el diagrama falla, el análisis textual sigue siendo útil)
- Extractor → Analista: **secuencial**
- Analista → Diagramador: **secuencial**
- Manager ↔ todos: **recíproco** (pueden devolver y pedir correcciones)

## 6. Estructura de carpetas

```
tgs-mapper-agent/
├── README.md
├── CLAUDE.md                          # memoria persistente para Claude Code
├── PROJECT_BRIEF.md                   # este archivo
├── DEPENDENCIES.md                    # dependencias del proyecto
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
│   ├── crew_setup.py                  # Define el Crew
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
│       └── llm.py                     # config OpenRouter
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

## 7. JSON schema del output final (Pydantic en schemas/tgs_output.py)

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

## 8. API contract del servicio CrewAI

### POST /analyze

**Request:**
```json
{
  "input_type": "text" | "url" | "pdf" | "image",
  "content": "texto plano | URL | base64",
  "user_id": "telegram_chat_id_opcional"
}
```

**Response (200):**
```json
{
  "ok": true,
  "analysis": { /* TGSAnalysis completo */ },
  "markdown": "# ... rendering legible",
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
{ "ok": false, "error": "mensaje", "stage": "extractor|analista|diagramador|manager" }
```

### GET /health
```json
{ "ok": true, "version": "0.1.0" }
```

## 9. Configuración del LLM (config/llm.py)

```python
from crewai import LLM
import os

def get_llm() -> LLM:
    return LLM(
        model="openrouter/deepseek/deepseek-chat-v4",  # ajustar al slug exacto en openrouter
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        temperature=0.3,  # estructurado, no creativo
        max_tokens=8000,
    )
```

## 10. Variables de entorno (.env.example)

```
# --- LLM ---
OPENROUTER_API_KEY=sk-or-v1-...
LLM_MODEL=deepseek/deepseek-chat-v4

# --- Telegram ---
TELEGRAM_BOT_TOKEN=8000000000:AAAA...
TELEGRAM_WEBHOOK_URL=https://n8n.gartnercodes.com/webhook/telegram

# --- n8n ---
N8N_BASIC_AUTH_USER=santiago
N8N_BASIC_AUTH_PASSWORD=cambiame
N8N_ENCRYPTION_KEY=generar_con_openssl_rand_hex_32
N8N_HOST=n8n.gartnercodes.com
WEBHOOK_URL=https://n8n.gartnercodes.com/

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
REDDIT_TARGET=u_<reddit_username>   # perfil propio, sin restricciones de karma
```

## 11. docker-compose.yml — servicios

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

  # OpenClaw corre aparte en el VPS, n8n lo llama por HTTP.

volumes:
  n8n_data:
```

## 12. n8n workflows

### Workflow 1: `01-telegram-to-crew`
1. **Telegram Trigger** — escucha mensajes nuevos del bot
2. **Switch por tipo** — texto / documento (PDF) / foto / URL detectada por regex
3. **Extracción de contenido** según tipo (descargar archivo de Telegram si aplica, convertir a base64 si es binario)
4. **HTTP Request** → POST `http://crewai:8000/analyze`
5. **Format response** — markdown + render Mermaid a imagen (vía servicio kroki.io o mermaid.ink)
6. **Telegram: Send Message** (markdown) + **Telegram: Send Photo** (con la imagen del diagrama)
7. **Guarda el análisis** en memoria de n8n keyed por `chat_id` para que `/publish` lo pueda recuperar

### Workflow 2: `02-openclaw-publish-reddit`
1. **Telegram Trigger** filtrado por comando `/publish`
2. **Recupera último análisis** del usuario (memoria de n8n keyed por `chat_id`)
3. **Formatea para Reddit:** título atractivo (≤300 chars) + cuerpo con markdown (resumen + propósito + subsistemas clave) + link al diagrama renderizado
4. **HTTP Request** → OpenClaw API → publica en `r/u_<REDDIT_USERNAME>` (perfil propio del autor, sin restricciones de karma)
5. **Confirma al usuario** en Telegram con el link del post de Reddit

**Solo Reddit en el MVP.** Otras redes quedan fuera por costo/fricción.

## 13. Reglas de oro para el código

1. **Idioma:** todo el código en inglés (variables, funciones, comentarios técnicos). Strings dirigidos al usuario final en **español**.
2. **Type hints obligatorios** en todo Python.
3. **Pydantic v2** para schemas. Usa `BaseModel`, `Field`, `Literal`.
4. **FastAPI** con tags y descripciones en cada endpoint (para docs auto en `/docs`).
5. **Logging** con `loguru`, NO `print()`.
6. **Errores explícitos:** cada agente puede fallar; capturar y retornar `{ok: false, stage: "..."}`.
7. **No hardcodear:** todo lo configurable va a `.env`.
8. **CrewAI 0.80+** (versión moderna con tools tipados y `output_pydantic`).
9. **Async donde tenga sentido** en FastAPI (endpoints `async def`).
10. **Tests mínimos:** un test de smoke por agente, un test e2e con input de prueba.
11. **No emojis en el código** (solo en strings al usuario final si encajan).

## 14. Plan de implementación (orden estricto)

1. Crear estructura de carpetas + archivos vacíos
2. `pyproject.toml` + `requirements.txt` + `Dockerfile` del crew
3. `schemas/` — Pydantic models
4. `config/llm.py` — config OpenRouter
5. `tools/` — pdf_reader, image_reader, url_fetcher
6. `agents/` — los 4 agentes
7. `tasks/` — las 4 tasks
8. `crew_setup.py` — ensambla el Crew jerárquico
9. `main.py` — FastAPI con `/analyze` y `/health`
10. `docker-compose.yml` + `.env.example` + `Makefile`
11. Test local con `examples/input-text.json`
12. Workflows de n8n (exportar JSON)
13. Frontend HTML (demo alternativa)
14. Documentación en `docs/`
15. README final

## 15. Lo que NO hay que hacer

- ❌ NO usar OpenAI o Anthropic API como LLM del agente. Solo open source vía OpenRouter (DeepSeek V4).
- ❌ NO inventar agentes adicionales fuera de los 4 definidos.
- ❌ NO meter base de datos. Memoria efímera por request basta (n8n maneja la persistencia mínima del último análisis).
- ❌ NO meter autenticación compleja en CrewAI API. Es servicio interno, expuesto solo a n8n.
- ❌ NO usar `print()`.
- ❌ NO generar diagramas Mermaid con más de 12 nodos.
- ❌ NO devolver markdown dentro del campo `mermaid` (es solo código Mermaid puro).
- ❌ NO publicar en otras redes que no sean Reddit.
- ❌ NO emojis en el código.

## 16. Criterios de "hecho"

- [ ] `docker compose up -d` levanta n8n + crewai sin errores
- [ ] `curl http://localhost:8000/health` responde `{ok: true}`
- [ ] `curl POST /analyze` con un texto devuelve un `TGSAnalysis` válido
- [ ] El workflow de Telegram importa en n8n y responde a un mensaje
- [ ] El bot devuelve markdown + imagen del diagrama
- [ ] El comando `/publish` publica un post en Reddit (`r/u_<username>`)
- [ ] El README explica cómo correr todo desde cero
- [ ] Hay análisis TGS del propio proyecto en `docs/tgs-analysis-of-itself.md`

---

> Si algo no está claro, PREGUNTA antes de inventar. Si algo del plan ya no aplica por una buena razón, EXPLICA antes de cambiarlo.
