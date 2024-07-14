import requests
import logging
from typing import Dict, Any, Optional
from config import Config

logger = logging.getLogger(__name__)

class LlamaClient:
    def __init__(self):
        self.api_url = Config.LLAMA_API_URL
        self.api_key = Config.LLAMA_API_KEY

    def generate_response(self, prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> Optional[str]:
        """
        Generate a response from the Llama 3 model.

        Args:
            prompt (str): The input prompt for the model.
            max_tokens (int): The maximum number of tokens to generate.
            temperature (float): Controls randomness in generation. Higher values make output more random.

        Returns:
            Optional[str]: The generated response, or None if an error occurred.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            return response.json()['choices'][0]['text']
        except requests.RequestException as e:
            logger.error(f"Error in LLM API call: {str(e)}")
            return None

    def get_model_info(self) -> Dict[str, Any]:
        """
        Retrieve information about the Llama 3 model.

        Returns:
            Dict[str, Any]: A dictionary containing model information.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(f"{self.api_url}/model_info", headers=headers, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error retrieving model info: {str(e)}")
            return {}

# Example usage and testing
if __name__ == "__main__":
    client = LlamaClient()
    
    # Test generate_response
    response = client.generate_response("Tell me a short story about a brave knight.")
    print("Generated Response:")
    print(response)
    print()

    # Test get_model_info
    model_info = client.get_model_info()
    print("Model Info:")
    print(model_info)
