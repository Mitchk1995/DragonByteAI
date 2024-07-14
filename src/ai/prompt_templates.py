class PromptTemplate:
    def __init__(self, template):
        self.template = template

    def format(self, **kwargs):
        return self.template.format(**kwargs)

# Example templates
QUEST_GENERATION = PromptTemplate(
    "Generate a quest for a {character_class} in the {location} with difficulty level {difficulty}."
)

NPC_DIALOGUE = PromptTemplate(
    "Create a dialogue for a {npc_type} NPC interacting with a {character_class} player in {context}."
)

COMBAT_NARRATION = PromptTemplate(
    "Narrate a combat scene between a {character_class} and a {enemy_type} in {location}."
)
