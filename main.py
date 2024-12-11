# import basic_game
import server 
import threading

def main():
    IPv4 = '127.0.0.1'
    player_port = 8080
    game_port = 8081
    server_thread = threading.Thread(target=server.start_server, args=(IPv4, player_port, game_port))
    server_thread.start()

main()