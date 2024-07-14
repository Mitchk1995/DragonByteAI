import re

def parse_command(command):
    # Simple command parsing using regular expressions
    go_match = re.match(r'go\s+(north|south|east|west)', command, re.IGNORECASE)
    if go_match:
        return {'action': 'move', 'direction': go_match.group(1).lower()}

    attack_match = re.match(r'attack\s+(\w+)', command, re.IGNORECASE)
    if attack_match:
        return {'action': 'attack', 'target': attack_match.group(1).lower()}

    use_match = re.match(r'use\s+(\w+)', command, re.IGNORECASE)
    if use_match:
        return {'action': 'use', 'item': use_match.group(1).lower()}

    # If no match is found, return None or a default action
    return None
