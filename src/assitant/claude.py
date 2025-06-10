from anthropic import AsyncAnthropic
from typing import List, Dict, Any
from src.assitant.base import BaseAssistant, AIMessage
from src.config import settings # Assuming API key might be in settings
import os

# Configure the Anthropic API key
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY") # Or settings.anthropic_api_key
if not ANTHROPIC_API_KEY:
    print("Warning: ANTHROPIC_API_KEY not found in environment variables.")
    # raise ValueError("ANTHROPIC_API_KEY not found in environment variables.")

class ClaudeAssistant(BaseAssistant):
    """AI assistant powered by Anthropic's Claude models."""

    def __init__(self, model_name: str = "claude-3-opus-20240229"):
        if not ANTHROPIC_API_KEY:
            raise EnvironmentError("ANTHROPIC_API_KEY is not set. Cannot initialize ClaudeAssistant.")
        self.model_name = model_name
        self.client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response for the given prompt."""
        try:
            # Claude's message API is preferred over completion for newer models
            response = await self.client.messages.create(
                model=self.model_name,
                max_tokens=kwargs.get("max_tokens", 1024),
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Error generating Claude response: {e}")
            return f"Error: Could not get response from Claude. {e}"

    async def generate_chat_response(
        self,
        messages: List[Dict[str, str]], # Expects [{'role': 'user'/'assistant', 'content': 'text'}]
        **kwargs
    ) -> str:
        """Generate a response in a chat context."""
        # Ensure system prompt is handled correctly if present
        system_prompt = None
        formatted_messages = []
        for msg in messages:
            if msg['role'] == 'system':
                system_prompt = msg['content']
            else:
                formatted_messages.append(msg)
        
        try:
            api_params = {
                "model": self.model_name,
                "max_tokens": kwargs.get("max_tokens", 1024),
                "messages": formatted_messages
            }
            if system_prompt:
                api_params["system"] = system_prompt
            
            response = await self.client.messages.create(**api_params)
            return response.content[0].text
        except Exception as e:
            print(f"Error generating Claude chat response: {e}")
            return f"Error: Could not get chat response from Claude. {e}"

    async def analyze_image(self, image_data: bytes, prompt: str) -> str:
        """Analyze an image (Claude Vision capabilities)."""
        # import base64
        # base64_image = base64.b64encode(image_data).decode('utf-8')
        # media_type = "image/jpeg" # Or other appropriate type

        # try:
        #     response = await self.client.messages.create(
        #         model=self.model_name, # Ensure it's a vision-capable model
        #         max_tokens=1024,
        #         messages=[
        #             {
        #                 "role": "user",
        #                 "content": [
        #                     {
        #                         "type": "image",
        #                         "source": {
        #                             "type": "base64",
        #                             "media_type": media_type,
        #                             "data": base64_image,
        #                         },
        #                     },
        #                     {"type": "text", "text": prompt}
        #                 ],
        #             }
        #         ],
        #     )
        #     return response.content[0].text
        # except Exception as e:
        #     print(f"Error analyzing image with Claude: {e}")
        #     return f"Error: Could not analyze image with Claude. {e}"
        print("Claude image analysis is not fully implemented in this example.")
        return "Claude image analysis placeholder response."

    async def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings for the given text (Claude does not offer a direct embedding API like OpenAI)."""
        print("Claude does not have a dedicated public API for generating embeddings in the same way as OpenAI or Gemini. This method is a placeholder.")
        # You might use a sentence-transformer model locally or another service for embeddings if needed.
        return []

# Example Usage (for testing):
async def main():
    if not ANTHROPIC_API_KEY:
        print("Skipping ClaudeAssistant example as API key is not set.")
        return

    assistant = ClaudeAssistant()
    
    # Test simple prompt
    # prompt = "What are the main differences between Python and JavaScript?"
    # response = await assistant.generate_response(prompt)
    # print(f"Prompt: {prompt}")
    # print(f"Claude Response: {response}")

    # Test chat
    # chat_messages = [
    #     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex scientific concepts with creative flair."},
    #     {"role": "user", "content": "Tell me about black holes."}
    # ]
    # chat_response = await assistant.generate_chat_response(chat_messages)
    # print(f"Chat Response: {chat_response}")

if __name__ == "__main__":
    import asyncio
    # asyncio.run(main()) # Comment out if not running directly or if API key is an issue
    pass