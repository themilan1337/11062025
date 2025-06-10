from typing import Optional

from .base import BaseAssistant, AIMessage, AIConversation
from .openai import OpenAIAssistant


def get_assistant(
    assistant_type: str, model_name: str | None = None
) -> BaseAssistant:
    if assistant_type == "openai":
        # Here you could add logic to select different OpenAI models 
        # or configurations based on model_name or other parameters
        # For now, it defaults to the standard OpenAIAssistant
        return OpenAIAssistant(model_name=model_name) 
    else:
        # Optionally, raise an error for unsupported types or default to OpenAI
        # For this refinement, we assume only 'openai' is valid and was intended.
        # If other types were accidentally passed, this would be a good place to log/error.
        # However, the request implies 'openai' is the only intended type now.
        return OpenAIAssistant(model_name=model_name) 


__all__ = [
    "BaseAssistant",
    "AIMessage",
    "AIConversation",
    "OpenAIAssistant",
    "get_assistant",
]