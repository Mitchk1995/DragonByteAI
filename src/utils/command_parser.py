import re
import spacy
from typing import Dict, Any, Optional

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

def parse_command(command: str) -> Optional[Dict[str, Any]]:
    words = command.lower().split()
    if not words:
        return None

    action = words[0]
    if action == "go" or action == "move":
        if len(words) > 1:
            return {"action": "move", "direction": words[1]}
    elif action == "attack":
        if len(words) > 1:
            return {"action": "attack", "target": " ".join(words[1:])}
    elif action == "use":
        if len(words) > 1:
            return {"action": "use", "item": " ".join(words[1:])}

    return None
    """
    Parse the user's command using advanced NLP techniques.
    
    Args:
        command (str): The user's input command.
    
    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the parsed command information,
                                  or None if the command couldn't be parsed.
    """
    # Process the command with spaCy
    doc = nlp(command.lower())
    
    # Extract the main verb (root) of the sentence
    root = next((token for token in doc if token.dep_ == "ROOT"), None)
    
    if not root:
        return None
    
    action = root.lemma_
    result = {"action": action}
    
    # Extract relevant entities and arguments based on the action
    if action in ["go", "move", "walk"]:
        direction = next((token for token in doc if token.dep_ in ["pobj", "dobj"] and token.text in ["north", "south", "east", "west"]), None)
        if direction:
            result["direction"] = direction.text
    elif action in ["attack", "fight"]:
        target = next((token for token in doc if token.dep_ in ["dobj", "pobj"]), None)
        if target:
            result["target"] = target.text
    elif action in ["use", "activate"]:
        item = next((token for token in doc if token.dep_ in ["dobj", "pobj"]), None)
        if item:
            result["item"] = item.text
    elif action in ["talk", "speak"]:
        npc = next((token for token in doc if token.dep_ in ["pobj"] and token.head.text in ["to", "with"]), None)
        if npc:
            result["npc"] = npc.text
    elif action in ["pick", "take"]:
        item = next((token for token in doc if token.dep_ in ["dobj", "pobj"] and token.head.text != "up"), None)
        if item:
            result["item"] = item.text
    
    # If we couldn't extract any additional information, return None
    return result if len(result) > 1 else None

# Example usage and testing
if __name__ == "__main__":
    test_commands = [
        "go north",
        "attack the goblin",
        "use healing potion",
        "talk to the innkeeper",
        "pick up the sword",
        "invalid command"
    ]
    
    for cmd in test_commands:
        parsed = parse_command(cmd)
        print(f"Command: {cmd}")
        print(f"Parsed: {parsed}")
        print()
