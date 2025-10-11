from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QTableWidget, QAbstractItemView, QVBoxLayout, QHBoxLayout, QPushButton

class MainView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Game")
        self.resize(500, 400)

        self.label_search_player = QLabel("Search Player:")
        self.input_search_player = QLineEdit()

        self.table_search_player = QTableWidget()
        self.table_search_player.setRowCount(5)
        self.table_search_player.setColumnCount(1)

        self.label_search_top_player = QLabel("Search Top Player:")
        self.input_search_top_player = QLineEdit()

        self.table_top_player = QTableWidget()
        self.table_top_player.setRowCount(5)
        self.table_top_player.setColumnCount(1)

        layout = QVBoxLayout()
        layout.addWidget(self.label_search_player)
        layout.addWidget(self.input_search_player)
        layout.addWidget(self.table_search_player)
        
        layout.addWidget(self.label_search_top_player)
        layout.addWidget(self.input_search_top_player)
        layout.addWidget(self.table_top_player)
        self.setLayout(layout)

