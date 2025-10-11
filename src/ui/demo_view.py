from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor
from .login_view import LoginView
from .register_view import RegisterView
from utils.ui_helper import set_background
from utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT

class DemoView(QWidget):
    message_received = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dart Duel")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        set_background(self, "demo_background.jpg")

        self.button_register_view = QPushButton("Đăng ký")
        self.button_register_view.setStyleSheet("background-color: #4CAF50; color: white;")
        self.button_register_view.setFixedWidth(100)
        self.button_register_view.setFixedHeight(40)
        self.button_register_view.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_register_view.clicked.connect(self.open_register_view)
        
        self.button_login_view = QPushButton("Đăng nhập")
        self.button_login_view.setStyleSheet("background-color: #2196F3; color: white;")
        self.button_login_view.setFixedWidth(100)
        self.button_login_view.setFixedHeight(40)
        self.button_login_view.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_login_view.clicked.connect(self.open_login_view)

        layout = QVBoxLayout()
        layout.addStretch(5)

        # Center both buttons in the same row
        button_row = QHBoxLayout()
        button_row.addStretch(1)
        button_row.addWidget(self.button_register_view)
        button_row.addSpacing(20)
        button_row.addWidget(self.button_login_view)
        button_row.addStretch(1)
        layout.addLayout(button_row)

        layout.addStretch(1)
        self.setLayout(layout)
        
    def open_login_view(self):
        self.hide()
        self.login_view = LoginView()
        self.login_view.go_to_register.connect(self.open_register_from_login)
        self.login_view.show()

    def open_register_view(self):
        self.hide()
        self.register_view = RegisterView()
        self.register_view.go_to_login.connect(self.open_login_from_register)
        self.register_view.show()
        
    def open_login_from_register(self):
        self.register_view.close()
        self.open_login_view()
    
    def open_register_from_login(self):
        self.login_view.close()
        self.open_register_view()