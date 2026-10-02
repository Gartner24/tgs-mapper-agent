"""
Generate docs/TGS_Mapper_Agent_Doc_Tecnico.docx
Comprehensive technical + theoretical document about the TGS Mapper Agent project.
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

OUTPUT = os.path.join(os.path.dirname(__file__), "..", "docs", "TGS_Mapper_Agent_Doc_Tecnico.docx")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def add_heading(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    h.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return h


def add_para(doc, text, bold=False, italic=False, space_before=0, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    return p


def add_bullet(doc, text, level=0):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent = Inches(0.25 * (level + 1))
    p.paragraph_format.space_after = Pt(2)
    p.add_run(text)
    return p


def add_numbered(doc, text):
    p = doc.add_paragraph(style="List Number")
    p.paragraph_format.space_after = Pt(2)
    p.add_run(text)
    return p


def add_code(doc, text):
    """Monospace block."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.4)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = "Courier New"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)
    return p


def add_table(doc, headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    # Header row
    hdr = table.rows[0]
    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        cell.text = h
        for para in cell.paragraphs:
            for run in para.runs:
                run.bold = True
                run.font.size = Pt(9)
        cell._tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), "2E4057")
        cell._tc.tcPr.append(shd)
        for para in cell.paragraphs:
            for run in para.runs:
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    # Data rows
    for r_idx, row_data in enumerate(rows):
        row = table.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.text = str(val)
            for para in cell.paragraphs:
                for run in para.runs:
                    run.font.size = Pt(9)
            if r_idx % 2 == 1:
                shd = OxmlElement("w:shd")
                shd.set(qn("w:val"), "clear")
                shd.set(qn("w:color"), "auto")
                shd.set(qn("w:fill"), "F0F4F8")
                cell._tc.get_or_add_tcPr().append(shd)
    if col_widths:
        for i, w in enumerate(col_widths):
            for row in table.rows:
                row.cells[i].width = Inches(w)
    doc.add_paragraph()
    return table


