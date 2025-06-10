from typing import Optional

from src.assitant.base import BaseAssistant
from src.assitant.gemini import GeminiAssistant
from src.assitant.openai import OpenAIAssistant
from src.assitant.claude import ClaudeAssistant

ASSISTANT_TYPE_GEMINI = "gemini"
ASSISTANT_TYPE_OPENAI = "openai"
ASSISTANT_TYPE_CLAUDE = "claude"


def get_assistant(
    assistant_type: str,
    model_name: Optional[str] = None
) -> BaseAssistant:
    """Factory function to get an instance of an AI assistant."""
    if assistant_type == ASSISTANT_TYPE_GEMINI:
        return GeminiAssistant(model_name=model_name or "gemini-pro")
    elif assistant_type == ASSISTANT_TYPE_OPENAI:
        return OpenAIAssistant(model_name=model_name or "gpt-3.5-turbo")
    elif assistant_type == ASSISTANT_TYPE_CLAUDE:
        # Ensure you use a valid Claude model name
        return ClaudeAssistant(model_name=model_name or "claude-3-opus-20240229") 
    else:
        raise ValueError(f"Unknown assistant type: {assistant_type}")

__all__ = [
    "BaseAssistant",
    "GeminiAssistant",
    "OpenAIAssistant",
    "ClaudeAssistant",
    "get_assistant",
    "ASSISTANT_TYPE_GEMINI",
    "ASSISTANT_TYPE_OPENAI",
    "ASSISTANT_TYPE_CLAUDE",
]