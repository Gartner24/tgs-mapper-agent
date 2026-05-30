# TGS Mapper - Guia de despliegue desde cero

Esta guia describe paso a paso como levantar el sistema completo (OpenClaw +
n8n + CrewAI) en cualquier servidor Linux con Docker. Cubre el caso de servidor
nuevo (VPS o local). Tiempo estimado: 30-45 minutos.

> Para entender la arquitectura primero, lee [`guia-equipo.md`](guia-equipo.md).

---

## 1. Requisitos del servidor

- Linux (Ubuntu 22.04+ probado). 2 vCPU, 4 GB RAM, 20 GB disco minimo.
- Docker Engine 24+ y `docker compose` v2 (plugin, no el viejo `docker-compose`).
- `git`, `curl`, `python3` (para diagnostico) y `just` (opcional, atajos).
- Puertos `5678`, `8000`, `18789` libres internamente. Solo `80/443` necesitan
  estar expuestos si usas nginx/Cloudflare delante.
- Acceso `sudo` para configurar nginx (opcional, solo si vas a exponer n8n
  publico).

Verificacion rapida:

```bash
docker --version          # Docker version 24+
docker compose version    # Docker Compose version v2.x
git --version
```

---

## 2. Cuentas y credenciales necesarias

Necesitas obtener (antes de empezar):

| Servicio | Que necesitas | Donde |
|---|---|---|
| **Telegram bot** | Token del bot (`123456:ABC...`) | `@BotFather` -> `/newbot`. Anota el token. |
| **Telegram canal** | Crear un canal publico (ej. `@tgs_mapper_bot_channel`) y agregar al bot como administrador con permiso "Publicar mensajes" | App de Telegram |
| **Anthropic** | API key (`sk-ant-...`) con creditos | https://console.anthropic.com/ |
| **(opcional) OpenRouter** | API key si vas a usar modelos open source | https://openrouter.ai/ |
| **(opcional) Tavily** | API key si activas web search en el agente | https://tavily.com/ |
| **(opcional) Cloudflare** | Token para emitir certificado TLS para `n8n.tu-dominio.com` | https://dash.cloudflare.com/profile/api-tokens |

---

## 3. Clonar el repositorio

```bash
cd /opt/apps    # o donde prefieras
git clone https://github.com/Gartner24/tgs-mapper-agent.git
cd tgs-mapper-agent
```

---

## 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` y llena los valores siguientes (los demas pueden quedarse con sus
defaults):

```env
# --- LLM ---
LLM_PROVIDER=anthropic          # anthropic | openrouter | groq
LLM_MODEL=claude-haiku-4-5
ANTHROPIC_API_KEY=sk-ant-...

# --- Telegram ---
TELEGRAM_BOT_TOKEN=8903...:AAG...      # del @BotFather
TELEGRAM_OWNER_ID=8788049620           # tu user_id de Telegram (averigualo con @userinfobot)

# --- n8n ---
N8N_HOST=n8n.tu-dominio.com            # solo si vas a exponer n8n; si no, dejalo localhost
N8N_PROTOCOL=https
N8N_PORT=5678
WEBHOOK_URL=https://n8n.tu-dominio.com/

# --- OpenClaw ---
# (la mayoria de la config esta en openclaw/config/openclaw.json; ver paso 6)
```

Si no expones n8n publico, basta con `N8N_HOST=localhost`, `N8N_PROTOCOL=http`,
`WEBHOOK_URL=http://localhost:5678/`. OpenClaw lo llama internamente como
`http://tgs-n8n:5678` por la red Docker, no necesita el host publico.

---

## 5. Levantar los contenedores

```bash
docker compose up -d
docker compose ps        # los 3 servicios deben quedar healthy/Up
```

Esperado:

```
NAME           STATUS
tgs-crewai     Up (healthy)
tgs-n8n        Up
tgs-openclaw   Up (healthy)
```

Si algo falla:

```bash
docker compose logs --tail=100 <servicio>     # crewai | n8n | openclaw
```

---

## 6. Configurar OpenClaw (gateway del bot)

OpenClaw escribe su estado en `openclaw/config/` (mapeado al volumen del
contenedor `/home/node/.openclaw`). El archivo principal es
`openclaw/config/openclaw.json`. La primera vez se crea solo; debe quedar asi:

```json
{
  "gateway":  { "port": 18789, "mode": "local", "bind": "lan" },
  "agents":   {
    "defaults": {
      "model": { "primary": "anthropic/claude-haiku-4-5" },
      "workspace": "/app/workspace"
    }
  },
  "skills":   {
    "load": { "extraDirs": ["/app/workspace/tgs-skills"], "watch": true }
  },
  "commands": { "ownerAllowFrom": ["telegram:8788049620"] },
  "session":  { "reset": { "mode": "idle", "idleMinutes": 10 } },
  "cron":     { "enabled": false }
}
```

Notas:

- `commands.ownerAllowFrom`: pon TU `user_id` de Telegram aqui para que solo
  tu puedas usar los comandos privilegiados.
- `session.reset` (idle 10 min) y `cron.enabled=false` son **importantes**:
  limitan el gasto de tokens. Sin esto el agente acumula contexto y se vuelve
  caro (mas detalles en `docs/cost-control.md`).

### Permisos

OpenClaw escribe en `/home/node/.openclaw` como uid 1000:

```bash
sudo chown -R 1000:1000 openclaw/config
docker compose restart openclaw
```

### Verificar

