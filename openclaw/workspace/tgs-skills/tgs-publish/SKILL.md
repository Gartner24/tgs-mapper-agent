---
name: tgs-publish
description: "Publica el ultimo analisis TGS entregado en el canal de Telegram. Usar SOLO cuando el usuario envie el comando /publish."
---

# Publicar analisis en el canal

Cuando el usuario envie el comando **/publish**, publica el ULTIMO analisis TGS
que entregaste en esta conversacion (su texto y su diagrama) en el canal de
Telegram **@tgs_mapper_bot_channel**.

## Procedimiento (3 pasos, en este orden, sin saltarte ninguno)

### Paso 1 - Verifica que haya un analisis previo

Si en la conversacion NO hay un analisis TGS previo entregado por el backend,
responde exactamente: "Primero pideme un analisis y luego usa /publish para publicarlo." y termina.

### Paso 2 - Escribe el contenido a archivos temporales

Usa tu herramienta de shell para escribir el TEXTO del analisis y la URL del
diagrama a archivos. NO intentes pasar el texto por argumentos: el shell rompe
las comillas y backticks del markdown. Usa heredocs con comillas simples para
preservar el contenido literal:

```bash
cat > /tmp/tgs-publish.txt <<'TGS_PUBLISH_EOF'
<<<AQUI VA EL MARKDOWN COMPLETO DEL ULTIMO ANALISIS>>>
TGS_PUBLISH_EOF

cat > /tmp/tgs-publish.url <<'TGS_PUBLISH_EOF'
<<<AQUI VA LA URL DEL DIAGRAMA (la que empieza con https://mermaid.ink/img/...)>>>
TGS_PUBLISH_EOF
```

Reglas obligatorias:
- El delimitador es `'TGS_PUBLISH_EOF'` con comillas simples.
- Reemplaza `<<<...>>>` por el contenido real, sin las marcas.
- Si no tienes la URL del diagrama, deja `/tmp/tgs-publish.url` vacio.
- NO uses `node -e`, `python -c` ni `ruby -e`: el sandbox los bloquea
  (`strictInlineEval`). Siempre invoca scripts por archivo.

### Paso 3 - Ejecuta el publicador

```bash
cd /app/workspace/tgs-skills/tgs-publish && node publish.mjs
```

El script imprime un JSON con el resultado.

- `{"ok":true,...,"link":"https://t.me/tgs_mapper_bot_channel/123"}` -> exito.
  Responde al usuario: "Publicado en el canal: <link>".
- `{"ok":false,...,"msg_error":"..."}` o `"error":"..."` -> falla.
  Responde con el error tal cual: "No se pudo publicar: <error>".

## Reglas

- Solo publica el analisis mas reciente; no inventes contenido nuevo.
- Responde en espanol (Colombia).
- Usa exec con `bash` y `node`. No uses `web_fetch`.
- No reintentes mas de una vez si falla; reporta el error al usuario.
