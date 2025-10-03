from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from tcp_client import TCPClient

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.client = TCPClient("127.0.0.1", 5000)

        self.setWindowTitle("Dart Duel - Login")
        self.resize(500, 600)

        # Widgets
        self.label_username = QLabel("Username:")
        self.input_username = QLineEdit()

        self.label_password = QLabel("Password:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)

        self.button_login = QPushButton("Login")
        self.button_login.clicked.connect(self.handle_login)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.button_login)

        self.setLayout(layout)

        # Kết nối TCP
        self.client.on_message = self.on_server_message
        self.client.connect()

    def handle_login(self):
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password")
            return

        # Gửi request login lên server
        message = f"LOGIN {username} {password}"
        self.client.send(message)

    def on_server_message(self, msg: str):
        print("[LOGIN WINDOW] server:", msg)
        if msg.startswith("LOGIN_OK"):
            QMessageBox.information(self, "Success", "Login successful!")
            # TODO: chuyển sang giao diện Lobby
        elif msg.startswith("LOGIN_FAIL"):
            QMessageBox.warning(self, "Failed", "Wrong username or password")
