from app import mongo
from bson import ObjectId

class GameState:
    def __init__(self, user_id, character_id, location, quest_progress, world_state, _id=None):
        self.user_id = user_id
        self.character_id = character_id
        self.location = location
        self.quest_progress = quest_progress
        self.world_state = world_state
        self._id = _id

    def save(self):
        if not self._id:
            result = mongo.db.game_states.insert_one(self.to_dict())
            self._id = result.inserted_id
        else:
            mongo.db.game_states.update_one({'_id': self._id}, {'$set': self.to_dict()})

    @staticmethod
    def get_game_state(user_id):
        game_state_data = mongo.db.game_states.find_one({'user_id': ObjectId(user_id)})
        if game_state_data:
            return GameState(
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
