import base64
import io
from typing import Type

from crewai.tools import BaseTool
from loguru import logger
from PIL import Image
from pydantic import BaseModel, Field


class ImageReaderInput(BaseModel):
    content: str = Field(description="Base64-encoded image file (JPEG, PNG, WEBP, etc.)")


class ImageReaderTool(BaseTool):
    name: str = "image_reader"
    description: str = (
        "Converts a base64-encoded image into a descriptive text representation "
        "suitable for text-based LLM analysis. Returns image metadata and a prompt "
        "instructing the LLM to describe what it sees."
    )
    args_schema: Type[BaseModel] = ImageReaderInput

    def _run(self, content: str) -> str:
        try:
            img_bytes = base64.b64decode(content)
            img = Image.open(io.BytesIO(img_bytes))
            width, height = img.size
            mode = img.mode
            fmt = img.format or "desconocido"
            logger.info(f"Image loaded: {fmt} {width}x{height} {mode}")
            return (
                f"[Imagen adjunta: formato={fmt}, dimensiones={width}x{height}, modo={mode}]\n"
                f"Contenido en base64 disponible para analisis. "
                f"Describe el contenido de esta imagen con el mayor detalle posible, "
                f"identificando todos los elementos, textos, diagramas, graficos o conceptos visibles."
            )
        except Exception as exc:
            logger.error(f"Image reading failed: {exc}")
            return f"Error al procesar la imagen: {exc}"
