import socket

def start_server(IPv4, port):
    clientID = 0
    client_directory = {}

    #Start server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IPv4, port))
    server_socket.listen(1)
    print(f"Listening on {IPv4}:{port}...")

    #Handle client connection
    while True:
        print("Searching for client connection...")
        client_socket, client_address = server_socket.accept()
        print(f"Connected to {client_address}")
        client_socket.send(f"Your clientID is {clientID}.".encode('utf-8'))
        client_directory[f'{clientID}'] = {
            'socket' : client_socket,
            'address' : client_address
        }
        clientID += 1
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
            for key in client_directory:
                if client_directory[key]['socket'] == client_socket:
                    clientID = int(key)
                    break
            del client_directory[f'{clientID}']
            print(f"Connection to {clientID} closed.")
            clientID += 1

start_server('127.0.0.1', 8080)
