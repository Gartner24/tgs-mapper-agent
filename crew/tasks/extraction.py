from crewai import Agent, Task

from schemas.extraction import ExtractionResult


def build_extraction_task(agent: Agent, input_type: str, content: str) -> Task:
    return Task(
        description=(
            f"Analiza el siguiente input de tipo '{input_type}'.\n\n"
            f"<CONTENIDO>\n{content}\n</CONTENIDO>\n\n"
            "Tu mision es extraer y estructurar la informacion sin aplicar ningun marco teorico. "
            "Identifica: el tema central, los conceptos clave, las relaciones implicitas entre "
            "conceptos, el dominio (academico/empresarial/tecnico/social/biologico/otro) y "
            "elabora un resumen objetivo del contenido. "
            "Si el tipo de input es 'pdf', 'image' o 'url', usa la herramienta correspondiente "
            "para obtener el texto antes de analizar."
        ),
        expected_output=(
            "Un objeto JSON con los campos: tema_central, conceptos (lista de strings), "
            "relaciones_implicitas (lista de objetos con concepto_a, concepto_b, tipo_relacion), "
            "dominio y resumen_objetivo."
        ),
        agent=agent,
        output_pydantic=ExtractionResult,
    )
