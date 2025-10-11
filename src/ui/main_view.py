
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from tcp_client import TCPClient
import threading

class MainView(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Danh sách người chơi online")
        self.resize(600, 400)

        title = QLabel("Người chơi đang online")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")

        # Table for online players
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Tên", "Tổng điểm", "Trạng thái", "Thách đấu"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.table)
        self.setLayout(layout)

        # TCP client setup
        self.tcp_client = TCPClient()
        self.tcp_client.on_message = self.on_message
        threading.Thread(target=self.tcp_client.connect, daemon=True).start()

        threading.Timer(0.5, self.fetch_online_players).start()

    def fetch_online_players(self):
        if self.tcp_client.is_connected:
            self.tcp_client.send_object({"command": "get_online_players"})

    def on_message(self, data):
        if data.get("command") == "online_players":
            players = data.get("players", [])
            self.table.setRowCount(len(players))
            for row, player in enumerate(players):
                self.table.setItem(row, 0, QTableWidgetItem(player.get("name", "")))
                self.table.setItem(row, 1, QTableWidgetItem(str(player.get("score", 0))))
                status = player.get("status", "")
                self.table.setItem(row, 2, QTableWidgetItem(status))
                btn = QPushButton("Thách đấu")
                btn.setEnabled(status == "Đang rỗi")
                self.table.setCellWidget(row, 3, btn)

