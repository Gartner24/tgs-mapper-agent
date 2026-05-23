import time
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from loguru import logger

from schemas.input import AnalyzeRequest
from schemas.tgs_output import TGSAnalysis
from crew_setup import run_analysis

VERSION = "0.1.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"TGS Mapper Agent v{VERSION} starting up")
    yield
    logger.info("TGS Mapper Agent shutting down")


app = FastAPI(
    title="TGS Mapper Agent",
    description=(
        "Servicio multi-agente que analiza cualquier input bajo el marco de la "
        "Teoria General de Sistemas (TGS). Recibe texto, PDF (base64), imagen (base64) "
        "o URL y devuelve un analisis TGS estructurado con diagrama Mermaid."
    ),
    version=VERSION,
    lifespan=lifespan,
)


def _analysis_to_markdown(analysis: TGSAnalysis) -> str:
    lines = [
        f"# Analisis TGS: {analysis.tema}",
        f"\n## Resumen\n{analysis.resumen}",
        f"\n## Proposito\n{analysis.proposito}",
        f"\n## Tipo de sistema",
        f"- Abierto/cerrado: **{analysis.tipo_de_sistema.abierto_o_cerrado}**",
        f"- Natural/artificial: **{analysis.tipo_de_sistema.natural_o_artificial}**",
        f"- Deterministico/estocastico: **{analysis.tipo_de_sistema.deterministico_o_estocastico}**",
        f"- Continuo/discreto: **{analysis.tipo_de_sistema.continuo_o_discreto}**",
        f"- Justificacion: {analysis.tipo_de_sistema.justificacion}",
        f"\n## Frontera\n{analysis.frontera.descripcion}",
        f"- Dentro: {', '.join(analysis.frontera.elementos_dentro)}",
        f"- Fuera: {', '.join(analysis.frontera.elementos_fuera)}",
        f"\n## Entorno\n{analysis.entorno.descripcion}",
        f"- Variables externas: {', '.join(analysis.entorno.variables_externas)}",
        f"\n## Suprasistema\n{analysis.suprasistema}",
        "\n## Elementos",
    ]
    for el in analysis.elementos:
        lines.append(f"- **{el.nombre}**: {el.rol}")
    lines.append("\n## Subsistemas")
    for sub in analysis.subsistemas:
        lines.append(f"- **{sub.nombre}**: {sub.proposito}")
    lines.append("\n## Relaciones")
    for rel in analysis.relaciones:
        lines.append(f"- {rel.origen} -> {rel.destino} [{rel.tipo_acoplamiento}]: {rel.descripcion}")
    lines.append("\n## Caja negra")
    lines.append(f"- Entradas: {', '.join(analysis.caja_negra.entradas)}")
    lines.append(f"- Procesos: {', '.join(analysis.caja_negra.procesos)}")
    lines.append(f"- Salidas: {', '.join(analysis.caja_negra.salidas)}")
    lines.append("\n## Retroalimentacion")
    for retro in analysis.retroalimentacion:
        lines.append(f"- [{retro.tipo}]: {retro.descripcion}")
    lines.append(f"\n## Complejidad\n**{analysis.complejidad.nivel}**: {analysis.complejidad.justificacion}")
    if analysis.supuestos:
        lines.append("\n## Supuestos")
        for s in analysis.supuestos:
            lines.append(f"- {s}")
    if analysis.preguntas_para_profundizar:
        lines.append("\n## Preguntas para profundizar")
        for q in analysis.preguntas_para_profundizar:
            lines.append(f"- {q}")
    return "\n".join(lines)


@app.get(
    "/health",
    tags=["Sistema"],
    summary="Health check",
    description="Verifica que el servicio este corriendo correctamente.",
)
async def health():
    return {"ok": True, "version": VERSION}


@app.post(
    "/analyze",
    tags=["Analisis"],
    summary="Analizar input bajo el marco TGS",
    description=(
        "Recibe un input (texto, URL, PDF en base64 o imagen en base64) y devuelve "
        "un analisis estructurado bajo la Teoria General de Sistemas, incluyendo un "
        "diagrama Mermaid del sistema identificado."
    ),
)
async def analyze(request: AnalyzeRequest):
    start = time.monotonic()
    logger.info(f"Analyze request: input_type={request.input_type!r} user_id={request.user_id!r}")

    stage = "extractor"
    try:
        stage = "extractor"
        analysis: TGSAnalysis = run_analysis(
            input_type=request.input_type,
            content=request.content,
        )
        stage = "manager"

        duration = round(time.monotonic() - start, 2)
        model_used = os.getenv("LLM_MODEL", "deepseek/deepseek-chat")
        markdown = _analysis_to_markdown(analysis)

        logger.info(f"Analysis complete in {duration}s")
        return {
            "ok": True,
            "analysis": analysis.model_dump(),
            "markdown": markdown,
            "mermaid": analysis.diagrama_mermaid,
            "metadata": {
                "duration_seconds": duration,
                "model_used": f"openrouter/{model_used}",
                "validated_by_manager": True,
                "corrections_applied": [],
            },
        }

    except Exception as exc:
        duration = round(time.monotonic() - start, 2)
        logger.error(f"Analysis failed at stage={stage!r} after {duration}s: {exc}")
        return JSONResponse(
            status_code=500,
            content={"ok": False, "error": str(exc), "stage": stage},
        )
