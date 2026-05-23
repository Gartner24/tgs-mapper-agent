# Architecture — TGS Mapper Agent

## Overview

TGS Mapper Agent is a multi-agent system that analyzes any input (text, PDF,
image, URL) under the General Systems Theory (TGS) framework and returns a
structured JSON analysis with a Mermaid diagram.

## Component diagram

```
User (Telegram)
    |
    | HTTPS (443)
    v
nginx-proxy  ──── [web Docker network] ────────────────────────────────┐
    |                                                                   |
    | proxy_pass http://tgs-n8n:5678                                   |
    v                                                                   |
tgs-n8n (n8n 5678)                                                     |
    |                                                                   |
    | Workflow 01: any message                                          |
    |   1. Detect input type (text/url/pdf/image)                      |
    |   2. Download binary from Telegram if needed                     |
    |   3. POST /analyze ──────────────────────────────────────────────┤
    |                                                                   |
    |   POST http://tgs-crewai:8000/analyze                            |
    |                              |                                    |
    |                              v                                    |
    |                     tgs-crewai (FastAPI 8000)                    |
    |                              |                                    |
    |                    CrewAI hierarchical Crew                      |
    |                              |                                    |
    |            ┌─────────────────┼──────────────┐                   |
    |            v                 v               v                   |
    |       Extractor          Analyst TGS    Diagrammer               |
    |       (sensor)           (processor)   (output)                  |
    |            └─────────────────┼──────────────┘                   |
    |                              v                                    |
    |                         Manager (control)                        |
    |                   validates + assembles TGSAnalysis               |
    |                              |                                    |
    |   <─── {ok, analysis, markdown, mermaid, metadata} ─────────────┘
    |
    |   4. Render mermaid.ink URL
    |   5. Store analysis in staticData[chat_id]
    |   6. Send markdown text to user
    |   7. Send diagram image to user
    |
    | Workflow 02: /publish command
    |   1. Retrieve analysis from staticData[chat_id]
    |   2. POST OpenClaw /publish
    v
OpenClaw (VPS, separate process)
    |
    v
Reddit r/u_<username>
```

## Services

| Service | Image | Network | Port | Purpose |
|---|---|---|---|---|
| `tgs-n8n` | n8n latest | web (external) | expose 5678 | Orchestration, Telegram I/O |
| `tgs-crewai` | ./crew (Python 3.12) | web (external) | expose 8000 | Multi-agent brain |
| `nginx-proxy` | custom nginx:alpine | web (external) | 80, 443 | TLS termination, routing |
| OpenClaw | separate VPS process | HTTP | varies | Reddit publishing |

## Request lifecycle

1. User sends a message to the Telegram bot.
2. Telegram delivers it to `https://n8n.qyvos.com/webhook/telegram`.
3. n8n Workflow 01 fires, detects the input type, downloads binary files if
   needed, converts them to base64.
4. n8n POSTs `{input_type, content, user_id}` to `http://tgs-crewai:8000/analyze`.
5. FastAPI receives the request and calls `run_analysis()`.
6. CrewAI builds a hierarchical Crew with 4 agents and runs `kickoff()`.
7. The Manager orchestrates: Extractor runs first, then Analyst, then Diagrammer,
   finally the Manager's coordination task validates and assembles the final
   `TGSAnalysis` JSON.
8. FastAPI returns `{ok, analysis, markdown, mermaid, metadata}`.
9. n8n formats the response, encodes the Mermaid diagram as a `mermaid.ink` URL,
   saves the analysis to `$workflow.staticData[chatId]`, and sends the markdown
   text + diagram image back to the user via Telegram.
10. If the user later sends `/publish`, Workflow 02 retrieves the stored analysis
    and posts it to Reddit via OpenClaw.

## LLM configuration

All 4 agents share a single `LLM` instance configured via `config/llm.py`:
- Provider: OpenRouter (`https://openrouter.ai/api/v1`)
- Model: `openrouter/{LLM_MODEL}` (env var, default `deepseek/deepseek-chat`)
- Temperature: 0.3 (structured output, not creative)
- Max tokens: 8000

## Data flow between agents

```
AnalyzeRequest
    -> ExtractionResult  (Extractor)
    -> TGSAnalysis*      (Analyst, diagrama_mermaid="PENDIENTE")
    -> DiagramOutput     (Diagrammer)
    -> TGSAnalysis       (Manager, final with diagrama_mermaid populated)
```

Each agent output is typed via Pydantic v2 (`output_pydantic` on the Task).
The Manager's coordination task receives all three prior outputs as `context`.

## Deployment

Project path on VPS: `/opt/projects/tgs-mapper-agent/`

```bash
git clone <repo> /opt/projects/tgs-mapper-agent
cd /opt/projects/tgs-mapper-agent
cp .env.example .env   # fill in all values
docker compose up -d
```

The `web` external Docker network must exist before starting:
```bash
docker network create web
```
