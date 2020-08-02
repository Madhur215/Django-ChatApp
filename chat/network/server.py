import socket
import threading
from chat.models import UserProfile

PORT = 5050
IP = socket.gethostbyname(socket.gethostname())
BUFF_SIZE = 1024
FORMAT = 'utf-8'
ADDRESS = (IP, PORT)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(ADDRESS)

clients = {}
addresses = {}


def handle_client(conn):
    pass


def run_server():
    server_socket.listen()
    print(f"[SERVER] is running on {IP}")

    while True:
        conn, address = server_socket.accept()
        addresses[conn] = address
        thread = threading.Thread(target=handle_client, args=(conn,))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


run_server()


