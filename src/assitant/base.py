from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BaseAssistant(ABC):
    """Base class for AI assistants."""

    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response for the given prompt."""
        pass

    @abstractmethod
    async def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> str:
        """Generate a response in a chat context."""
        pass

    @abstractmethod
    async def analyze_image(self, image_data: bytes, prompt: str) -> str:
        """Analyze an image and generate a response based on the prompt."""
        pass

    @abstractmethod
    async def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings for the given text."""
        pass

class AIMessage:
    """Represents a message in an AI conversation."""
    def __init__(
        self,
        role: str,
        content: str,
        name: Optional[str] = None,
        function_call: Optional[Dict[str, Any]] = None
    ):
        self.role = role
        self.content = content
        self.name = name
        self.function_call = function_call

    def to_dict(self) -> Dict[str, Any]:
        """Convert the message to a dictionary format."""
        message = {"role": self.role, "content": self.content}
        if self.name:
            message["name"] = self.name
        if self.function_call:
            message["function_call"] = self.function_call
        return message

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AIMessage':
        """Create a message instance from a dictionary."""
        return cls(
            role=data["role"],
            content=data["content"],
            name=data.get("name"),
            function_call=data.get("function_call")
        )

class AIConversation:
    """Manages a conversation with an AI assistant."""
    def __init__(self):
        self.messages: List[AIMessage] = []

    def add_message(self, message: AIMessage) -> None:
        """Add a message to the conversation."""
        self.messages.append(message)

    def get_messages(self) -> List[AIMessage]:
        """Get all messages in the conversation."""
        return self.messages

    def clear(self) -> None:
        """Clear all messages from the conversation."""
        self.messages = []

    def to_dict_list(self) -> List[Dict[str, Any]]:
        """Convert all messages to a list of dictionaries."""
        return [msg.to_dict() for msg in self.messages]