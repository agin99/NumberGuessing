import socket

def connect_client_to_game(IPv4, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IPv4, port))
    print(f"Client connected to the server at {IPv4}:{port}")
    return client_socket

def main(): 
    try:
        #Connect player to game server
        server_IPv4 = input("Submit the server IPv4: ")
        server_port = int(input("Submit the server port: "))
        client_socket = connect_client_to_game(server_IPv4, server_port)

        #Send messages to game server
        while True:
            msg = input("What would you like to say to the server? \n")
            if not msg:
                print("Closing the connection to the server.")
                client_socket.send('exit'.encode('utf-8'))
                break
            client_socket.send(f"{msg}".encode('utf-8'))
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        print("Disconnecting client...")
        client_socket.close()
        print("Successfully disconnected.")
    

    #Respond to game server prompt

main()