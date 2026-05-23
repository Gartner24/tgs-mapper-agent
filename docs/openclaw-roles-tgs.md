# OpenClaw: Roles bajo el marco TGS

> Este documento mapea cada uno de los 6 roles de OpenClaw a los conceptos
> de la Teoria General de Sistemas. Es complemento de `tgs-analysis-of-itself.md`.

---

## Vision general

OpenClaw actua como un **subsistema de extension** del TGS Mapper Agent. Desde la
perspectiva TGS, amplia la frontera del sistema al incorporar capacidades que antes
estaban fuera de ella (memoria persistente, investigacion web, publicacion autonoma).

---

## Rol A — reddit-publisher (Subsistema de salida extendido)

**Skill:** `reddit-publisher`
**Clasificacion TGS:** Transductor de salida hacia el entorno social

**Descripcion:** Convierte el analisis TGS interno (JSON estructurado) en una
publicacion legible para la comunidad de Reddit. Es la frontera entre el sistema
y el ecosistema de conocimiento publico.

**Acoplamiento:** Debil con el nucleo. Si falla, el analisis textual sigue siendo
util. El usuario activa este rol de forma voluntaria con `/publish`.

**Analogia TGS:** Es el subsistema de salida secundario. El principal envia la
respuesta al usuario; este proyecta el conocimiento al entorno social.

---

## Rol B — crewai-caller (Canal de entrada alternativo)

**Skill:** `crewai-caller`
**Clasificacion TGS:** Subsistema de entrada alternativo / variedad de canales

**Descripcion:** Permite acceder al nucleo de analisis (CrewAI) sin pasar por
el canal Telegram-n8n. Implementa el principio de **variedad de Ashby**: un sistema
con mas canales de entrada puede responder a mas tipos de perturbaciones del entorno.

**Acoplamiento:** Paralelo al subsistema Extractor. Ambos producen el mismo tipo
de salida (AnalyzeRequest), pero desde caminos diferentes.

**Analogia TGS:** Es como un segundo receptor sensorial del sistema que acepta
estimulos desde una fuente diferente.

---

## Rol C — web-search (Enriquecedor de entrada)

**Skill:** `web-search`
**Clasificacion TGS:** Subsistema de pre-procesamiento / amplificador de senal

**Descripcion:** Antes de que el Extractor procese el input del usuario, este rol
busca contexto actualizado en la web sobre el tema. Enriquece la senal de entrada
con informacion que el LLM puede no tener (eventos recientes, datos especificos).

**Acoplamiento:** Secuencial fuerte con el Extractor. Si la busqueda falla, el
sistema continua con el input original (degradacion graciosa).

**Analogia TGS:** Es un amplificador de senal en el canal de entrada. Aumenta la
calidad de la informacion que entra al procesador central.

---

## Rol D — tgs-validator (Retroalimentacion negativa externa)

**Skill:** `tgs-validator`
**Clasificacion TGS:** Segundo mecanismo de retroalimentacion negativa

**Descripcion:** Despues de que el Manager ensambla el analisis final, este rol
verifica la coherencia interna: que los nodos del diagrama correspondan a
subsistemas reales, que las relaciones sean consistentes, que la complejidad sea
coherente con la estructura.

**Acoplamiento:** Secuencial con el Manager. Complementa (no reemplaza) la
retroalimentacion interna del Manager.

**Analogia TGS:** Es un segundo nivel de homeostasis. Mientras el Manager opera
retroalimentacion interna entre agentes, el validador opera retroalimentacion
sobre el output final antes de enviarlo al usuario.

---

## Rol E — analysis-memory (Memoria del sistema)

**Skill:** `analysis-memory`
**Clasificacion TGS:** Subsistema de memoria / estado persistente

**Descripcion:** Almacena los analisis TGS por usuario en memoria persistente
(SQLite). Permite que el sistema mantenga estado entre sesiones, transformandolo
de un sistema **sin memoria** (en el MVP) a uno con **memoria episodica**.

**Acoplamiento:** Asincrono (fire-and-forget). El flujo principal no espera su
confirmacion para responder al usuario.

**Analogia TGS:** Cambia la clasificacion del sistema. Con este rol activo, el
sistema pasa de discreto-sin-memoria a discreto-con-memoria. Es el equivalente
a la memoria de largo plazo en sistemas biologicos.

**Impacto en la clasificacion:** El sistema ahora puede acumular aprendizaje
sobre el dominio de cada usuario sin modificar su logica de procesamiento.

---

## Rol F — analysis-chat (Canal de dialogo reflexivo)

**Skill:** `analysis-chat`
**Clasificacion TGS:** Subsistema de dialogo / retroalimentacion del usuario

**Descripcion:** Permite al usuario hacer preguntas de seguimiento sobre su
analisis TGS previo. El rol usa la memoria (Rol E) para recuperar el contexto
y responde de forma pedagogica, ayudando al usuario a profundizar en los
conceptos TGS de su propio sistema.

**Acoplamiento:** Dependiente del Rol E (memoria). Sin analisis previo almacenado,
responde con un mensaje orientativo.

**Analogia TGS:** Implementa el principio de **dialogo reflexivo** entre el
sistema y su usuario. El sistema no solo produce outputs sino que puede discutir
su propio output, cerrando el ciclo de comprension.

---

## Tabla resumen

| Rol | Skill | Tipo TGS | Activacion | Dependencias |
|---|---|---|---|---|
| A | reddit-publisher | Transductor de salida | Manual (/publish) | Ninguna |
| B | crewai-caller | Canal de entrada alternativo | Webhook directo | Ninguna |
| C | web-search | Amplificador de senal | Automatica (pre-analisis) | TAVILY_API_KEY |
| D | tgs-validator | Retroalimentacion negativa | Automatica (post-analisis) | Ninguna |
| E | analysis-memory | Memoria persistente | Automatica (fire-and-forget) | Ninguna |
| F | analysis-chat | Canal de dialogo | Manual (/ask) | Rol E |

---

## Pregunta para profundizar

Con la incorporacion de los roles C, D y E, el sistema desarrolla tres propiedades
nuevas desde la perspectiva TGS:

1. **Rol C:** El sistema adquiere capacidad de buscar activamente informacion en
   su entorno antes de procesar. Pasa de reactivo a semi-proactivo.

2. **Rol D:** Se agrega un segundo lazo de retroalimentacion negativa externo al
   nucleo CrewAI. Aumenta la robustez homeostasica.

3. **Rol E:** El sistema adquiere memoria episodica. Ya no es un sistema de estado
   cero entre sesiones. Esto cambia su clasificacion de "sistema discreto sin
   memoria" a "sistema discreto con memoria episodica".

**Pregunta:** Como cambia el nivel de complejidad del sistema con estos tres roles
activos? Justifica usando los criterios de Bertalanffy.
