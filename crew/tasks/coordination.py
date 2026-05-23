from crewai import Agent, Task

from schemas.tgs_output import TGSAnalysis


def build_coordination_task(agent: Agent, context: list[Task]) -> Task:
    return Task(
        description=(
            "Eres el director del analisis. Tienes acceso a los outputs de los tres agentes: "
            "el extractor, el analista TGS y el diagramador. Tu tarea final es:\n\n"
            "1. VALIDAR la coherencia entre los tres outputs:\n"
            "   - Cada subsistema en el diagrama Mermaid debe existir en 'subsistemas'.\n"
            "   - Cada relacion en el diagrama debe tener 'origen' y 'destino' validos "
            "que referencien elementos o subsistemas del analisis.\n"
            "   - El tipo de sistema y la complejidad deben ser coherentes con los subsistemas "
            "y relaciones identificados.\n"
            "   - Los supuestos deben estar documentados si el analisis los requirio.\n\n"
            "2. SI encuentras inconsistencias, indica claramente cuales son y corrígelas "
            "directamente en el output final.\n\n"
            "3. INTEGRAR todo en el JSON final completo de tipo TGSAnalysis:\n"
            "   - Copia el analisis TGS validado.\n"
            "   - Reemplaza el campo 'diagrama_mermaid' con el mermaid_code del diagramador "
            "(codigo puro, sin markdown fences).\n"
            "   - Asegurate de que 'supuestos' y 'preguntas_para_profundizar' esten completos.\n\n"
            "4. El output debe ser un TGSAnalysis 100% completo y coherente."
        ),
        expected_output=(
            "El JSON final completo de tipo TGSAnalysis, con todos los campos poblados, "
            "el campo diagrama_mermaid con el codigo Mermaid puro del diagramador, "
            "y coherencia total entre subsistemas, relaciones y diagrama."
        ),
        agent=agent,
        context=context,
        output_pydantic=TGSAnalysis,
    )
