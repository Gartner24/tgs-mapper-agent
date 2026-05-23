# OpenClaw — TGS Mapper Agent

Self-hosted AI agent framework that extends the TGS Mapper Agent with 6 roles:

| Role | Skill | Purpose |
|---|---|---|
| A | `reddit-publisher` | Publish TGS analysis to Reddit |
| B | `crewai-caller` | Alternative direct channel bypassing n8n |
| C | `web-search` | Pre-analysis web research to enrich context |
| D | `tgs-validator` | Post-analysis coherence validation |
| E | `analysis-memory` | Long-term per-user analysis memory |
| F | `analysis-chat` | Conversational follow-up about past analyses |

## Configuration

Config file: `openclaw/config/openclaw.json` (mounted to `/root/.openclaw/openclaw.json`)

Required env vars (add to `.env`):

```
OPENCLAW_API_KEY=<bearer token for /tools/invoke>
TAVILY_API_KEY=<for web-search skill>
```

## API

All skills are invoked via:

```bash
POST http://tgs-openclaw:18789/tools/invoke
Authorization: Bearer $OPENCLAW_API_KEY
Content-Type: application/json

{
  "tool": "<skill-name>",
  "args": { ... }
}
```

## Skills

### reddit-publisher

Args: `title`, `body`, `target` (e.g. `u_myusername`)

### web-search

Args: `topic`

### tgs-validator

Args: `analysis` (stringified TGSAnalysis JSON)

### analysis-memory

Args: `action` (`store`|`retrieve`), `user_id`, `analysis` (for store), `query` (for retrieve)

### analysis-chat

Args: `user_id`, `question`

### crewai-caller

Args: `input_type`, `content`, `user_id`

## Health check

```bash
curl http://localhost:18789/healthz
```

## Logs

```bash
just openclaw-logs
```
