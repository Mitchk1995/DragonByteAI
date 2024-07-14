import requests
from config import Config

class LlamaClient:
    def __init__(self):
        self.api_url = Config.LLAMA_API_URL
        self.api_key = Config.LLAMA_API_KEY

    def generate_response(self, prompt, max_tokens=100):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": prompt,
            "max_tokens": max_tokens
        }
        response = requests.post(self.api_url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['text']
        else:
            raise Exception(f"Error in LLM API call: {response.text}")
