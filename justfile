# TGS Mapper Agent — task runner (https://github.com/casey/just)

# Start all services in the background
up:
    docker compose up -d

# Stop all services
down:
    docker compose down

# Stream logs from all services
logs:
    docker compose logs -f

# Rebuild and restart only the crewai service
rebuild:
    docker compose build crewai
    docker compose up -d crewai

# Run a smoke test against /analyze using examples/input-text.json
test:
    docker compose exec crewai python3 -c "\
import httpx, json; \
data = json.load(open('examples/input-text.json')); \
r = httpx.post('http://localhost:8000/analyze', json=data, timeout=120); \
print(r.status_code); \
print(json.dumps(r.json(), indent=2, ensure_ascii=False)[:2000])"

# Open a shell inside the crewai container
shell:
    docker compose exec crewai /bin/bash

# Check health endpoint
health:
    docker compose exec crewai curl -s http://localhost:8000/health | python3 -m json.tool

# Stream logs from OpenClaw only
openclaw-logs:
    docker compose logs -f openclaw

# Open a shell inside the OpenClaw container
openclaw-shell:
    docker compose exec openclaw /bin/sh

# Smoke test all 6 OpenClaw roles (requires OPENCLAW_API_KEY in env)
test-openclaw:
    bash scripts/test-openclaw-roles.sh
