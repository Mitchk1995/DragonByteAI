from flask import Blueprint
from .models.user import users_bp
from .models.character import characters_bp
from .models.game_state import game_states_bp

api_bp = Blueprint('api', __name__)

api_bp.register_blueprint(users_bp, url_prefix='/users')
api_bp.register_blueprint(characters_bp, url_prefix='/characters')
api_bp.register_blueprint(game_states_bp, url_prefix='/game-states')
