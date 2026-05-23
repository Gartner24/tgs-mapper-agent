from pydantic import BaseModel, Field


class RelacionImplicita(BaseModel):
    concepto_a: str
    concepto_b: str
    tipo_relacion: str = Field(description="e.g. 'depende_de', 'parte_de', 'opuesto_a'")


class ExtractionResult(BaseModel):
    tema_central: str
    conceptos: list[str]
    relaciones_implicitas: list[RelacionImplicita]
    dominio: str = Field(description="academico | empresarial | tecnico | social | biologico | otro")
    resumen_objetivo: str
