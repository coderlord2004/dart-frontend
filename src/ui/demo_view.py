from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal
from .login_view import LoginView
from .register_view import RegisterView

class DemoView(QWidget):
    message_received = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dart Duel")
        self.resize(500, 400)

        self.button_register_view = QPushButton("Register")
        self.button_register_view.setStyleSheet("background-color: #4CAF50; color: white;")
        self.button_register_view.clicked.connect(self.open_register_view)
        
        self.button_login_view = QPushButton("Login")
        self.button_login_view.setStyleSheet("background-color: #2196F3; color: white;")
        self.button_login_view.clicked.connect(self.open_login_view)

        layout = QVBoxLayout()
        layout.addWidget(self.button_register_view)
        layout.addWidget(self.button_login_view)
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