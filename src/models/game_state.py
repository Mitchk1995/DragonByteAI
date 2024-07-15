from pymongo import MongoClient
from bson import ObjectId
from .character import Character

class GameState:
    _client = MongoClient('mongodb://localhost:27017/')
    _db = _client['dragonbyte_realms']
    _collection = _db['game_states']

    def __init__(self, user_id, character_id, location, quest_progress, world_state, _id=None):
        self.user_id = user_id
        self.character_id = character_id
        self.location = location
        self.quest_progress = quest_progress
        self.world_state = world_state
        self._id = _id

    def save(self):
        data = self.to_dict()
        if not self._id:
            result = self._collection.insert_one(data)
            self._id = result.inserted_id
        else:
            self._collection.update_one({'_id': self._id}, {'$set': data})

    @classmethod
    def get_game_state(cls, user_id):
        game_state_data = cls._collection.find_one({'user_id': user_id})
        if game_state_data:
            return cls(
                user_id=game_state_data['user_id'],
                character_id=game_state_data['character_id'],
                location=game_state_data['location'],
                quest_progress=game_state_data['quest_progress'],
                world_state=game_state_data['world_state'],
                _id=game_state_data['_id']
            )
        return None

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'character_id': self.character_id,
            'location': self.location,
            'quest_progress': self.quest_progress,
            'world_state': self.world_state
        }

    @classmethod
    def set_collection(cls, collection):
        cls._collection = collection

    def get_player_character(self):
        return Character.get_character(self.character_id)
