# Analisis TGS del TGS Mapper Agent

> Este documento aplica el marco de la Teoria General de Sistemas (TGS)
> al propio sistema que construimos. Es a la vez producto y demostracion
> del agente.

---

## 1. Sistema

**Nombre:** TGS Mapper Agent
**Tema:** Sistema multiagente de analisis bajo TGS
**Proposito:** Recibir cualquier input (texto, PDF, imagen, URL) y devolver
un analisis estructurado bajo el marco de la TGS, incluyendo un diagrama
Mermaid del sistema identificado. Permite ademas publicar el analisis en Reddit.

---

## 2. Tipo de sistema

| Dimension | Clasificacion | Justificacion |
|---|---|---|
| Abierto / cerrado | **Abierto** | Intercambia informacion con el usuario, Telegram, OpenRouter y Reddit |
| Natural / artificial | **Artificial (sociotecnico)** | Construido por humanos; combina codigo, modelos de lenguaje y protocolos de comunicacion |
| Deterministico / estocastico | **Estocastico** | El LLM produce outputs probabilisticos; el mismo input puede generar analisis ligeramente distintos |
| Continuo / discreto | **Discreto** | Procesa un mensaje a la vez; los estados cambian en eventos discretos (recepcion, analisis, respuesta) |

---

## 3. Frontera

**Descripcion:** La frontera del sistema es el perimetro del stack de software
bajo nuestro control: los contenedores Docker `tgs-n8n` y `tgs-crewai`,
sus procesos internos y la logica de los 4 agentes.

| Dentro de la frontera | Fuera de la frontera |
|---|---|
| Orquestador n8n | Telegram Bot API |
| FastAPI + CrewAI | OpenRouter / DeepSeek V4 |
| Los 4 agentes | Reddit / OpenClaw |
| Esquemas Pydantic | El usuario final |
| Workflows n8n | La red Docker `web` y el proxy Nginx |

---

## 4. Entorno

**Descripcion:** El entorno esta compuesto por los servicios externos con los
que el sistema interactua sin controlarlos directamente.

**Variables externas:**
- Disponibilidad de la API de OpenRouter (latencia, rate limits, costo)
- Politicas de la API de Telegram (tamano maximo de archivo, tipos de media)
- Disponibilidad de Reddit y restricciones de la API
- Disponibilidad de la instancia OpenClaw en el VPS
- Calidad del input del usuario (inputs ambiguos producen analisis con mas supuestos)

---

## 5. Suprasistema

El TGS Mapper Agent es un subsistema del **ecosistema de herramientas academicas
del curso de Teoria General de Sistemas (TGS) de la Universidad Tecnologica de
Pereira (UTP)**. A nivel tecnico, pertenece al ecosistema de proyectos del VPS
`qyvos.com`, coordinado por el proxy Nginx centralizado.

---

## 6. Elementos

| Elemento | Rol |
|---|---|
| `tgs-n8n` | Orquestador externo; recibe, enruta y responde mensajes |
| `tgs-crewai` | Servidor de agentes; expone el endpoint `/analyze` |
| Agente Extractor | Sensor; convierte el input crudo en datos procesables |
| Agente Analista TGS | Procesador central; aplica el marco TGS |
| Agente Diagramador | Transductor de salida; convierte el analisis en codigo Mermaid |
| Agente Manager | Control y retroalimentacion; valida coherencia y ensambla el JSON final |
| Esquemas Pydantic | Contratos de datos internos; garantizan la coherencia entre agentes |
| LLM (DeepSeek V4) | Motor de razonamiento compartido por los 4 agentes |
| OpenRouter | Adaptador de protocolo hacia el LLM |

---

## 7. Subsistemas

### Subsistema 1 — Extractor (Sensor / entrada)
**Proposito:** Convertir la realidad externa (texto, binario, URL) en datos
internos procesables por el sistema.
**TGS:** Es el subsistema de entrada; transforma las perturbaciones del entorno
en senales internas. Sin el, el sistema no puede recibir informacion del exterior.
**Elementos clave:** `agents/extractor.py`, `tools/pdf_reader.py`,
`tools/image_reader.py`, `tools/url_fetcher.py`

### Subsistema 2 — Analista TGS (Procesador / nucleo)
**Proposito:** Aplicar el marco completo de TGS al contenido extraido.
**TGS:** Es el subsistema de procesamiento central; aqui ocurre el comportamiento
emergente del sistema (el analisis que ningun agente podria producir solo).
**Elementos clave:** `agents/analista_tgs.py`, `tasks/analysis.py`,
`schemas/tgs_output.py`

### Subsistema 3 — Diagramador (Salida / transduccion)
**Proposito:** Convertir el analisis interno en una representacion visual
(codigo Mermaid) comprensible para el usuario.
**TGS:** Es el subsistema de salida; transforma la informacion interna en una
forma que el entorno (el usuario) puede consumir.
**Elementos clave:** `agents/diagramador.py`, `tasks/diagram.py`,
`schemas/diagram.py`

