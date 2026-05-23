---
name: analysis-memory
description: "Almacena o recupera analisis TGS en memoria persistente por usuario. Permite recordar analisis previos en conversaciones futuras."
required_bins: [jq]
required_env: []
install: |
  echo "analysis-memory listo"
---

# Implementation

Este skill maneja memoria persistente de analisis TGS por usuario.

Arg {action}: "store" o "retrieve"
Arg {user_id}: identificador unico del usuario (Telegram chat_id)
Arg {analysis}: JSON del analisis TGS (solo para action=store)
Arg {query}: termino de busqueda (solo para action=retrieve, opcional)

Para action="store":
- Guardar el analisis en memoria con clave user_id y timestamp actual
- Incluir el campo tema del analisis como etiqueta
- Retornar: {"ok":true,"stored":true,"user_id":"{user_id}"}

Para action="retrieve":
- Recuperar los ultimos 3 analisis del usuario {user_id}
- Si se provee {query}, filtrar por tema relevante
- Retornar: {"ok":true,"analyses":[{"tema":"...","fecha":"...","resumen":"..."}]}

Si no hay analisis previos para el usuario:
- Retornar: {"ok":true,"analyses":[],"message":"Sin analisis previos para este usuario"}
