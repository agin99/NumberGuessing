# import basic_game
import game_server_startup 
import threading

def main():
    IPv4 = '127.0.0.1'
    port = 8080
    game_server_thread = threading.Thread(target=game_server_startup.start_server, args=(IPv4, port))
    game_server_thread.start()

main()