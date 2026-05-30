// Robust publisher for tgs-publish skill.
// Reads /tmp/tgs-publish.txt (analysis markdown) and /tmp/tgs-publish.url (diagram URL).
// Posts both to the Telegram channel @tgs_mapper_bot_channel using TELEGRAM_BOT_TOKEN.

import fs from 'node:fs';

const token = process.env.TELEGRAM_BOT_TOKEN;
const channel = '@tgs_mapper_bot_channel';

if (!token) {
  console.log(JSON.stringify({ ok: false, error: 'TELEGRAM_BOT_TOKEN not set' }));
  process.exit(1);
}

const text = fs.existsSync('/tmp/tgs-publish.txt')
  ? fs.readFileSync('/tmp/tgs-publish.txt', 'utf8').trim()
  : '';
const imgUrl = fs.existsSync('/tmp/tgs-publish.url')
  ? fs.readFileSync('/tmp/tgs-publish.url', 'utf8').trim()
  : '';

if (!text) {
  console.log(JSON.stringify({ ok: false, error: 'No analysis text at /tmp/tgs-publish.txt' }));
  process.exit(1);
}

const TG_LIMIT = 4096;
const safeText =
  text.length > TG_LIMIT - 100
    ? text.slice(0, TG_LIMIT - 100) + '\n\n...(continua en el chat)'
    : text;

async function tg(method, body) {
  const r = await fetch(`https://api.telegram.org/bot${token}/${method}`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
  return r.json();
}

(async () => {
  const msg = await tg('sendMessage', { chat_id: channel, text: safeText });
  let img = { ok: true };
  if (imgUrl) {
    img = await tg('sendPhoto', {
      chat_id: channel,
      photo: imgUrl,
      caption: 'Diagrama del sistema analizado',
    });
  }
  const link =
    msg.ok && msg.result && msg.result.message_id
      ? `https://t.me/tgs_mapper_bot_channel/${msg.result.message_id}`
      : 'https://t.me/tgs_mapper_bot_channel';
  console.log(
    JSON.stringify({
      ok: msg.ok && img.ok,
      msg_ok: msg.ok,
      msg_error: msg.description,
      img_ok: img.ok,
      img_error: img.description,
      link,
    }),
  );
})().catch((e) => {
  console.log(JSON.stringify({ ok: false, error: String(e) }));
  process.exit(1);
});
