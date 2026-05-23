import base64
import binascii
import io
from typing import Type

import pdfplumber
from crewai.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field

_MAX_PDF_BYTES = 20_000_000
_MAX_OUTPUT_CHARS = 40_000


class PdfReaderInput(BaseModel):
    content: str = Field(description="Base64-encoded PDF file content")


class PdfReaderTool(BaseTool):
    name: str = "pdf_reader"
    description: str = "Extracts plain text from a base64-encoded PDF file."
    args_schema: Type[BaseModel] = PdfReaderInput

    def _run(self, content: str) -> str:
        if len(content) > (_MAX_PDF_BYTES * 4 // 3 + 100):
            return "Error: el PDF supera el tamano maximo permitido (20 MB)."
        try:
            pdf_bytes = base64.b64decode(content)
        except binascii.Error:
            return "Error: el contenido no es un PDF valido en base64."
        if len(pdf_bytes) > _MAX_PDF_BYTES:
            return "Error: el PDF supera el tamano maximo permitido (20 MB)."
        if pdf_bytes[:4] != b"%PDF":
            return "Error: el archivo no es un PDF valido."
        try:
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                pages = [page.extract_text() or "" for page in pdf.pages]
                page_count = len(pdf.pages)
            text = "\n\n".join(p for p in pages if p.strip())
            logger.info(f"PDF extracted: {page_count} pages, {len(text)} chars")
            if len(text) > _MAX_OUTPUT_CHARS:
                text = text[:_MAX_OUTPUT_CHARS]
            return text or "El PDF no contiene texto extraible."
        except Exception as exc:
            logger.error(f"PDF extraction failed: {exc}")
            return f"Error al leer el PDF: {exc}"
