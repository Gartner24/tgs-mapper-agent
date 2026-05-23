from crewai import Agent, Task

from schemas.tgs_output import TGSAnalysis


def build_analysis_task(agent: Agent, context: list[Task]) -> Task:
    return Task(
        description=(
            "Usando el resultado de la extraccion de contenido, aplica el marco completo de la "
            "Teoria General de Sistemas (TGS) para producir un analisis riguroso.\n\n"
            "Debes identificar y completar TODOS los siguientes campos:\n"
            "- tema, resumen, proposito\n"
            "- tipo_de_sistema (abierto_o_cerrado, natural_o_artificial, "
            "deterministico_o_estocastico, continuo_o_discreto, justificacion)\n"
            "- frontera (descripcion, elementos_dentro, elementos_fuera)\n"
            "- entorno (descripcion, variables_externas)\n"
            "- suprasistema\n"
            "- elementos (lista con nombre y rol de cada elemento)\n"
            "- subsistemas (lista con nombre, proposito y elementos_clave)\n"
            "- relaciones (lista con origen, destino, tipo_acoplamiento: "
            "fuerte/debil/secuencial/reciproco, descripcion)\n"
            "- caja_negra (entradas, procesos, salidas)\n"
            "- retroalimentacion (tipo: positiva/negativa, descripcion)\n"
            "- estados_y_transiciones\n"
            "- complejidad (nivel: simple/complicado/complejo/caotico, justificacion)\n"
            "- supuestos (lista de supuestos explicitos que hagas)\n"
            "- preguntas_para_profundizar (minimo 3 preguntas abiertas)\n\n"
            "Para el campo 'diagrama_mermaid' escribe 'PENDIENTE': "
            "el diagramador lo completara en el siguiente paso.\n\n"
            "Justifica cada clasificacion. No omitas ningun campo."
        ),
        expected_output=(
            "Un objeto JSON completo que cumple el esquema TGSAnalysis. "
            "El campo diagrama_mermaid debe contener la cadena 'PENDIENTE'."
        ),
        agent=agent,
        context=context,
        output_pydantic=TGSAnalysis,
    )