### Subsistema 4 — Manager (Control / retroalimentacion)
**Proposito:** Coordinar los otros 3 agentes, detectar inconsistencias,
solicitar correcciones y producir el JSON final integrado.
**TGS:** Es el subsistema de control; implementa retroalimentacion negativa
(detecta desviaciones respecto al proposito y activa correcciones). Es el
mecanismo homeostasico del sistema.
**Elementos clave:** `agents/manager.py`, `tasks/coordination.py`

---

## 8. Relaciones y acoplamientos

| Origen | Destino | Tipo | Justificacion |
|---|---|---|---|
| Manager | Extractor | Fuerte | El Manager depende directamente del output del Extractor para iniciar el analisis |
| Manager | Analista TGS | Fuerte | El analisis TGS es el producto central; sin el, no hay sistema |
| Manager | Diagramador | Debil | Si el diagrama falla, el analisis textual sigue siendo util |
| Extractor | Analista TGS | Secuencial | El Analista no puede operar sin el output previo del Extractor |
| Analista TGS | Diagramador | Secuencial | El Diagramador necesita el analisis completo antes de generar el diagrama |
| Manager | todos | Reciproco | El Manager puede re-delegar a cualquier agente si detecta inconsistencias |

---

## 9. Caja negra

**Entradas:**
- Input del usuario (texto, PDF en base64, imagen en base64, URL)
- Credenciales de API (OPENROUTER_API_KEY, TELEGRAM_BOT_TOKEN)

**Procesos:**
- Extraccion y comprension del contenido
- Analisis bajo el marco TGS
- Generacion del diagrama Mermaid
- Validacion de coherencia y ensamblaje del JSON final
- Formateo y envio de la respuesta

**Salidas:**
- Analisis TGS estructurado (JSON `TGSAnalysis`)
- Texto markdown con el analisis (para Telegram)
- Diagrama Mermaid renderizado (imagen PNG via mermaid.ink)
- Post en Reddit (cuando el usuario envia `/publish`)

---

## 10. Retroalimentacion

### Retroalimentacion negativa (principal)
El **Manager** revisa los outputs del Extractor, Analista y Diagramador. Si
detecta inconsistencias (subsistema en el diagrama que no existe en el analisis,
relaciones con nodos inexistentes), re-delega al agente correspondiente para
correccion. Este es el mecanismo homeostasico que mantiene la coherencia del
output del sistema.

### Retroalimentacion negativa (usuario)
Si el usuario indica que el analisis es incorrecto, puede enviar un nuevo input
con mas contexto. El sistema inicia un nuevo ciclo de analisis. No existe
memoria entre sesiones (por diseno, para simplicidad del MVP).

---

## 11. Estados y transiciones

| Estado | Descripcion | Transicion siguiente |
|---|---|---|
| Inactivo | El sistema espera un mensaje en Telegram | Mensaje recibido -> Procesando |
| Procesando | n8n detecto un mensaje y llamo a /analyze | Analisis completo -> Respondiendo |
| Respondiendo | n8n formatea y envia la respuesta al usuario | Envio exitoso -> Inactivo |
| Publicando | Usuario envio /publish; n8n llama a OpenClaw | Publicacion exitosa -> Confirmando |
| Confirmando | n8n envia la URL del post al usuario | Envio exitoso -> Inactivo |
| Error | Fallo en cualquier etapa | Se envia mensaje de error al usuario -> Inactivo |

---

## 12. Complejidad

**Nivel: Complejo**

**Justificacion:** El sistema exhibe las caracteristicas de un sistema complejo:
1. **Emergencia:** El analisis TGS final no es producido por ningun agente
   individual; emerge de la interaccion entre los 4 agentes.
2. **Retroalimentacion:** El Manager implementa retroalimentacion negativa
   dinamica que ajusta el proceso en tiempo de ejecucion.
3. **No-linealidad:** El mismo input puede producir analisis diferentes en
   distintas ejecuciones (por la naturaleza estocastica del LLM).
4. **Adaptacion:** El sistema se adapta a inputs de dominios completamente
   distintos (biologia, empresas, software, sociedad) sin requerir configuracion
   especifica por dominio.

---

## 13. Supuestos del analisis

- Se asume que el LLM externo (DeepSeek V4 via OpenRouter) es un elemento del
  entorno, no un subsistema interno, porque el sistema no lo controla.
- Se omite el subsistema de infraestructura (Docker, Nginx, VPS) para mantener
  el foco en los elementos funcionales del sistema.
- La persistencia de estado entre el analisis y el `/publish` se implementa
  via `$workflow.staticData` de n8n; es efimera y no sobrevive reinicios.

---

## 14. Preguntas para profundizar

1. Como cambiaria la clasificacion del sistema si se agregara memoria persistente
   entre sesiones (base de datos)?
2. El LLM externo, es parte del entorno o de la frontera? Justifica segun el
   criterio de control.
3. Que tipo de acoplamiento existe entre el subsistema n8n y el subsistema
   CrewAI? Cambiaria si CrewAI fuera llamado directamente por el usuario?
4. Como afecta la variabilidad estocastica del LLM a la homeostasis del sistema?
   Que mecanismos podrian reducirla?
5. Es el Manager un subsistema de control puro o tambien cumple funciones de
   procesamiento? Justifica con la definicion de Bertalanffy.
