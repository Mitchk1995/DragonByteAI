from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import mongo

class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.created_at = datetime.utcnow()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def create_user(username, password):
        user = User(username, password)
        mongo.db.users.insert_one({
            'username': user.username,
            'password_hash': user.password_hash,
            'created_at': user.created_at
        })
        return user

    @staticmethod
    def authenticate(username, password):
        user_data = mongo.db.users.find_one({'username': username})
        if user_data and check_password_hash(user_data['password_hash'], password):
            return User(user_data['username'], '')
        return None
