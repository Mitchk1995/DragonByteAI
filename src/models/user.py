from datetime import datetime
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['dragonbyte_realms']
users_collection = db['users']

class User:
    def __init__(self, username, password, _id=None):
        self.username = username
        self.password = password
        self._id = _id
        self.created_at = datetime.utcnow()

    def save(self):
        if not self._id:
            result = users_collection.insert_one({
                'username': self.username,
                'password': self.password,
                'created_at': self.created_at
            })
            self._id = result.inserted_id
        else:
            users_collection.update_one({'_id': self._id}, {'$set': self.to_dict()})

    @staticmethod
    def find_by_username(username):
        user_data = users_collection.find_one({'username': username})
        if user_data:
            return User(username=user_data['username'], password=user_data['password'], _id=user_data['_id'])
        return None

    @staticmethod
    def find_by_id(user_id):
        user_data = users_collection.find_one({'_id': user_id})
        if user_data:
            return User(username=user_data['username'], password=user_data['password'], _id=user_data['_id'])
        return None

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'created_at': self.created_at
        }

    def get_active_character(self):
        # This is a placeholder. Implement the logic to get the active character.
        return None
