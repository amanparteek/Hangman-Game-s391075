import random
import time

class HangmanGame:
    def __init__(self, words, lives=6, timer_limit=15):
        self.words = words
        self.lives = lives
        self.timer_limit = timer_limit
        self.word = ''
        self.masked_word = ''
        self.guessed_letters = set()
        self.start_time = None

    def start_new_game(self, level='basic'):
        self.word = random.choice(self.words[level]).upper()
        self.lives = 6
        self.guessed_letters.clear()
        self.start_time = time.time()

        # Randomly reveal 1–2 letters at start
        letters_to_reveal = set()
        all_letters = [ch for ch in self.word if ch.isalpha()]
        if all_letters:
            letters_to_reveal = set(random.sample(all_letters, min(2, len(all_letters))))

        self.guessed_letters |= letters_to_reveal
        self.masked_word = ''.join([
            ch if not ch.isalpha() or ch in self.guessed_letters else '_'
            for ch in self.word
        ])
        return self.masked_word

    def guess_letter(self, letter):
        letter = letter.upper()
        if not letter.isalpha() or len(letter) != 1:
            return False, "Invalid input"
        if letter in self.guessed_letters:
            return False, "Already guessed"
        
        self.guessed_letters.add(letter)
        if letter in self.word:
            self.masked_word = ''.join([
                ch if not ch.isalpha() or ch in self.guessed_letters else '_'
                for ch in self.word
            ])
            return True, "Correct"
        else:
            self.lives -= 1
            return False, "Wrong"
        
    def time_expired(self):
        return (time.time() - self.start_time) > self.timer_limit

    def is_won(self):
        return '_' not in self.masked_word

    def is_lost(self):
        return self.lives <= 0

    def is_game_over(self):
        return self.is_won() or self.is_lost()
