# Proxy integration

The TGS Mapper Agent runs behind the centralized VPS reverse proxy
(repo: github.com/Gartner24/vps-proxy). This folder is version-controlled
in the project repo; on deploy the operator copies the vhost file manually.

## Prerequisites

- DNS record: `n8n.qyvos.com` -> VPS IP (Cloudflare, proxied or DNS-only)
- External Docker network `web` already created:
  `docker network create web` (usually done once during VPS setup)
- The proxy stack is running at `/opt/projects/proxy/`

## Install vhost on the VPS

From the project folder on the VPS (`/opt/projects/tgs-mapper-agent/`):

```bash
sudo cp deploy/proxy/n8n.qyvos.com.conf \
  /opt/projects/proxy/conf.d/active/
```

## Issue TLS certificate (first deploy only)

```bash
cd /opt/projects/proxy
docker compose exec certbot certbot certonly \
  --dns-cloudflare \
  --dns-cloudflare-credentials /run/secrets/cloudflare.ini \
  -d n8n.qyvos.com
```

## Reload the proxy

```bash
docker compose -f /opt/projects/proxy/compose.yml exec nginx nginx -s reload
```

The Nginx container watches `conf.d/` with inotify and reloads automatically
on file changes, but an explicit reload is safer after a first install.

## Network topology

```
Internet -> nginx-proxy (ports 80/443, network: web)
                |
         tgs-n8n:5678  (network: web, no host port)
                |
        tgs-crewai:8000 (network: web, no host port, internal only)
```

The CrewAI service has no public vhost in the MVP. n8n reaches it at
`http://tgs-crewai:8000` over the shared `web` Docker network.

## Telegram webhook

Once TLS is live, register the webhook with Telegram:

```bash
curl "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  -d "url=https://n8n.qyvos.com/webhook/telegram"
```

n8n creates the `/webhook/telegram` path automatically when the
Telegram Trigger workflow is activated.
