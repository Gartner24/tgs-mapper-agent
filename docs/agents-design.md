# Agents Design — TGS Mapper Agent

## Process

`Process.hierarchical` with `manager_agent=Manager`.
The Manager orchestrates the 3 worker agents and executes the final
coordination task. All 4 tasks are listed in `Crew(tasks=[...])`.

## Agent 1 — Extractor (`agents/extractor.py`)

| Field | Value |
|---|---|
| Role | Extractor y comprensor de contenido |
| Allow delegation | False |
| Tools | PdfReaderTool, ImageReaderTool, UrlFetcherTool |
| Output schema | `ExtractionResult` |

**Responsibility:** Read any input format and identify the central theme,
key concepts, implicit relationships, and domain. No TGS interpretation —
only extracts the "what" of the content.

**Tools:**
- `PdfReaderTool` — decodes base64 PDF, extracts text with pdfplumber
- `ImageReaderTool` — decodes base64 image, returns metadata + description prompt
- `UrlFetcherTool` — fetches URL, strips HTML with BeautifulSoup, truncates at 12 000 chars

**Output fields:** `tema_central`, `conceptos`, `relaciones_implicitas`,
`dominio`, `resumen_objetivo`

---

## Agent 2 — Analyst TGS (`agents/analista_tgs.py`)

| Field | Value |
|---|---|
| Role | Analista experto en Teoria General de Sistemas |
| Allow delegation | False |
| Tools | None |
| Output schema | `TGSAnalysis` (with `diagrama_mermaid="PENDIENTE"`) |

**Responsibility:** Apply the complete TGS framework to the extracted content.
Identify all 14 fields of `TGSAnalysis`. Document explicit assumptions in
`supuestos`. Produce at least 3 `preguntas_para_profundizar`.

**Key constraint:** Writes `"PENDIENTE"` in `diagrama_mermaid` — the Diagrammer
fills it in the next step; the Manager's coordination task replaces it with the
final Mermaid code.

---

## Agent 3 — Diagrammer (`agents/diagramador.py`)

| Field | Value |
|---|---|
| Role | Diagramador de sistemas complejos |
| Allow delegation | False |
| Tools | None |
| Output schema | `DiagramOutput` |

**Responsibility:** Convert the TGS analysis into a Mermaid diagram.

**Hard constraints enforced in backstory and task description:**
- Maximum 12 nodes
- `graph TD` as diagram type
- `subgraph` for the system boundary
- Arrow styles by coupling type:
  - Strong: `-->`
  - Weak: `-.->` (dashed)
  - Sequential: `-->` with label
  - Reciprocal: `<-->`
- `mermaid_code` field: pure Mermaid code, NO markdown fences, NO backticks

**Output fields:** `mermaid_code`, `leyenda`

---

## Agent 4 — Manager (`agents/manager.py`)

| Field | Value |
|---|---|
| Role | Director del analisis TGS |
| Allow delegation | True |
| Tools | None |
| Output schema | `TGSAnalysis` (complete, final) |
| Special | `manager_agent` of the hierarchical Crew |

**Responsibility:**
1. Coordinate the 3 worker agents (via `Process.hierarchical`)
2. Validate consistency across the 3 outputs:
   - Every subsystem in the Mermaid diagram must exist in `subsistemas`
   - Every relation must reference valid `origen` and `destino`
   - `tipo_de_sistema` and `complejidad` must be coherent with the analysis
3. Request corrections by re-delegating if inconsistencies are found
4. Assemble the final `TGSAnalysis`:
   - Copy the validated TGS analysis
   - Replace `diagrama_mermaid` with `DiagramOutput.mermaid_code`
   - Finalize `supuestos` and `preguntas_para_profundizar`

**Task context:** receives `[t_extraction, t_analysis, t_diagram]` as context,
giving it access to all intermediate outputs.

---

## Task dependency chain

```
build_extraction_task(extractor, input_type, content)
    context: []

build_analysis_task(analista, context=[t_extraction])
    context: [ExtractionResult]

build_diagram_task(diagramador, context=[t_analysis])
    context: [TGSAnalysis*]

build_coordination_task(manager, context=[t_extraction, t_analysis, t_diagram])
    context: [ExtractionResult, TGSAnalysis*, DiagramOutput]
    output:  TGSAnalysis (final)
```

---

## Consistency validation rules (Manager)

The coordination task description instructs the Manager to check:

1. **Diagram-analysis coherence:** every node in `mermaid_code` must correspond
   to a `subsistema.nombre` or `elemento.nombre` in the analysis
2. **Relation validity:** every `Relacion.origen` and `Relacion.destino` must
   reference a valid subsystem or element
3. **Type coherence:** `tipo_de_sistema` classifications must be consistent with
   the identified subsystems and relations
4. **Completeness:** `supuestos` must be non-empty if the input was ambiguous;
   `preguntas_para_profundizar` must have at least 3 items

---

## LLM shared configuration

All 4 agents call `get_llm()` from `config/llm.py`:

```python
LLM(
    model=f"openrouter/{os.getenv('LLM_MODEL', 'deepseek/deepseek-chat')}",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0.3,
    max_tokens=8000,
)
```

Temperature 0.3 keeps outputs structured and consistent while allowing the
model to handle diverse input domains.
