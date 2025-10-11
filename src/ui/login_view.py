from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal
from tcp_client import TCPClient
from .main_view import MainView
from uuid import uuid4

class LoginView(QWidget):
    message_received = pyqtSignal(dict)
    go_to_register = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.client = TCPClient("172.11.32.112", 5000)

        self.setWindowTitle("Login Form")
        self.resize(500, 400)

        self.label_username = QLabel("Username:")
        self.input_username = QLineEdit()
        
        self.label_password = QLabel("Password:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        
        self.button_login = QPushButton("Login")
        self.button_login.setStyleSheet("background-color: #2196F3; color: white;")
        self.button_login.clicked.connect(self.handle_login)

        self.button_register = QPushButton("Register")
        self.button_register.setStyleSheet("background-color: #4CAF50; color: white;")
        self.button_register.clicked.connect(self.go_to_register.emit)

        layout = QVBoxLayout()
        
        username_row = QHBoxLayout()
        username_row.addWidget(self.label_username)
        username_row.addWidget(self.input_username)
        layout.addLayout(username_row)
        
        password_row = QHBoxLayout()
        password_row.addWidget(self.label_password)
        password_row.addWidget(self.input_password)
        layout.addLayout(password_row)
        
        layout.addWidget(self.button_login)
        layout.addWidget(self.button_register)
        self.setLayout(layout)

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
            self.close()
            self.main_view = MainView()
            self.main_view.show()
        else:
            message = msg.get("message")
            QMessageBox.warning(self, "Failed", message or "Wrong username or password")
