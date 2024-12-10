import random
import json
import socket

class RepeatGuess(Exception):
    pass

def take_yn_input(query_string):
    while True:
        user_input = input(f"{query_string}")
        try:
            if user_input == 'y' or user_input == 'n':
                return user_input
            else:
                raise ValueError()
        except ValueError:
            print("Must choose y or n.")
        

def guessing_game():
    game_skeleton = {
        "game_info": {
            "game_config": {
                "difficulty": 0,
                "random_number": 0
            },
            "gameplay": {
                "turns": 0,
                "guesses": [],
                "guess_temp": []
            }
        }
    }

    #Listen to player commands
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8080))
    print("Connected to the server at 127.0.0.1:8080")
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Player: {response}")
    if response == 'exit':
        print("The player has ended the game instance.")
        client_socket.close()
        return 0
    elif not response: 
        print("The game server has shut off.")
        client_socket.close()
        return 0
    else:
        print("New game:")
        return 1

    with open('player_progress.json', 'r+') as file:
        player_progress = json.load(file)
        formatted_dict = json.dumps(player_progress, indent=4)
        print(f"Current stats: \n{formatted_dict}")

        #Account config
        game_continuation = take_yn_input("Continue on previous account? (y/n)")
        if game_continuation == 'y' and player_progress['games'] != "":
            games_played = player_progress['games_played']
            print(f"Hello, {player_progress['username']}. Welcome back to my number guessing game!")
        else:
            player_progress['username'] = input("Choose username: ")
            player_progress['game_active'] = False
            player_progress['games'] = []
            player_progress['games_played'] = 0
            player_progress['points'] = 0
            file.seek(0)
            json.dump(player_progress, file, indent=4)
            file.truncate()
            print(f"Hello, {player_progress['username']}. Welcome to my number guessing game!")
        #Game config 
        games_played = player_progress['games_played']
        distance = 0
        random_number = 0
        if player_progress['games'] == [] or not player_progress['game_active']:
            current_game_progress = game_skeleton
            pass
        else: 
            current_game_progress = player_progress['games'][games_played]['game_info'] 
        if player_progress['game_active']:
            print(f"Config: {current_game_progress['game_config']}")
            print(f"Gameplay: {current_game_progress['gameplay']}")
            random_number = current_game_progress['game_config']['random_number']
            if current_game_progress['gameplay']['guesses'] != []:
                last_guess = current_game_progress['gameplay']['guesses'][-1]
                distance = abs(random_number - last_guess)
            restart_inquiry = take_yn_input("Would you like to continue your current game? (y/n)")
            if restart_inquiry == 'n':
                player_progress['game_active'] = False
                player_progress['games_played'] += 1
        if not player_progress['game_active']:
            while True:
                user_input = input("Choose a difficulty level:\n1. Easy (10)\n2. \033[93mMedium (100)\033[0m\n3. \033[31mHard (1000)\033[0m\n\n")
                try:
                    difficulty_choice = int(user_input)
                    if difficulty_choice < 1 or difficulty_choice > 3:
                        raise ValueError("Must choose a value corresponding to the difficulty level.")
                    break
                except ValueError:
                    print(f"Must input an integer, your input {user_input}.")
            new_game = game_skeleton
            new_game['game_info']['game_config']['difficulty'] = difficulty_choice
            random_number = int(random.random() * 10**(difficulty_choice) // 1)
            new_game['game_info']['game_config']['random_number'] = random_number
            player_progress['game_active'] = True
            player_progress['games'].append(game_skeleton)
            file.seek(0)
            json.dump(player_progress, file, indent=4)
            file.truncate()
            print(random_number)
        print(distance)
        #Gameplay
        max_turns = 10
        current_gameplay = player_progress['games'][games_played]['game_info']['gameplay']
        if current_gameplay['guesses'] != []:
            player_guess = current_gameplay['guesses'][-1]
        else: player_guess = 0
        while player_guess != random_number:
            while True:
                user_input = input("Guess a number: ")
                try:
                    player_guess = int(user_input)
                    if(player_guess in current_gameplay['guesses']):
                        raise RepeatGuess()
                    break
                except ValueError:
                    print(f"Must input an integer, your input {user_input}.")
                except RepeatGuess:
                    print(f"Already guessed {player_guess}, please choose another number.")
            current_gameplay['guesses'].append(player_guess)
            current_gameplay['turns'] += 1
            if (current_gameplay['turns']) == 10:
                break
            if(player_guess > random_number):
                print("Too high!")
            elif(player_guess < random_number):
                print("Too low!")
            if current_gameplay['turns'] > 1:
                if distance > abs(random_number - player_guess):
                    current_gameplay['guess_temp'].append("Warmer")
                    print("Warmer")
                else:
                    current_gameplay['guess_temp'].append("Colder")
                    print("Colder")
            distance = abs(random_number - player_guess)
            file.seek(0)
            json.dump(player_progress, file, indent=4)
            file.truncate()

        player_progress['games_played'] += 1
        points_earned = player_progress['games'][games_played]['game_info']['game_config']['difficulty'] * (max_turns - current_gameplay['turns'])
        player_progress['games'][games_played]['game_info']['points_earned'] = points_earned
        player_progress['points'] += points_earned
        if player_guess == random_number:
            print(f"\033[5mYou win!!\033[0m You guessed {player_guess} in {current_gameplay['turns']} turns.")
        else:
            print(f"You lose. You exceeded the maximum of {max_turns} turns.\nThe correct number was {random_number}.")
        player_progress['game_active'] = False
        file.seek(0)
        json.dump(player_progress, file, indent=4)
        file.truncate()

def main():
    run_instance = 1
    while run_instance == 1:
        run_instance = guessing_game()