def add_divider(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run("─" * 80)
    run.font.color.rgb = RGBColor(0xCC, 0xCC, 0xCC)
    run.font.size = Pt(7)


# ---------------------------------------------------------------------------
# Document
# ---------------------------------------------------------------------------

def build():
    doc = Document()

    # Page margins
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(3)
        section.right_margin = Cm(2.5)

    # -----------------------------------------------------------------------
    # COVER
    # -----------------------------------------------------------------------
    cover = doc.add_paragraph()
    cover.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover.paragraph_format.space_before = Pt(60)
    r = cover.add_run("TGS MAPPER AGENT")
    r.bold = True
    r.font.size = Pt(26)
    r.font.color.rgb = RGBColor(0x2E, 0x40, 0x57)

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = sub.add_run("Documento Tecnico Completo")
    r2.font.size = Pt(16)
    r2.italic = True

    sub2 = doc.add_paragraph()
    sub2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r3 = sub2.add_run(
        "Sistema Multiagente de Analisis bajo la Teoria General de Sistemas\n"
        "Universidad Tecnologica de Pereira — Ingenieria de Sistemas\n"
        "Curso: Teoria General de Sistemas\n\n"
        "Autor: Santiago Valencia Leon\n"
        "Repositorio: github.com/Gartner24/tgs-mapper-agent"
    )
    r3.font.size = Pt(11)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # TABLE OF CONTENTS (manual)
    # -----------------------------------------------------------------------
    add_heading(doc, "Tabla de Contenidos", 1)
    toc_items = [
        "1. Teoria General de Sistemas (TGS) — Fundamentos Teoricos",
        "2. Vision General del Proyecto",
        "3. Pila Tecnologica (Stack)",
        "4. Arquitectura del Sistema",
        "5. Estructura de Carpetas y Archivos",
        "6. Los 4 Agentes de CrewAI — Diseno Detallado",
        "7. Esquemas Pydantic (Contratos de Datos)",
        "8. Flujo de Datos Paso a Paso",
        "9. OpenClaw — Capa de Extension",
        "10. n8n — Orquestacion y Workflows",
        "11. Variables de Entorno (.env)",
        "12. Despliegue desde Cero",
        "13. Comandos del Dia a Dia",
        "14. Detener y Reiniciar el Sistema",
        "15. Solucion de Problemas Comunes",
        "16. API del Servicio CrewAI",
        "17. El Sistema se Analiza a Si Mismo (TGS del Proyecto)",
        "18. Conceptos TGS Aplicados en el Codigo",
        "19. Preguntas de Profundizacion",
        "20. Glosario",
    ]
    for item in toc_items:
        add_bullet(doc, item)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # 1. TGS FUNDAMENTOS TEORICOS
    # -----------------------------------------------------------------------
    add_heading(doc, "1. Teoria General de Sistemas (TGS) — Fundamentos Teoricos", 1)

    add_para(doc,
        "La Teoria General de Sistemas (TGS) fue propuesta por el biologo austriaco Ludwig von "
        "Bertalanffy en la decada de 1940 y publicada formalmente en 1968 en su obra 'General "
        "System Theory'. Su objetivo es encontrar principios y leyes aplicables a sistemas en "
        "general, independientemente de su naturaleza (biologica, social, tecnica, etc.).",
        space_after=8)

    add_heading(doc, "1.1 Definicion de Sistema", 2)
    add_para(doc,
        "Un sistema es un conjunto de elementos interrelacionados que forman un todo con "
        "propiedades que ninguno de los elementos posee por separado. Esta propiedad se llama "
        "EMERGENCIA: el todo es mas que la suma de sus partes.", space_after=6)

    add_heading(doc, "1.2 Conceptos Clave que Usa este Proyecto", 2)

    concepts = [
        ("Sistema", "Conjunto organizado de elementos que interactuan para lograr un proposito."),
        ("Frontera", "Limite que separa al sistema de su entorno. Define que esta dentro y que esta fuera del control del sistema."),
        ("Entorno", "Todo lo que rodea al sistema y con lo que interactua pero que el sistema no controla."),
        ("Suprasistema", "Sistema de mayor nivel del que el sistema analizado es parte."),
        ("Elemento", "Componente basico del sistema. No tiene subestructura relevante para el analisis."),
        ("Subsistema", "Parte del sistema que tiene su propio proposito, estructura interna y elementos. Es un sistema dentro del sistema."),
        ("Relacion", "Interaccion o dependencia entre elementos o subsistemas."),
        ("Acoplamiento fuerte", "El fallo de un componente afecta directamente al otro. Alta dependencia."),
        ("Acoplamiento debil", "Los componentes pueden operar relativamente independientes. Bajo impacto mutuo ante fallos."),
        ("Acoplamiento secuencial", "La salida de A es la entrada de B. Dependencia unidireccional en orden."),
        ("Acoplamiento reciproco", "A y B se afectan mutuamente. Bidireccional."),
        ("Caja negra", "Vision del sistema desde fuera: solo entradas, procesos y salidas, sin ver el interior."),
        ("Retroalimentacion negativa", "El sistema detecta desviaciones de su objetivo y aplica correcciones para volver al estado deseado. Produce estabilidad (homeostasis)."),
        ("Retroalimentacion positiva", "El sistema amplifica las desviaciones. Puede llevar al crecimiento exponencial o a la inestabilidad."),
        ("Homeostasis", "Capacidad del sistema de mantener su estado interno estable frente a perturbaciones externas."),
        ("Emergencia", "Propiedades que aparecen en el sistema como un todo pero que no existen en ninguno de sus partes."),
        ("Complejidad", "Nivel de dificultad para predecir y comprender el comportamiento del sistema. Escala: simple -> complicado -> complejo -> caotico."),
        ("Sistema abierto", "Intercambia materia, energia o informacion con su entorno."),
        ("Sistema cerrado", "No intercambia con el entorno."),
        ("Sistema deterministico", "Dado el mismo estado inicial, siempre produce el mismo resultado."),
        ("Sistema estocastico", "Tiene componentes probabilisticos; el mismo input puede dar resultados distintos."),
        ("Sistema discreto", "Los estados cambian en eventos puntuales, no de forma continua."),
        ("Variedad de Ashby", "Ley del requisito de variedad: un sistema de control debe tener al menos tanta variedad como el sistema que controla."),
    ]
    add_table(doc,
        ["Concepto TGS", "Definicion"],
        concepts,
        col_widths=[2.0, 4.5])

    add_heading(doc, "1.3 Por que TGS es relevante para sistemas de software", 2)
    add_para(doc,
        "TGS permite analizar sistemas de software como sistemas abiertos con entradas, procesos "
        "y salidas; identificar sus subsistemas (modulos, servicios, agentes); mapear sus "
        "acoplamientos (microservicios fuertemente vs debilmente acoplados); y disenar mecanismos "
        "de retroalimentacion (monitoreo, validacion, correccion de errores). Este proyecto "
        "aplica TGS a cualquier dominio y a la vez demuestra los conceptos TGS en su propia "
        "arquitectura.", space_after=8)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # 2. VISION GENERAL DEL PROYECTO
    # -----------------------------------------------------------------------
    add_heading(doc, "2. Vision General del Proyecto", 1)

    add_para(doc,
        "TGS Mapper Agent es un sistema multiagente academico que recibe cualquier input "
        "(texto libre, PDF, imagen, URL) y devuelve un analisis estructurado bajo el marco "
        "de la Teoria General de Sistemas, incluyendo un diagrama Mermaid del sistema "
        "identificado.", space_after=6)

    add_para(doc,
        "El canal principal de uso es un bot de Telegram. El usuario escribe o adjunta "
        "contenido, el sistema lo analiza y responde con el analisis completo y el diagrama "
        "como imagen. Con el comando /publish el sistema publica el ultimo analisis en un "
        "canal de Telegram.", space_after=6)

    add_heading(doc, "2.1 Que analiza exactamente el sistema", 2)
    campos = [
        "tema: nombre del sistema identificado",
        "resumen: descripcion breve del sistema",
        "proposito: para que existe el sistema",
        "tipo_de_sistema: abierto/cerrado, natural/artificial, deterministico/estocastico, continuo/discreto",
        "frontera: que esta dentro y fuera del sistema",
        "entorno: variables externas que afectan al sistema",
        "suprasistema: sistema de nivel superior al que pertenece",
        "elementos: componentes basicos del sistema",
        "subsistemas: partes con estructura y proposito propio",
        "relaciones: interacciones entre elementos/subsistemas con tipo de acoplamiento",
        "caja_negra: entradas, procesos y salidas del sistema",
        "retroalimentacion: mecanismos de control (positiva/negativa)",
        "estados_y_transiciones: estados del sistema y como cambia entre ellos",
        "complejidad: nivel (simple/complicado/complejo/caotico) con justificacion",
        "diagrama_mermaid: codigo Mermaid del diagrama del sistema (maximo 12 nodos)",
        "supuestos: suposiciones hechas cuando el input era ambiguo",
        "preguntas_para_profundizar: al menos 3 preguntas para continuar el analisis",
    ]
    for c in campos:
        add_bullet(doc, c)

    add_heading(doc, "2.2 Ejemplo de uso", 2)
    add_para(doc, "El usuario envia al bot de Telegram:", space_after=2)
    add_code(doc,
        'Una panaderia tiene un horno, un mostrador y un cajero.\n'
        'Compra harina, hornea pan y lo vende a clientes del barrio.')
    add_para(doc, "El sistema responde con:", space_after=2)
    add_bullet(doc, "Un texto markdown con el analisis TGS completo (~1000 palabras)")
    add_bullet(doc, "Una imagen del diagrama Mermaid renderizado")
    add_para(doc, "Si el usuario luego escribe /publish:", space_after=2)
    add_bullet(doc, "El sistema publica el analisis en el canal @tgs_mapper_bot_channel de Telegram")

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # 3. PILA TECNOLOGICA
    # -----------------------------------------------------------------------
    add_heading(doc, "3. Pila Tecnologica (Stack)", 1)

    add_para(doc,
        "El stack esta cerrado: todas estas tecnologias son las definidas en el proyecto "
        "y no se pueden cambiar sin justificacion.", space_after=6)

    stack = [
        ("n8n", "docker.n8n.io/n8nio/n8n:latest", "Orquestacion de workflows, integracion con Telegram, enrutamiento de mensajes"),
        ("CrewAI (FastAPI)", "Python 3.12, build ./crew", "Motor multiagente: los 4 agentes corren aqui. Expone /analyze y /health"),
        ("OpenClaw", "alpine/openclaw:2026.5.20", "Gateway del bot de Telegram. Ejecuta skills: tgs-analyze, tgs-publish"),
        ("Docker Compose", "v2 plugin", "Levanta los 3 servicios con un solo comando"),
        ("LLM: DeepSeek / Groq / Anthropic", "Via OpenRouter, Groq API, o Anthropic API", "Cerebro de los 4 agentes. Seleccionable via LLM_PROVIDER en .env"),
        ("Pydantic v2", ">=2.9.0", "Validacion estricta del JSON de salida del analisis TGS"),
        ("FastAPI", ">=0.115.0", "Framework HTTP del servicio CrewAI"),
        ("Loguru", ">=0.7.0", "Logging. Nunca se usa print() en el proyecto"),
        ("Mermaid.ink", "Servicio externo gratuito", "Renderiza el codigo Mermaid a imagen PNG para enviarlo por Telegram"),
        ("Telegram Bot API", "Externo", "Canal principal de entrada/salida del usuario"),
        ("VPS Hostinger + Nginx", "Infraestructura", "Donde corre todo en produccion. Nginx hace TLS termination"),
    ]
    add_table(doc,
        ["Componente", "Imagen / Version", "Proposito"],
        stack,
        col_widths=[1.8, 1.8, 3.0])

    add_heading(doc, "3.1 Por que estas tecnologias", 2)
    reasons = [
        ("n8n", "Permite construir workflows visuales sin codigo adicional para la integracion con Telegram. "
                "Maneja los timeouts, la descarga de archivos de Telegram (PDF, imagenes) y el almacenamiento "
                "efimero del ultimo analisis por usuario."),
        ("CrewAI", "Framework Python disenado para sistemas multiagente. Permite definir agentes con roles, "
                   "objetivos y herramientas, y encadenarlos en un proceso secuencial con paso de contexto "
                   "entre tareas. Version 0.80+ tiene output_pydantic para validacion automatica del JSON de salida."),
        ("OpenClaw", "Gateway para bots de Telegram que carga 'skills' (archivos Markdown + scripts Node.js). "
                     "Permite que el bot tenga comportamiento complejo sin necesidad de una aplicacion de bot "
                     "separada. Es quien posee el token de Telegram."),
        ("DeepSeek / LLM via API", "Modelo de lenguaje open source de alto rendimiento disponible via OpenRouter "
                                    "o Groq. Temperatura 0.3 para outputs estructurados. max_tokens=8000 para "
                                    "analisis detallados."),
        ("Pydantic v2", "Garantiza que el LLM produzca JSON valido con todos los campos requeridos. Si el LLM "
                        "produce JSON invalido, Pydantic lanza ValidationError y el sistema devuelve un error "
                        "claro en lugar de datos corruptos."),
    ]
    for name, reason in reasons:
        add_para(doc, name, bold=True, space_after=2)
        add_para(doc, reason, space_after=6)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # 4. ARQUITECTURA DEL SISTEMA
    # -----------------------------------------------------------------------
    add_heading(doc, "4. Arquitectura del Sistema", 1)

    add_heading(doc, "4.1 Diagrama de componentes (texto)", 2)
    add_code(doc,
        "Usuario (Telegram)\n"
        "    |\n"
        "    | HTTPS mensaje\n"
        "    v\n"
        "tgs-openclaw (OpenClaw :18789)  <-- posee el token del bot\n"
        "    |\n"
        "    | Skill: tgs-analyze\n"
        "    | POST /webhook/tgs-analyze\n"
        "    v\n"
        "tgs-n8n (n8n :5678)  <-- Workflow 05: Analysis Webhook\n"
        "    |\n"
        "    | POST http://tgs-crewai:8000/analyze\n"
        "    v\n"
        "tgs-crewai (FastAPI :8000)\n"
        "    |\n"
        "    | CrewAI sequential Crew\n"
        "    |-- Agente 1: Extractor (sensor)\n"
        "    |-- Agente 2: Analista TGS (procesador)\n"
        "    |-- Agente 3: Diagramador (transductor de salida)\n"
        "    |-- Agente 4: Manager (control / retroalimentacion)\n"
        "    |\n"
        "    | {ok, analysis, markdown, mermaid, metadata}\n"
        "    v\n"
        "tgs-n8n  --> formatea respuesta\n"
        "    |\n"
        "    | texto markdown + URL de diagrama (mermaid.ink)\n"
        "    v\n"
        "tgs-openclaw  --> envia al usuario en Telegram\n"
        "    |\n"
        "    v\n"
        "Usuario recibe: texto TGS + imagen del diagrama\n"
        "\n"
        "Usuario envia /publish\n"
        "    |\n"
        "    v\n"
        "tgs-openclaw  --> Skill: tgs-publish\n"
        "    |  publica markdown + diagrama en @tgs_mapper_bot_channel\n"
        "    v\n"
        "Usuario recibe: enlace al canal de Telegram"
    )

    add_heading(doc, "4.2 Servicios Docker", 2)
    services = [
        ("tgs-n8n", "docker.n8n.io/n8nio/n8n:latest", "5678 (interno)", "web (Docker)", "Orquestacion, workflows"),
        ("tgs-crewai", "build ./crew (Python 3.12)", "8000 (interno)", "web (Docker)", "Motor de 4 agentes, API /analyze"),
        ("tgs-openclaw", "alpine/openclaw:2026.5.20", "18789 (interno)", "web (Docker)", "Bot Telegram, skills"),
    ]
    add_table(doc,
        ["Nombre", "Imagen", "Puerto", "Red", "Funcion"],
        services,
        col_widths=[1.3, 1.8, 1.1, 1.0, 2.2])

    add_para(doc,
        "Nota: ninguno de los puertos se expone directamente al exterior. El trafico "
        "entra por Nginx (puerto 443) que hace proxy hacia n8n. OpenClaw se comunica "
        "con n8n y con el exterior via la red Docker 'web'.", space_after=6)

    add_heading(doc, "4.3 Red Docker", 2)
    add_para(doc,
        "Los tres servicios comparten la red externa 'web'. Esta red debe existir antes "
        "de levantar los contenedores:", space_after=4)
    add_code(doc, "docker network create web")
    add_para(doc,
        "Los servicios se llaman entre si por su nombre de contenedor: tgs-n8n llama "
        "a http://tgs-crewai:8000/analyze, OpenClaw llama a http://tgs-n8n:5678. "
        "No se usan IPs; Docker resuelve los nombres por DNS interno.", space_after=6)

    add_heading(doc, "4.4 Dependencias de inicio (health checks)", 2)
    add_para(doc,
        "El orden de inicio es importante. tgs-crewai tiene un healthcheck que verifica "
        "GET /health cada 30 segundos. tgs-n8n y tgs-openclaw tienen depends_on con "
        "condition: service_healthy sobre tgs-crewai, lo que significa que no arrancan "
        "hasta que crewai este saludable.", space_after=6)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # 5. ESTRUCTURA DE CARPETAS
    # -----------------------------------------------------------------------
    add_heading(doc, "5. Estructura de Carpetas y Archivos", 1)

    add_code(doc,
        "tgs-mapper-agent/\n"
        "|\n"
        "|-- compose.yml               # Docker Compose: define los 3 servicios\n"
        "|-- .env.example              # Plantilla de variables de entorno\n"
        "|-- .env                      # Variables reales (NO se sube a git)\n"
        "|-- justfile                  # Atajos de comandos (just up, just logs, etc.)\n"
        "|-- PROJECT_BRIEF.md          # Especificacion completa del proyecto\n"
        "|-- DEPENDENCIES.md           # Lista de dependencias y servicios externos\n"
        "|-- CLAUDE.md                 # Memoria persistente para Claude Code\n"
        "|-- README.md\n"
        "|\n"
        "|-- crew/                     # Servicio Python: los 4 agentes CrewAI\n"
        "|   |-- Dockerfile            # Imagen Python 3.12-slim\n"
        "|   |-- requirements.txt      # Dependencias Python\n"
        "|   |-- pyproject.toml\n"
        "|   |-- main.py               # FastAPI: endpoints /analyze y /health\n"
        "|   |-- crew_setup.py         # Ensambla y ejecuta la Crew secuencial\n"
        "|   |-- agents/\n"
        "|   |   |-- extractor.py      # Agente 1: extrae el contenido\n"
        "|   |   |-- analista_tgs.py   # Agente 2: aplica TGS\n"
        "|   |   |-- diagramador.py    # Agente 3: genera Mermaid\n"
        "|   |   |-- manager.py        # Agente 4: valida y ensambla\n"
        "|   |-- tasks/\n"
        "|   |   |-- extraction.py     # Tarea del Extractor\n"
        "|   |   |-- analysis.py       # Tarea del Analista\n"
        "|   |   |-- diagram.py        # Tarea del Diagramador\n"
        "|   |   |-- coordination.py   # Tarea del Manager (ultima)\n"
        "|   |-- tools/\n"
        "|   |   |-- pdf_reader.py     # Decodifica base64 PDF con pdfplumber\n"
        "|   |   |-- image_reader.py   # Decodifica base64 imagen con Pillow\n"
        "|   |   |-- url_fetcher.py    # Fetch HTTP + limpieza HTML con BeautifulSoup\n"
        "|   |-- schemas/\n"
        "|   |   |-- tgs_output.py     # TGSAnalysis: el JSON de salida (17 campos)\n"
        "|   |   |-- extraction.py     # ExtractionResult: salida del Extractor\n"
        "|   |   |-- diagram.py        # DiagramOutput: salida del Diagramador\n"
        "|   |   |-- input.py          # AnalyzeRequest: entrada del endpoint /analyze\n"
        "|   |-- config/\n"
        "|       |-- llm.py            # Fabrica del LLM: Anthropic | Groq | OpenRouter\n"
        "|\n"
        "|-- openclaw/\n"
        "|   |-- config/               # openclaw.json y estado del bot (no en git)\n"
        "|   |-- workspace/\n"
        "|       |-- AGENTS.md         # Instrucciones del bot (reglas de comportamiento)\n"
        "|       |-- SOUL.md           # Personalidad e identidad del bot\n"
        "|       |-- TOOLS.md          # Herramientas disponibles para el bot\n"
        "|       |-- USER.md           # Perfil del usuario propietario\n"
        "|       |-- HEARTBEAT.md      # Tarea periodica del bot\n"
        "|       |-- tgs-skills/\n"
        "|           |-- tgs-analyze/\n"
        "|           |   |-- SKILL.md  # Instrucciones del skill de analisis\n"
        "|           |   |-- analyze.mjs  # Script Node.js que llama al backend\n"
        "|           |-- tgs-publish/\n"
        "|               |-- SKILL.md  # Instrucciones del skill de publicacion\n"
        "|               |-- publish.mjs  # Script Node.js que publica en Telegram\n"
        "|\n"
        "|-- n8n/\n"
        "|   |-- workflows/\n"
        "|       |-- 05-analyze-webhook.json  # Workflow: recibe POST, llama CrewAI, devuelve JSON\n"
        "|\n"
        "|-- docs/\n"
        "|   |-- architecture.md\n"
        "|   |-- agents-design.md\n"
        "|   |-- tgs-analysis-of-itself.md\n"
        "|   |-- demo-script.md\n"
        "|   |-- setup-guide.md\n"
        "|   |-- TGS_Mapper_Agent_Doc_Tecnico.docx   # este documento\n"
        "|\n"
        "|-- examples/\n"
        "|   |-- input-text.json       # Ejemplo de request al /analyze\n"
        "|   |-- input-pdf.json        # Ejemplo con PDF en base64\n"
        "|   |-- output-sample.json    # Ejemplo de respuesta completa\n"
        "|\n"
        "|-- frontend/\n"
        "    |-- index.html            # Frontend alternativo para demos sin Telegram\n"
    )

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # 6. LOS 4 AGENTES
    # -----------------------------------------------------------------------
    add_heading(doc, "6. Los 4 Agentes de CrewAI — Diseno Detallado", 1)

    add_para(doc,
        "CrewAI es el framework que coordina los 4 agentes. El proceso es SECUENCIAL: "
        "las 4 tareas corren en orden estricto. Cada tarea recibe el output de la(s) "
        "tarea(s) anterior(es) como contexto. No hay paralelismo ni delegacion entre agentes.",
        space_after=8)

    add_heading(doc, "Proceso secuencial:", 2)
    add_code(doc,
        "Extraccion  -->  Analisis TGS  -->  Diagrama  -->  Coordinacion (Manager)\n"
        "  (Tarea 1)        (Tarea 2)         (Tarea 3)         (Tarea 4, final)")

    add_para(doc,
        "El Manager es el agente de la Tarea 4. Recibe como contexto los outputs de las "
        "3 tareas anteriores, detecta inconsistencias, las corrige directamente y produce "
        "el JSON final TGSAnalysis. NO redelega: corrige el mismo.", space_after=10)

    # Agent 1
    add_heading(doc, "6.1 Agente 1 — Extractor (Sensor)", 2)
    add_para(doc,
        "Rol TGS: Sensor del sistema. Convierte la realidad externa (texto crudo, PDF, imagen, URL) "
        "en datos internos procesables.", space_after=4)
    add_table(doc,
        ["Campo", "Valor"],
        [
            ("Archivo", "crew/agents/extractor.py"),
            ("Rol", "Extractor y comprensor de contenido"),
            ("allow_delegation", "False"),
            ("max_iter", "5"),
            ("Herramientas (PDF/imagen/URL)", "PdfReaderTool, ImageReaderTool, UrlFetcherTool"),
            ("Herramientas (texto plano)", "Ninguna (tools=[])"),
            ("Output schema", "ExtractionResult (schemas/extraction.py)"),
        ],
        col_widths=[2.0, 4.5])
    add_para(doc, "Optimizacion importante:", bold=True, space_after=2)
    add_para(doc,
        "Las herramientas solo se adjuntan cuando el input_type es 'pdf', 'image' o 'url'. "
        "Para texto plano (input_type='text'), el agente no recibe herramientas (tools=[]), "
        "lo que elimina el overhead del ciclo ReAct (observar-pensar-actuar) y reduce el "
        "numero de llamadas al LLM de ~4 a ~1.", space_after=6)
    add_para(doc, "Campos del output (ExtractionResult):", bold=True, space_after=2)
    for f in ["tema_central: el tema principal del input", "conceptos: lista de conceptos clave identificados",
              "relaciones_implicitas: relaciones entre conceptos (lista de dicts)",
              "dominio: academico / empresarial / tecnico / social / biologico / otro",
              "resumen_objetivo: resumen objetivo del contenido sin interpretacion teorica"]:
        add_bullet(doc, f)

    # Agent 2
    add_heading(doc, "6.2 Agente 2 — Analista TGS (Procesador)", 2)
    add_para(doc,
        "Rol TGS: Procesador central. Es donde ocurre el comportamiento emergente del sistema: "
        "aplica el marco completo de TGS al contenido extraido.", space_after=4)
    add_table(doc,
        ["Campo", "Valor"],
        [
            ("Archivo", "crew/agents/analista_tgs.py"),
            ("Rol", "Analista experto en Teoria General de Sistemas"),
            ("allow_delegation", "False"),
            ("max_iter", "5"),
            ("Herramientas", "Ninguna"),
            ("Output schema", "TGSAnalysis (con diagrama_mermaid='PENDIENTE')"),
        ],
        col_widths=[2.0, 4.5])
    add_para(doc,
        "El Analista escribe 'PENDIENTE' en el campo diagrama_mermaid porque aun no existe "
        "el diagrama. El Diagramador lo genera en el siguiente paso y el Manager reemplaza "
        "'PENDIENTE' con el codigo real en el paso final.", space_after=6)

    # Agent 3
    add_heading(doc, "6.3 Agente 3 — Diagramador (Transductor de salida)", 2)
    add_para(doc,
        "Rol TGS: Transductor de salida. Convierte el analisis interno (JSON) en una "
        "representacion visual (codigo Mermaid) que el entorno (el usuario) puede consumir.",
        space_after=4)
    add_table(doc,
        ["Campo", "Valor"],
        [
            ("Archivo", "crew/agents/diagramador.py"),
            ("Rol", "Diagramador de sistemas complejos"),
            ("allow_delegation", "False"),
            ("max_iter", "5"),
            ("Herramientas", "Ninguna"),
            ("Output schema", "DiagramOutput: {mermaid_code: str, leyenda: str}"),
        ],
        col_widths=[2.0, 4.5])
    add_para(doc, "Reglas de diagrama (forzadas en el prompt del agente):", bold=True, space_after=2)
    rules = [
        "Tipo de diagrama: graph TD (top-down)",
        "Maximo 12 nodos (para legibilidad)",
        "Frontera del sistema como subgraph",
        "Acoplamiento fuerte: --> (flecha solida)",
        "Acoplamiento debil: -.-> (flecha punteada)",
        "Acoplamiento secuencial: --> con etiqueta",
        "Acoplamiento reciproco: <-->",
        "El campo mermaid_code NUNCA contiene backticks ni bloques markdown: solo codigo Mermaid puro",
    ]
    for r in rules:
        add_bullet(doc, r)

    # Agent 4
    add_heading(doc, "6.4 Agente 4 — Manager (Control / Retroalimentacion)", 2)
    add_para(doc,
        "Rol TGS: Subsistema de control. Implementa retroalimentacion negativa: recibe los "
        "outputs de los 3 agentes, detecta inconsistencias, las corrige y entrega el JSON "
        "final. Es el mecanismo homeostasico del sistema.", space_after=4)
    add_table(doc,
        ["Campo", "Valor"],
        [
            ("Archivo", "crew/agents/manager.py"),
            ("Rol", "Director del analisis TGS"),
            ("allow_delegation", "False (no redelega, corrige directamente)"),
            ("max_iter", "5"),
            ("Herramientas", "Ninguna"),
            ("Contexto de tarea", "Recibe outputs de las 3 tareas anteriores"),
            ("Output schema", "TGSAnalysis (completo y final, diagrama_mermaid poblado)"),
        ],
        col_widths=[2.0, 4.5])
    add_para(doc, "Reglas de validacion que aplica el Manager:", bold=True, space_after=2)
    validation = [
        "Cada nodo del codigo Mermaid debe corresponder a un subsistema o elemento en el analisis",
        "Cada relacion (Relacion.origen y Relacion.destino) debe referenciar subsistemas o elementos validos",
        "tipo_de_sistema y complejidad deben ser coherentes con los subsistemas y relaciones identificados",
        "supuestos debe ser no vacio si el input fue ambiguo",
        "preguntas_para_profundizar debe tener al menos 3 preguntas",
    ]
    for v in validation:
        add_bullet(doc, v)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # 7. ESQUEMAS PYDANTIC
    # -----------------------------------------------------------------------
    add_heading(doc, "7. Esquemas Pydantic (Contratos de Datos)", 1)

    add_para(doc,
        "Pydantic v2 garantiza que el LLM produzca JSON valido con todos los campos requeridos. "
        "CrewAI usa output_pydantic en cada Task para validar automaticamente el output del agente. "
        "Si el JSON no cumple el schema, Pydantic lanza ValidationError y el sistema devuelve "
        "un error controlado.", space_after=6)

    add_heading(doc, "7.1 TGSAnalysis — el schema principal (17 campos)", 2)
    add_para(doc, "Archivo: crew/schemas/tgs_output.py", italic=True, space_after=4)

    fields_main = [
        ("tema", "str", "Nombre del sistema analizado"),
        ("resumen", "str", "Descripcion breve del sistema"),
        ("proposito", "str", "Para que existe el sistema"),
        ("tipo_de_sistema", "TipoSistema", "Clasificacion en 4 dimensiones con justificacion"),
        ("frontera", "Frontera", "Descripcion + lista de elementos dentro y fuera"),
        ("entorno", "Entorno", "Descripcion + lista de variables externas"),
        ("suprasistema", "str", "Sistema de nivel superior"),
        ("elementos", "list[Elemento]", "Componentes basicos: nombre + rol"),
        ("subsistemas", "list[Subsistema]", "Partes con proposito propio: nombre + proposito + elementos_clave"),
        ("relaciones", "list[Relacion]", "Interacciones: origen + destino + tipo_acoplamiento + descripcion"),
        ("caja_negra", "CajaNegra", "entradas + procesos + salidas"),
        ("retroalimentacion", "list[Retroalimentacion]", "tipo (positiva/negativa) + descripcion"),
        ("estados_y_transiciones", "list[EstadoTransicion]", "Estado actual + lista de transiciones posibles"),
        ("complejidad", "Complejidad", "nivel (simple/complicado/complejo/caotico) + justificacion"),
        ("diagrama_mermaid", "str", "Codigo Mermaid puro del diagrama del sistema"),
        ("supuestos", "list[str]", "Suposiciones hechas cuando el input era ambiguo"),
        ("preguntas_para_profundizar", "list[str]", "Minimo 3 preguntas para continuar el analisis"),
    ]
    add_table(doc,
        ["Campo", "Tipo Python", "Descripcion"],
        fields_main,
        col_widths=[1.8, 1.5, 3.2])

    add_heading(doc, "7.2 Nota sobre los nombres de campos", 2)
    add_para(doc,
        "Los nombres de campo del schema estan en ESPANOL (frontera, subsistemas, retroalimentacion, etc.) "
        "porque el LLM debe responder en espanol usando la terminologia del curso TGS. Los nombres de clase "
        "estan en INGLES siguiendo la convencion Python (TGSAnalysis, Subsistema, Frontera, etc.).",
        space_after=8)

    add_heading(doc, "7.3 Tipos Literal y sus valores validos", 2)
    literals = [
        ("abierto_o_cerrado", '"abierto", "cerrado", "mixto"'),
        ("natural_o_artificial", '"natural", "artificial", "sociotecnico"'),
        ("deterministico_o_estocastico", '"deterministico", "estocastico", "mixto"'),
        ("continuo_o_discreto", '"continuo", "discreto", "hibrido"'),
        ("tipo_acoplamiento", '"fuerte", "debil", "secuencial", "reciproco"'),
        ("tipo retroalimentacion", '"positiva", "negativa"'),
        ("nivel complejidad", '"simple", "complicado", "complejo", "caotico"'),
    ]
    add_table(doc,
        ["Campo", "Valores validos (Literal)"],
        literals,
        col_widths=[2.5, 4.0])

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # 8. FLUJO DE DATOS
    # -----------------------------------------------------------------------
    add_heading(doc, "8. Flujo de Datos Paso a Paso", 1)

    steps = [
        ("1", "Usuario envia mensaje en Telegram",
         "El usuario escribe texto, adjunta un PDF o una imagen, o pega una URL. "
         "OpenClaw recibe el mensaje porque posee el TELEGRAM_BOT_TOKEN."),
        ("2", "OpenClaw invoca la skill tgs-analyze",
         "AGENTS.md le dice al bot que para cualquier contenido analizable debe ejecutar la skill tgs-analyze. "
         "El bot avisa: 'Procesando tu analisis bajo el marco TGS (tarda 2-4 minutos)...' y escribe el contenido "
         "a /tmp/tgs-analyze.txt. Luego ejecuta analyze.mjs."),
        ("3", "analyze.mjs llama al webhook de n8n",
         "El script Node.js lee el archivo /tmp/tgs-analyze.txt y hace POST a "
         "http://tgs-n8n:5678/webhook/tgs-analyze con {input_type, content}. Espera hasta 6 minutos (yieldMs=360000)."),
        ("4", "n8n Workflow 05 procesa la peticion",
         "El workflow recibe el POST, detecta el tipo de input, y hace POST a "
         "http://tgs-crewai:8000/analyze con {input_type, content, user_id}. Timeout: 600 segundos."),
        ("5", "FastAPI /analyze recibe la peticion",
         "main.py recibe el AnalyzeRequest, llama run_analysis() en un thread separado "
         "(asyncio.to_thread para no bloquear el event loop), y mide el tiempo de ejecucion."),
        ("6", "crew_setup.py ensambla y ejecuta la Crew",
         "build_crew() crea los 4 agentes y las 4 tareas. "
         "Crew(process=Process.sequential).kickoff() los ejecuta en orden."),
        ("7a", "Tarea 1 — Extractor",
         "El agente lee el input. Si es PDF/imagen/URL, usa sus herramientas para extraer texto. "
         "Produce ExtractionResult: {tema_central, conceptos, relaciones_implicitas, dominio, resumen_objetivo}."),
        ("7b", "Tarea 2 — Analista TGS",
         "Recibe el ExtractionResult como contexto. Aplica TGS completo. Produce TGSAnalysis con "
         "diagrama_mermaid='PENDIENTE'. Los 17 campos deben estar completos segun el schema."),
        ("7c", "Tarea 3 — Diagramador",
         "Recibe el TGSAnalysis como contexto. Genera el codigo Mermaid. Maximo 12 nodos. "
         "Produce DiagramOutput: {mermaid_code, leyenda}."),
        ("7d", "Tarea 4 — Manager (Coordinacion)",
         "Recibe los 3 outputs anteriores como contexto. Valida coherencia. Corrige inconsistencias. "
         "Ensambla TGSAnalysis final reemplazando diagrama_mermaid='PENDIENTE' con el mermaid_code real."),
        ("8", "FastAPI devuelve la respuesta",
         "Retorna {ok: true, analysis: TGSAnalysis, markdown: str, mermaid: str, metadata: {...}}."),
        ("9", "n8n formatea y responde",
         "El workflow toma el markdown y construye la URL de mermaid.ink para renderizar el diagrama. "
         "Guarda el analisis en staticData[chatId]. Devuelve {ok, markdown, diagram_url} a analyze.mjs."),
        ("10", "OpenClaw envia la respuesta al usuario",
         "El bot envia el markdown como mensaje de texto y la diagram_url como foto al chat de Telegram."),
        ("11", "Usuario envia /publish (opcional)",
         "OpenClaw invoca la skill tgs-publish. El script publish.mjs toma el ultimo analisis "
         "(markdown + diagram_url) del contexto de la conversacion y los publica en @tgs_mapper_bot_channel."),
    ]

    for step_num, title, desc in steps:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(f"Paso {step_num}: {title}")
        r.bold = True
        r.font.size = Pt(10)
        add_para(doc, desc, space_after=4)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # 9. OPENCLAW
    # -----------------------------------------------------------------------
    add_heading(doc, "9. OpenClaw — Capa de Extension del Bot", 1)

    add_para(doc,
        "OpenClaw es un gateway de bots de Telegram que carga 'skills': archivos Markdown que "
        "describen comportamientos + scripts que los ejecutan. Es quien posee el TELEGRAM_BOT_TOKEN "
        "y se encarga de toda la interaccion con el usuario. n8n y CrewAI son servicios de backend "
        "que OpenClaw llama, NO interfaces de usuario.", space_after=6)

    add_heading(doc, "9.1 Archivos del workspace", 2)
    workspace_files = [
        ("SOUL.md", "Personalidad e identidad del bot. Define el tono, idioma y quien es el bot."),
        ("AGENTS.md", "Instrucciones de comportamiento. La regla central: NUNCA producir un analisis TGS sin llamar al backend. Define que hacer ante /publish."),
        ("TOOLS.md", "Herramientas disponibles para el bot (exec, web_fetch, etc.)."),
        ("USER.md", "Perfil del usuario propietario."),
        ("HEARTBEAT.md", "Tarea periodica del bot (si aplica)."),
        ("tgs-skills/tgs-analyze/SKILL.md", "Instrucciones paso a paso del skill de analisis. Define el procedimiento exacto: avisar, escribir archivo, ejecutar script, enviar resultado."),
        ("tgs-skills/tgs-analyze/analyze.mjs", "Script Node.js: lee /tmp/tgs-analyze.txt, hace POST al webhook de n8n, devuelve JSON."),
        ("tgs-skills/tgs-publish/SKILL.md", "Instrucciones del skill de publicacion. Verifica que haya analisis previo, escribe archivos temporales, ejecuta publish.mjs."),
        ("tgs-skills/tgs-publish/publish.mjs", "Script Node.js: lee los archivos temporales, publica en @tgs_mapper_bot_channel via Telegram Bot API."),
    ]
    add_table(doc,
        ["Archivo", "Proposito"],
        workspace_files,
        col_widths=[2.5, 4.0])

    add_heading(doc, "9.2 Por que OpenClaw (y no un bot de Python directamente)", 2)
    add_para(doc,
        "OpenClaw permite definir el comportamiento del bot en Markdown y ejecutar logica "
        "en scripts Node.js sin escribir una aplicacion de bot completa. Las skills son "
        "archivos de texto versionados en git. El bot carga las instrucciones al iniciar y "
        "las aplica en cada mensaje. Esto separa el comportamiento (skills) de la "
        "infraestructura (contenedor).", space_after=6)

    add_heading(doc, "9.3 La regla mas importante (AGENTS.md)", 2)
    add_para(doc,
        "El bot tiene una regla critica: NUNCA produce el analisis TGS con su propio conocimiento. "
        "SIEMPRE debe llamar al backend (CrewAI) via la skill tgs-analyze. Esto garantiza que el "
        "analisis sea formal, estructurado y conforme al schema TGSAnalysis, y no una respuesta "
        "improvisada del LLM del bot.", space_after=6)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # 10. N8N WORKFLOWS
    # -----------------------------------------------------------------------
    add_heading(doc, "10. n8n — Orquestacion y Workflows", 1)

    add_para(doc,
        "n8n es el orquestador de la arquitectura. Recibe peticiones de OpenClaw, "
        "descarga archivos de Telegram si es necesario, llama al endpoint /analyze de "
        "CrewAI, y devuelve el resultado formateado.", space_after=6)

    add_heading(doc, "10.1 Workflow 05: analyze-webhook", 2)
    add_para(doc, "Archivo: n8n/workflows/05-analyze-webhook.json", italic=True, space_after=4)
    add_para(doc, "Disparo: POST /webhook/tgs-analyze (llamado por analyze.mjs de OpenClaw)", space_after=4)

    wf_steps = [
        ("Webhook trigger", "Recibe {input_type, content, user_id} de OpenClaw"),
        ("HTTP Request al CrewAI", "POST http://tgs-crewai:8000/analyze con timeout 600 segundos"),
        ("Formateo de respuesta", "Extrae markdown y mermaid del JSON de respuesta"),
        ("Construccion de diagram_url", "Codifica el codigo Mermaid como URL de mermaid.ink (imagen PNG)"),
        ("Respuesta al caller", "Devuelve {ok, markdown, diagram_url} a OpenClaw"),
    ]
    add_table(doc,
        ["Nodo", "Funcion"],
        wf_steps,
        col_widths=[2.0, 4.5])

    add_heading(doc, "10.2 Timeouts criticos", 2)
    add_para(doc,
        "El CrewAI tarda 2-4 minutos por analisis (4 llamadas al LLM en secuencia). "
        "Por esto los timeouts estan configurados en 600 segundos (10 minutos) en el nodo "
        "HTTP Request de n8n. El script analyze.mjs espera hasta 6 minutos (yieldMs=360000).",
        space_after=6)

    add_heading(doc, "10.3 Como importar el workflow", 2)
    add_code(doc,
        "# Opcion 1: importar desde el host\n"
        "docker compose exec -T n8n n8n import:workflow \\\n"
        "  --input=/workflows/05-analyze-webhook.json\n"
        "\n"
        "# Opcion 2: copiar y luego importar\n"
        "docker compose cp n8n/workflows/05-analyze-webhook.json n8n:/tmp/wf.json\n"
        "docker compose exec n8n n8n import:workflow --input=/tmp/wf.json")
    add_para(doc,
        "Despues de importar, abrir la UI de n8n (http://localhost:5678), abrir el "
        "workflow y activarlo con el switch Active.", space_after=6)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # 11. VARIABLES DE ENTORNO
    # -----------------------------------------------------------------------
    add_heading(doc, "11. Variables de Entorno (.env)", 1)

    add_para(doc,
        "Copia .env.example a .env y llena los valores. El archivo .env NUNCA se sube "
        "a git (esta en .gitignore).", space_after=6)

    env_vars = [
        ("LLM_PROVIDER", "groq", "Proveedor de LLM: anthropic | groq | openrouter"),
        ("LLM_MODEL", "llama-3.3-70b-versatile", "Nombre del modelo segun el proveedor"),
        ("ANTHROPIC_API_KEY", "(vacio)", "API key de Anthropic (si LLM_PROVIDER=anthropic)"),
        ("GROQ_API_KEY", "(vacio)", "API key de Groq (si LLM_PROVIDER=groq)"),
        ("OPENROUTER_API_KEY", "(vacio)", "API key de OpenRouter (si LLM_PROVIDER=openrouter)"),
        ("TELEGRAM_BOT_TOKEN", "REQUERIDO", "Token del bot de Telegram (de @BotFather)"),
        ("TELEGRAM_OWNER_ID", "REQUERIDO", "Tu user_id de Telegram (para comandos privilegiados)"),
        ("N8N_HOST", "n8n.tu-dominio.com", "Host publico de n8n (si se expone)"),
        ("N8N_PROTOCOL", "https", "Protocolo de n8n"),
        ("N8N_PORT", "5678", "Puerto de n8n"),
        ("WEBHOOK_URL", "https://n8n.tu-dominio.com/", "URL base del webhook de n8n"),
        ("N8N_BASIC_AUTH_USER", "admin", "Usuario de autenticacion basica de n8n"),
        ("N8N_BASIC_AUTH_PASSWORD", "REQUERIDO", "Contrasena de autenticacion basica de n8n"),
        ("N8N_ENCRYPTION_KEY", "REQUERIDO", "Clave de cifrado de n8n (openssl rand -hex 32)"),
        ("CREW_API_URL", "http://tgs-crewai:8000", "URL interna del servicio CrewAI"),
        ("TAVILY_API_KEY", "(opcional)", "API key de Tavily para web search"),
        ("REDDIT_CLIENT_ID", "(opcional)", "ID de app de Reddit para publicacion"),
        ("REDDIT_CLIENT_SECRET", "(opcional)", "Secret de app de Reddit"),
        ("REDDIT_USERNAME", "(opcional)", "Usuario de Reddit"),
        ("REDDIT_PASSWORD", "(opcional)", "Contrasena de Reddit"),
        ("REDDIT_TARGET", "u_miusuario", "Perfil propio de Reddit donde publicar"),
    ]
    add_table(doc,
        ["Variable", "Valor ejemplo", "Descripcion"],
        env_vars,
        col_widths=[2.2, 1.8, 2.5])

    add_heading(doc, "11.1 Como elegir el proveedor de LLM", 2)
    providers = [
        ("anthropic", "claude-haiku-4-5 o claude-sonnet-4-6",
         "ANTHROPIC_API_KEY", "Requiere is_litellm=True en llm.py para evitar error 'compiled grammar too large'"),
        ("groq", "llama-3.3-70b-versatile",
         "GROQ_API_KEY", "Muy rapido, gratuito con limites. Recomendado para desarrollo"),
        ("openrouter", "deepseek/deepseek-chat",
         "OPENROUTER_API_KEY", "Acceso a muchos modelos open source. Pago por uso"),
    ]
    add_table(doc,
        ["LLM_PROVIDER", "LLM_MODEL ejemplo", "Key necesaria", "Notas"],
        providers,
        col_widths=[1.2, 2.0, 1.6, 2.0])

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # 12. DESPLIEGUE DESDE CERO
    # -----------------------------------------------------------------------
    add_heading(doc, "12. Despliegue desde Cero", 1)

    add_para(doc,
        "Tiempo estimado: 30-45 minutos en un servidor Linux nuevo.", space_after=6)

    add_heading(doc, "12.1 Requisitos del servidor", 2)
    reqs = [
        "Linux (Ubuntu 22.04+ recomendado)",
        "2 vCPU, 4 GB RAM, 20 GB disco (minimo)",
        "Docker Engine 24+ instalado",
        "Docker Compose v2 plugin (comando: docker compose, NO docker-compose)",
        "git, curl instalados",
        "Puertos 80 y 443 expuestos si se usa nginx delante",
        "Puerto 5678, 8000, 18789 libres internamente",
    ]
    for r in reqs:
        add_bullet(doc, r)

    add_heading(doc, "12.2 Cuentas y credenciales necesarias antes de empezar", 2)
    creds = [
        ("Bot de Telegram", "Crear con @BotFather -> /newbot. Anota el token (TELEGRAM_BOT_TOKEN)."),
        ("API key del LLM", "Groq (gratis): https://console.groq.com. Anthropic: https://console.anthropic.com. OpenRouter: https://openrouter.ai"),
        ("Canal de Telegram (opcional)", "Para /publish: crear canal publico, agregar el bot como admin con permiso 'Post Messages'."),
    ]
    add_table(doc,
        ["Servicio", "Como obtenerlo"],
        creds,
        col_widths=[2.0, 4.5])

    add_heading(doc, "12.3 Pasos de instalacion", 2)

    install_steps = [
        ("Verificar Docker", "docker --version\ndocker compose version"),
        ("Clonar el repositorio", "git clone https://github.com/Gartner24/tgs-mapper-agent.git\ncd tgs-mapper-agent"),
        ("Crear la red Docker", "docker network create web"),
        ("Configurar variables de entorno",
         "cp .env.example .env\nnano .env   # o vim .env\n# Llenar: LLM_PROVIDER, LLM_MODEL, API key del LLM,\n# TELEGRAM_BOT_TOKEN, TELEGRAM_OWNER_ID,\n# N8N_BASIC_AUTH_PASSWORD, N8N_ENCRYPTION_KEY"),
        ("Levantar los contenedores", "docker compose up -d"),
        ("Verificar que esten saludables",
         "docker compose ps\n# Deben aparecer como Up (healthy) los 3 servicios"),
        ("Importar el workflow de n8n",
         "docker compose exec -T n8n n8n import:workflow \\\n  --input=/workflows/05-analyze-webhook.json"),
        ("Activar el workflow en n8n",
         "Abrir http://localhost:5678\nAbrir el workflow 'Analysis Webhook'\nActivar el switch Active"),
        ("Verificar el health del backend",
         "curl http://localhost:8000/health\n# Respuesta esperada: {\"ok\": true, \"version\": \"0.1.0\"}"),
        ("Test end-to-end desde Telegram",
         "Enviar al bot: 'Una panaderia tiene un horno y un cajero'\nEsperar 2-4 minutos\nRecibir: texto de analisis TGS + imagen del diagrama"),
    ]

    for i, (title, cmd) in enumerate(install_steps, 1):
        add_para(doc, f"Paso {i}: {title}", bold=True, space_after=2)
        add_code(doc, cmd)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # 13. COMANDOS DEL DIA A DIA
    # -----------------------------------------------------------------------
    add_heading(doc, "13. Comandos del Dia a Dia", 1)

    add_para(doc,
        "El proyecto usa 'just' como task runner. Si no tienes just instalado, "
        "usa directamente los comandos docker compose equivalentes.", space_after=6)

    cmds = [
        ("just up", "docker compose up -d", "Levantar todos los servicios en segundo plano"),
        ("just down", "docker compose down", "Detener y eliminar los contenedores"),
        ("just logs", "docker compose logs -f", "Ver logs de todos los servicios en tiempo real"),
        ("just rebuild", "docker compose build crewai && docker compose up -d crewai", "Reconstruir solo el contenedor CrewAI (cuando cambias codigo Python)"),
        ("just test", "(python + httpx)", "Smoke test: llama a /analyze con el ejemplo de texto y muestra el resultado"),
        ("just health", "curl http://localhost:8000/health", "Verificar que el servicio CrewAI este respondiendo"),
        ("just shell", "docker compose exec crewai /bin/bash", "Abrir shell dentro del contenedor CrewAI"),
        ("just openclaw-logs", "docker compose logs -f openclaw", "Ver logs solo de OpenClaw"),
        ("just openclaw-shell", "docker compose exec openclaw /bin/sh", "Abrir shell dentro del contenedor OpenClaw"),
    ]
    add_table(doc,
        ["Comando just", "Equivalente docker", "Que hace"],
        cmds,
        col_widths=[1.5, 2.5, 2.5])

    add_heading(doc, "13.1 Comandos de diagnostico utiles", 2)
    diag_cmds = [
        ("Ver estado de todos los contenedores", "docker compose ps"),
        ("Ver logs de crewai (ultimas 50 lineas)", "docker compose logs --tail=50 crewai"),
        ("Ver logs de n8n", "docker compose logs --tail=50 n8n"),
        ("Ver logs de openclaw", "docker compose logs --tail=50 openclaw"),
        ("Test manual del endpoint /analyze",
         "curl -X POST http://localhost:8000/analyze \\\n"
         "  -H 'content-type: application/json' \\\n"
         "  -d '{\"input_type\":\"text\",\"content\":\"Una empresa de logistica\"}'"),
        ("Test del webhook de n8n",
         "curl -X POST http://localhost:5678/webhook/tgs-analyze \\\n"
         "  -H 'content-type: application/json' \\\n"
         "  -d '{\"input_type\":\"text\",\"content\":\"Una panaderia\"}'"),
        ("Reiniciar un servicio especifico", "docker compose restart crewai  # o n8n o openclaw"),
    ]
    for desc, cmd in diag_cmds:
        add_para(doc, desc, bold=True, space_after=2)
        add_code(doc, cmd)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # 14. DETENER Y REINICIAR
    # -----------------------------------------------------------------------
    add_heading(doc, "14. Detener y Reiniciar el Sistema", 1)

    add_heading(doc, "14.1 Detener todo", 2)
    add_code(doc,
        "# Detener y eliminar contenedores (los datos de n8n se conservan en el volumen n8n_data)\n"
        "docker compose down\n\n"
        "# Detener SIN eliminar contenedores (mas rapido para reiniciar)\n"
        "docker compose stop\n\n"
        "# Detener y eliminar TODO incluyendo volumenes (PELIGROSO: borra workflows de n8n)\n"
        "docker compose down -v")

    add_heading(doc, "14.2 Reiniciar un servicio", 2)
    add_code(doc,
        "# Reiniciar solo OpenClaw (por ejemplo, si el bot no responde)\n"
        "docker compose restart openclaw\n\n"
        "# Reiniciar solo CrewAI (si hubo un error en el backend)\n"
        "docker compose restart crewai\n\n"
        "# Reiniciar n8n (si los workflows no responden)\n"
        "docker compose restart n8n")

    add_heading(doc, "14.3 Reconstruir despues de cambios en el codigo", 2)
    add_code(doc,
        "# Cuando cambias archivos Python en crew/\n"
        "docker compose build crewai\n"
        "docker compose up -d crewai\n\n"
        "# Cuando cambias skills de OpenClaw (SKILL.md, .mjs)\n"
        "# No se necesita rebuild: OpenClaw lee los archivos del volumen montado\n"
        "docker compose restart openclaw\n\n"
        "# Cuando cambias workflows de n8n\n"
        "# Importar el JSON actualizado y reactivar en la UI de n8n")

    add_heading(doc, "14.4 Ver si los contenedores estan saludables", 2)
    add_code(doc,
        "docker compose ps\n"
        "# Salida esperada:\n"
        "# NAME           STATUS\n"
        "# tgs-crewai     Up (healthy)\n"
        "# tgs-n8n        Up\n"
        "# tgs-openclaw   Up (healthy)")

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # 15. SOLUCION DE PROBLEMAS
    # -----------------------------------------------------------------------
    add_heading(doc, "15. Solucion de Problemas Comunes", 1)

    problems = [
        ("El bot no responde nada al enviar un mensaje",
         "OpenClaw no tiene el token o fue desplazado por otro proceso",
         "docker compose restart openclaw\nVerificar en los logs: '[telegram] starting provider'"),
        ("'Hubo un problema tecnico con el backend'",
         "n8n esta inactivo o el workflow no esta activado",
         "Entrar a la UI de n8n, abrir el workflow y verificar que este Active"),
        ("El bot hace onboarding / pide nombre / propone configurar personalidad",
         "Falta AGENTS.md o SOUL.md en el workspace de OpenClaw",
         "Verificar que existen:\n  openclaw/workspace/AGENTS.md\n  openclaw/workspace/SOUL.md\ndocker compose restart openclaw"),
        ("El analisis tarda mas de 10 minutos",
         "El LLM esta lento o el timeout de n8n es insuficiente",
         "Verificar LLM_PROVIDER y los creditos disponibles\nCambiar a Groq (mas rapido) si es posible"),
        ("'compiled grammar too large' (error de Anthropic)",
         "CrewAI usa el provider nativo de Anthropic en lugar de litellm",
         "En crew/config/llm.py verificar que el bloque anthropic tiene is_litellm=True"),
        ("Anthropic 'credit balance is too low'",
         "Sin creditos en la cuenta de Anthropic",
         "Recargar en https://console.anthropic.com o cambiar a Groq (gratis con limites)"),
        ("/publish dice 'Bad Request: chat not found'",
         "El bot no es administrador del canal o el username del canal esta incorrecto",
         "Agregar el bot como Administrador del canal con permiso 'Post Messages'\n"
         "Verificar el username en publish.mjs"),
        ("ValidationError al ejecutar /analyze",
         "El LLM produjo JSON que no cumple el schema TGSAnalysis",
         "El sistema devuelve {ok: false}. Intentar de nuevo.\n"
         "Si persiste, revisar el modelo LLM o reducir la complejidad del input"),
        ("Los contenedores no arrancan (network 'web' not found)",
         "La red Docker externa no existe",
         "docker network create web\ndocker compose up -d"),
        ("n8n no importa el workflow",
         "El archivo no esta en la ruta esperada dentro del contenedor",
         "docker compose cp n8n/workflows/05-analyze-webhook.json n8n:/tmp/wf.json\n"
         "docker compose exec n8n n8n import:workflow --input=/tmp/wf.json"),
    ]

    for symptom, cause, fix in problems:
        add_para(doc, f"Problema: {symptom}", bold=True, space_after=2)
        add_para(doc, f"Causa: {cause}", italic=True, space_after=2)
        add_code(doc, f"Solucion:\n{fix}")
        add_divider(doc)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # 16. API DEL SERVICIO CREWAI
    # -----------------------------------------------------------------------
    add_heading(doc, "16. API del Servicio CrewAI", 1)

    add_para(doc,
        "El servicio CrewAI expone dos endpoints. La documentacion interactiva "
        "esta disponible en http://localhost:8000/docs (Swagger UI generado "
        "automaticamente por FastAPI).", space_after=6)

    add_heading(doc, "16.1 GET /health", 2)
    add_para(doc, "Verifica que el servicio este corriendo.", space_after=4)
    add_code(doc,
        "# Request\n"
        "GET http://localhost:8000/health\n\n"
        "# Response 200\n"
        '{"ok": true, "version": "0.1.0"}')

    add_heading(doc, "16.2 POST /analyze", 2)
    add_para(doc, "Analiza el input bajo TGS y devuelve el analisis estructurado.", space_after=4)

    add_code(doc,
        "# Request body (JSON)\n"
        "{\n"
        '  "input_type": "text",   // text | pdf | image | url\n'
        '  "content": "...",       // texto libre | URL | base64 de PDF | base64 de imagen\n'
        '  "user_id": "opcional"   // chat_id de Telegram\n'
        "}\n\n"
        "# Response 200 (exitoso)\n"
        "{\n"
        '  "ok": true,\n'
        '  "analysis": { /* TGSAnalysis completo, 17 campos */ },\n'
        '  "markdown": "# Analisis TGS: ...",\n'
        '  "mermaid": "graph TD\\n  A --> B ...",\n'
        '  "metadata": {\n'
        '    "duration_seconds": 142.5,\n'
        '    "model_used": "groq/llama-3.3-70b-versatile",\n'
        '    "validated_by_manager": true,\n'
        '    "corrections_applied": []\n'
        '  }\n'
        "}\n\n"
        "# Response 500 (error)\n"
        "{\n"
        '  "ok": false,\n'
        '  "error": "Error interno al procesar el analisis. Intenta de nuevo.",\n'
        '  "stage": "extractor"  // etapa donde fallo\n'
        "}")

    add_heading(doc, "16.3 Ejemplo de llamada directa", 2)
    add_code(doc,
        "curl -X POST http://localhost:8000/analyze \\\n"
        "  -H 'content-type: application/json' \\\n"
        "  -d '{\n"
        '    "input_type": "text",\n'
        '    "content": "Una universidad tiene facultades, departamentos y estudiantes. '
        'Recibe presupuesto del Estado y produce profesionales."\n'
        "  }' \\\n"
        "  | python3 -m json.tool")

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # 17. TGS DEL PROYECTO
    # -----------------------------------------------------------------------
    add_heading(doc, "17. El Sistema se Analiza a Si Mismo", 1)

    add_para(doc,
        "El punto mas interesante del proyecto: el TGS Mapper Agent es en si mismo un "
        "sistema que puede ser analizado bajo TGS. Aqui esta el analisis formal del "
        "propio sistema.", space_after=6)

    add_heading(doc, "17.1 Tipo de sistema", 2)
    system_type = [
        ("Abierto / cerrado", "Abierto", "Intercambia informacion con el usuario, Telegram, el LLM y el canal de Telegram"),
        ("Natural / artificial", "Sociotecnico (artificial)", "Construido por humanos; combina codigo, LLMs y protocolos de comunicacion"),
        ("Deterministico / estocastico", "Estocastico", "El LLM produce outputs probabilisticos; el mismo input puede dar analisis ligeramente distintos"),
        ("Continuo / discreto", "Discreto", "Procesa un mensaje a la vez; los estados cambian en eventos discretos"),
    ]
    add_table(doc,
        ["Dimension", "Clasificacion", "Justificacion"],
        system_type,
        col_widths=[1.8, 1.5, 3.2])

    add_heading(doc, "17.2 Frontera del sistema", 2)
    add_para(doc,
        "La frontera es el perimetro del stack de software bajo nuestro control: "
        "los contenedores Docker (tgs-n8n, tgs-crewai, tgs-openclaw) y la logica "
        "de los 4 agentes y las 2 skills.", space_after=4)
    add_table(doc,
        ["Dentro de la frontera", "Fuera de la frontera"],
        [
            ("Orquestador n8n", "Telegram Bot API (servicio externo)"),
            ("FastAPI + CrewAI", "OpenRouter / LLM (servicio externo)"),
            ("Los 4 agentes", "El usuario final"),
            ("Schemas Pydantic", "La red Docker 'web' y el proxy Nginx"),
            ("Skills de OpenClaw", "Canal de Telegram @tgs_mapper_bot_channel"),
        ],
        col_widths=[3.0, 3.0])

    add_heading(doc, "17.3 Los 4 agentes como subsistemas TGS", 2)
    agent_tgs = [
        ("Extractor", "Sensor / entrada", "Convierte la realidad externa (texto, binario, URL) en datos internos procesables. Sin el, el sistema no puede recibir informacion del entorno."),
        ("Analista TGS", "Procesador / nucleo", "Aplica el marco TGS. Aqui ocurre el comportamiento EMERGENTE: el analisis que ningun agente podria producir solo."),
        ("Diagramador", "Transductor de salida", "Convierte el analisis interno en una representacion visual (Mermaid) que el entorno (usuario) puede consumir."),
        ("Manager", "Control / retroalimentacion", "Implementa retroalimentacion NEGATIVA: detecta inconsistencias y las corrige antes de entregar. Es el mecanismo homeostasico del sistema."),
    ]
    add_table(doc,
        ["Agente", "Rol TGS", "Justificacion"],
        agent_tgs,
        col_widths=[1.3, 1.8, 3.4])

    add_heading(doc, "17.4 Acoplamientos entre agentes", 2)
    couplings = [
        ("Manager", "Extractor", "Fuerte", "El Manager depende directamente del output del Extractor"),
        ("Manager", "Analista TGS", "Fuerte", "El analisis TGS es el producto central del sistema"),
        ("Manager", "Diagramador", "Debil", "Si el diagrama falla, el analisis textual sigue siendo util"),
        ("Extractor", "Analista TGS", "Secuencial", "El Analista no opera sin el output previo del Extractor"),
        ("Analista TGS", "Diagramador", "Secuencial", "El Diagramador necesita el analisis completo"),
        ("Todos", "Manager", "Reciproco", "El Manager recibe todos los outputs y puede corregir cualquiera"),
    ]
    add_table(doc,
        ["Origen", "Destino", "Tipo", "Justificacion"],
        couplings,
        col_widths=[1.2, 1.5, 1.2, 2.6])

    add_heading(doc, "17.5 Retroalimentacion del sistema", 2)
    retro = [
        ("Negativa (principal)", "El Manager revisa los 3 outputs. Si detecta inconsistencias (subsistema en el diagrama que no existe en el analisis), las corrige directamente al ensamblar el JSON final. Mantiene la homeostasis del output."),
        ("Negativa (usuario)", "Si el usuario indica que el analisis es incorrecto, puede enviar mas contexto. El sistema inicia un nuevo ciclo. El usuario es un lazo de retroalimentacion externo."),
    ]
    add_table(doc,
        ["Tipo", "Descripcion"],
        retro,
        col_widths=[2.0, 4.5])

    add_heading(doc, "17.6 Estados del sistema", 2)
    states = [
        ("Inactivo", "El sistema espera un mensaje en Telegram", "Mensaje recibido -> Procesando"),
        ("Procesando", "OpenClaw recibio el mensaje y llamo al backend", "Analisis completo -> Respondiendo"),
        ("Respondiendo", "OpenClaw envia la respuesta al usuario", "Envio exitoso -> Inactivo"),
        ("Publicando", "Usuario envio /publish; skill tgs-publish esta activa", "Publicacion exitosa -> Confirmando"),
        ("Confirmando", "OpenClaw envia el enlace del canal al usuario", "Envio exitoso -> Inactivo"),
        ("Error", "Fallo en cualquier etapa", "Se envia mensaje de error -> Inactivo"),
    ]
    add_table(doc,
        ["Estado", "Descripcion", "Transicion siguiente"],
        states,
        col_widths=[1.5, 2.5, 2.5])

    add_heading(doc, "17.7 Nivel de complejidad", 2)
    add_para(doc, "Nivel: COMPLEJO", bold=True, space_after=4)
    complexity_reasons = [
        "Emergencia: el analisis TGS final emerge de la interaccion de los 4 agentes, no puede ser producido por ninguno solo",
        "Retroalimentacion negativa: el Manager implementa homeostasis sobre el output",
        "No-linealidad: el mismo input puede producir analisis ligeramente distintos (LLM estocastico)",
        "Adaptacion: el sistema se adapta a inputs de dominios completamente distintos sin requerir configuracion especifica",
        "Memoria episodica (skill analysis-memory): el sistema acumula historia de analisis por usuario",
        "Variedad de canales (principio de Ashby): multiple canales de entrada y salida amplian la variedad del sistema",
    ]
    for r in complexity_reasons:
        add_bullet(doc, r)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # 18. CONCEPTOS TGS EN EL CODIGO
    # -----------------------------------------------------------------------
    add_heading(doc, "18. Conceptos TGS Aplicados en el Codigo", 1)

    add_para(doc,
        "Esta seccion conecta cada concepto teorico de TGS con su implementacion "
        "concreta en el proyecto.", space_after=6)

    mappings = [
        ("Emergencia",
         "El analisis TGS final (17 campos) no puede ser producido por ningun agente individual. "
         "El Extractor solo extrae texto. El Analista solo aplica TGS. El Diagramador solo hace Mermaid. "
         "El Manager solo valida. La emergencia ocurre cuando los 4 trabajan en secuencia.",
         "crew_setup.py: Crew(process=Process.sequential).kickoff()"),
        ("Retroalimentacion negativa",
         "El Manager compara el output ensamblado contra el schema TGSAnalysis. Si hay subsistemas "
         "en el diagrama que no existen en el analisis, los corrige. Esto mantiene la coherencia "
         "(homeostasis) del output.",
         "agents/manager.py: build_manager_agent()"),
        ("Frontera del sistema",
         "Los schemas Pydantic son la frontera tecnica del sistema. Cualquier JSON que no cumple "
         "el schema es rechazado. Los datos validos estan 'dentro'; los invalidos son rechazados "
         "en la frontera.",
         "schemas/tgs_output.py: class TGSAnalysis(BaseModel)"),
        ("Sensor (transductor de entrada)",
         "Las herramientas del Extractor (PdfReaderTool, ImageReaderTool, UrlFetcherTool) convierten "
         "senales del entorno (archivos binarios, URLs) en datos procesables internamente. Son los "
         "sensores del sistema.",
         "tools/pdf_reader.py, image_reader.py, url_fetcher.py"),
        ("Transductor de salida",
         "El Diagramador convierte la representacion interna (JSON TGS) en una representacion "
         "que el entorno puede consumir (codigo Mermaid -> imagen PNG via mermaid.ink).",
         "agents/diagramador.py"),
        ("Acoplamiento debil",
         "Si el Diagramador falla (produce codigo Mermaid invalido), el sistema no falla "
         "completamente: n8n tiene continueOnFail en el nodo Send Diagram. El analisis "
         "textual se entrega aunque el diagrama no se renderice.",
         "n8n workflow: nodo Send Diagram con continueOnFail=true"),
        ("Principio de Ashby (variedad requerida)",
         "El sistema acepta 4 tipos de input (texto, PDF, imagen, URL) para poder manejar "
         "la variedad del entorno. El Extractor tiene herramientas diferentes segun el tipo, "
         "aplicando el principio de que el controlador debe tener tanta variedad como el sistema "
         "controlado.",
         "agents/extractor.py: tools = [...] if input_type in ('pdf','image','url') else []"),
        ("Proceso secuencial vs jerarquico",
         "El proyecto originalmente usaba Process.hierarchical (el Manager orquestaba y delegaba "
         "a los agentes). Esto generaba 8-12 llamadas al LLM por analisis (latencia 8-12 min). "
         "Cambiar a Process.sequential redujo las llamadas a 4-8 (latencia 2-4 min). Commit: 40ed33d.",
         "crew_setup.py: Crew(process=Process.sequential, ...)"),
        ("Caja negra",
         "Para el usuario, el sistema es una caja negra: envia contenido por Telegram y recibe "
         "el analisis TGS. No necesita saber que internamente hay 4 agentes, un workflow de n8n, "
         "y un schema Pydantic. La API /analyze es la interfaz de la caja negra para los integradores.",
         "main.py: POST /analyze"),
    ]

    for concept, explanation, code_ref in mappings:
        add_para(doc, concept, bold=True, space_after=2)
        add_para(doc, explanation, space_after=2)
        add_para(doc, f"En el codigo: {code_ref}", italic=True, space_after=6)
        add_divider(doc)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # 19. PREGUNTAS DE PROFUNDIZACION
    # -----------------------------------------------------------------------
    add_heading(doc, "19. Preguntas de Profundizacion", 1)

    add_para(doc,
        "Estas preguntas son utiles para la presentacion con el profesor y para "
        "demostrar comprension profunda del proyecto bajo TGS.", space_after=6)

    questions = [
        ("El LLM externo (DeepSeek, Groq, Anthropic), es parte del entorno o de la frontera del sistema?",
         "Segun el criterio de CONTROL: si el sistema no controla el componente, esta en el entorno. "
         "El sistema no controla el LLM: no puede modificar sus pesos, no garantiza sus outputs, "
         "no tiene acceso a su infraestructura. Por tanto, el LLM es parte del ENTORNO, no del sistema."),
        ("Como cambiaria la clasificacion del sistema si se agrega memoria persistente entre sesiones?",
         "Actualmente el sistema es discreto y sin memoria entre sesiones (cada analisis es independiente). "
         "Con memoria persistente (base de datos) el sistema acumularia historia, lo que podria hacerlo "
         "mas COMPLEJO (ya tiene algo de memoria via analysis-memory skill) y cambiaria la clasificacion "
         "de complejidad de complejo a potencialmente caotico si la memoria influye en analisis futuros."),
        ("Por que el Manager usa retroalimentacion NEGATIVA y no positiva?",
         "Retroalimentacion negativa = el sistema detecta desviaciones y las CORRIGE para volver al "
         "estado deseado (homeostasis). Retroalimentacion positiva = el sistema AMPLIFICA las desviaciones. "
         "El Manager detecta inconsistencias y las CORRIGE para que el output cumpla el schema TGSAnalysis. "
         "Eso es reducir la desviacion, no amplificarla. Por tanto es retroalimentacion negativa."),
        ("Que tipo de acoplamiento existe entre n8n y CrewAI?",
         "SECUENCIAL: n8n llama a CrewAI, espera su respuesta, y luego continua con el formateo "
         "y envio al usuario. Ademas es FUERTE porque si CrewAI falla, n8n no puede entregar el "
         "analisis (aunque puede entregar un mensaje de error). No es reciproco porque CrewAI "
         "nunca llama a n8n; solo responde cuando n8n lo llama."),
        ("Es el Manager un subsistema de control puro o tambien cumple funciones de procesamiento?",
         "Segun Bertalanffy, control puro seria solo comparar con un estandar y generar senales "
         "correctivas. El Manager hace eso (valida contra el schema TGSAnalysis), PERO tambien "
         "procesa: ensambla el JSON final integrando los 3 outputs. Por tanto cumple funciones "
         "de CONTROL Y PROCESAMIENTO. Es un caso de subsistema con roles multiples, lo cual "
         "es comun en sistemas complejos."),
        ("Como afecta la variabilidad estocastica del LLM a la homeostasis del sistema?",
         "El LLM puede producir outputs ligeramente distintos en cada ejecucion. Esto amenaza "
         "la homeostasis (consistencia del output). Los mecanismos de compensacion son: (1) "
         "temperatura=0.3 reduce pero no elimina la variabilidad, (2) el schema Pydantic valida "
         "que el JSON sea valido (frontera de validacion), (3) el Manager corrige inconsistencias "
         "logicas aunque el JSON sea valido. Si el LLM produce un JSON invalido, el sistema "
         "rechaza el output y devuelve un error en lugar de datos corruptos."),
    ]

    for i, (q, a) in enumerate(questions, 1):
        add_para(doc, f"{i}. {q}", bold=True, space_after=4)
        add_para(doc, a, space_after=8)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # 20. GLOSARIO
    # -----------------------------------------------------------------------
    add_heading(doc, "20. Glosario", 1)

    glossary = [
        ("AgentAI / CrewAI", "Framework Python para sistemas multiagente. Permite definir agentes con roles y encadenarlos en procesos."),
        ("FastAPI", "Framework Python para APIs HTTP. Genera documentacion Swagger automaticamente. Usado para el endpoint /analyze."),
        ("Pydantic", "Libreria Python para validacion de datos con tipos. Garantiza que el JSON del LLM sea valido y completo."),
        ("Docker Compose", "Herramienta para definir y correr aplicaciones multi-contenedor. El archivo compose.yml define los 3 servicios."),
        ("n8n", "Plataforma de automatizacion de workflows low-code. En este proyecto recibe peticiones HTTP y llama a CrewAI."),
        ("OpenClaw", "Gateway de bots de Telegram basado en skills (archivos Markdown + scripts). Es quien posee el token del bot."),
        ("Mermaid", "Lenguaje de texto para generar diagramas. El Diagramador produce codigo Mermaid que mermaid.ink convierte en imagen PNG."),
        ("Skill (OpenClaw)", "Un archivo SKILL.md con instrucciones en lenguaje natural + scripts opcionales. Define un comportamiento especifico del bot."),
        ("Process.sequential (CrewAI)", "Modo de ejecucion donde las tareas corren en orden estricto, una por una. Cada tarea recibe el output de las anteriores como contexto."),
        ("Process.hierarchical (CrewAI)", "Modo donde un agente manager orquesta y delega a otros agentes. Genera mas llamadas al LLM. NO se usa en este proyecto."),
        ("output_pydantic (CrewAI)", "Parametro de Task que valida el output del agente contra un schema Pydantic. Si el JSON es invalido, CrewAI reintenta."),
        ("mermaid.ink", "Servicio web gratuito que recibe codigo Mermaid codificado en la URL y devuelve una imagen PNG. Usado para enviar el diagrama por Telegram."),
        ("asyncio.to_thread", "Funcion Python que ejecuta una funcion sincrona en un thread separado sin bloquear el event loop de FastAPI."),
        ("ReAct (ciclo)", "Paradigma de agentes: Razonar -> Actuar -> Observar. Cada iteracion puede generar una llamada al LLM. max_iter=5 limita el numero de ciclos."),
        ("litellm", "Libreria que unifica multiples proveedores de LLM bajo una interfaz comun. Usada en el bloque de Anthropic para evitar el error 'compiled grammar too large'."),
        ("is_litellm=True", "Parametro de CrewAI LLM que fuerza el uso de litellm en lugar del provider nativo. Necesario para Anthropic con schemas Pydantic grandes."),
        ("VPS", "Virtual Private Server. Servidor virtual en la nube donde corre el sistema en produccion (Hostinger en este proyecto)."),
        ("Nginx", "Servidor web usado como proxy inverso. Recibe el trafico HTTPS en el puerto 443 y lo enruta a n8n en el puerto 5678."),
    ]
    add_table(doc,
        ["Termino", "Definicion"],
        glossary,
        col_widths=[2.0, 4.5])

    # -----------------------------------------------------------------------
    # Final
    # -----------------------------------------------------------------------
    doc.add_page_break()
    final = doc.add_paragraph()
    final.alignment = WD_ALIGN_PARAGRAPH.CENTER
    final.paragraph_format.space_before = Pt(80)
    r = final.add_run("Fin del documento")
    r.italic = True
    r.font.color.rgb = RGBColor(0xAA, 0xAA, 0xAA)
    r.font.size = Pt(10)

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = sub.add_run(
        "Santiago Valencia Leon\n"
        "github.com/Gartner24/tgs-mapper-agent\n"
        "Teoria General de Sistemas — UTP 2026"
    )
    r2.font.size = Pt(9)
    r2.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

    # Save
    out = os.path.abspath(OUTPUT)
    doc.save(out)
    print(f"Saved: {out}")


if __name__ == "__main__":
    build()
