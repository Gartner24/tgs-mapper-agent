# CLAUDE.md

Persistent project memory for Claude Code. Always read me before acting.

## Project

**TGS Mapper Agent** — multi-agent system that analyzes any input under the lens of General Systems Theory (TGS / GST). Academic project for Systems Engineering (UTP), General Systems Theory course.

## Stack (closed)

- **n8n** (Docker) — orchestration + Telegram integration
- **CrewAI** (FastAPI in Docker) — hierarchical multi-agent, 4 agents (Extractor, TGS Analyst, Diagrammer, Manager)
- **OpenRouter + DeepSeek V4** — open source LLM via API
- **Telegram Bot** — main user channel
- **OpenClaw → Reddit** — publishes the analysis to `r/u_<username>` when the user sends `/publish`. Reddit only in MVP.
- **Docker Compose** — everything starts with a single command

## Language rules (CRITICAL)

- **Code, comments, variable names, function names, technical docs:** English
- **End-user strings (Telegram, errors, Reddit posts):** Spanish (Colombia)
- **LLM agent prompts (role, goal, backstory):** Spanish (Colombia)
- **LLM outputs / analysis content:** Spanish (Colombia)
- **Pydantic field names:** Spanish (matches TGS course terminology — `frontera`, `subsistemas`, etc.). Class names in English.

## Hard rules

1. Do NOT use OpenAI or Anthropic as the agent LLM. Only open source via OpenRouter.
2. Type hints mandatory in Python.
3. Pydantic v2 for all schemas.
4. Logging with `loguru`. No `print()`.
5. CrewAI 0.80+.
6. Do not add agents beyond the 4 defined.
7. Do not add dependencies without justifying them.
8. No emojis in code.
9. Reddit only as publication network (no Twitter, no LinkedIn).

## Architecture decisions

- CrewAI process: **`Process.hierarchical`** with Manager as `manager_agent`.
- Agent output: strictly conforms to the Pydantic `TGSAnalysis` schema.
- Each subsystem = one agent. Deliberate: the project **is itself a TGS system**.
- The Manager works as a negative feedback mechanism (TGS concept).

## Reference documents

- `PROJECT_BRIEF.md` — full project specification.
- `DEPENDENCIES.md` — list of dependencies and external services.
- `docs/architecture.md` — architecture diagram and description.
- `docs/tgs-analysis-of-itself.md` — TGS analysis of the project itself (key for the presentation).
- `docs/agents-design.md` — detailed roles, goals, backstories of the 4 agents.
- `docs/demo-script.md` — presentation script.

## Useful commands

```bash
just up         # docker compose up -d
just logs       # docker compose logs -f
just test       # run smoke test against /analyze
just down       # stop everything
just rebuild    # rebuild crewai container
just health     # check /health endpoint
just shell      # open shell in crewai container
```

## Endpoints

- CrewAI (internal): `http://crewai:8000/analyze`
- CrewAI (optional external): `https://api.qyvos.com/analyze`
- n8n UI: `https://n8n.qyvos.com`
- Telegram webhook: `https://n8n.qyvos.com/webhook/telegram`

## Message flow

User → Telegram → n8n (Workflow 01) → CrewAI `/analyze` → response back to Telegram (text + rendered diagram).

If the user sends `/publish` → n8n (Workflow 02) → OpenClaw → Reddit (`r/u_<username>`).
