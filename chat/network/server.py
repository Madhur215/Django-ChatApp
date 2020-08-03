import socket
import threading
from chat.models import UserProfile
from . import person

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


def handle_client(client):
    conn = client.conn
    addr = client.addr
    name = conn.recv(BUFF_SIZE).decode(FORMAT)
    client.set_name(name)
    clients[conn] = name

    while True:
        msg = conn.recv(BUFF_SIZE)
        if msg != "quit":
            send_message(msg)
        else:
            conn.close()
            del clients[conn]
            break


def send_message(message):
    pass


def run_server():
    server_socket.listen()
    print(f"[SERVER] is running on {IP}")

    while True:
        conn, address = server_socket.accept()
        client = person.Person(conn, address)
        addresses[conn] = address
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


run_server()


