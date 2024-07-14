from app import mongo

def init_db():
    db = mongo.db
    
    # Create collections if they don't exist
    if 'users' not in db.list_collection_names():
        db.create_collection('users')
    
    if 'characters' not in db.list_collection_names():
        db.create_collection('characters')
    
    if 'game_states' not in db.list_collection_names():
        db.create_collection('game_states')

    print("Database initialized with collections: users, characters, game_states")

if __name__ == "__main__":
    init_db()
