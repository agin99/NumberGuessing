import socket

def connect_to_server(IPv4, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IPv4, port))
    print(f"Client connected to the server at {IPv4}:{port}")
    return client_socket

def main(): 
    try:
        #Connect player to game server
        server_IPv4 = input("Submit the server IPv4: ")
        server_port = int(input("Submit the server port: "))
        server_connection_socket = connect_to_server(server_IPv4, server_port)

        #Send messages to game server
        while True:
            data = server_connection_socket.recv(4096)
            if not data or data.decode('utf-8') == 'Shutting down game client.':
                print("Server shutdown.")
                break
            print(data.decode('utf-8'))
            player_response = input("")
            server_connection_socket.send(f"{player_response}".encode('utf-8'))
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        print("Closing connection between the player client and the server...")
        try:
            server_connection_socket.close()
            print("Successfully disconnected.")
        except Exception as e:
            print(f"Failed to close the connection between the player client and the server properly:\n{e}")
    return

main()