# TGS Mapper - Fuente de contenido para diapositivas (NotebookLM)

> Este documento es la **fuente unica** para generar las diapositivas de la
> presentacion del proyecto. Esta escrito en bloques tipo diapositiva: cada
> seccion `## Diapositiva N` corresponde a una lamina. Los puntos clave son
> los bullets; el resto es contexto para que NotebookLM lo use al redactar.
>
> **Presentador:** Santiago Valencia Leon
> **Materia:** Teoria General de Sistemas
> **Programa:** Ingenieria de Sistemas y Computacion, UTP
> **Duracion objetivo:** 8-10 minutos
> **Tono:** Tecnico-academico, claro, sin jerga innecesaria.

---

## Diapositiva 1 - Portada

- Titulo: **TGS Mapper Agent**
- Subtitulo: Un sistema multi-agente que aplica la Teoria General de Sistemas
  a cualquier idea que el usuario le envie por Telegram.
- Presentador: Santiago Valencia Leon
- Materia: Teoria General de Sistemas
- Programa: Ingenieria de Sistemas y Computacion, UTP

---

## Diapositiva 2 - ¿Que problema resuelve?

- La TGS es poderosa para analizar cualquier dominio pero su aplicacion manual
  es tediosa: identificar frontera, entorno, subsistemas, retroalimentacion,
  diagramar, etc.
- Idea del proyecto: **automatizar ese analisis** con una pipeline de
  agentes especializados que produzcan, ante cualquier entrada en lenguaje
  natural, un analisis TGS formal y un diagrama listo para revisar.
- Hipotesis academica: el sistema mismo es un ejemplo de TGS (cada componente
  es un subsistema con frontera, entradas, salidas y retroalimentacion).

---

## Diapositiva 3 - Objetivo del proyecto

- **Objetivo general:** construir un agente conversacional accesible por
  Telegram que entregue un analisis TGS formal de cualquier sistema descrito
  en lenguaje natural, junto con un diagrama del sistema analizado.
- **Objetivos especificos:**
  - Aplicar TGS al diseno mismo del software (auto-referencia didactica).
  - Demostrar el uso de multi-agente (CrewAI) con un proceso secuencial.
  - Integrar un canal real de usuario (Telegram) con un backend distribuido.
  - Mantener el stack autocontenible y reproducible (Docker Compose).

---

## Diapositiva 4 - El sistema en una frase

> "El usuario envia un texto al bot. El bot pide a un equipo de 4 agentes que
> analicen el texto bajo la Teoria General de Sistemas y devuelve el analisis
> escrito y un diagrama."

- El usuario interactua solo por Telegram (un canal natural y movil).
- Detras: 3 servicios coordinados (gateway conversacional, orquestador, motor
  de analisis) corriendo en Docker en un VPS.
- Modelo de lenguaje: Claude Haiku 4.5 via Anthropic (integrado por litellm).

---

## Diapositiva 5 - Arquitectura general (3 capas)

- **Capa de interaccion (OpenClaw):** dueno del bot de Telegram, decide cuando
  invocar el backend y cuando responder con conocimiento propio (preguntas de
  seguimiento). Equivalente al subsistema de **entrada y dialogo**.
- **Capa de orquestacion (n8n):** workflow low-code que recibe la peticion de
  OpenClaw, llama al motor de analisis, arma la URL del diagrama y devuelve el
  resultado. Equivalente al subsistema de **coordinacion**.
- **Capa de procesamiento (CrewAI):** 4 agentes especializados que producen
  el analisis TGS formal. Equivalente al subsistema de **procesamiento**.
- Todo orquestado por Docker Compose. Frente publico: nginx + Cloudflare TLS.

---

## Diapositiva 6 - Los 4 agentes (CrewAI)

- Proceso `sequential`: cada agente recibe el output del anterior.
- **Extractor** - lee el texto del usuario y extrae tema, conceptos y
  relaciones. Es el "sensor" del sistema.
- **Analista TGS** - aplica el marco completo: frontera, entorno,
  suprasistema, subsistemas, elementos, acoplamientos, E/P/S, retroalimentacion,
  estados, tipo y complejidad. Es el "procesador".
- **Diagramador** - convierte el analisis en codigo **Mermaid** listo para
  renderizar. Es la "salida" visual.
- **Manager** - valida coherencia y arma el JSON final segun el esquema
  Pydantic `TGSAnalysis`. Es el subsistema de **control / retroalimentacion**.

---

## Diapositiva 7 - El flujo paso a paso

