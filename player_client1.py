import socket

def connect_client_to_game(IPv4, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IPv4, port))
    print(f"Client connected to the server at {IPv4}:{port}")
    return client_socket

def main(): 
    try:
        #Connect player to game server
        # server_IPv4 = input("Submit the server IPv4: ")
        # server_port = int(input("Submit the server port: "))
        # game_connection = connect_client_to_game(server_IPv4, server_port)
        game_connection = connect_client_to_game('127.0.0.1', 8080)

        #Send messages to game server
        while True:
            # msg = input("What would you like to say to the server? \n")
            # if not msg:
            #     print("Closing the connection to the server.")
            #     game_connection.send('exit'.encode('utf-8'))
            #     break
            data = game_connection.recv(1024)
            if not data:
                print("Server shutdown.")
                break
            print(data.decode('utf-8'))
            # game_connection.send(f"0, {msg}".encode('utf-8'))
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        print("Disconnecting client...")
        game_connection.close()
        print("Successfully disconnected.")
    

    #Respond to game server prompt

main()