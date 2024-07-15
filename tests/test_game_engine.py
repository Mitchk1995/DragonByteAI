import unittest
from unittest.mock import patch, MagicMock
from src.game.engine import GameEngine
from src.models.game_state import GameState

class TestGameEngine(unittest.TestCase):
    @patch('src.models.game_state.GameState.get_game_state')
    @patch('src.models.game_state.GameState.save')
    def setUp(self, mock_save, mock_get_game_state):
        self.mock_get_game_state = mock_get_game_state
        self.mock_save = mock_save
        self.engine = GameEngine()

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

if __name__ == '__main__':
    unittest.main()
