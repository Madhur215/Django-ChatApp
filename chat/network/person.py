

class Person:

    def __init__(self, conn, addr):
        self.addr = addr
        self.conn = conn
        self.username = None

    def __repr__(self):
        return f"Person({self.addr}, {self.username})"

    def set_name(self, name):
        self.username = name
