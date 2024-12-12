> ~~Generate a random number between 1 and 100.~~  
> ~~Allow the player to guess the number.~~  
> ~~Tell the player if the guess is too high, too low, or correct.~~  
> ~~End the game when the player guesses correctly.~~  
> ~~Add a maximum attempt limit (e.g., 10 attempts) for the player to guess the number.~~  
> ~~End the game when the player runs out of attempts.~~  
> ~~Display a message revealing the correct number if the player fails to guess.~~  
> ~~Ensure the player enters only integers.~~  
> ~~Handle non-integer inputs gracefully (e.g., text or symbols).~~  
> ~~Print a message if the input is invalid and prompt the player to try again.~~  
> ~~Allow the player to choose a difficulty level:~~  
> ~~> Easy: Number range (1-10)~~  
> ~~> Medium: Number range (1-100)~~  
> ~~> Hard: Number range (1-1000)~~  
> ~~Adjust the number range and attempt limit based on the difficulty level selected.~~  
> ~~Keep track of all guesses made by the player.~~  
> ~~Print the list of all previous guesses at the end of the game.~~  
> ~~Warn the player if they try to guess a number they have already guessed before.~~  
> ~~Calculate a score based on how quickly the player guesses the number.~~  
> ~~Display the final score at the end of the game.~~  
> ~~Save the player's progress (current attempts, current number, and guess history) to a JSON file.~~  
> ~~Allow the player to resume their previous game if it exists.~~  
> ~~Automatically load saved progress at the start of the game.~~  
> ~~Add color to the output for better visuals.~~  
> ~~> Use red for "Game Over" or "Incorrect" messages.~~  
> ~~> Use green for "Correct!" messages.~~  
> ~~Multiple accounts to run games concurrently~~  
> ~~Allow a player to host the game as a "server" using Python’s socket library.~~  
> ~~Send guess information and feedback (too high, too low) between players in real time.~~   

<u>Overlay Module<u>  
Window overlay that allows the player to toggle between account and game state  
Dynamically update as the account and game progress  

<u>Comprehensive Logging System<u>  
Log key events (e.g., player input, attempts, wins, and losses) to a file.  
Include timestamps for every log entry.  
Implement log levels (`INFO`, `DEBUG`, `ERROR`) using Python's logging module.  
Write logs to both a file and the console.   

<u>Refactoring for Maintainability<u>  
Refactor the game logic into a GuessingGame class.  
Break the game into smaller functions, such as:  
> `startgame()`  
> `processguess()`  
> `save_progress()`  
> `load_progress()`  
> `display_guess_history()`  

<u>Packaged & Distributable Version<u>  
Turn the game into a standalone package.  
Create a setup.py or pyproject.toml file for package distribution.  
Allow installation using pip install . and run it with a simple command (e.g., guessing-game).  
Publish it to PyPI as a public or private package.  