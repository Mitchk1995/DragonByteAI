import unittest
from src.game.engine import GameEngine

class TestGameEngine(unittest.TestCase):
    def setUp(self):
        self.engine = GameEngine()

    def test_start_game(self):
        self.engine.start_game("test_user_id")
        self.assertIsNotNone(self.engine.game_state)
        self.assertEqual(self.engine.game_state.location, "starting_location")

    def test_process_input(self):
        self.engine.start_game("test_user_id")
        response = self.engine.process_input("look around")
        self.assertIsNotNone(response)
        self.assertIn(response, self.engine.llm_client.responses)

if __name__ == '__main__':
    unittest.main()
