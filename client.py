import socket
import threading
import pickle
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem
from PyQt5 import uic

HOST = ("192.168.0.106", 7777)


class Messenger(QMainWindow):
    def __init__(self, name):
        super().__init__()
        uic.loadUi("a.ui", self)
        self.name = name
        self.button.clicked.connect(self.send)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(HOST)
        self.t = threading.Thread(target=self.f, args=())
        self.t.start()

    def f(self, *args, **kwargs):
        while True:
            data = self.sock.recv(1024)
            if data:
                d = pickle.loads(data)
                item = QListWidgetItem(f"{d['name']}: {d['message']}")
                self.chat.addItem(item)

    def send(self):
        msg = self.message.text()
        self.message.clear()
        if msg:
            item = QListWidgetItem("Вы: " + msg)
            self.chat.addItem(item)
            d = {"name": self.name, "message": msg}
            self.sock.send(pickle.dumps(d))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mess = Messenger("User1")
    mess.show()
    sys.exit(app.exec())
