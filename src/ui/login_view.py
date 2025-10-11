from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor
from tcp_client import TCPClient
from .main_view import MainView
from uuid import uuid4
from utils.ui_helper import set_background
from utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, HOST, PORT

class LoginView(QWidget):
    message_received = pyqtSignal(dict)
    go_to_register = pyqtSignal()

    def center_container(self):
        parent_width = self.width()
        parent_height = self.height()
        container_x = (parent_width - self.container_width) // 2
        container_y = (parent_height - self.container_height) // 2
        self.container.setGeometry(container_x, container_y, self.container_width, self.container_height)
        
    def resizeEvent(self, event):
        self.center_container()
        super().resizeEvent(event)

    def __init__(self):
        super().__init__()
        self.client = TCPClient(HOST, PORT)

        self.setWindowTitle("Login Form")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        set_background(self, "demo_background.jpg")

        self.label_username = QLabel("Username:")
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Nhập username")
        self.input_username.setFixedHeight(40)
        
        self.label_password = QLabel("Password:")
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Nhập password")
        self.input_password.setFixedHeight(40)
        self.input_password.setEchoMode(QLineEdit.Password)
        
        self.button_login = QPushButton("Đăng nhập")
        self.button_login.setStyleSheet("background-color: #2196F3; color: white;")
        self.button_login.setFixedWidth(100)
        self.button_login.setFixedHeight(40)
        self.button_login.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_login.clicked.connect(self.handle_login)

        self.label_button_register = QLabel("Chưa có tài khoản?")
        self.button_register = QPushButton("Đăng ký ngay")
        self.button_register.setStyleSheet("background-color: #4CAF50; color: white;")
        self.button_register.setFixedWidth(100)
        self.button_register.setFixedHeight(40)
        self.button_register.setCursor(QCursor(Qt.PointingHandCursor))
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
        
        login_row = QHBoxLayout()
        login_row.addStretch(1)
        login_row.addWidget(self.button_login)
        login_row.addStretch(1)
        layout.addLayout(login_row)
        
        register_row = QHBoxLayout()
        register_row.addStretch(1)
        register_row.addWidget(self.label_button_register)
        register_row.addWidget(self.button_register)
        register_row.addStretch(1)
        layout.addLayout(register_row)
        

        self.container_width = 380
        self.container_height = 250
        self.container = QWidget(self)
        self.container.setObjectName("loginContainer")
        self.container.setStyleSheet("""
            #loginContainer {
                background-color: rgba(0, 0, 0, 0.5);
                color: white;
                border-radius: 8px;
            }
            #loginContainer QLabel, #loginContainer QPushButton {
                color: white;
                font-size: 14px;
            }
            #loginContainer QLineEdit {
                background-color: rgba(0, 0, 0, 0.3);
                color: white;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)
        self.container.setLayout(layout)
        self.center_container()
        
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
