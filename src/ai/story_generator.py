import random

class StoryGenerator:
    def __init__(self):
        self.story_snippets = [
            "You enter a dark cave. The air is damp and cold.",
            "A mysterious figure approaches you in the tavern.",
            "You find an ancient artifact buried in the sand.",
            "A dragon's roar echoes in the distance.",
            "You stumble upon a hidden village in the forest."
        ]

    def generate_story_snippet(self):
        return random.choice(self.story_snippets)
