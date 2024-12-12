import random
import json
import socket

class RepeatGuess(Exception):
    pass

def connect_game_client_to_server(IPv4, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IPv4, port))
    print(f"Client connected to the server at {IPv4}:{port}")
    return client_socket

def take_yn_input(server_client, query_string):
    while True:
        server_client.send(f"{query_string}".encode('utf-8'))
        data = server_client.recv(1024)
        if not data:
            print("Server shutdown.")
            break
        player_response = data.decode('utf-8')
        try:
            if player_response == 'y' or player_response == 'n':
                return player_response
            else:
                raise ValueError()
        except ValueError:
            server_client.send(f"{receiver},Must choose y or n.".encode('utf-8'))

def reset_player_progress(player_progress):
    player_progress['game_active'] = False
    player_progress['games'] = []
    player_progress['games_played'] = 0
    player_progress['points'] = 0
    return player_progress

def guessing_game(client_socket, player_progress):
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

    print(f"Current stats: \n{player_progress}\n")
    #Game config 
    games_played = player_progress['games_played']
    distance = 0
    random_number = 0
    if player_progress['games'] == [] or not player_progress['game_active']:
        current_game_progress = game_skeleton
    else: 
        current_game_progress = player_progress['games'][games_played]['game_info']
    if player_progress['game_active']:
        print(f"Config: {current_game_progress['game_config']}")
        print(f"Gameplay: {current_game_progress['gameplay']}")
        random_number = current_game_progress['game_config']['random_number']
        if current_game_progress['gameplay']['guesses'] != []:
            last_guess = current_game_progress['gameplay']['guesses'][-1]
            distance = abs(random_number - last_guess)
        restart_inquiry = take_yn_input(client_socket, "Would you like to continue your current game? (y/n)")
        if restart_inquiry == 'n':
            player_progress['game_active'] = False
            player_progress['games_played'] += 1
    if not player_progress['game_active']:
        while True:
            error_string = ""
            difficulty_choice_query_string = error_string + "Choose a difficulty level:\n1. Easy (10)\n2. Medium (100)\n3. Hard (1000)\n"
            client_socket.send(difficulty_choice_query_string.encode('utf-8'))
            difficulty_choice_query_choice = client_socket.recv(1024).decode('utf-8')
            try:
                difficulty_choice = int(difficulty_choice_query_choice)
                if difficulty_choice < 1 or difficulty_choice > 3:
                    raise ValueError()
                break
            except ValueError:
                error_string = f"Must input an integer that corresponds to a difficulty level. Your input was {difficulty_choice_query_choice}.\n"
        new_game = game_skeleton
        new_game['game_info']['game_config']['difficulty'] = difficulty_choice
        random_number = int(random.random() * 10**(difficulty_choice) // 1)
        new_game['game_info']['game_config']['random_number'] = random_number
        player_progress['game_active'] = True
        player_progress['games'].append(game_skeleton)
        print(random_number)
        print(distance)

    #update JSON with new game config 
    serialized_updated_player_progress = json.dumps(player_progress, indent=4)
    client_socket.send(f"player_progress {serialized_updated_player_progress}".encode('utf-8'))
    print(client_socket.recv(1024).decode('utf-8'))

    #Gameplay
    player_progress_game_list = player_progress['games'][games_played]
    max_turns = player_progress_game_list['game_info']['game_config']['difficulty'] * 5
    current_gameplay = player_progress_game_list['game_info']['gameplay']
    # print(f"guessing_game::early gameplay: {current_gameplay}")
    if current_gameplay['guesses'] != []:
        player_guess = current_gameplay['guesses'][-1]
    else: player_guess = 0
    guess_guidance_string = ""
    while player_guess != random_number:
        error_string = ""
        while True:
            client_socket.send(f"\nPrevious guess guidance:\n{guess_guidance_string}\n{error_string}\nGuess a number ({max_turns - current_gameplay['turns']} Remaining):".encode('utf-8'))
            user_input = client_socket.recv(1024).decode('utf-8')
            try:
                player_guess = int(user_input)
                if(player_guess in current_gameplay['guesses']):
                    raise RepeatGuess()
                break
            except ValueError:
                error_string = f"Must input an integer, your input {user_input}."
            except RepeatGuess:
                error_string = f"Already guessed {player_guess}, please choose another number."
        current_gameplay['guesses'].append(player_guess)
        current_gameplay['turns'] += 1
        if (current_gameplay['turns']) == 10:
            break
        if(player_guess > random_number):
            guess_guidance_string = "Too high!"
        elif(player_guess < random_number):
            guess_guidance_string = "Too low!"
        if current_gameplay['turns'] > 1:
            if distance > abs(random_number - player_guess):
                current_gameplay['guess_temp'].append("Warmer")
                guess_guidance_string += "\nWarmer"
            else:
                current_gameplay['guess_temp'].append("Colder")
                guess_guidance_string += "\nColder"
        distance = abs(random_number - player_guess)

        #update JSON with new move
        player_progress['games'][games_played]['game_info']['gameplay'] = current_gameplay
        serialized_updated_player_progress = json.dumps(player_progress, indent=4)
        client_socket.send(f"player_progress {serialized_updated_player_progress}".encode('utf-8'))
        print(client_socket.recv(1024).decode('utf-8'))

    #update JSON with new game result 
    player_progress['games_played'] += 1
    # print(f"Game client::Guessing game: {player_progress['games'][games_played]}")
    points_earned = player_progress['games'][games_played]['game_info']['game_config']['difficulty'] * (max_turns - current_gameplay['turns'])
    # print(player_progress['games'][games_played])
    player_progress['games'][games_played]['game_info']['points_earned'] = points_earned
    current_game = player_progress['games'][games_played]
    current_game['game_info']['points_earned'] = points_earned
    player_progress['points'] += points_earned
    if player_guess == random_number:
        print(f"\033[5mYou win!!\033[0m You guessed {player_guess} in {current_gameplay['turns']} turns.")
    else:
        print(f"You lose. You exceeded the maximum of {max_turns} turns.\nThe correct number was {random_number}.")
    player_progress['game_active'] = False
    serialized_updated_player_progress = json.dumps(player_progress, indent=4)
    client_socket.send(f"player_progress {serialized_updated_player_progress}".encode('utf-8'))
    print(client_socket.recv(1024).decode('utf-8'))

def configure_game_client(IPv4, port): 
    #connect to server_socket
    client_socket = connect_game_client_to_server(IPv4, port)

    #receive any existing player progress from game server
    client_socket.send("READY".encode('utf-8'))
    serialized_player_progress = client_socket.recv(4096).decode('utf-8')
    player_progress = json.loads(serialized_player_progress)
    continuation_inquiry_choice = "n"
    if player_progress['games'] != []:
        #ask player if they want to continue on previous account progress
        query_string = f"You have an existing account, with the following state:\n{player_progress}. \ny to continue. \nn to restart."
        continuation_inquiry_choice = take_yn_input(client_socket, query_string)
        print(f"configure_game_client::continuation_inquiry_choice: {continuation_inquiry_choice}")

    #create or resume account
    print(f"configure_game_client::player_progress: {player_progress}")
    if continuation_inquiry_choice != 'y':
        player_progress = reset_player_progress(player_progress)
    
    #update central JSON
    serialized_player_progress = json.dumps(player_progress)
    client_socket.send(f"player_progress {serialized_player_progress}".encode('utf-8'))
    print(client_socket.recv(1024).decode('utf-8'))

    print("Game config complete, starting the game.")

    #Run game until player exits (no threading required since its a single player interaction in this case)
    while True:
        game_start_inquiry = take_yn_input(client_socket, "Start new game?\ny to start a new game. \nn to exit.")
        if game_start_inquiry == 'n':
            break
        guessing_game(client_socket, player_progress)
    client_socket.send("Shutting down game client.".encode('utf-8'))
    client_socket.close()
    return