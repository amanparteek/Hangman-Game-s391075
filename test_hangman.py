import unittest
from hangman_game import HangmanGame

class TestHangman(unittest.TestCase):
    def setUp(self):
        words = {'basic': ['PYTHON'], 'intermediate': ['UNIT TEST']}
        self.game = HangmanGame(words)

    def test_start_game_masks_word_with_letters(self):
        masked = self.game.start_new_game('basic')
        self.assertEqual(len(masked), len('PYTHON'))
        self.assertTrue(any(c.isalpha() for c in masked))
        self.assertTrue('_' in masked)

    def test_correct_guess(self):
        self.game.start_new_game('basic')
        result, message = self.game.guess_letter('P')
        self.assertTrue(result)
        self.assertIn('P', self.game.masked_word)

    def test_wrong_guess_deducts_life(self):
        self.game.start_new_game('basic')
        start_lives = self.game.lives
        result, message = self.game.guess_letter('Z')
        self.assertFalse(result)
        self.assertEqual(self.game.lives, start_lives - 1)

    def test_game_win_condition(self):
        self.game.start_new_game('basic')
        for ch in "PYTHON":
            self.game.guess_letter(ch)
        self.assertTrue(self.game.is_won())

if __name__ == '__main__':
    unittest.main()
