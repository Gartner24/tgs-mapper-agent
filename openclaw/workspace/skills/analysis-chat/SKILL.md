---
name: analysis-chat
description: "Responde preguntas de seguimiento sobre el ultimo analisis TGS del usuario usando memoria del contexto de la conversacion."
required_bins: [jq]
required_env: []
install: |
  echo "analysis-chat listo"
---

# Implementation

Responder una pregunta de seguimiento sobre el analisis TGS del usuario.

Arg {user_id}: identificador del usuario (Telegram chat_id)
Arg {question}: la pregunta del usuario sobre su analisis TGS

Pasos:
1. Recuperar el ultimo analisis almacenado para {user_id} desde memoria.
2. Si no existe analisis previo, responder explicando que el usuario debe enviar primero un texto para analizar.
3. Si existe, usar el analisis como contexto y responder la pregunta {question} en espanol colombiano.
4. La respuesta debe ser concisa (maximo 300 palabras) y pedagogicamente util para un estudiante de TGS.

Campos clave del analisis para usar como contexto:
tema, tipo_sistema, frontera, subsistemas[].nombre, relaciones, complejidad.nivel

Retornar:
{"ok":true,"reply":"<respuesta en espanol>","user_id":"{user_id}"}

Si no hay analisis previo:
{"ok":true,"reply":"No tienes ningun analisis guardado. Enviame primero un texto, PDF, imagen o URL para analizar.","user_id":"{user_id}"}
