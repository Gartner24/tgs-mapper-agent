# CLAUDE.md

Memoria persistente del proyecto para Claude Code. Léeme siempre antes de actuar.

## Proyecto

**TGS Mapper Agent** — sistema multi-agente que analiza cualquier input bajo el marco de la Teoría General de Sistemas. Proyecto académico de Ingeniería de Sistemas (UTP), curso Teoría General de Sistemas.

## Stack (cerrado)

- **n8n** (Docker) — orquestación + integración con Telegram
- **CrewAI** (FastAPI en Docker) — multi-agente jerárquico, 4 agentes (Extractor, Analista TGS, Diagramador, Manager)
- **OpenRouter + DeepSeek V4** — LLM open source vía API
- **Telegram Bot** — canal principal de usuario
- **OpenClaw → Reddit** — publica el análisis en `r/u_<username>` cuando el usuario manda `/publish`. Solo Reddit en el MVP.
- **Docker Compose** — todo arranca con un solo comando

## Reglas duras

1. NO usar OpenAI ni Anthropic como LLM del agente. Solo open source vía OpenRouter.
2. Idioma del código: inglés. Strings al usuario final: español.
3. Type hints obligatorios en Python.
4. Pydantic v2 para todos los schemas.
5. Logging con `loguru`. Nada de `print()`.
6. CrewAI 0.80+.
7. No agregar agentes fuera de los 4 definidos.
8. No agregar dependencias sin justificarlo.
9. No emojis en código.
10. Solo Reddit como red de publicación (no Twitter, no LinkedIn).

## Decisiones de arquitectura

- Proceso CrewAI: **`Process.hierarchical`** con Manager como `manager_agent`.
- Output del agente: estrictamente conforme al schema Pydantic `TGSAnalysis`.
- Cada subsistema = un agente. Esto es deliberado: el proyecto **es en sí mismo un sistema TGS**.
- Manager funciona como mecanismo de retroalimentación negativa (concepto TGS).

## Documentos de referencia

- `PROJECT_BRIEF.md` — especificación completa del proyecto.
- `DEPENDENCIES.md` — lista de dependencias y servicios externos.
- `docs/architecture.md` — diagrama y descripción de la arquitectura.
- `docs/tgs-analysis-of-itself.md` — análisis TGS del propio proyecto (importante para la exposición).
- `docs/agents-design.md` — roles, goals, backstories detallados de los 4 agentes.
- `docs/demo-script.md` — guion de la exposición.

## Comandos útiles

```bash
make up         # docker compose up -d
make logs       # docker compose logs -f
make test       # corre tests de smoke
make down       # detiene todo
make rebuild    # rebuild crewai container
```

## Endpoints

- CrewAI (interno): `http://crewai:8000/analyze`
- CrewAI (externo opcional): `https://api.gartnercodes.com/analyze`
- n8n UI: `https://n8n.gartnercodes.com`
- Telegram webhook: `https://n8n.gartnercodes.com/webhook/telegram`

## Flujo de un mensaje

Usuario → Telegram → n8n (Workflow 01) → CrewAI `/analyze` → respuesta a Telegram (texto + diagrama renderizado).

Si el usuario manda `/publish` → n8n (Workflow 02) → OpenClaw → Reddit (`r/u_<username>`).
