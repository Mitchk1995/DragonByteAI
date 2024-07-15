import unittest
from utils.command_parser import parse_command

class TestCommandParser(unittest.TestCase):
    def test_move_command(self):
        result = parse_command("go north")
        self.assertEqual(result, {'action': 'move', 'direction': 'north'})

    def test_attack_command(self):
        result = parse_command("attack goblin")
        self.assertEqual(result, {'action': 'attack', 'target': 'goblin'})

    def test_use_command(self):
        result = parse_command("use potion")
        self.assertEqual(result, {'action': 'use', 'item': 'potion'})

    def test_invalid_command(self):
        result = parse_command("invalid command")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()