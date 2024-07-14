from flask import Flask
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure MongoDB
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/ai_dungeon")
mongo = PyMongo(app)

@app.errorhandler(404)
def not_found(error):
    return {"error": "Not found"}, 404

@app.errorhandler(500)
def internal_error(error):
    return {"error": "Internal server error"}, 500

@app.route('/')
def hello_world():
    return 'Welcome to AI Dungeon Master!'

if __name__ == '__main__':
    app.run(debug=True)
