from pydantic import BaseModel, Field
from typing import Literal, Optional


class AnalyzeRequest(BaseModel):
    input_type: Literal["text", "url", "pdf", "image"]
    content: str = Field(description="Plain text, URL, or base64-encoded binary")
    user_id: Optional[str] = Field(default=None, description="Telegram chat_id, optional")
