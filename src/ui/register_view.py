from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import pyqtSignal
from tcp_client import TCPClient
from utils.ui_helper import set_background


class RegisterView(QWidget):
    message_received = pyqtSignal(dict)
    go_to_login = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.client = TCPClient("172.11.32.112", 5000)

        self.setWindowTitle("Register Form")
        self.resize(500, 400)

        # Gán tên object để tránh CSS ảnh hưởng widget con
        self.setObjectName("register_form")

        # Đặt ảnh nền chỉ cho widget này (không ảnh hưởng input/button)
        set_background(self, "background.jpg")

        # --- UI Components ---
        self.label_username = QLabel("Username:")
        self.input_username = QLineEdit()

        self.label_password = QLabel("Password:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)

        self.button_register = QPushButton("Register")
        self.button_register.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        self.button_register.setFixedHeight(40)
        self.button_register.clicked.connect(self.handle_register)

        self.button_login = QPushButton("Login")
        self.button_login.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
        """)
        self.button_login.setFixedHeight(40)
        self.button_login.clicked.connect(self.go_to_login.emit)

        # --- Layout ---
        layout = QVBoxLayout()

        username_row = QHBoxLayout()
        username_row.addWidget(self.label_username)
        username_row.addWidget(self.input_username)
        layout.addLayout(username_row)

        password_row = QHBoxLayout()
        password_row.addWidget(self.label_password)
        password_row.addWidget(self.input_password)
        layout.addLayout(password_row)

        button_row = QHBoxLayout()
        button_row.addStretch(1)
        button_row.addWidget(self.button_register)
        button_row.addWidget(self.button_login)
        button_row.addStretch(1)
        layout.addLayout(button_row)

        # Container trong suốt để nội dung không che nền
        container = QWidget(self)
        container.setLayout(layout)
        container.setStyleSheet("background: transparent;")
        container.setGeometry(60, 80, 380, 250)

        # --- TCP setup ---
        self.message_received.connect(self.on_receive_from_server)
        self.client.on_message = self._handle_tcp_message
        self.client.connect()

    # ========================
    #        HANDLERS
    # ========================
    def handle_register(self):
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password")
            return

        request = {
            "command": "register",
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
            QMessageBox.information(self, "Success", "Register successful!")
            self.go_to_login.emit()
        else:
            message = msg.get("message")
            QMessageBox.warning(self, "Failed", message or "Registration failed")
