"""Hangman Game Logic """
import random
import time


class HangmanGame:
    """A class representing the Hangman game logic."""

    def __init__(self, words, lives=6, timer_limit=15):
        """
        Initializes the Hangman game with given words, lives, and timer limit.
        
        :param words: Dictionary of words categorized by level.
        :param lives: Number of lives the player has (default is 6).
        :param timer_limit: Time limit for each guess in seconds (default is 15).
        """
        self.words = words
        self.lives = lives
        self.timer_limit = timer_limit
        self.word = ''
        self.masked_word = ''
        self.guessed_letters = set()
        self.start_time = None

    def start_new_game(self, level='basic'):
        """
        Starts a new game by selecting a word based on the level.
        Initializes the game variables and masks the word.

        :param level: Difficulty level ('basic' or 'intermediate').
        :return: Masked word with some letters revealed.
        """
        self.word = random.choice(self.words[level]).upper()
        self.lives = 6
        self.guessed_letters.clear()
        self.start_time = time.time()

        self.masked_word = ''.join([
            ch if ch in self.guessed_letters or not ch.isalpha() else '_'
            for ch in self.word
        ])
        return self.masked_word

    def guess_letter(self, letter):
        """
        Takes a letter guess, updates the game state (masked word, lives), and returns feedback.

        :param letter: The guessed letter.
        :return: A tuple (boolean, message) indicating the result of the guess.
        """
        letter = letter.upper()
        if len(letter) != 1 or not letter.isalpha():
            return False, "Invalid input"
        if letter in self.guessed_letters:
            return False, "Already guessed"

        self.guessed_letters.add(letter)
        if letter in self.word:
            self.masked_word = ''.join([
                ch if ch in self.guessed_letters or not ch.isalpha() else '_'
                for ch in self.word
            ])
            return True, "Correct"
        else:
            self.lives -= 1
            return False, "Wrong"

    def time_expired(self):
        """Checks if the time has expired for the current round."""
        return (time.time() - self.start_time) > self.timer_limit

    def is_game_over(self):
        """Checks if the game is over (either won or lost)."""
        return self.is_won() or self.lives <= 0

    def is_won(self):
        """Checks if the player has won the game by guessing all the letters."""
        return '_' not in self.masked_word
