import unittest
from unittest.mock import patch, MagicMock
from game.engine import GameEngine
from models.game_state import GameState
from src.websockets.handler import WebSocketHandler

class TestGameEngine(unittest.TestCase):
    @patch('src.models.game_state.GameState.get_game_state')
    @patch('src.models.game_state.GameState.save')
    @patch('src.models.game_state.GameState._collection')
    @patch('src.websockets.handler.WebSocketHandler')
    def setUp(self, mock_websocket_handler, mock_collection, mock_save, mock_get_game_state):
        GameState.set_collection(mock_collection)
        self.mock_collection = mock_collection
        self.mock_get_game_state = mock_get_game_state
        self.mock_save = mock_save
        self.mock_websocket = mock_websocket_handler.return_value
        self.engine = GameEngine(websocket=self.mock_websocket)

    def test_start_game(self):
        self.mock_get_game_state.return_value = None
        self.engine.start_game("test_user_id")
        self.assertIsNotNone(self.engine.game_state)
        self.assertEqual(self.engine.game_state.location, "starting_location")
        self.mock_save.assert_called_once()

    @patch('src.game.engine.GameEngine.main_game_loop')
    def test_process_input(self, mock_main_game_loop):
        self.mock_get_game_state.return_value = None
        self.engine.start_game("test_user_id")
        response = self.engine.process_input("look around")
        self.assertIsNotNone(response)
        self.assertIn(response, self.engine.llm_client.responses)

    def test_websocket_communication(self):
        self.engine.start_game("test_user_id")
        self.engine.process_input("look around")
        self.mock_websocket.send.assert_called()

    @patch('src.game.engine.GameEngine.update_game_state')
    def test_main_game_loop(self, mock_update_game_state):
        self.engine.start_game("test_user_id")
        self.engine.main_game_loop()
        mock_update_game_state.assert_called()
        self.mock_websocket.receive.assert_called()

if __name__ == '__main__':
    unittest.main()
