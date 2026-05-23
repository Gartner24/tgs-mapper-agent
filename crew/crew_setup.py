from crewai import Crew, Process
from loguru import logger

from agents import (
    build_extractor_agent,
    build_analista_tgs_agent,
    build_diagramador_agent,
    build_manager_agent,
)
from tasks import (
    build_extraction_task,
    build_analysis_task,
    build_diagram_task,
    build_coordination_task,
)
from schemas.tgs_output import TGSAnalysis


def build_crew(input_type: str, content: str) -> Crew:
    extractor = build_extractor_agent()
    analista = build_analista_tgs_agent()
    diagramador = build_diagramador_agent()
    manager = build_manager_agent()

    t_extraction = build_extraction_task(agent=extractor, input_type=input_type, content=content)
    t_analysis = build_analysis_task(agent=analista, context=[t_extraction])
    t_diagram = build_diagram_task(agent=diagramador, context=[t_analysis])
    t_coordination = build_coordination_task(
        agent=manager,
        context=[t_extraction, t_analysis, t_diagram],
    )

    logger.info(f"Assembling hierarchical Crew for input_type={input_type!r}")

    return Crew(
        agents=[extractor, analista, diagramador],
        tasks=[t_extraction, t_analysis, t_diagram, t_coordination],
        process=Process.hierarchical,
        manager_agent=manager,
        verbose=True,
    )


def run_analysis(input_type: str, content: str) -> TGSAnalysis:
    crew = build_crew(input_type=input_type, content=content)
    result = crew.kickoff()
    if isinstance(result.pydantic, TGSAnalysis):
        return result.pydantic
    raise ValueError(f"Unexpected crew output type: {type(result.pydantic)}")
