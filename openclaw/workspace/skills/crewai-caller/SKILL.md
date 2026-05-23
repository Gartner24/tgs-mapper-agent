---
name: crewai-caller
description: "Llama directamente al endpoint /analyze del servicio CrewAI y retorna el analisis TGS completo. Canal alternativo que bypasa n8n."
required_bins: [curl, jq]
required_env: [CREW_API_URL]
install: |
  echo "crewai-caller listo"
---

# Implementation

Llamar al endpoint /analyze del servicio CrewAI con los parametros recibidos.

Arg {input_type}: "text", "url", "pdf" o "image"
Arg {content}: texto plano, URL, o contenido en base64
Arg {user_id}: identificador del usuario (opcional)

Construir el payload con jq para evitar inyeccion JSON:

  PAYLOAD=$(jq -n \
    --arg it "{input_type}" \
    --arg c "{content}" \
    --arg uid "{user_id}" \
    '{input_type: $it, content: $c, user_id: $uid}')

  curl -s -X POST "${CREW_API_URL}/analyze" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" \
    --max-time 120

Validar que la respuesta contenga "ok":true y el campo "analysis".

Si la llamada es exitosa, retornar el JSON completo de la respuesta de CrewAI tal como llega.
Si falla (timeout, error HTTP o ok:false), retornar:
{"ok":false,"error":"El servicio de analisis no esta disponible: <mensaje de error>"}
