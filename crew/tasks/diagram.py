from crewai import Agent, Task

from schemas.diagram import DiagramOutput


def build_diagram_task(agent: Agent, context: list[Task]) -> Task:
    return Task(
        description=(
            "Usando el analisis TGS producido por el analista, genera un diagrama Mermaid "
            "que represente visualmente el sistema analizado.\n\n"
            "Reglas obligatorias:\n"
            "1. Usa 'graph TD' como tipo de diagrama.\n"
            "2. Representa los subsistemas como nodos.\n"
            "3. Representa las relaciones como aristas:\n"
            "   - Acoplamiento fuerte: --> (flecha solida)\n"
            "   - Acoplamiento debil: -.-> (flecha punteada)\n"
            "   - Acoplamiento secuencial: --> con etiqueta 'secuencial'\n"
            "   - Acoplamiento reciproco: <--> (flecha bidireccional)\n"
            "4. Usa subgraph para representar la frontera del sistema.\n"
            "5. MAXIMO 12 nodos en total.\n"
            "6. El campo mermaid_code debe contener SOLO el codigo Mermaid puro, "
            "SIN bloques de markdown (sin ```mermaid, sin ```), SIN explicaciones.\n"
            "7. El campo leyenda debe explicar brevemente las convenciones visuales usadas."
        ),
        expected_output=(
            "Un objeto JSON con dos campos: mermaid_code (codigo Mermaid puro, sin fences, "
            "max 12 nodos) y leyenda (texto breve explicando las convenciones del diagrama)."
        ),
        agent=agent,
        context=context,
        output_pydantic=DiagramOutput,
    )
