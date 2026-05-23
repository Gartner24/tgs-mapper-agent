# TGS Mapper - Guia para el equipo

Este documento explica, en español, como funciona el proyecto **TGS Mapper**:
la arquitectura, el flujo de una conversacion, las herramientas que usamos y el
workflow de n8n. Esta pensado para que cualquier integrante del equipo entienda
el sistema completo.

> Nota importante: la arquitectura cambio respecto al diseño inicial del brief.
> Antes n8n era el dueño del bot de Telegram; ahora **OpenClaw** es el dueño del
> bot y n8n quedo como backend de orquestacion. Este documento describe el estado
> **actual y real** del sistema.

---

## 1. Que hace el sistema

El usuario le escribe a un bot de Telegram (**@tgs_mapper_bot**) describiendo
cualquier cosa (una empresa, un proceso, un tema academico, una idea). El bot
responde con un **analisis bajo la Teoria General de Sistemas (TGS)**: frontera,
entorno, suprasistema, subsistemas, elementos, acoplamientos, entradas/procesos/
salidas, retroalimentacion, estados, tipo de sistema y complejidad. Ademas envia
un **diagrama** del sistema analizado.

Despues del analisis, el usuario puede hacer **preguntas de seguimiento** (por
ejemplo "por que es un sistema abierto?") y el bot responde de forma conversacional.

---

## 2. Arquitectura (componentes)

Todo corre en **Docker** sobre un VPS. Hay tres contenedores principales mas un
proxy:

| Componente | Que es | Rol en el sistema |
|---|---|---|
| **OpenClaw** (`tgs-openclaw`) | Gateway de agente (Node) con LLM | Es el **cerebro conversacional**. Es dueño del bot de Telegram, tiene la persona fija "TGS Mapper", decide cuando analizar vs conversar, y llama al backend |
| **n8n** (`tgs-n8n`) | Orquestador low-code | **Coordinacion**: expone un webhook que recibe el texto, llama a CrewAI, arma la URL del diagrama y devuelve el resultado |
| **CrewAI** (`tgs-crewai`) | Servicio Python (FastAPI) | **Motor de analisis TGS**: 4 agentes en secuencia que producen el analisis formal |
| **nginx + certbot** | Proxy inverso + TLS | Publica la interfaz de n8n en `https://n8n.qyvos.com` |

Servicios externos:

- **Claude (Anthropic)** - el modelo LLM que usan tanto OpenClaw como CrewAI.
  (El brief pedia un modelo open source via OpenRouter, pero se cambio a Claude
  por disponibilidad de creditos. El proveedor es configurable: ver seccion 6.)
- **mermaid.ink** - servicio que convierte el codigo Mermaid en una imagen.
- **Telegram Bot API** - el canal con el usuario.

### Los 4 agentes de CrewAI

El analisis formal lo produce CrewAI con un proceso **secuencial** de 4 agentes:

1. **Extractor** - lee el input y extrae tema, conceptos y relaciones (el "sensor").
2. **Analista TGS** - aplica el marco TGS completo (el "procesador").
3. **Diagramador** - convierte el analisis en codigo **Mermaid** (la "salida").
4. **Manager** - valida la coherencia y arma el JSON final (el "control").

---

## 3. El flujo de una conversacion

```
Usuario (Telegram @tgs_mapper_bot)
        |
        v
   OpenClaw  (dueño del bot; persona "TGS Mapper")
        |
        |  decide: contenido a analizar  -->  ejecuta skill "tgs-analyze"
        |                                          |
        |                                          v
        |                          n8n: POST /webhook/tgs-analyze
        |                                          |
        |                                          v
        |                          CrewAI /analyze  (Extractor -> Analista -> Diagramador -> Manager)
        |                                          |
        |                          n8n arma diagram_url (mermaid.ink) y responde {markdown, diagram_url}
        |                                          |
        |  <---------------------------------------+
        v
   OpenClaw envia al usuario: texto del analisis + imagen del diagrama
```

Paso a paso:

1. El usuario le escribe al bot.
2. **OpenClaw** recibe el mensaje (es dueño del bot, lo escucha por polling).
3. La persona "TGS Mapper" (definida en `AGENTS.md` y `SOUL.md`) decide:
   - Si es **contenido para analizar**: ejecuta la skill **tgs-analyze**, que hace
     una llamada HTTP al webhook de n8n con `{ input_type: "text", content: "..." }`.
   - Si es una **pregunta de seguimiento** sobre un analisis ya entregado: responde
     ella misma con su conocimiento de TGS.
4. **n8n** (workflow 05) recibe el texto, llama a **CrewAI** `/analyze`, espera el
   analisis (los 4 agentes corren en secuencia), arma la URL del diagrama con
   **mermaid.ink** y devuelve `{ markdown, diagram_url }`.
5. **OpenClaw** recibe la respuesta y le envia al usuario el **texto del analisis**
   y luego el **diagrama como imagen**.
