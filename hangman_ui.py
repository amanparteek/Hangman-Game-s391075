"""
This module contains the user interface (UI) for the Hangman game, built using the Tkinter library.

It includes the `HangmanUI` class, which handles the graphical interface for the game.
The UI allows the user to:
1. Select the game difficulty (basic or intermediate).
2. Enter guesses and view the masked word.
3. See the number of lives left and the timer countdown.
4. Restart the game after it ends.

The UI communicates with the `HangmanGame` class to update the game state and displays the results.
"""
import tkinter as tk
import time
import threading
from hangman_game import HangmanGame

WORDS = {
    'basic': ["PYTHON", "HANGMAN", "COMPUTER", "SOFTWARE", "DEVELOPER", "ALGORITHM"],
    'intermediate': ["OPEN SOURCE", "UNIT TESTING", "ARTIFICIAL INTELLIGENCE", "OBJECT ORIENTED", "SOFTWARE ENGINEERING"]
}

MAX_LIVES = 6  # Maximum number of lives


class HangmanUI:
    """A class representing the Hangman game user interface."""

    def __init__(self, root):
        """
        Initializes the Hangman game UI, sets up widgets, and starts the game.

        :param root: The Tkinter root window.
        """
        self.root = root
        self.root.title("Hangman Game")
        self.game = HangmanGame(WORDS, lives=MAX_LIVES)
        self.current_level = "basic"
        self.timer_thread = None
        self.stop_timer = False
        self._setup_ui()

    def _setup_ui(self):
        """
        Sets up all the UI components for the Hangman game.
        """
        header = tk.Label(self.root, text="Hangman (TDD Version)", font=("Helvetica", 18, "bold"))
        header.pack(pady=6)

        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=4)
        self.level_var = tk.StringVar(value="basic")
        tk.Label(top_frame, text="Select Level:", font=("Helvetica", 12)).pack(side="left", padx=6)
        tk.OptionMenu(top_frame, self.level_var, "basic", "intermediate").pack(side="left")
        tk.Button(top_frame, text="Restart", command=self.restart_game).pack(side="left", padx=10)

        self.canvas = tk.Canvas(self.root, width=320, height=260,
                                bg="#f7f7f7", highlightthickness=0)
        self.canvas.pack(pady=6)

        self.word_label = tk.Label(self.root, text="", font=("Consolas", 28))
        self.word_label.pack(pady=8)

        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=4)
        self.info_label = tk.Label(info_frame, text="", font=("Helvetica", 12))
        self.info_label.pack()

        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=6)
        self.entry = tk.Entry(input_frame, font=("Helvetica", 14), width=5, justify="center")
        self.entry.grid(row=0, column=0, padx=4)
        self.entry.bind("<Return>", self.make_guess)
        self.submit_btn = tk.Button(input_frame, text="Guess", command=self.make_guess)
        self.submit_btn.grid(row=0, column=1, padx=6)

        status_frame = tk.Frame(self.root)
        status_frame.pack(pady=6)
        self.lives_label = tk.Label(status_frame, text=f"Lives: {MAX_LIVES}",
                                    font=("Helvetica", 12))
        self.lives_label.grid(row=0, column=0, padx=10)
        self.timer_label = tk.Label(status_frame, text="Time: 15", font=("Helvetica", 12))
        self.timer_label.grid(row=0, column=1, padx=10)

        self.start_game(self.level_var.get())

    def start_game(self, level):
        """
        Starts a new game based on the selected difficulty level.

        :param level: Difficulty level ('basic' or 'intermediate').
        """
        self.current_level = level
        word = self.game.start_new_game(level)
        self.word_label.config(text=self._spaced(word))
        self.lives_label.config(text=f"Lives: {self.game.lives}")
        self.info_label.config(text="Type a letter and press Enter.")
        self.entry.config(state="normal")
        self.submit_btn.config(state="normal")
        self.entry.focus_set()
        self.stop_timer = False
        self.draw_hangman()
        self.start_timer()

    def restart_game(self):
        """Restarts the game with the selected difficulty level."""
        self.stop_timer = True
        self.start_game(self.level_var.get())

    def make_guess(self):
        """
        Handles the player's guess and updates the UI accordingly.

        :param event: The event triggered by pressing the Enter key or the "Guess" button.
        """
        guess = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        message = self.game.guess_letter(guess)
        self.word_label.config(text=self._spaced(self.game.masked_word))
        self.lives_label.config(text=f"Lives: {self.game.lives}")
        self.info_label.config(text=message)
        self.draw_hangman()
        if self.game.is_game_over():
            self.end_game()

    def start_timer(self):
        """Starts the timer for the game."""
        self.stop_timer = True
        if hasattr(self, "timer_thread") and self.timer_thread and self.timer_thread.is_alive():
            time.sleep(0.1)
        self.stop_timer = False

        def countdown():
            while not self.game.is_game_over() and not self.stop_timer:
                remaining = self.game.timer_limit - int(time.time() - self.game.start_time)
                if remaining <= 0:
                    self.game.lives -= 1
                    if self.game.is_lost():
                        self.end_game()
                        return
                    self.game.start_time = time.time()
                    self.lives_label.config(text=f"Lives: {self.game.lives}")
                    self.info_label.config(text="Time up! Life deducted.")
                    self.draw_hangman()
                    remaining = self.game.timer_limit
                self.timer_label.config(text=f"Time: {remaining}")
                time.sleep(1)

        self.timer_thread = threading.Thread(target=countdown, daemon=True)
        self.timer_thread.start()

    def draw_hangman(self):
        """Draws the hangman on the canvas based on incorrect guesses."""
        self.canvas.delete("all")
        wrong = MAX_LIVES - self.game.lives

        self.canvas.create_line(20, 240, 300, 240, width=3)
        self.canvas.create_line(60, 240, 60, 40, width=3)
        self.canvas.create_line(60, 40, 200, 40, width=3)
        self.canvas.create_line(200, 40, 200, 70, width=3)

        if wrong >= 1:
            self.canvas.create_oval(180, 70, 220, 110, width=3)
        if wrong >= 2:
            self.canvas.create_line(200, 110, 200, 170, width=3)
        if wrong >= 3:
            self.canvas.create_line(200, 125, 175, 145, width=3)
        if wrong >= 4:
            self.canvas.create_line(200, 125, 225, 145, width=3)
        if wrong >= 5:
            self.canvas.create_line(200, 170, 180, 205, width=3)
        if wrong >= 6:
            self.canvas.create_line(200, 170, 220, 205, width=3)

    def _spaced(self, masked):
        """Adds spaces between characters for readability (keeps spaces in phrases)."""
        return " ".join(list(masked))

    def end_game(self):
        """Ends the game and displays the result."""
        self.stop_timer = True
        self.draw_hangman()
        if self.game.is_won():
            self.info_label.config(text="You won! 🎉")
        else:
            self.info_label.config(text=f"You lost! The answer was: {self.game.word}")
            self.entry.config(state="disabled")
            self.submit_btn.config(state="disabled")
if __name__ == "__main__":
    root = tk.Tk()  # Initialize the Tkinter root window
    app = HangmanUI(root)  # Create the game UI
    root.mainloop()  # Start the Tkinter event loop
