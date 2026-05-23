---
name: tgs-publish
description: "Publica el ultimo analisis TGS entregado en el canal de Telegram. Usar SOLO cuando el usuario envie el comando /publish."
---

# Publicar analisis en el canal

Cuando el usuario envie el comando **/publish**, publica el ULTIMO analisis TGS
que entregaste en esta conversacion (su texto y su diagrama) en el canal de
Telegram **@tgs_mapper_bot_channel**.

## Procedimiento

1. Si en la conversacion NO hay un analisis TGS previo entregado por el backend,
   responde: "Primero pideme un analisis y luego usa /publish para publicarlo."
   y termina.
2. Si si hay analisis, toma su texto (el `markdown`) y la URL del diagrama
   (`diagram_url`). Publica usando tu herramienta de shell/exec con node y el
   token del bot (variable de entorno `TELEGRAM_BOT_TOKEN`):

   ```bash
   node -e "const t=process.env.TELEGRAM_BOT_TOKEN; const ch='@tgs_mapper_bot_channel'; const text=process.argv[1]; const img=process.argv[2]||''; (async()=>{ const a=await (await fetch('https://api.telegram.org/bot'+t+'/sendMessage',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({chat_id:ch,text})})).json(); let b={ok:true}; if(img){ b=await (await fetch('https://api.telegram.org/bot'+t+'/sendPhoto',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({chat_id:ch,photo:img,caption:'Diagrama del sistema analizado'})})).json(); } console.log(JSON.stringify({msg:a.ok,img:b.ok,id:a.result&&a.result.message_id})); })().catch(e=>console.log(JSON.stringify({ok:false,error:String(e)})));" "TEXTO_DEL_ANALISIS_AQUI" "DIAGRAM_URL_AQUI"
   ```

3. Si la publicacion fue exitosa, confirma al usuario con el enlace
   `https://t.me/tgs_mapper_bot_channel`. Si fallo, avisale del error.

## Reglas
- Solo publica el analisis mas reciente; no inventes contenido nuevo.
- Responde en espanol (Colombia).
- Usa exec con node (no la herramienta web_fetch).
