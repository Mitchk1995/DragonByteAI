from app import mongo

class Character:
    def __init__(self, name, char_class, race, stats, inventory=None, skills=None):
        self.name = name
        self.char_class = char_class
        self.race = race
        self.stats = stats
        self.inventory = inventory or []
        self.skills = skills or []

    def save(self):
        return mongo.db.characters.insert_one({
            'name': self.name,
            'class': self.char_class,
            'race': self.race,
            'stats': self.stats,
            'inventory': self.inventory,
            'skills': self.skills
        })

    @staticmethod
    def get_character(character_id):
        character_data = mongo.db.characters.find_one({'_id': character_id})
        if character_data:
            return Character(
                character_data['name'],
                character_data['class'],
                character_data['race'],
                character_data['stats'],
                character_data['inventory'],
                character_data['skills']
            )
        return None
