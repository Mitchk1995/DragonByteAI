import logging
from ..utils.text_ui import display_text, get_user_input
from ..utils.command_parser import parse_command
from ..models.game_state import GameState
from ..ai.mock_ai_client import MockAIClient
from ..ai.prompt_generator import PromptGenerator
from ..ai.response_parser import ResponseParser
from ..websockets.handler import WebSocketHandler
from ..game.combat import CombatSystem, PlayerCombatant, NPCCombatant

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GameEngine:
    def __init__(self, websocket: WebSocketHandler = None):
        self.game_state = None
        self.llm_client = MockAIClient()
        self.websocket = websocket
        self.prompt_generator = PromptGenerator()
        self.combat_system = CombatSystem()

    def start_game(self, user_id):
        self.game_state = GameState.get_game_state(user_id)
        if not self.game_state:
            self.game_state = GameState(user_id, None, "starting_location", {}, {})
            self.game_state.save()
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
            if parsed_command['action'] == 'start_combat':
                return self.start_combat()
            elif self.combat_system.combatants:
                return self.process_combat_action(parsed_command)
            else:
                prompt = self.prompt_generator.generate_prompt(self.game_state, parsed_command)
                llm_response = self.llm_client.generate_response(prompt)
                response_parser = ResponseParser()
                parsed_response = response_parser.parse_dialogue(llm_response)
                self.apply_response(parsed_response)
                return llm_response
        else:
            return "I don't understand that command."

    def start_combat(self):
        player = self.game_state.get_player_character()
        player_combatant = PlayerCombatant(player.name, player.health, player.attack, player.defense, player.speed)
        
        # For simplicity, we'll create a dummy NPC enemy
        npc_enemy = NPCCombatant("Goblin", 20, 5, 2, 5)
        
        self.combat_system.start_combat([player_combatant], [npc_enemy])
        return "Combat has started! " + self.combat_system.get_combat_summary()

    def process_combat_action(self, parsed_command):
        current_combatant = self.combat_system.turn_order[self.combat_system.current_turn]
        
        if isinstance(current_combatant, PlayerCombatant):
            action = parsed_command['action']
            target = self.combat_system.combatants[parsed_command.get('target_index', 0)]
            self.combat_system.process_action(current_combatant, action, target)
        else:
            npc_action = current_combatant.get_action(self.combat_system.__dict__)
            self.combat_system.process_action(current_combatant, npc_action['action'], npc_action['target'])

        if self.combat_system.check_combat_end():
            result = "Combat has ended! "
            self.combat_system = CombatSystem()  # Reset combat system
        else:
            self.combat_system.next_turn()
            result = ""

        return result + self.combat_system.get_combat_summary()

    def apply_response(self, parsed_response):
        # Apply the effects of the parsed response to the game state
        # This could include updating the player's location, inventory, quest progress, etc.
        pass

    def update_game_state(self):
        self.game_state.save()

if __name__ == "__main__":
    engine = GameEngine()
    engine.start_game("test_user_id")
