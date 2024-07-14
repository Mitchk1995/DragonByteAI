from app import mongo

class GameState:
    def __init__(self, user_id, character_id, location, quest_progress, world_state):
        self.user_id = user_id
        self.character_id = character_id
        self.location = location
        self.quest_progress = quest_progress
        self.world_state = world_state

    def save(self):
        return mongo.db.game_states.insert_one({
            'user_id': self.user_id,
            'character_id': self.character_id,
            'location': self.location,
            'quest_progress': self.quest_progress,
            'world_state': self.world_state
        })

    @staticmethod
    def get_game_state(user_id):
        game_state_data = mongo.db.game_states.find_one({'user_id': user_id})
        if game_state_data:
            return GameState(
                game_state_data['user_id'],
                game_state_data['character_id'],
                game_state_data['location'],
                game_state_data['quest_progress'],
                game_state_data['world_state']
            )
        return None
