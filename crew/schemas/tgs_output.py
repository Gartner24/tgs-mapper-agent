from pydantic import BaseModel
from typing import Literal


class TipoSistema(BaseModel):
    abierto_o_cerrado: Literal["abierto", "cerrado", "mixto"]
    natural_o_artificial: Literal["natural", "artificial", "sociotecnico"]
    deterministico_o_estocastico: Literal["deterministico", "estocastico", "mixto"]
    continuo_o_discreto: Literal["continuo", "discreto", "hibrido"]
    justificacion: str


class Frontera(BaseModel):
    descripcion: str
    elementos_dentro: list[str]
    elementos_fuera: list[str]


class Entorno(BaseModel):
    descripcion: str
    variables_externas: list[str]


class Elemento(BaseModel):
    nombre: str
    rol: str


class Subsistema(BaseModel):
    nombre: str
    proposito: str
    elementos_clave: list[str]


class Relacion(BaseModel):
    origen: str
    destino: str
    tipo_acoplamiento: Literal["fuerte", "debil", "secuencial", "reciproco"]
    descripcion: str


class CajaNegra(BaseModel):
    entradas: list[str]
    procesos: list[str]
    salidas: list[str]


class Retroalimentacion(BaseModel):
    tipo: Literal["positiva", "negativa"]
    descripcion: str


class Transicion(BaseModel):
    hacia: str
    disparador: str


class EstadoTransicion(BaseModel):
    estado: str
    transiciones: list[Transicion]


class Complejidad(BaseModel):
    nivel: Literal["simple", "complicado", "complejo", "caotico"]
    justificacion: str


class TGSAnalysis(BaseModel):
    tema: str
    resumen: str
    proposito: str
    tipo_de_sistema: TipoSistema
    frontera: Frontera
    entorno: Entorno
    suprasistema: str
    elementos: list[Elemento]
    subsistemas: list[Subsistema]
    relaciones: list[Relacion]
    caja_negra: CajaNegra
    retroalimentacion: list[Retroalimentacion]
    estados_y_transiciones: list[EstadoTransicion]
    complejidad: Complejidad
    diagrama_mermaid: str
    supuestos: list[str]
    preguntas_para_profundizar: list[str]
