---
name: web-search
description: "Busca informacion reciente en la web sobre un tema y devuelve contexto enriquecido para el analisis TGS."
required_bins: [curl, jq]
required_env: [TAVILY_API_KEY]
install: |
  echo "web-search listo"
---

# Implementation

Buscar informacion sobre el tema {topic} usando la API de Tavily.

  curl -s -X POST "https://api.tavily.com/search" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TAVILY_API_KEY" \
    -d "{\"query\":\"{topic}\",\"search_depth\":\"basic\",\"max_results\":3,\"include_answer\":true}"

Extraer los campos: answer (resumen de Tavily) y results[].content (fragmentos relevantes).
Concatenar todo en un texto de contexto de maximo 1500 caracteres.

Retornar: {"result":"<contexto concatenado>","topic":"{topic}"}

Si TAVILY_API_KEY no esta disponible o la llamada falla, retornar:
{"result":"","topic":"{topic}","skipped":true}
