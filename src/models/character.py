from app import mongo
from bson import ObjectId

class Character:
    def __init__(self, name, char_class, race, stats, inventory=None, skills=None, _id=None):
        self.name = name
        self.char_class = char_class
        self.race = race
        self.stats = stats
        self.inventory = inventory or []
        self.skills = skills or []
        self._id = _id

    def save(self):
        if not self._id:
            result = mongo.db.characters.insert_one(self.to_dict())
            self._id = result.inserted_id
        else:
            mongo.db.characters.update_one({'_id': self._id}, {'$set': self.to_dict()})

    @staticmethod
    def get_character(character_id):
        character_data = mongo.db.characters.find_one({'_id': ObjectId(character_id)})
        if character_data:
            return Character(
                name=character_data['name'],
                char_class=character_data['class'],
                race=character_data['race'],
                stats=character_data['stats'],
                inventory=character_data['inventory'],
                skills=character_data['skills'],
                _id=character_data['_id']
            )
        return None

    def to_dict(self):
        return {
            'name': self.name,
            'class': self.char_class,
            'race': self.race,
            'stats': self.stats,
            'inventory': self.inventory,
            'skills': self.skills
        }
