# OpenClaw skill test payloads

Test each skill against the running OpenClaw container.

## Prerequisites

OpenClaw must be running:
```bash
just up
just health
```

Set your API key:
```bash
export OPENCLAW_API_KEY=your_key_here
```

## Run all role tests

```bash
bash scripts/test-openclaw-roles.sh
```

## Individual tests

```bash
# Role C - web-search
curl -s -X POST http://localhost:18789/tools/invoke \
  -H "Authorization: Bearer $OPENCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d @examples/openclaw/test-web-search.json | jq

# Role D - tgs-validator
curl -s -X POST http://localhost:18789/tools/invoke \
  -H "Authorization: Bearer $OPENCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d @examples/openclaw/test-tgs-validator.json | jq

# Role E - analysis-memory (store)
curl -s -X POST http://localhost:18789/tools/invoke \
  -H "Authorization: Bearer $OPENCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d @examples/openclaw/test-analysis-memory.json | jq

# Role F - analysis-chat
curl -s -X POST http://localhost:18789/tools/invoke \
  -H "Authorization: Bearer $OPENCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d @examples/openclaw/test-analysis-chat.json | jq

# Role B - crewai-caller (requires CrewAI running)
curl -s -X POST http://localhost:18789/tools/invoke \
  -H "Authorization: Bearer $OPENCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d @examples/openclaw/test-crewai-caller.json | jq

# Role A - reddit-publisher (requires Reddit credentials in .env)
curl -s -X POST http://localhost:18789/tools/invoke \
  -H "Authorization: Bearer $OPENCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d @examples/openclaw/test-reddit-publisher.json | jq
```
