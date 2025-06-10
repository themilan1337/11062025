import google.generativeai as genai
from typing import List, Dict, Any
from src.assitant.base import BaseAssistant, AIMessage
from src.config import settings # Assuming API key might be in settings
import os

# Configure the Gemini API key
# It's better to load this from environment variables or a config file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # Or settings.gemini_api_key
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY not found in environment variables.")
    # raise ValueError("GEMINI_API_KEY not found in environment variables.")
else:
    genai.configure(api_key=GEMINI_API_KEY)

class GeminiAssistant(BaseAssistant):
    """AI assistant powered by Google Gemini."""

    def __init__(self, model_name: str = "gemini-pro"):
        if not GEMINI_API_KEY:
            raise EnvironmentError("GEMINI_API_KEY is not set. Cannot initialize GeminiAssistant.")
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
        self.vision_model = genai.GenerativeModel('gemini-pro-vision') # For image analysis
        self.embedding_model = 'models/embedding-001' # For text embeddings

    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response for the given prompt."""
        try:
            response = await self.model.generate_content_async(prompt, **kwargs)
            return response.text
        except Exception as e:
            print(f"Error generating Gemini response: {e}")
            # Consider more specific error handling or re-raising
            return f"Error: Could not get response from Gemini. {e}"

    async def generate_chat_response(
        self,
        messages: List[Dict[str, str]], # Expects [{'role': 'user'/'model', 'parts': ['text']}]
        **kwargs
    ) -> str:
        """Generate a response in a chat context using Gemini's format."""
        # Gemini expects a list of Content objects or dicts with 'role' and 'parts'
        # Convert AIMessage style to Gemini's expected format if necessary
        # For simplicity, assuming messages are already in a compatible format or can be adapted
        
        # Start a chat session if not already started or manage history appropriately
        # chat = self.model.start_chat(history=messages) # This creates a stateful chat
        # response = await chat.send_message_async(messages[-1]['parts'][0]) # Send the last message

        # For stateless generation from a list of messages:
        try:
            # Ensure messages are in the correct format for generate_content_async
            # Gemini's `generate_content_async` can take a list of alternating user/model messages.
            # Example: [{'role':'user', 'parts': ['Hello!']}, {'role':'model', 'parts': ['Hi there!']}]
            response = await self.model.generate_content_async(contents=messages, **kwargs)
            return response.text
        except Exception as e:
            print(f"Error generating Gemini chat response: {e}")
            return f"Error: Could not get chat response from Gemini. {e}"

    async def analyze_image(self, image_data: bytes, prompt: str) -> str:
        """Analyze an image and generate a response based on the prompt."""
        try:
            image_parts = [
                {
                    "mime_type": "image/jpeg", # Or other appropriate mime type
                    "data": image_data
                }
            ]
            response = await self.vision_model.generate_content_async([prompt, image_parts[0]], **{})
            return response.text
        except Exception as e:
            print(f"Error analyzing image with Gemini: {e}")
            return f"Error: Could not analyze image with Gemini. {e}"

    async def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings for the given text."""
        try:
            result = genai.embed_content(model=self.embedding_model, content=text)
            return result['embedding']
        except Exception as e:
            print(f"Error generating Gemini embeddings: {e}")
            return [] # Return empty list or handle error as appropriate

# Example Usage (for testing):
async def main():
    if not GEMINI_API_KEY:
        print("Skipping GeminiAssistant example as API key is not set.")
        return

    assistant = GeminiAssistant()
    
    # Test simple prompt
    # prompt = "What is the capital of France?"
    # response = await assistant.generate_response(prompt)
    # print(f"Prompt: {prompt}")
    # print(f"Gemini Response: {response}")

    # Test chat
    # chat_messages = [
    #     {'role': 'user', 'parts': ['Hello, I have a question.']},
    #     {'role': 'model', 'parts': ['Sure, what is your question?']},
    #     {'role': 'user', 'parts': ['What is the weather like today?']}
    # ]
    # chat_response = await assistant.generate_chat_response(chat_messages)
    # print(f"Chat Response: {chat_response}")

    # Test embeddings
    # text_to_embed = "This is a test sentence for embeddings."
    # embeddings = await assistant.generate_embeddings(text_to_embed)
    # print(f"Embeddings for '{text_to_embed}': {embeddings[:5]}... (first 5 dimensions)")

if __name__ == "__main__":
    import asyncio
    # asyncio.run(main()) # Comment out if not running directly or if API key is an issue
    pass