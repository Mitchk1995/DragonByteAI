from datetime import datetime
from app import mongo

class User:
    def __init__(self, username, password, _id=None):
        self.username = username
        self.password = password
        self._id = _id
        self.created_at = datetime.utcnow()

    def save(self):
        if not self._id:
            result = mongo.db.users.insert_one({
                'username': self.username,
                'password': self.password,
                'created_at': self.created_at
            })
            self._id = result.inserted_id
        else:
            mongo.db.users.update_one({'_id': self._id}, {'$set': self.to_dict()})

    @staticmethod
    def find_by_username(username):
        user_data = mongo.db.users.find_one({'username': username})
        if user_data:
            return User(username=user_data['username'], password=user_data['password'], _id=user_data['_id'])
        return None

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'created_at': self.created_at
        }
