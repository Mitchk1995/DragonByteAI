import unittest
from unittest.mock import patch, MagicMock
from src.game.engine import GameEngine
from src.models.game_state import GameState

class TestGameEngine(unittest.TestCase):
    @patch('src.models.game_state.GameState._collection')
    def setUp(self, mock_collection):
        self.mock_collection = mock_collection
        self.engine = GameEngine()

    def test_start_game(self):
        self.mock_collection.find_one.return_value = None
        self.engine.start_game("test_user_id")
        self.assertIsNotNone(self.engine.game_state)
        self.assertEqual(self.engine.game_state.location, "starting_location")

    def test_process_input(self):
        self.mock_collection.find_one.return_value = None
        self.engine.start_game("test_user_id")
        with patch.object(self.engine, 'main_game_loop'):  # Prevent the game loop from starting
            response = self.engine.process_input("look around")
            self.assertIsNotNone(response)
            self.assertIn(response, self.engine.llm_client.responses)

if __name__ == '__main__':
    unittest.main()