1. Usuario escribe un texto en `@tgs_mapper_bot`.
2. OpenClaw recibe el mensaje (polling Telegram). Decide: "esto es contenido
   para analizar".
3. OpenClaw ejecuta la skill **tgs-analyze**: escribe el texto a un archivo
   temporal y lanza `node analyze.mjs`.
4. `analyze.mjs` hace POST a `http://tgs-n8n:5678/webhook/tgs-analyze`.
5. n8n recibe la peticion (workflow "Analysis Webhook") y la pasa a CrewAI:
   `POST http://tgs-crewai:8000/analyze`.
6. CrewAI corre los 4 agentes (~2-4 minutos).
7. n8n codifica el codigo Mermaid en base64url y arma la URL del diagrama con
   `mermaid.ink`. Devuelve `{ ok, markdown, diagram_url }`.
8. OpenClaw envia al usuario el markdown como texto y el diagrama como imagen.
9. Si el usuario envia `/publish`, OpenClaw lanza la skill **tgs-publish** que
   replica texto + imagen al canal `@tgs_mapper_bot_channel`.

---

## Diapositiva 8 - El proyecto como un sistema TGS (auto-referencia)

| Subsistema TGS | Componente del proyecto |
|---|---|
| Interfaz / dialogo (entrada-salida) | OpenClaw + Telegram |
| Coordinacion | n8n |
| Procesamiento | CrewAI (4 agentes en secuencia) |
| Control / retroalimentacion | Agente Manager (validacion Pydantic) |
| Transductor de salida | mermaid.ink (codigo -> imagen) |
| Frontera | Red Docker (`tgs-*`) y el VPS |
| Entorno | Usuarios, Telegram, internet, proveedor LLM (Anthropic) |
| Suprasistema | La nube y los servicios externos |

- Eligimos a proposito esta estructura: el proyecto **es un ejemplo vivo de
  TGS**. Al mostrar como funciona, mostramos TGS aplicada.

---

## Diapositiva 9 - Stack y herramientas

- **Docker Compose** - orquesta los 3 servicios; un solo `up -d` levanta todo.
- **OpenClaw** (Node.js) - gateway de agente con sistema de "skills"
  (instrucciones en archivos `SKILL.md`) y dueno de los canales (Telegram).
- **n8n** - orquestador low-code, expone un webhook HTTP que OpenClaw consume.
- **CrewAI** (Python + FastAPI) - framework multi-agente; expone `/analyze` y
  `/health`. Devuelve estructura validada por Pydantic v2.
- **litellm** - capa que abstrae al proveedor LLM (usado para evitar la
  validacion estricta del proveedor nativo de Anthropic en CrewAI).
- **mermaid.ink** - servicio publico que renderiza diagramas Mermaid a PNG.
- **nginx + certbot + Cloudflare** - proxy publico y TLS para n8n.
- **Telegram Bot API** - canal con el usuario; un bot y un canal publico de
  Telegram para publicaciones.

---

## Diapositiva 10 - El modelo de lenguaje

