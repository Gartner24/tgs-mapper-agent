// Calls the n8n analysis webhook and prints the response as JSON.
// Reads the user content from /tmp/tgs-analyze.txt to avoid argv escaping.

import fs from 'node:fs';

const inputPath = '/tmp/tgs-analyze.txt';
const url = 'http://tgs-n8n:5678/webhook/tgs-analyze';

if (!fs.existsSync(inputPath)) {
  console.log(JSON.stringify({ ok: false, error: `Missing ${inputPath}` }));
  process.exit(1);
}

const content = fs.readFileSync(inputPath, 'utf8').trim();
if (!content) {
  console.log(JSON.stringify({ ok: false, error: 'Empty content' }));
  process.exit(1);
}

try {
  const r = await fetch(url, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ input_type: 'text', content, user_id: 'tg' }),
  });
  const text = await r.text();
  try {
    const j = JSON.parse(text);
    console.log(JSON.stringify(j));
  } catch {
    console.log(JSON.stringify({ ok: false, error: 'Backend returned non-JSON', body: text.slice(0, 500) }));
  }
} catch (e) {
  console.log(JSON.stringify({ ok: false, error: String(e) }));
  process.exit(1);
}