6. Mas tarde, el comando **/publish** (pendiente) publicara el ultimo analisis en
   un canal de Telegram.

---

## 4. El workflow de n8n (workflow 05 - "Analysis Webhook")

Es el unico workflow de n8n que usamos. Es el backend que OpenClaw llama. Tiene
4 nodos en linea:

```
[Webhook]  ->  [Analyze]  ->  [Format]  ->  [Respond]
```

1. **Webhook** (`POST /webhook/tgs-analyze`, modo "Respond to Webhook")
   - Recibe el cuerpo `{ input_type, content, user_id }`.

2. **Analyze** (HTTP Request)
   - `POST http://tgs-crewai:8000/analyze` con `{ input_type, content, user_id }`.
   - Timeout de 600s (el analisis puede tardar).

3. **Format** (Code / JavaScript)
   - Si la respuesta no es `ok`, devuelve `{ ok: false, error }`.
   - Codifica el codigo Mermaid en base64url y arma
     `diagram_url = https://mermaid.ink/img/<base64>`.
   - Trunca el markdown si es muy largo (limite de Telegram).
   - Devuelve `{ ok: true, markdown, diagram_url, tema }`.

4. **Respond** (Respond to Webhook)
   - Devuelve ese JSON a quien llamo (OpenClaw).

El archivo del workflow esta en `n8n/workflows/05-analyze-webhook.json` y se
importa en n8n. Su URL interna es `http://tgs-n8n:5678/webhook/tgs-analyze`.

> Los workflows 01-04 del diseño anterior (trigger de Telegram, publicacion en
> Reddit, etc.) fueron **retirados**: ya no se usan porque OpenClaw es quien
> maneja Telegram.

---

## 5. Herramientas usadas

- **Docker / Docker Compose** - empaqueta y levanta todos los servicios con un
  solo comando.
- **OpenClaw** - gateway de agente que conecta canales (Telegram) con un LLM y
  un sistema de "skills" (instrucciones en archivos `SKILL.md`).
- **n8n** - orquestador low-code; aqui solo el workflow 05 (webhook -> CrewAI).
- **CrewAI + FastAPI** - servicio Python con los 4 agentes y el endpoint
  `/analyze`.
- **Claude (Anthropic)** - el LLM, integrado via **litellm**.
- **mermaid.ink** - renderiza los diagramas Mermaid a imagen.
- **nginx + certbot** - proxy inverso y certificado TLS para `n8n.qyvos.com`.
- **Telegram Bot API** - el canal con el usuario.

---

## 6. Configuracion del LLM (importante)

El proveedor del modelo es **configurable** por variables de entorno en `.env`:

```
LLM_PROVIDER=anthropic        # anthropic | groq | openrouter
LLM_MODEL=claude-haiku-4-5
ANTHROPIC_API_KEY=sk-ant-...
```

- En CrewAI esto lo lee `crew/config/llm.py`. Para Anthropic se fuerza la ruta
  por **litellm** (`is_litellm=True`) porque el proveedor nativo de CrewAI compila
  los esquemas grandes de TGS en una "gramatica" que Anthropic rechaza.
- En OpenClaw el modelo se define en su config (`agents.defaults.model.primary =
  "anthropic/claude-haiku-4-5"`) y la clave viaja por `ANTHROPIC_API_KEY`.

Por que se cambio de DeepSeek/OpenRouter a Claude: nos quedamos sin creditos en
OpenRouter, el tier gratis de Groq tenia un limite de tokens por minuto muy bajo
para el pipeline de 4 agentes, y teniamos creditos disponibles en Claude. Si se
quiere volver al requisito original (open source via OpenRouter), basta con poner
creditos en OpenRouter y cambiar `LLM_PROVIDER=openrouter` + `LLM_MODEL`.

---

## 7. El proyecto como un sistema TGS

El propio sistema es un ejemplo de TGS (cada componente es un subsistema):

| Componente | Rol TGS |
|---|---|
| OpenClaw | Subsistema de interfaz y dialogo (entrada/salida hacia el usuario) |
| n8n | Subsistema de coordinacion (conecta y orquesta los demas) |
| CrewAI (4 agentes) | Subsistema de procesamiento (donde ocurre el analisis) |
| Manager (dentro de CrewAI) | Subsistema de control / retroalimentacion |
| mermaid.ink | Transductor de salida (convierte informacion en imagen) |

---

## 8. Comandos utiles

```bash
docker compose up -d        # levantar todo
docker compose ps           # ver estado de los contenedores
docker compose logs -f openclaw   # ver logs de OpenClaw
docker compose logs -f crewai     # ver logs de CrewAI
```

- Interfaz de n8n: `https://n8n.qyvos.com`
- Bot de Telegram: `@tgs_mapper_bot`
- Webhook interno de analisis: `http://tgs-n8n:5678/webhook/tgs-analyze`
