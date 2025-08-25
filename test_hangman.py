import unittest
from hangman_game import HangmanGame


class TestHangman(unittest.TestCase):
    """Test cases for Hangman game logic."""

    def setUp(self):
        """Sets up the game with a small word list for testing."""
        words = {'basic': ['PYTHON'], 'intermediate': ['UNIT TEST']}
        self.game = HangmanGame(words)

    def test_start_game_masks_word_with_letters(self):
        """Test that starting a new game masks the word correctly with letters."""
        masked = self.game.start_new_game('basic')
        self.assertEqual(len(masked), len('PYTHON'))  # The masked word should match the length of the word.
        self.assertTrue(any(c.isalpha() for c in masked))  # Ensure some letters are revealed.
        self.assertTrue('_' in masked)  # The word should have underscores for hidden letters.

    def test_correct_guess(self):
        """Test that a correct guess reveals the correct letter and doesn't deduct lives."""
        self.game.start_new_game('basic')
        result, message = self.game.guess_letter('P')  # Test for correct guess 'P'
        self.assertTrue(result)  # The result should be True for a correct guess.
        self.assertIn('P', self.game.masked_word)  # 'P' should be revealed in the masked word.

    def test_wrong_guess_deducts_life(self):
        """Test that a wrong guess deducts a life and the game continues."""
        self.game.start_new_game('basic')
        start_lives = self.game.lives  # Store the starting number of lives.
        result, message = self.game.guess_letter('Z')  # Test for wrong guess 'Z'
        self.assertFalse(result)  # The result should be False for a wrong guess.
        self.assertEqual(self.game.lives, start_lives - 1)  # The number of lives should decrease by 1.

    def test_game_win_condition(self):
        """Test that the game correctly detects a win when all letters are guessed."""
        self.game.start_new_game('basic')
        for ch in "PYTHON":  # Guess each letter in the word.
            self.game.guess_letter(ch)
        self.assertTrue(self.game.is_won())  # The game should be won when all letters are revealed.

    def test_time_expiration(self):
        """Test that the time expiration check works correctly."""
        self.game.start_new_game('basic')
        time_expired = self.game.time_expired()
        self.assertFalse(time_expired)  # Time should not be expired immediately after starting the game.
        self.game.start_time -= 20  # Simulate time passing.
        time_expired = self.game.time_expired()
        self.assertTrue(time_expired)  # Time should be expired after 20 seconds.

if __name__ == '__main__':
    unittest.main()
