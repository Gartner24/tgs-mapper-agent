# Guia de estilo para la presentacion (NotebookLM)

> Esta guia define el aspecto visual y la voz de la presentacion del proyecto
> **TGS Mapper Agent**. Usar junto con `presentacion-slides-source.md` para
> generar las laminas. Modo claro, estilo estudiantil-profesional.

---

## 1. Concepto general

- **Audiencia:** companeros de clase y docente de Teoria General de Sistemas.
- **Tono visual:** estudiantil pero limpio. Ni corporativo agresivo ni casual
  con emojis. Pensar "tesis bien presentada".
- **Tono verbal:** primera persona singular ("yo construi", "decidi"). Sin
  jerga innecesaria; cuando se use un termino tecnico se explica una vez.
- **Idioma:** espanol neutro (Colombia). Sin anglicismos cuando hay un
  equivalente claro.

---

## 2. Paleta de colores (modo claro)

| Uso | Color | Hex |
|---|---|---|
| Fondo principal | Blanco hueso | `#F9FAFB` |
| Fondo de tarjeta | Blanco puro | `#FFFFFF` |
| Texto principal | Gris muy oscuro | `#111827` |
| Texto secundario | Gris medio | `#4B5563` |
| Acento primario (titulos, lineas) | Azul tinta | `#1E3A8A` |
| Acento secundario (resaltado) | Ambar suave | `#F59E0B` |
| Exito / OK | Verde sobrio | `#059669` |
| Error / alerta | Rojo tierra | `#B91C1C` |
| Bordes y divisores | Gris claro | `#E5E7EB` |

Reglas:
- Fondo siempre claro. Nada de modo oscuro.
- Maximo 2 acentos por lamina (azul tinta + ambar). No mezclar verde/rojo
  salvo en estados (OK/error).
- Texto sobre fondo claro: contraste minimo 7:1 para titulos, 4.5:1 para
  cuerpo.

---

## 3. Tipografia

- **Titulos:** sans-serif geometrica. Recomendado: **Inter** o **Helvetica
  Neue**. Peso 700.
  - Tamano titulo de portada: 56 pt.
  - Tamano titulo de lamina: 36 pt.
  - Subtitulo: 24 pt, peso 500.
- **Cuerpo:** misma familia, peso 400. Tamano 20 pt.
- **Codigo / nombres tecnicos** (`OpenClaw`, `tgs-n8n`, etc.): mono.
  Recomendado **JetBrains Mono** o **Fira Code**, peso 400, tamano 18 pt.
  Fondo `#F3F4F6`, padding 2-4 px, esquinas 4 px.
- Interlineado 1.4. Sin justificado: solo alineado a la izquierda.
- Nunca subrayar (reservado para enlaces).

---

## 4. Layout y composicion

- Formato: 16:9 (1920x1080 px).
- Margen seguro: 80 px por borde.
- Cuadricula de 12 columnas, gap 24 px.
- **Portada:** titulo arriba-izquierda, subtitulo debajo, datos del autor
  abajo-izquierda. Espacio negativo dominante.
- **Laminas de contenido:** titulo en la franja superior (banda blanca con
  linea azul 4 px), contenido en el resto. Numero de lamina abajo-derecha
  en gris medio.
- **Bullets:** maximo 5 por lamina, indentacion 24 px, viñeta cuadrada azul
  tinta (4 px). Nunca emoji como vinieta.
- **Tablas:** sin bordes verticales; solo lineas horizontales sutiles
  (`#E5E7EB`). Header en azul tinta con texto blanco.
- **Diagramas:** caja blanca centrada, sombra muy suave
  (`0 1px 3px rgba(0,0,0,0.06)`), borde 1 px gris claro.

---

## 5. Iconografia e imagenes

- Iconos: estilo lineal (1.5 px stroke), no rellenos, color azul tinta.
  Recomendado: **Lucide** o **Phosphor Icons (regular)**.
- Capturas de pantalla: encuadradas con borde 1 px gris claro, esquinas 8 px,
  fondo del slide rodeandolas con padding 32 px.
- Diagramas Mermaid: renderizados en tema neutral (`%%{init: {'theme':'neutral'}}%%`)
  con tipografia compatible con el resto.
- Prohibido: emojis decorativos, clip art, stock photos genericas, gradientes
  saturados.

---

## 6. Pie de pagina y branding

- Pie de cada lamina (excepto portada): linea horizontal `#E5E7EB`, debajo
  una franja con:
  - Izquierda: "TGS Mapper Agent" en mono.
  - Centro: nombre de la materia ("Teoria General de Sistemas - UTP").
  - Derecha: numero de lamina ("06 / 16").
  - Tipografia 14 pt, color gris medio (`#4B5563`).
- Logo institucional (UTP): si se incluye, va en la esquina superior derecha
  de la portada, tamano maximo 80 px de alto, sin distorsion.

---

## 7. Voz y redaccion

- Frases cortas. Un parrafo = una idea.
- Verbos en activa, presente: "el sistema analiza", "el bot responde".
- Para conceptos TGS, usar la terminologia del curso tal cual: frontera,
  entorno, suprasistema, subsistemas, retroalimentacion, etc. No traducir
  a sinonimos.
- Para conceptos tecnicos, una frase explicandolos la primera vez que aparecen
  (ej. "Docker Compose, una herramienta que levanta varios servicios con un
  solo comando").
- Evitar:
  - "En este slide veremos..." (redundante).
  - Mayusculas para enfasis (`MUY IMPORTANTE`).
  - Signos de exclamacion.
  - Anglicismos cuando hay traduccion limpia ("hacer deploy" -> "desplegar").

---

## 8. Animaciones y transiciones

- Transicion entre laminas: fade simple, 200 ms. Nada de slide, zoom o
  efectos en 3D.
- Apariciones dentro de la lamina: solo si la lista es larga o si se quiere
  enfatizar secuencia (ej. los 4 agentes). Una a una, fade-in 150 ms.
- Nunca animar el titulo de la lamina ni el pie de pagina.

---

## 9. Plantilla por tipo de lamina

| Tipo | Estructura |
|---|---|
| Portada | Titulo grande + subtitulo + bloque autor abajo |
| Concepto | Titulo + 1 frase ancla + 3 bullets |
| Lista | Titulo + bullets (max 5) |
| Arquitectura | Titulo + diagrama centrado + caption |
| Tabla | Titulo + tabla a media altura + 1 linea de cierre |
| Demo | Titulo + storyboard de pasos (1-2-3, columnas) |
| Cierre | "Gracias" + datos de contacto + repo + bot |

---

## 10. Reglas que nunca rompemos

1. Una idea principal por lamina.
2. Maximo 30-40 palabras visibles por lamina.
3. Codigo siempre con sintaxis resaltada en estilo claro (no oscuro), maximo
   8 lineas. Si necesita mas, va en anexo.
4. Sin pie de pagina = no es una lamina nuestra.
5. El nombre del proyecto (`TGS Mapper Agent`) y el del bot
   (`@tgs_mapper_bot`) van en mono cuando aparezcan en cuerpo de texto.
6. Si una lamina necesita scroll mental para entenderse, dividirla.
