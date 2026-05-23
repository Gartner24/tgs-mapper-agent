from crewai import Agent

from config.llm import get_llm


def build_manager_agent() -> Agent:
    return Agent(
        role="Director del analisis TGS",
        goal=(
            "Validar la coherencia entre el contenido extraido, el analisis TGS y el diagrama "
            "generado. Detectar inconsistencias — por ejemplo, que el diagrama mencione un "
            "subsistema que no esta en el analisis, o que las relaciones referencien elementos "
            "inexistentes — y corregirlas directamente en el output final. Integrar todo en el "
            "JSON final completo de tipo TGSAnalysis."
        ),
        backstory=(
            "Eres editor en jefe y arquitecto de sistemas. Tu superpoder es ver el bosque "
            "mientras los demas ven el arbol. Nunca entregas un producto a medias: si detectas "
            "un problema, lo corriges directamente antes de cerrar. Conoces TGS profundamente y "
            "puedes evaluar si un analisis es riguroso o superficial. Tu output final siempre "
            "es un JSON que cumple el esquema TGSAnalysis al 100%, con el campo diagrama_mermaid "
            "poblado con el codigo Mermaid del diagramador."
        ),
        tools=[],
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=5,
    )
