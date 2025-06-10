from openai import AsyncOpenAI # Use AsyncOpenAI for FastAPI
from typing import List, Dict, Any
from src.assitant.base import BaseAssistant, AIMessage
from src.config import settings # Assuming API key might be in settings
import os

# Configure the OpenAI API key
# It's better to load this from environment variables or a config file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # Or settings.openai_api_key
if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY not found in environment variables.")
    # raise ValueError("OPENAI_API_KEY not found in environment variables.")

class OpenAIAssistant(BaseAssistant):
    """AI assistant powered by OpenAI's GPT models."""

    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        if not OPENAI_API_KEY:
            raise EnvironmentError("OPENAI_API_KEY is not set. Cannot initialize OpenAIAssistant.")
        self.model_name = model_name
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response for the given prompt (using chat completions)."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating OpenAI response: {e}")
            return f"Error: Could not get response from OpenAI. {e}"

    async def generate_chat_response(
        self,
        messages: List[Dict[str, str]], # Expects [{'role': 'user'/'assistant'/'system', 'content': 'text'}]
        **kwargs
    ) -> str:
        """Generate a response in a chat context."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                **kwargs
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating OpenAI chat response: {e}")
            return f"Error: Could not get chat response from OpenAI. {e}"

    async def analyze_image(self, image_data: bytes, prompt: str) -> str:
        """Analyze an image (using GPT-4 Vision if available and configured)."""
        # This requires a model like gpt-4-vision-preview and specific formatting
        # For simplicity, this is a placeholder. Actual implementation needs base64 encoding.
        # from openai.types.chat import ChatCompletionMessageParam
        # import base64
        # base64_image = base64.b64encode(image_data).decode('utf-8')
        # vision_messages: List[ChatCompletionMessageParam] = [
        #     {
        #         "role": "user",
        #         "content": [
        #             {"type": "text", "text": prompt},
        #             {
        #                 "type": "image_url",
        #                 "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
        #             }
        #         ]
        #     }
        # ]
        # try:
        #     response = await self.client.chat.completions.create(
        #         model="gpt-4-vision-preview", # Or other vision-capable model
        #         messages=vision_messages,
        #         max_tokens=300 
        #     )
        #     return response.choices[0].message.content.strip()
        # except Exception as e:
        #     print(f"Error analyzing image with OpenAI: {e}")
        #     return f"Error: Could not analyze image with OpenAI. {e}"
        print("OpenAI image analysis is not fully implemented in this example.")
        return "OpenAI image analysis placeholder response."

    async def generate_embeddings(self, text: str, model: str = "text-embedding-ada-002") -> List[float]:
        """Generate embeddings for the given text."""
        try:
            response = await self.client.embeddings.create(
                input=text,
                model=model
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating OpenAI embeddings: {e}")
            return []

# Example Usage (for testing):
async def main():
    if not OPENAI_API_KEY:
        print("Skipping OpenAIAssistant example as API key is not set.")
        return

    assistant = OpenAIAssistant()
    
    # Test simple prompt
    # prompt = "Explain quantum computing in simple terms."
    # response = await assistant.generate_response(prompt)
    # print(f"Prompt: {prompt}")
    # print(f"OpenAI Response: {response}")

    # Test chat
    # chat_messages = [
    #     {"role": "system", "content": "You are a helpful assistant."},
    #     {"role": "user", "content": "Who won the world series in 2020?"},
    #     {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    #     {"role": "user", "content": "Where was it played?"}
    # ]
    # chat_response = await assistant.generate_chat_response(chat_messages)
    # print(f"Chat Response: {chat_response}")

    # Test embeddings
    # text_to_embed = "OpenAI is a research and deployment company."
    # embeddings = await assistant.generate_embeddings(text_to_embed)
    # print(f"Embeddings for '{text_to_embed}': {embeddings[:5]}... (first 5 dimensions)")

if __name__ == "__main__":
    import asyncio
    # asyncio.run(main()) # Comment out if not running directly or if API key is an issue
    pass