- Proveedor seleccionado: **Anthropic Claude Haiku 4.5**.
- Integracion en CrewAI: forzada por **litellm** (`is_litellm=True`) porque el
  proveedor nativo de Anthropic en CrewAI compila los esquemas Pydantic
  grandes a una gramatica que el servicio rechaza ("compiled grammar too
  large").
- Razon de la eleccion: en el ciclo de desarrollo nos quedamos sin creditos
  en OpenRouter (DeepSeek) y Groq tenia un rate limit de tokens-por-minuto
  insuficiente para una pipeline de 4 agentes. Anthropic ofrecia creditos
  inmediatos.
- Multi-proveedor: el codigo soporta cambiar el proveedor por variable de
  entorno (`LLM_PROVIDER=anthropic|openrouter|groq`).

---

## Diapositiva 11 - Servidor y despliegue

- VPS Linux (Ubuntu 22.04+, 2 vCPU, 4 GB RAM).
- 3 contenedores principales: `tgs-openclaw`, `tgs-n8n`, `tgs-crewai`.
- Proxy: `nginx-proxy` + `certbot` en otra red Docker; expone
  `n8n.qyvos.com` con TLS de Cloudflare DNS-01.
- Dominio publico solo para la UI de n8n; el bot y CrewAI no necesitan estar
  expuestos.
- Persistencia: volumenes Docker (`n8n_data/`, `openclaw/config/`).
- Setup completo desde cero: ~30-45 minutos siguiendo `docs/setup-guide.md`.

---

## Diapositiva 12 - Interfaz con el usuario

- **Bot:** `@tgs_mapper_bot` en Telegram. Cualquier persona puede escribirle.
- **Canal:** `@tgs_mapper_bot_channel` para publicar analisis aprobados.
- **Comandos relevantes:**
  - Cualquier texto -> dispara un analisis TGS completo.
  - `/publish` -> publica el ultimo analisis en el canal.
  - `/reset` -> limpia el contexto de la conversacion.
- **Tiempo de respuesta tipico:** ~3-4 minutos por analisis (los 4 agentes
  corren en secuencia).
- **Forma de entrega:** mensaje de texto con el analisis estructurado +
  imagen del diagrama Mermaid renderizado.

---

## Diapositiva 13 - Decisiones de diseno relevantes

- **Proceso secuencial (no jerarquico) en CrewAI:** el modo `hierarchical`
  introducia el doble de latencia. Sequencial: 1 agente a la vez, salida del
  anterior es entrada del siguiente. Manager queda al final como validador.
- **OpenClaw es dueno del bot (no n8n):** version inicial el bot vivia dentro
  de n8n; se pivotó para que OpenClaw lo controlara y pudiera mantener
  conversacion natural (preguntas de seguimiento, /publish).
- **Skills por archivo, no `node -e`:** el sandbox de OpenClaw bloquea
  inline-eval (`strictInlineEval`); los scripts viven en `tgs-skills/*.mjs`.
- **Cache de sesion con reset por idle:** sin esto, OpenClaw acumula contexto
  y cada turno reescribe ~1M tokens de cache (caro). Con `idleMinutes=10` la
  sesion se limpia y el costo cae drasticamente.
- **Manager como control TGS:** dentro del propio framework TGS, el Manager
  representa el subsistema de retroalimentacion: detecta inconsistencias y
  corrige antes de entregar al usuario.

---

## Diapositiva 14 - Demo en vivo (storyboard)

1. Mostrar `docker compose ps` con los 3 servicios en verde.
2. Abrir el chat con `@tgs_mapper_bot` desde el celular.
3. Enviar: "Una panaderia tiene un horno, un mostrador y un cajero. Compra
   harina, hornea pan y lo vende a clientes del barrio."
4. Bot responde "Procesando..."
5. Mientras corre, mostrar logs en vivo: `docker compose logs -f crewai`.
6. ~3 minutos despues: bot envia el analisis formateado.
7. Inmediatamente despues: bot envia el diagrama como imagen.
8. Enviar `/publish`. Bot confirma con enlace al canal.
9. Abrir el canal `@tgs_mapper_bot_channel`: el analisis y el diagrama
   aparecen publicados.

---

## Diapositiva 15 - Aprendizajes y limites

- **Aprendizajes:**
  - Disenar pensando "el software es un sistema TGS" alinea de forma natural
    componentes con conceptos teoricos.
  - Multi-agente secuencial es predecible y mas barato que jerarquico.
  - La integracion Telegram -> OpenClaw -> n8n -> CrewAI demuestra como un
    canal natural puede esconder una pipeline tecnica.
- **Limites:**
  - Tiempo de respuesta (3-4 min) restringe el uso a analisis on-demand,
    no a chat fluido.
  - Costo: cada analisis consume tokens del LLM; el caching de OpenClaw fue
    clave para no agotar creditos.
  - Calidad del analisis depende del modelo; Haiku 4.5 es economico y rapido
    pero no equivalente a un experto humano.
- **Posibles extensiones:** soporte de PDF/imagen como entrada (los agentes
  ya tienen herramientas listas), publicacion en otros canales, modo grupal
  en Telegram.

---

## Diapositiva 16 - Cierre

- **TGS Mapper Agent** es un puente entre Teoria General de Sistemas y
  practica de ingenieria multi-agente.
- Convertimos un usuario casual escribiendo en Telegram en el iniciador de
  una pipeline de 4 agentes que produce TGS formal y diagramada.
- El propio software es un sistema TGS: dialogo (entrada), coordinacion
  (proceso), procesamiento (transformacion), control (retroalimentacion).
- **Repositorio:** github.com/Gartner24/tgs-mapper-agent
- **Bot:** t.me/tgs_mapper_bot
- **Canal:** t.me/tgs_mapper_bot_channel
- **Presentador:** Santiago Valencia Leon - Ingenieria de Sistemas y
  Computacion, UTP - Teoria General de Sistemas.
