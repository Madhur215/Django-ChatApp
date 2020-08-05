import threading
import socket

class Client:

    PORT = 5050
    IP = socket.gethostbyname(socket.gethostname())
    BUFF_SIZE = 1024
    FORMAT = 'utf-8'
    ADDRESS = (IP, PORT)

    def __init__(self, name):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.connect(self.ADDRESS)
        self.messages = []
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()
        self.send_message(name)

    def receive_messages(self):

        while True:
            try:
                msg = self.client_socket.recv(self.BUFF_SIZE).decode(self.FORMAT)
                self.messages.append(msg)
            except Exception as e:
                print("[EXCEPTION] e")
                break

    def send_message(self, message):

        try:
            self.client_socket.send(message.encode(self.FORMAT))
            if message == "quit":
                self.client_socket.close()
        except Exception as e:
            print("[EXCEPTION] e")


