from pydantic import BaseModel, Field


class DiagramOutput(BaseModel):
    mermaid_code: str = Field(description="Pure Mermaid code, no markdown fences, max 12 nodes")
    leyenda: str = Field(description="Brief legend explaining visual conventions used")
