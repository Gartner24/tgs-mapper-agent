# TGS Mapper - Comandos del dia a dia

Cheatsheet de los comandos que necesitas para correr la demo y diagnosticar
problemas en caliente. Asume que estas en `/opt/apps/tgs-mapper-agent` (el
repo).

> Si vas a hacer la demo, lee primero la seccion **"Antes de la demo"** y luego
> **"Durante la demo"**. Todo lo demas son comandos para cuando algo falle.

---

## 0. Servicios y puertos

| Contenedor | Servicio | Puerto interno | Expuesto |
|---|---|---|---|
| `tgs-openclaw` | Gateway del bot (LLM) | 18789 | no |
| `tgs-n8n` | Orquestador (webhook) | 5678 | via nginx -> https://n8n.qyvos.com |
| `tgs-crewai` | 4 agentes TGS | 8000 | no |

Red Docker: los servicios se llaman entre si por nombre del contenedor
(`http://tgs-n8n:5678`, `http://tgs-crewai:8000`).

---

## 1. Antes de la demo (checklist)

```bash
# 1. Verifica que .env tiene credenciales y creditos
grep -E '^(ANTHROPIC_API_KEY|TELEGRAM_BOT_TOKEN|LLM_PROVIDER|LLM_MODEL)=' .env

# 2. Levanta todo
docker compose up -d

# 3. Verifica que los 3 contenedores estan arriba (espera ~30s)
docker compose ps

# 4. Verifica que el backend responde
curl -s http://localhost:8000/health
# -> {"status":"ok"}

# 5. Verifica que el workflow de n8n esta activo
#    Entra a https://n8n.qyvos.com -> "Analysis Webhook" debe tener el switch ACTIVE en verde

# 6. Verifica que el bot esta conectado a Telegram
docker compose logs --tail=20 openclaw | grep -E "telegram.*starting provider"
# -> [telegram] [default] starting provider (@tgs_mapper_bot)

# 7. Verifica que el bot puede postear al canal
TOKEN=$(grep '^TELEGRAM_BOT_TOKEN=' .env | cut -d= -f2)
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -H 'content-type: application/json' \
  -d '{"chat_id":"@tgs_mapper_bot_channel","text":"check pre-demo"}' \
  | python3 -m json.tool | head -5
# -> "ok": true. Luego borralo manualmente del canal.
```

Si los 7 pasos pasan, estas listo.

---

## 2. Durante la demo (comandos vivos)

Estos los puedes correr en una terminal mientras el publico mira la pantalla.

```bash
# Ver el flujo en vivo (deja correr en una terminal aparte)
docker compose logs -f openclaw crewai

# Ver solo lo que el bot esta haciendo
docker compose logs -f openclaw | grep -iE "inbound|sendMessage|tool|skill"

# Si el bot tarda mucho, revisar si CrewAI esta procesando
docker compose logs -f crewai | grep -E "agent|task|complete"
```

Flujo esperado de la demo desde el lado del usuario:

1. Mandas al bot un texto cualquiera (ej. "Una panaderia ...").
2. Bot responde inmediatamente: `Procesando tu analisis bajo el marco TGS (tarda ~1-2 minutos)...`
3. ~3 minutos despues: bloque de texto con el analisis.
4. Justo despues: imagen del diagrama.
5. Mandas `/publish`. Bot responde: `Publicado en el canal: https://t.me/tgs_mapper_bot_channel/N`.
6. Abres el canal y se ve el post.

---

## 3. Diagnostico cuando algo falle

### El bot no responde nada

```bash
# 1. Esta el contenedor arriba?
docker compose ps openclaw

# 2. Esta conectado a Telegram?
docker compose logs --tail=50 openclaw | grep -iE "telegram|error"

# 3. Reiniciar (mata cualquier sesion atascada)
docker compose restart openclaw

# 4. Despues del restart, espera 10 s y vuelve a mandar un mensaje
```