```bash
docker compose logs --tail=20 openclaw | grep -E "ready|listening|telegram"
```

Debes ver `gateway ready` y `[telegram] [default] starting provider (@tu_bot)`.

---

## 7. Importar el workflow de n8n

Hay un solo workflow: `n8n/workflows/05-analyze-webhook.json`.

```bash
docker compose exec -T n8n n8n import:workflow --input=/repo/n8n/workflows/05-analyze-webhook.json
```

(Si `--input` no encuentra el archivo, copialo primero:
`docker compose cp n8n/workflows/05-analyze-webhook.json n8n:/tmp/wf.json` y
usa `--input=/tmp/wf.json`.)

Despues, en la UI de n8n (`http://localhost:5678` o tu host publico):

1. Abrir el workflow "Analysis Webhook".
2. Verificar que el nodo **Analyze** apunte a `http://tgs-crewai:8000/analyze`.
3. Pulsar el switch **Active** (esquina superior derecha).

Verificacion:

```bash
curl -X POST http://localhost:5678/webhook/tgs-analyze \
  -H 'content-type: application/json' \
  -d '{"input_type":"text","content":"Una panaderia vende pan al barrio."}'
```

Debe devolver `{"ok": true, "markdown": "...", "diagram_url": "..."}` en
~2-4 minutos.

---

## 8. (Opcional) Exponer n8n publico con nginx + Cloudflare

Solo necesario si quieres acceso remoto a la UI de n8n. Si vas a usar todo
local/SSH, salta este paso.

1. Apuntar `n8n.tu-dominio.com` a la IP del VPS (record A en Cloudflare,
   proxy desactivado para el primer emit del certificado).
2. Crear un sitio en nginx (ver `vps-proxy/sites/n8n.conf` como ejemplo) con
   el patron resolver + `proxy_pass $var` para evitar que un contenedor caido
   bloquee todo nginx.
3. Emitir el certificado con certbot/Cloudflare DNS-01.
4. Activar el proxy naranja de Cloudflare.

Referencia completa: <https://github.com/Gartner24/vps-proxy>.

---

## 9. Crear y conectar el canal de Telegram

1. En la app de Telegram, **New Channel** -> tipo **Public** -> username
   ej. `tgs_mapper_bot_channel`.
2. Agregar al bot (`@tgs_mapper_bot`) como **Administrator** del canal con
   permiso **Post Messages** activado.
3. Verificar desde el servidor:

   ```bash
   TOKEN=$(grep '^TELEGRAM_BOT_TOKEN=' .env | cut -d= -f2)
   curl -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
     -H 'content-type: application/json' \
     -d '{"chat_id":"@tgs_mapper_bot_channel","text":"setup ok"}'
   ```

   Si responde `"ok": true`, el `/publish` del bot funcionara.

Si el username del canal es distinto, edita
`openclaw/workspace/tgs-skills/tgs-publish/publish.mjs` y reemplaza la
constante `channel`.

---

## 10. Prueba end-to-end

Desde Telegram, abre el chat con `@tgs_mapper_bot` y envia:

```
Una panaderia tiene un horno, un mostrador y un cajero. Compra harina, hornea pan y lo vende a clientes del barrio.
```

Esperado:

1. Casi inmediato: "Procesando tu analisis bajo el marco TGS (tarda ~1-2 minutos)..."
2. ~3 minutos despues: bloque de texto con el analisis TGS completo.
3. Inmediatamente despues: imagen del diagrama Mermaid.
4. Envia `/publish` -> el bot responde "Publicado en el canal: https://t.me/tgs_mapper_bot_channel/N".
5. Abre el canal y verifica que aparezcan el texto y la imagen.

---

## 11. Solucion de problemas comunes

| Sintoma | Causa probable | Que hacer |
|---|---|---|
| El bot no responde nada | OpenClaw no esta dueno del bot (otro proceso lo robo) | `docker compose restart openclaw` y revisar `[telegram] starting provider` |
| "Hubo un problema tecnico con el backend" | n8n esta inactivo o el workflow no esta activado | Reactivar el workflow en la UI de n8n |
| Bot pide configurar personalidad u onboarding | Falta `AGENTS.md` / `SOUL.md` en el workspace | Verificar `openclaw/workspace/AGENTS.md` y `SOUL.md` existen y reiniciar OpenClaw |
| `/publish` dice "no se pudo publicar: Bad Request: chat not found" | El bot no es admin del canal | Anadirlo como administrador con "Post Messages" |
| Anthropic devuelve "compiled grammar too large" | CrewAI esta usando el provider nativo de Anthropic | Verificar `crew/config/llm.py` usa `is_litellm=True` |
| Anthropic devuelve "credit balance is too low" | Sin creditos | Recargar en https://console.anthropic.com/. Considera un spend limit. |
| Mucho gasto sin uso visible | OpenClaw esta acumulando contexto | Asegurarse que `session.reset.mode=idle` esta en `openclaw.json`, ver `docs/cost-control.md` |

---

## 12. Comandos rapidos

```bash
# Levantar y tumbar todo
docker compose up -d
docker compose down

# Logs en vivo
docker compose logs -f openclaw
docker compose logs -f n8n
docker compose logs -f crewai

# Estado
docker compose ps

# Reiniciar solo un servicio
docker compose restart openclaw

# Health del backend
curl http://localhost:8000/health
```

Para todos los comandos del dia a dia (demos, debugging, despublicar) ver
[`demo-commands.md`](demo-commands.md).
