# Prompt para NotebookLM - Generar diapositivas del proyecto

> Copiar y pegar el bloque siguiente en NotebookLM despues de haber subido
> como sources los archivos `presentacion-slides-source.md` y
> `presentacion-style-guide.md` (y opcionalmente `docs/guia-equipo.md` y
> `README.md`).

---

## Sources requeridos (subir a NotebookLM primero)

1. `docs/presentacion-slides-source.md` - contenido de las laminas.
2. `docs/presentacion-style-guide.md` - guia visual y de voz.
3. (Opcional) `docs/guia-equipo.md` - contexto de arquitectura.
4. (Opcional) `README.md` del repo - contexto general.

---

## Prompt (copiar tal cual)

```
Genera el guion completo y listo para Google Slides / PowerPoint de una
presentacion academica titulada "TGS Mapper Agent", presentada por
Santiago Valencia Leon para la materia Teoria General de Sistemas del
programa de Ingenieria de Sistemas y Computacion de la Universidad
Tecnologica de Pereira (UTP).

REGLAS GENERALES

- Usa EXCLUSIVAMENTE la informacion presente en los sources adjuntos. No
  inventes datos, cifras, nombres, fechas, dominios ni decisiones de diseno
  que no aparezcan en los sources. Si un dato no esta en los sources, omitelo
  o marcalo como "[por confirmar]".
- La estructura, el orden y el contenido de las laminas deben seguir el
  documento `presentacion-slides-source.md`. Cada bloque "## Diapositiva N"
  del source corresponde a UNA lamina.
- La presentacion completa debe entregarse en espanol neutro (Colombia).
- Tono: tecnico-academico, claro, primera persona singular. Sin emojis, sin
  jerga corporativa, sin frases hechas tipo "en este slide veremos...".

REGLAS DE ESTILO VISUAL Y DE VOZ

- Aplica de forma estricta la guia `presentacion-style-guide.md`:
  modo claro, paleta (azul tinta #1E3A8A como acento, ambar #F59E0B como
  resaltado, blanco hueso de fondo), tipografia sans-serif geometrica para
  cuerpo y mono para nombres tecnicos, layout 16:9, maximo 5 bullets por
  lamina, sin iconos rellenos ni emojis decorativos.
- Cada lamina debe tener:
  1. Numero y titulo.
  2. Una frase ancla (1 linea) que resuma la idea.
  3. Bullets concisos (maximo 5, idealmente 3-4) usando la informacion del
     source correspondiente.
  4. Notas del presentador (script hablado) de 30-60 segundos por lamina,
     en primera persona, en parrafo corrido, sin repetir literalmente los
     bullets.
- Las laminas de tipo tabla, arquitectura, demo y cierre deben seguir el
  template indicado en la guia de estilo (seccion 9).

FORMATO DE SALIDA

Devuelve un documento markdown con esta forma para cada lamina:

### Lamina N - Titulo

**Frase ancla:** una frase corta que centra el mensaje de la lamina.

**Bullets visibles:**
- Punto 1
- Punto 2
- Punto 3

**Notas del presentador:**
Parrafo de 60-80 palabras en primera persona singular, leible en 30-60
segundos, que amplia el contenido visible sin repetirlo. Mencionar nombres
tecnicos solo cuando aparecen en los sources.

**Layout sugerido:** uno de los templates de la guia de estilo (portada,
concepto, lista, arquitectura, tabla, demo, cierre).

ELEMENTOS OBLIGATORIOS

- Lamina 1 (portada): titulo "TGS Mapper Agent", subtitulo del source,
  presentador "Santiago Valencia Leon", materia "Teoria General de Sistemas",
  programa "Ingenieria de Sistemas y Computacion - UTP".
- Lamina de arquitectura: representar las 3 capas (interaccion / orquestacion
  / procesamiento) tal como aparecen en el source, usando un diagrama
  textual (caja > flecha > caja) que pueda traducirse facilmente a Mermaid o
  a una figura.
- Lamina del proyecto como sistema TGS: presentar la tabla del source
  (subsistema TGS -> componente) sin cambiar las equivalencias.
- Lamina de demo: presentar el storyboard de 9 pasos del source como
  secuencia numerada.
- Lamina final: incluir el repositorio github.com/Gartner24/tgs-mapper-agent,
  el bot t.me/tgs_mapper_bot y el canal t.me/tgs_mapper_bot_channel
  EXACTAMENTE como aparecen en el source.

DESPUES DE LAS LAMINAS

Anade al final un apartado titulado "Notas para la conversion a Google Slides"
con:

- Lista de colores hex y donde se usa cada uno.
- Familias tipograficas recomendadas con su uso (titulo / cuerpo / mono).
- Lista de iconos sugeridos por lamina (estilo lineal Lucide o Phosphor),
  con el concepto que representa cada uno.
- Indicacion del template de pie de pagina (`TGS Mapper Agent`,
  "Teoria General de Sistemas - UTP", numero de lamina).

CHECKS FINALES

Antes de entregar, verifica que:

- El numero total de laminas coincide con el numero de bloques
  "## Diapositiva N" del source.
- Ninguna lamina contiene mas de 40 palabras visibles.
- Las notas del presentador estan en primera persona singular.
- No hay datos, cifras o nombres que no aparezcan en los sources.
- El cierre incluye el repo, el bot y el canal con los enlaces correctos.

Entrega el resultado completo en un solo documento markdown.
```

---

## Variantes del prompt (opcional)

### Para version corta (5 laminas, lightning talk)

Anadir al final del prompt:

> Adicionalmente, despues del documento principal, genera una version corta
> de 5 laminas para una presentacion de 3 minutos (lightning talk):
> portada, problema, arquitectura, demo storyboard y cierre. Misma guia de
> estilo y mismas reglas de tono.

### Para incluir capturas de pantalla

> Donde el source mencione capturas (logs en vivo, UI de n8n, chat de
> Telegram, canal con publicacion), agrega en las notas del presentador
> una sugerencia explicita: "Captura recomendada: <descripcion>".

### Para version en ingles

> Traduce el resultado completo a ingles academico (neutral, no britanico
> ni americano). Manten los nombres propios (`OpenClaw`, `tgs-n8n`,
> `@tgs_mapper_bot`) sin traducir. La materia se traduce como
> "General Systems Theory".

---

## Tras recibir la respuesta de NotebookLM

1. Revisar que cada lamina respete la regla de 40 palabras visibles.
2. Verificar que no se haya introducido ningun dato externo (cifras de
   benchmarks, nombres de empresas, etc.).
3. Pasar las notas del presentador a un audio TTS si se requiere para
   ensayo (~30-60 s por lamina = ~10-12 min de audio total).
4. Pegar lamina por lamina en Google Slides aplicando el template y los
   colores indicados en la seccion "Notas para la conversion".
