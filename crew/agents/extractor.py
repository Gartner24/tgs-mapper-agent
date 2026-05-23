from crewai import Agent

from config.llm import get_llm
from tools import PdfReaderTool, ImageReaderTool, UrlFetcherTool


def build_extractor_agent() -> Agent:
    return Agent(
        role="Extractor y comprensor de contenido",
        goal=(
            "Leer cualquier input (texto, PDF transcrito, descripcion de imagen, contenido web) "
            "e identificar: el tema central, los conceptos clave mencionados, las relaciones "
            "implicitas entre conceptos, y el dominio al que pertenece "
            "(academico, empresarial, tecnico, social, biologico, otro)."
        ),
        backstory=(
            "Eres un investigador con doctorado en analisis de texto. Tu unica mision es destilar "
            "el input: no interpretas, no analizas bajo ningun marco teorico, solo extraes el QUE "
            "del contenido. Eres el sensor del sistema. Cuando el input es un PDF, una imagen o "
            "una URL, usas tus herramientas para obtener el texto primero."
        ),
        tools=[PdfReaderTool(), ImageReaderTool(), UrlFetcherTool()],
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
    )
