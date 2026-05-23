import base64
import io
from typing import Type

import pdfplumber
from crewai.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field


class PdfReaderInput(BaseModel):
    content: str = Field(description="Base64-encoded PDF file content")


class PdfReaderTool(BaseTool):
    name: str = "pdf_reader"
    description: str = "Extracts plain text from a base64-encoded PDF file."
    args_schema: Type[BaseModel] = PdfReaderInput

    def _run(self, content: str) -> str:
        try:
            pdf_bytes = base64.b64decode(content)
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                pages = [page.extract_text() or "" for page in pdf.pages]
            text = "\n\n".join(p for p in pages if p.strip())
            logger.info(f"PDF extracted: {len(pdf.pages)} pages, {len(text)} chars")
            return text or "El PDF no contiene texto extraible."
        except Exception as exc:
            logger.error(f"PDF extraction failed: {exc}")
            return f"Error al leer el PDF: {exc}"
