from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal
from login_view import LoginView

class MainView(QWidget):
    message_received = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dart Duel")
        self.resize(500, 400)

        self.button_register_view = QPushButton("Register")
        self.button_register_view.clicked(LoginView())
        self.button_login_view = QPushButton("Login")
        self.button_register_view.clicked(LoginView())

        layout = QVBoxLayout()
        layout.addWidget(self.button_register_view)
        layout.addWidget(self.button_login_view)
        self.setLayout(layout)