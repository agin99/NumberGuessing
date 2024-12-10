import socket
import threading
import json

client_directory = {'clients' : {}}

def handle_client(clientID, client_socket, client_address):
    print(f"Connected to {client_address}")
    client_socket.send(f"Your clientID is {clientID}.".encode('utf-8'))
    #Handle player action
    try: 
        while True:
            msg = client_socket.recv(1024).decode('utf-8')
            msg = msg.split(',')
            if msg == '' or msg[1] == 'exit':
                print(f"Client {msg[0]} disconnected.")
                break
            target = client_directory['clients'][msg[0]]['socket']
            target.send(msg[1].encode('utf-8'))
    finally:
        client_socket.close()
        del client_directory['clients'][f'{clientID}']
        print(f"Connection to {clientID} closed.")
    return client_directory

def start_server(IPv4, port):
    #Start server
    clientID = 0
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IPv4, port))
    server_socket.listen(3)
    print(f"Listening on {IPv4}:{port}...")
    try:
        while True:
            print("Searching for client connection...")
            client_socket, client_address = server_socket.accept()
            client_IPv4, client_port = client_socket.getpeername()
            client_directory['clients'][f'{clientID}'] = {
                'IPv4' : client_IPv4,
                'port' : client_port,
                'socket' : client_socket
            }
            client_thread = threading.Thread(target=handle_client, args=(clientID, client_socket, client_address))
            clientID += 1
            client_thread.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")  
    finally:
        for client in client_directory:
            client_socket = socket.connect(client['clients']['IPv4'], client['clients']['port'])
            client_socket.close()
            del client
        server_socket.close()
        print("Server fully shut down.")
