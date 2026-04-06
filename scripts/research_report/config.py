"""Shared configuration: LLM initialisation and environment setup."""

import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()


def get_llm(temperature: float = 0):
    """Return a ChatModel using env-configurable provider and model name.

    Environment variables (all optional, sensible defaults):
        MODEL_PROVIDER  – "openai" (default), "anthropic", "ollama"
        MODEL_NAME      – "gpt-4o-mini" (default)
    """
    provider = os.getenv("MODEL_PROVIDER", "openai")
    model = os.getenv("MODEL_NAME", "gpt-4o-mini")
    return init_chat_model(f"{provider}:{model}", temperature=temperature)
