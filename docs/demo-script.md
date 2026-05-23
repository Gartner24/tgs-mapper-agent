# Guion de Demo — TGS Mapper Agent

**Curso:** Teoria General de Sistemas — UTP
**Duracion estimada:** 10-15 minutos
**Audiencia:** Profesor y grupo de clase

---

## Antes de empezar (checklist tecnico)

- [ ] `docker compose up -d` corriendo en el VPS
- [ ] `curl http://tgs-crewai:8000/health` devuelve `{ok: true}`
- [ ] Los dos workflows de n8n estan activos
- [ ] El webhook de Telegram esta registrado
- [ ] Tener el chat de Telegram abierto en pantalla
- [ ] Tener `frontend/index.html` abierto en el navegador como alternativa
- [ ] Tener este documento en otra pantalla como referencia

---

## 1. Introduccion (2 min)

> "Buenos dias/tardes. Vamos a presentar el **TGS Mapper Agent**: un sistema
> multiagente que analiza cualquier input bajo el marco de la Teoria General
> de Sistemas y devuelve un analisis estructurado con diagrama."

**Puntos clave a mencionar:**
- El sistema recibe texto, PDFs, imagenes o URLs via Telegram
- Internamente usa 4 agentes de inteligencia artificial con roles distintos
- El output es un JSON estructurado con todos los conceptos de TGS: frontera,
  subsistemas, relaciones, acoplamientos, retroalimentacion, etc.
- El sistema es en si mismo un ejemplo de los conceptos que analiza

---

## 2. Arquitectura rapida (2 min)

Mostrar el diagrama en `docs/architecture.md` o dibujar en el tablero:

```
Usuario -> Telegram -> n8n -> CrewAI -> 4 agentes -> respuesta
```

> "La arquitectura tiene dos capas: n8n actua como orquestador externo
> (recibe el mensaje de Telegram y envia la respuesta), y CrewAI es el
> cerebro multiagente que hace el analisis."

**Los 4 agentes como subsistemas TGS:**
- Extractor = sensor (transforma el input en datos)
- Analista TGS = procesador (aplica el marco)
- Diagramador = transductor de salida (genera el diagrama)
- Manager = control/retroalimentacion (valida y corrige)

> "El Manager es el mecanismo homeostasico del sistema: detecta
> inconsistencias y las corrige directamente antes de entregar el resultado."

---

## 3. Demo en vivo — Caso 1: texto (3 min)

Enviar al bot de Telegram:

```
Una empresa de logistica tiene un gerente general, un area de operaciones
que coordina los camiones y conductores, un area de finanzas que maneja
la facturacion, y un area de tecnologia que mantiene el sistema de rastreo
GPS. Los clientes generan pedidos y los conductores los entregan. El
gobierno regula el transporte de carga.
```

**Mientras espera (2-4 min):**
> "El sistema esta procesando. Los 4 agentes corren en secuencia: primero el
> Extractor identifica los conceptos clave, luego el Analista aplica TGS, el
> Diagramador genera el codigo Mermaid, y finalmente el Manager valida que todo
> sea coherente y ensambla el JSON final."

**Cuando llega la respuesta, senalar:**
- El tipo de sistema identificado (abierto, sociotecnico...)
- Los subsistemas vs elementos
- Los tipos de acoplamiento en las relaciones
- La frontera (que esta dentro y fuera)
- El diagrama Mermaid renderizado como imagen

---

## 4. Demo en vivo — Caso 2: URL (2 min)

Enviar al bot una URL de Wikipedia o un articulo tecnico relevante para el
curso. Por ejemplo, el articulo de Wikipedia sobre "General Systems Theory".

> "Ahora le damos una URL. El agente Extractor usa su herramienta de fetch
> para obtener el contenido de la pagina, lo limpia, y lo pasa al Analista."

---

## 5. Publicar en Reddit (1 min)

Despues de recibir el analisis del caso 1 o 2, enviar:

```
/publish
```

> "Con el comando /publish, el sistema toma el ultimo analisis guardado
> y lo publica en Reddit a traves de OpenClaw. El analisis queda disponible
> publicamente con el diagrama incluido."

Mostrar la URL de Reddit que devuelve el bot.

---

## 6. Frontend alternativo (1 min, si aplica)

Si hay problemas con Telegram o para mostrar el JSON completo:

Abrir `frontend/index.html` en el navegador, pegar el mismo texto del
caso 1, hacer clic en "Analizar".

> "Tambien tenemos un frontend web alternativo para demos sin Telegram.
> Muestra el diagrama renderizado, el markdown y el JSON completo con
> todos los campos del esquema TGSAnalysis."

---

## 7. El sistema se analiza a si mismo (2 min)

Mostrar `docs/tgs-analysis-of-itself.md` o enviarlo al bot como texto.

> "El punto mas interesante: el propio sistema es un ejemplo de TGS.
> Cada agente es un subsistema. El Manager implementa retroalimentacion
> negativa. El sistema es abierto, estocastico y complejo."

Puntos para discusion con el profesor:
- Por que clasificamos el LLM como parte del entorno y no del sistema?
- Por que el Manager usa retroalimentacion negativa y no positiva?
- Que pasaria si se agrega memoria persistente? Cambiaria la clasificacion?

---

## 8. Cierre (1 min)

> "En resumen: construimos un sistema que aplica TGS a cualquier dominio,
> y que a su vez demuestra los conceptos de TGS en su propia arquitectura.
> El codigo esta disponible en GitHub. Gracias."

**Links utiles para el profesor:**
- Repositorio: `github.com/Gartner24/tgs-mapper-agent`
- Demo en vivo: `https://n8n.qyvos.com` (con credenciales)
- Analisis del sistema: `docs/tgs-analysis-of-itself.md`

---

## Plan B (si algo falla)

| Problema | Solucion |
|---|---|
| Bot no responde | Usar `frontend/index.html` apuntando a `localhost:8000` |
| CrewAI tarda mucho | Mostrar `examples/output-sample.json` como resultado esperado |
| Docker no levanta | Mostrar el codigo fuente y explicar la arquitectura con el diagrama |
| Sin internet | Tener el output de ejemplo listo en pantalla |
