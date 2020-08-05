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
users = []


def handle_client(client):
    conn = client.conn
    addr = client.addr
    name = conn.recv(BUFF_SIZE).decode(FORMAT)
    client.set_name(name)
    clients[conn] = name
    users.append(client)

    while True:
        msg = conn.recv(BUFF_SIZE)
        receiver_name = msg.split()[0]
        # msg = msg.split(' ', 1)[1]
        if msg != "quit":
            send_message(msg, receiver_name)
        else:
            conn.close()
            del clients[conn]
            users.remove(client)
            break


def send_message(message, receiver):
    for user in users:
        if user.username == receiver:
            user.conn.send(message.encode(FORMAT))
            break


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


