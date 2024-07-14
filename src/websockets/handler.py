import asyncio
import json
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedError
from src.models.user import User
from src.game.engine import GameEngine
from src.utils.jwt_utils import decode_jwt

class WebSocketHandler:
    def __init__(self):
        self.connections = {}  # Store active connections
        self.game_engine = GameEngine()

    async def handle_connection(self, websocket: WebSocketServerProtocol, path: str):
        try:
            # Authenticate the connection
            auth_token = await websocket.recv()
            user = self.authenticate_user(auth_token)
            if not user:
                await websocket.close(code=4001, reason="Authentication failed")
                return

            # Store the connection
            self.connections[user.id] = websocket

            # Handle messages
            async for message in websocket:
                await self.process_message(user, message)

        except ConnectionClosedError:
            print(f"Connection closed for user {user.id}")
        finally:
            if user:
                del self.connections[user.id]

    def authenticate_user(self, auth_token):
        try:
            payload = decode_jwt(auth_token)
            user_id = payload['user_id']
            return User.find_by_id(user_id)
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return None

    async def process_message(self, user, message):
        try:
            data = json.loads(message)
            message_type = data.get('type')
            content = data.get('content')

            if message_type == 'game_action':
                response = self.game_engine.process_input(content)
                await self.send_message(user.id, 'game_update', response)
            elif message_type == 'chat_message':
                # Process chat messages (if implementing a chat feature)
                pass
            else:
                await self.send_message(user.id, 'error', 'Unknown message type')

        except json.JSONDecodeError:
            await self.send_message(user.id, 'error', 'Invalid JSON')
        except Exception as e:
            await self.send_message(user.id, 'error', str(e))

    async def send_message(self, user_id, message_type, content):
        if user_id in self.connections:
            message = json.dumps({
                'type': message_type,
                'content': content
            })
            await self.connections[user_id].send(message)

    async def broadcast(self, message_type, content):
        message = json.dumps({
            'type': message_type,
            'content': content
        })
        await asyncio.gather(
            *[conn.send(message) for conn in self.connections.values()]
        )

websocket_handler = WebSocketHandler()
