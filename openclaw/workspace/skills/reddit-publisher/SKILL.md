---
name: reddit-publisher
description: "Publica un analisis TGS como post de texto en el perfil de Reddit del usuario."
required_bins: [curl, jq]
required_env: [REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD]
install: |
  echo "reddit-publisher listo"
---

# Implementation

Publicar el post en Reddit usando la API OAuth2 de Reddit.

Paso 1 — obtener token OAuth2:

  curl -s -X POST "https://www.reddit.com/api/v1/access_token" \
    -u "$REDDIT_CLIENT_ID:$REDDIT_CLIENT_SECRET" \
    --data-urlencode "grant_type=password" \
    --data-urlencode "username=$REDDIT_USERNAME" \
    --data-urlencode "password=$REDDIT_PASSWORD" \
    -H "User-Agent: TGSMapperAgent/1.0" \
    | jq -r '.access_token'

Paso 2 — publicar el post (reemplazar {title}, {body}, {target} con los args recibidos):

  curl -s -X POST "https://oauth.reddit.com/api/submit" \
    -H "Authorization: Bearer $TOKEN" \
    -H "User-Agent: TGSMapperAgent/1.0" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    --data-urlencode "kind=self" \
    --data-urlencode "sr={target}" \
    --data-urlencode "title={title}" \
    --data-urlencode "text={body}"

Paso 3 — retornar resultado:
Si la respuesta contiene .json.data.url, retornar: {"ok":true,"post_url":"<url>"}
Si hay error, retornar: {"ok":false,"error":"<mensaje>"}
