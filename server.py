import socket
import threading
import json
import multiprocessing
from game_client import configure_game_client

directory_skeleton = {'players' : {}}

def process_username_choice(client_socket, directory):
        client_socket.send("Username:".encode('utf-8'))
        client_id = client_socket.recv(4096).decode('utf-8')
        while True: 
            try:
                print('process_username_choice:', directory)
                if client_id not in directory['players']:
                    client_socket.send(f"Welcome {client_id}, please choose a password.".encode('utf-8'))
                    password = client_socket.recv(4096).decode('utf-8')
                    directory['players'][client_id] = {
                        "credentials": {
                            "username": client_id,
                            "password": password,
                        },
                        "game_active": False,
                        "games": [],
                        "games_played": 0,
                        "points": 0
                    }
                    with open('directory.json','r+') as file:
                        file.seek(0)
                        json.dump(directory, file, indent=4)
                        file.truncate()
                    return client_id
                else:
                    client_socket.send("Enter your password:".encode('utf-8'))
                    password_submission = client_socket.recv(4096).decode('utf-8')
                    if directory['players'][client_id]['credentials']['password'] != password_submission:
                        raise ValueError()
                    return client_id
            except ValueError:
                client_socket.send(f"Incorrect password, please try again.".encode('utf-8'))

def handle_game_client(client_id, directory, player_server_socket, game_server_socket):
    try: 
        while True:
            #listen for game_client messages
            game_client_msg = game_server_socket.recv(4096).decode('utf-8')
            print("Server, handle_game_client (1):", game_client_msg)
            if game_client_msg == '':
                print(f"Client {client_id} wants to disconnect.")
                break
            #relay to player_client
            if len(game_client_msg) > 15 and game_client_msg[0:15] == 'player_progress':
                print(game_client_msg[0:15])
                print(json.loads(game_client_msg[15:]))
                updated_player_progress = json.loads(game_client_msg[15:])
                directory['players'][client_id] = updated_player_progress
                with open('directory.json','r+') as file:
                    file.seek(0)
                    json.dump(directory, file, indent=4)
                    file.truncate()
                game_server_socket.send("Successfully updated".encode("utf-8"))
            else: 
                print("Server, handle_game_client (2):", game_client_msg)
                player_server_socket.send(game_client_msg.encode('utf-8'))
    except Exception as e:
        print(f"Failed to handle game client because of error: {e}")
    finally:
        print("Game client has been shut down.")
    

def handle_player_client(client_id, player_server_socket, game_server_socket):
    try: 
        while True:
            #listen for player_client messages
            player_client_msg = player_server_socket.recv(4096).decode('utf-8')
            #relay to game_client
            if player_client_msg == '' or player_client_msg == 'exit':
                print(f"Client {client_id} wants to disconnect.")
                break
            game_server_socket.send(player_client_msg.encode('utf-8'))
    except Exception as e:
        print(f"Client communication failed: {e}")
    finally:
        game_server_socket.close()
        print(f"Connection to game client closed.")
        player_server_socket.close()
        print(f"Connection to {client_id} closed.")

def create_game_client(IPv4, player_port, game_port, directory, client_id, game_server_socket, player_server_socket, client_address):
    print(f"Connected to {client_address}")
    #Handle player client request for game client
    game_client_socket = None
    try:
        while True: 
            if not game_client_socket:
                player_server_socket.send("Create a game client?".encode('utf-8'))
                msg = player_server_socket.recv(4096).decode('utf-8')
                print(f"Message in create_game_client:", msg)
                if msg == '' or msg == 'exit':
                    print(f"Client {client_id} disconnected.")
                    break
                elif msg == 'y': 
                    #Create game client thread
                    print("Checkpoint 1.")
                    process = multiprocessing.Process(target=configure_game_client, args=(IPv4, game_port))
                    process.start()
                    print("Checkpoint 2.")
                    game_client_socket, game_client_address = game_server_socket.accept()
                    player_client_thread = threading.Thread(
                        target=handle_player_client, 
                        args=(client_id, player_server_socket, game_client_socket)
                    )
                    player_client_thread.start()
                    print("Checkpoint 3.")
                    serialized_player_progress = json.dumps(directory['players'][client_id])
                    print("Checkpoint 4.")
                    ready_signal = game_client_socket.recv(1024).decode('utf-8')
                    if ready_signal == 'READY':
                        print("Game client is ready to receive data")
                    print("Sending player progress data to game client.")
                    game_client_socket.send(serialized_player_progress.encode('utf-8'))
                    game_client_thread = threading.Thread(
                        target=handle_game_client, 
                        args=(client_id, directory, player_server_socket, game_client_socket)
                    )
                    game_client_thread.start()
                elif msg == 'n':
                    player_server_socket.send("Got it. When ready respond y to create a game client or exit to shut down.".encode('utf-8'))
                else:
                    raise ValueError()
    except ValueError:
        client_socket.send(
        f"""The allowed choices are: 
        1. y to create a game client.
        2. n to keep the account open.
        3. exit to cose the account.""".encode('utf-8'))
    finally: 
        print(f"Player requested to end game. Closing sockets...")
        if game_client_socket and not game_client_socket._closed:
            try:
                game_client_socket.close()
                print(f"Connection to game client {game_client_address} closed.")
            except Exception as e:
                print(f"Failed to disconnect game client properly: {e}")
        else: 
            print(f"No game client to close for {client_id}")
        try:
            if not client_socket._closed:
                client_socket.close()
                print(f"Connection to player client {client_address} closed.")
        except Exception as e:
            print(f"Failed to disconnect player client properly: {e}")

def start_server(IPv4, player_port, game_port):
    #Start server
    game_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    game_server_socket.bind((IPv4, game_port))
    game_server_socket.listen(3)
    print(f"Listening for game client connections on {IPv4}:{game_port}...")
    player_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    player_server_socket.bind((IPv4, player_port))
    player_server_socket.listen(3)
    print(f"Listening for player client connections on {IPv4}:{player_port}...")
    with open('directory.json', 'r') as file:
        directory = json.load(file)
    try:
        while True:
            print("Searching for client connection...")
            #Connect new player client to server 
            client_socket, client_address = player_server_socket.accept()
            client_id = process_username_choice(client_socket, directory)
            create_game_client_thread = threading.Thread(
                target=create_game_client, 
                args=(IPv4, player_port, game_port, directory, client_id, game_server_socket, client_socket, client_address)
            )
            create_game_client_thread.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")  
    finally:
        for client in directory:
            client_socket = socket.connect(client['clients']['IPv4'], client['clients']['port'])
            client_socket.close()
            del client
        server_socket.close()
        print("Server fully shut down.")
