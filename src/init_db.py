from pymongo import MongoClient
from config import Config

def init_db():
    client = MongoClient(Config.MONGODB_URI)
    db = client[Config.MONGODB_DB_NAME]
    
    # Create collections if they don't exist
    collections = ['users', 'characters', 'game_states']
    for collection in collections:
        if collection not in db.list_collection_names():
            db.create_collection(collection)
    
    # Create indexes
    db.users.create_index('username', unique=True)
    db.characters.create_index('user_id')
    db.game_states.create_index('user_id', unique=True)

    print(f"Database initialized with collections: {', '.join(collections)}")
    print("Indexes created for users, characters, and game_states collections")

if __name__ == "__main__":
    init_db()
