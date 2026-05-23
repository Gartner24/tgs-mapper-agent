# n8n Workflows

Two workflows handle the Telegram integration and Reddit publishing.

## Import

1. Open the n8n UI at `https://n8n.qyvos.com`
2. Go to **Workflows** -> **Import from file**
3. Import `workflows/01-telegram-to-crew.json`
4. Import `workflows/02-openclaw-publish-reddit.json`

## Post-import configuration (required)

### 1. Telegram credential

In n8n go to **Credentials** -> **New** -> **Telegram API**.
Enter your bot token. Name it exactly `Telegram Bot`.
Then open each workflow and assign this credential to every Telegram node.

### 2. Environment variables in n8n

The workflows read these from the container environment (set in `.env`):

| Variable | Used in |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Get File + Download File HTTP nodes |
| `OPENCLAW_URL` | Publish to Reddit HTTP node |
| `OPENCLAW_API_KEY` | Publish to Reddit HTTP node |
| `REDDIT_TARGET` | Publish to Reddit HTTP node |
| `REDDIT_CLIENT_ID` | Publish to Reddit HTTP node |
| `REDDIT_CLIENT_SECRET` | Publish to Reddit HTTP node |
| `REDDIT_USERNAME` | Publish to Reddit HTTP node |
| `REDDIT_PASSWORD` | Publish to Reddit HTTP node |

n8n exposes container env vars via `$env.VARIABLE_NAME` in expressions.
Ensure these are all set in `.env` before starting the stack.

### 3. Activate both workflows

After configuring credentials, toggle each workflow to **Active**.
n8n will register the Telegram webhook automatically.

Then set the webhook on Telegram's side:

```bash
curl "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  -d "url=https://n8n.qyvos.com/webhook/telegram"
```

## Workflow 01 — Telegram to CrewAI

```
Telegram Trigger
  -> Skip /publish (IF: ignore /publish commands)
  -> Detect Type (Code: text / url / pdf / image)
  -> Needs Download (IF)
       TRUE  -> Get Telegram File -> Download File -> To Base64 -> Analyze Binary
       FALSE -> Analyze Text
  -> Format and Store (Code: format markdown, encode mermaid.ink URL, save to staticData by chat_id)
  -> Send Analysis (Telegram: markdown text)
  -> Send Diagram (Telegram: mermaid.ink PNG)
```

**Timeout:** `/analyze` is called with a 120s timeout. CrewAI LLM calls can take
15-60s depending on the model and input size.

**Diagram rendering:** Uses `https://mermaid.ink/img/<base64url>` — no local
Mermaid install needed.

## Workflow 02 — OpenClaw Publish Reddit

```
Telegram Trigger
  -> Is /publish (IF: only /publish commands)
  -> Retrieve Analysis (Code: reads staticData[chat_id])
  -> Has Analysis (IF)
       FALSE -> No Analysis Message (Telegram)
       TRUE  -> Publish to Reddit (HTTP: OpenClaw)
             -> Confirm Publication (Telegram: post URL)
```

**staticData:** n8n persists `$workflow.staticData` across executions of the
same workflow. Workflow 01 writes to it; Workflow 02 reads from it.
Both workflows must be in the same n8n instance for this to work.

## Notes

- The OpenClaw HTTP node body includes Reddit credentials inline.
  If your OpenClaw instance handles credentials differently, edit that node.
- `REPLACE_WITH_CREDENTIAL_ID` and `REPLACE_WITH_INSTANCE_ID` in the JSON
  are replaced automatically when you import and configure credentials in n8n.