### El bot responde "hubo un problema tecnico con el backend"

n8n no respondio o devolvio error.

```bash
# 1. n8n arriba?
docker compose ps n8n

# 2. El workflow esta activo? (la respuesta debe tener "ok":true)
curl -s -X POST http://localhost:5678/webhook/tgs-analyze \
  -H 'content-type: application/json' \
  -d '{"input_type":"text","content":"prueba"}' \
  | head -c 300

# 3. CrewAI arriba y respondiendo?
curl -s http://localhost:8000/health

# 4. CrewAI no tiene creditos? (ver logs)
docker compose logs --tail=100 crewai | grep -iE "anthropic|error|credit"
```

### `/publish` falla

```bash
# 1. El bot es admin del canal?
TOKEN=$(grep '^TELEGRAM_BOT_TOKEN=' .env | cut -d= -f2)
curl -s "https://api.telegram.org/bot${TOKEN}/getChatMember?chat_id=@tgs_mapper_bot_channel&user_id=$(curl -s "https://api.telegram.org/bot${TOKEN}/getMe" | python3 -c 'import sys,json;print(json.load(sys.stdin)["result"]["id"])')" | python3 -m json.tool

# 2. Probar publicacion directa (esto deberia "ok": true)
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -H 'content-type: application/json' \
  -d '{"chat_id":"@tgs_mapper_bot_channel","text":"prueba directa"}' \
  | python3 -m json.tool | head -10

# 3. Probar el script del skill desde adentro del contenedor
docker compose exec openclaw bash -c "echo 'prueba' > /tmp/tgs-publish.txt; > /tmp/tgs-publish.url; cd /app/workspace/tgs-skills/tgs-publish && node publish.mjs"
# -> debe imprimir {"ok":true,...}
```

Si la prueba directa falla con `chat not found`, el bot no es admin del canal.
Si falla con `chat_write_forbidden`, no tiene permiso "Post Messages".

### Sin creditos en Anthropic

Mira la consola: https://console.anthropic.com/settings/billing

Si se acabaron a la mitad de la demo, las opciones son:

1. Recargar (Anthropic acepta tarjetas; tarda <1 min en aplicar).
2. Apagar OpenClaw y entregar la demo manual: mostrar el endpoint de CrewAI
   directo o el frontend HTML.

---

## 4. Reset entre pruebas

A veces el bot acumula contexto y se confunde. Para limpiar:

```bash
# Opcion A: comando dentro del chat con el bot (recomendado)
#   manda al bot:  /reset

# Opcion B: borrar todas las sesiones del agente (hard reset)
docker compose exec openclaw sh -c 'rm -f /home/node/.openclaw/agents/main/sessions/*.jsonl*'
docker compose restart openclaw
```

---

## 5. Apagar todo (despues de la demo)

```bash
# Conserva los datos (puedes volver a `up -d` mas tarde)
docker compose down

# Borra ademas volumenes (n8n se reinicia de cero, pierdes el workflow):
docker compose down -v
# NO hagas esto a menos que quieras empezar desde cero.
```

---

## 6. Atajos con `just`

Si tienes `just` instalado, el `Justfile` del repo define:

```bash
just up         # docker compose up -d
just down       # docker compose down
just logs       # docker compose logs -f
just ps         # docker compose ps
just health     # curl /health
just shell      # entrar al contenedor de crewai
just rebuild    # docker compose build crewai && restart
```

---

## 7. Comandos del bot (en el chat con @tgs_mapper_bot)

| Comando | Que hace |
|---|---|
| `<cualquier texto>` | Genera un analisis TGS (3-4 min) y manda texto + diagrama |
| `/publish` | Publica el ULTIMO analisis en el canal `@tgs_mapper_bot_channel` |
| `/reset` | Borra el contexto de la conversacion (si el bot se confunde) |
| `/help` | Lista los comandos disponibles (los expone OpenClaw, varios; nosotros solo usamos los 3 de arriba) |
