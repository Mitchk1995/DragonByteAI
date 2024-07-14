import logging
from src.utils.text_ui import display_text, get_user_input
from src.nlp.command_parser import parse_command
from src.models.game_state import GameState
from src.ai.llm_client import LlamaClient
from src.ai.prompt_generator import PromptGenerator
from src.ai.response_parser import parse_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GameEngine:
    def __init__(self):
        self.game_state = None
        self.llm_client = LlamaClient()
        self.prompt_generator = PromptGenerator()

    def start_game(self, user_id):
        self.game_state = GameState.get_game_state(user_id) or GameState(user_id, None, "starting_location", {}, {})
        self.main_game_loop()

    def main_game_loop(self):
        while True:
            self.display_current_state()
            user_input = self.get_player_input()
            if user_input.lower() == 'quit':
                logger.info("Player quit the game")
                break
            self.process_input(user_input)
            self.update_game_state()

    def display_current_state(self):
        display_text(f"You are in {self.game_state.location}")

    def get_player_input(self):
        return get_user_input("What would you like to do? ")

    def process_input(self, user_input):
        parsed_command = parse_command(user_input)
        if parsed_command:
            prompt = self.prompt_generator.generate_prompt(self.game_state, parsed_command)
            llm_response = self.llm_client.generate_response(prompt)
            parsed_response = parse_response(llm_response)
            self.apply_response(parsed_response)
        else:
            display_text("I don't understand that command.")

    def apply_response(self, parsed_response):
        # Apply the effects of the parsed response to the game state
        # This could include updating the player's location, inventory, quest progress, etc.
        pass

    def update_game_state(self):
        self.game_state.save()

if __name__ == "__main__":
    engine = GameEngine()
    engine.start_game("test_user_id")
