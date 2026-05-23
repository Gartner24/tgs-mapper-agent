import os

from crewai import LLM
from loguru import logger


def get_llm() -> LLM:
    model = os.getenv("LLM_MODEL", "deepseek/deepseek-chat")  # TODO: verify slug at https://openrouter.ai/models
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set")
    logger.info(f"LLM initialized: openrouter/{model}")
    return LLM(
        model=f"openrouter/{model}",
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.3,
        max_tokens=8000,
    )
