#!/usr/bin/env bash
# Smoke test for all 6 OpenClaw roles.
# Requires: OPENCLAW_API_KEY set, OpenClaw running on localhost:18789.

if [[ -z "${OPENCLAW_API_KEY:-}" ]]; then
  echo "ERROR: OPENCLAW_API_KEY no esta definido. Ejecuta: export OPENCLAW_API_KEY=<tu_clave>" >&2
  exit 1
fi

set -euo pipefail

BASE_URL="${OPENCLAW_URL:-http://localhost:18789}"
AUTH="Authorization: Bearer ${OPENCLAW_API_KEY}"
CT="Content-Type: application/json"

pass=0
fail=0

invoke() {
  local role="$1"
  local skill="$2"
  local payload="$3"
  local check_field="$4"

  echo -n "Role ${role} (${skill})... "
  RESP=$(curl -sf -X POST "${BASE_URL}/tools/invoke" \
    -H "$AUTH" -H "$CT" \
    -d "$payload" 2>&1) || { echo "FAIL (curl error)"; ((fail++)); return; }

  if echo "$RESP" | jq -e ".${check_field}" > /dev/null 2>&1; then
    echo "OK"
    ((pass++))
  else
    echo "FAIL (missing .${check_field} in response)"
    echo "  Response: $(echo "$RESP" | head -c 200)"
    ((fail++))
  fi
}

echo "=== OpenClaw role smoke tests ==="
echo "Endpoint: ${BASE_URL}"
echo ""

invoke "C" "web-search" \
  '{"tool":"web-search","args":{"topic":"sistemas complejos"}}' \
  "topic"

invoke "D" "tgs-validator" \
  '{"tool":"tgs-validator","args":{"analysis":"{\"tema\":\"test\",\"subsistemas\":[]}"}}' \
  "valid"

invoke "E" "analysis-memory" \
  '{"tool":"analysis-memory","args":{"action":"store","user_id":"test-user","analysis":"{\"tema\":\"test\"}"}}' \
  "ok"

invoke "F" "analysis-chat" \
  '{"tool":"analysis-chat","args":{"user_id":"test-user","question":"Que tipo de sistema es?"}}' \
  "ok"

invoke "B" "crewai-caller" \
  "{\"tool\":\"crewai-caller\",\"args\":{\"input_type\":\"text\",\"content\":\"sistema de prueba\",\"user_id\":\"test\"}}" \
  "ok"

invoke "A" "reddit-publisher" \
  '{"tool":"reddit-publisher","args":{"title":"[TEST] TGS Mapper","body":"Test post","target":"u_testuser"}}' \
  "ok"

echo ""
echo "Results: ${pass} passed, ${fail} failed"
[ "$fail" -eq 0 ] && exit 0 || exit 1
