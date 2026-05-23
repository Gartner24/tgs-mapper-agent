import os

from crewai import LLM
from loguru import logger


def get_llm() -> LLM:
    provider = os.getenv("LLM_PROVIDER", "groq").lower()
    model = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
    temperature = 0.3
    max_tokens = 8000

    if provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set")
        logger.info(f"LLM initialized: anthropic/{model} (via litellm)")
        # is_litellm=True forces the litellm path instead of CrewAI's native
        # Anthropic provider, whose strict structured-output compiles the large
        # TGS schemas into a grammar Anthropic rejects ("compiled grammar too large").
        return LLM(
            model=f"anthropic/{model}",
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            is_litellm=True,
        )

    if provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not set")
        logger.info(f"LLM initialized: groq/{model}")
        return LLM(
            model=f"groq/{model}",
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    if provider == "openrouter":
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise RuntimeError("OPENROUTER_API_KEY is not set")
        logger.info(f"LLM initialized: openrouter/{model}")
        return LLM(
            model=f"openrouter/{model}",
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            temperature=temperature,
            max_tokens=max_tokens,
        )

    raise RuntimeError(f"Unsupported LLM_PROVIDER: {provider!r}")
