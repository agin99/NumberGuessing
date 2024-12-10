import socket

def handle_client(client_directory, clientID, client_socket, client_address):
    print(f"Connected to {client_address}")
    client_socket.send(f"Your clientID is {clientID}.".encode('utf-8'))
    #Handle player action
    try: 
        while True:
            msg = client_socket.recv(1024).decode('utf-8')
            if msg == 'exit':
                print(f"Client {clientID} disconnected.")
                break
            print(f"Client {clientID}: {msg}")
    finally:
        client_socket.close()
        del client_directory[f'{clientID}'] 
        print(f"Connection to {clientID} closed.")
    return client_directory

def main():
    #Start server
    clientID = 0
    client_directory = {}
    IPv4 = '127.0.0.1'
    port = 8080
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IPv4, port))
    server_socket.listen(1)
    print(f"Listening on {IPv4}:{port}...")

    try:
        while True:
            print("Searching for client connection...")
            client_socket, client_address = server_socket.accept()
            client_directory[f'{clientID}'] = {
                'socket' : client_socket,
                'address' : client_address
            }
            handle_client(client_directory, clientID, client_socket, client_address)
            clientID += 1
    except KeyboardInterrupt:
        print("\nServer shutting down...")
        
    finally:
        server_socket.close()
        print("Server fully shut down.")

main()