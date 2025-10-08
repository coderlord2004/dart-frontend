from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal
from tcp_client import TCPClient

class RegisterView(QWidget):
    message_received = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.client = TCPClient()

        self.setWindowTitle("Register")
        self.resize(500, 400)

        self.label_username = QLabel("Username:")
        self.input_username = QLineEdit()
        self.label_password = QLabel("Password:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        self.button_login = QPushButton("Login")
        self.button_login.clicked.connect(self.handle_login)

        layout = QVBoxLayout()
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.button_login)
        self.setLayout(layout)

        # signal-slot kết nối
        self.message_received.connect(self.on_receive_from_server)
        self.client.on_message = self._handle_tcp_message
        self.client.connect()

    def handle_login(self):
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password")
            return

        request = {
            "command": "login",
            "body": {
                "username": username,
                "password": password,
            },
        }
        self.client.send_object(request)

    def _handle_tcp_message(self, msg: dict):
        self.message_received.emit(msg)

    def on_receive_from_server(self, msg: dict):
        success = msg.get("ok")
        if success:
            QMessageBox.information(self, "Success", "Login successful!")
        else:
            message = msg.get("message")
            QMessageBox.warning(self, "Failed", message or "Wrong username or password")
