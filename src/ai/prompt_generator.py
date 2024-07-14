import logging
from typing import Dict, Any
from src.models.game_state import GameState
from src.ai.prompt_templates import PromptTemplate

logger = logging.getLogger(__name__)

class PromptGenerator:
    """
    Responsible for generating prompts for the LLM based on the current game state and player actions.
    """
    def __init__(self):
        self.prompt_templates = {
            "default": PromptTemplate("You are an AI Dungeon Master assisting a player in an interactive fantasy adventure. The player is currently in {location}. {player_action}"),
            "move": PromptTemplate("The player wants to move {direction}. Describe the new location and any relevant details."),
            "attack": PromptTemplate("The player wants to attack {target}. Describe the combat encounter and its outcome."),
            "use": PromptTemplate("The player wants to use {item}. Describe the effects of using the item."),
            "talk": PromptTemplate("The player wants to talk to {npc}. Describe the conversation and any relevant information the NPC provides."),
            "pick": PromptTemplate("The player wants to pick up {item}. Describe the player acquiring the item.")
        }

    def generate_prompt(self, game_state: GameState, parsed_command: Dict[str, Any]) -> str:
        """
        Generate a prompt for the LLM based on the current game state and the parsed player command.

        Args:
            game_state (GameState): The current state of the game.
            parsed_command (Dict[str, Any]): The parsed player command.

        Returns:
            str: The generated prompt.
        """
        action = parsed_command.get("action")
        template = self.prompt_templates.get(action, self.prompt_templates["default"])

        prompt_data = {
            "location": game_state.location,
            "player_action": self._format_player_action(parsed_command)
        }
        prompt_data.update(parsed_command)

        try:
            return template.format(**prompt_data)
        except KeyError as e:
            logger.error(f"Error generating prompt: {e}")
            return "I'm sorry, I couldn't generate a prompt for that action."

    def _format_player_action(self, parsed_command: Dict[str, Any]) -> str:
        """
        Format the player's action based on the parsed command.

        Args:
            parsed_command (Dict[str, Any]): The parsed player command.

        Returns:
            str: The formatted player action.
        """
        action = parsed_command.get("action")
        if action == "move":
            return f"The player wants to go {parsed_command.get('direction')}."
        elif action == "attack":
            return f"The player wants to attack {parsed_command.get('target')}."
        elif action == "use":
            return f"The player wants to use {parsed_command.get('item')}."
        elif action == "talk":
            return f"The player wants to talk to {parsed_command.get('npc')}."
        elif action == "pick":
            return f"The player wants to pick up {parsed_command.get('item')}."
        else:
            return "The player wants to perform an action."
