# Hangman-Game-s391075

Hangman Game - Python with Tkinter UI (TDD Concept)

This is a Hangman game developed in Python using the Tkinter library for the graphical user interface (GUI). The game is based on the classic word-guessing game where the player must guess a randomly chosen word or phrase, one letter at a time, before they run out of lives. The game incorporates an interactive, colorful user interface, real-time timer, and dynamic hangman drawing that reacts to the player's guesses.

Features

  1. Interactive UI: The game features a clean and user-friendly graphical interface built using Tkinter, including vibrant colors, fonts, and responsive buttons.

  2. Word Levels: Players can choose between two difficulty levels — Basic and Intermediate, with different sets of words and phrases.

  3. Live Countdown Timer: The game has a built-in timer that counts down with each guess, and players lose a life if the timer runs out.

  4. Dynamic Hangman Drawing: The hangman figure is drawn progressively as the player makes incorrect guesses. The game graphically shows the body parts of the hangman based on the number of wrong guesses.

  5. Game Reset: Players can restart the game without needing to reload the application, ensuring a smooth experience.

  6. Real-Time Feedback: The game provides live feedback on the number of remaining lives, the current word (masked with guessed letters), and the time left.

Key Concepts

  1. Test-Driven Development (TDD): The game was developed using the principles of Test-Driven Development. Various aspects of the game’s logic, such as word generation, player guesses, and timer, were tested before implementation to ensure correctness.

  2. Timer Logic: The game features a built-in timer to challenge players, adding an extra layer of difficulty and excitement. When the timer runs out, the player loses a life, and the   game continues.

  3. Hangman Drawing: As the player makes incorrect guesses, a hangman figure is progressively drawn to visually represent the player’s remaining lives.

Technologies Used

 1. Python 3: The core programming language.

 2. Tkinter: A standard Python library for creating GUIs, used for rendering the game's interface.

 3. Threading: Used to implement the real-time countdown timer without blocking the main UI thread.
