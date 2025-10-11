from PyQt5.QtWidgets import QWidget
from utils.ui_helper import set_background
from utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, HOST, PORT
from tcp_client import TCPClient

class GameView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fighting Game")
        self.resize(800, 600)