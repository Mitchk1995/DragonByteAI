from utils.text_ui import display_text, get_user_input
from utils.command_parser import parse_command

def game_loop(game_state):
    while True:
        display_text(f"You are in {game_state.location}")
        command = get_user_input("What would you like to do? ")
        
        parsed_command = parse_command(command)
        
        if parsed_command is None:
            display_text("I don't understand that command.")
            continue
        
        if parsed_command['action'] == 'move':
            game_state.location = f"the area to the {parsed_command['direction']}"
            display_text(f"You move to {game_state.location}")
        elif parsed_command['action'] == 'attack':
            display_text(f"You attack the {parsed_command['target']}!")
        elif parsed_command['action'] == 'use':
            display_text(f"You use the {parsed_command['item']}.")
        elif command.lower() == 'quit':
            display_text("Thanks for playing!")
            break
        
        # Here you would update the game state and handle more complex game logic
        
        game_state.save()
