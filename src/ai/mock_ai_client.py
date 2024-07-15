import random

class MockAIClient:
    def __init__(self):
        self.responses = [
            "You enter a dark cave. The air is damp and cold.",
            "A mysterious figure approaches you in the tavern.",
            "You find an ancient artifact buried in the sand.",
            "A dragon's roar echoes in the distance.",
            "You stumble upon a hidden village in the forest."
        ]

    def generate_response(self, prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> str:
        return random.choice(self.responses)

    def get_model_info(self):
        return {"model": "Mock AI Model", "version": "1.0"}
