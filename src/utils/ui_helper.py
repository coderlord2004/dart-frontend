from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt
import os

def set_background(widget, image_name: str):
    abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", image_name))
    if not os.path.exists(abs_path):
        print(f"[ERROR] Background image not found: {abs_path}")
        return

    pixmap = QPixmap(abs_path)
    if pixmap.isNull():
        print(f"[ERROR] Cannot load pixmap: {abs_path}")
        return

    def update_background():
        scaled = pixmap.scaled(
            widget.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        palette = widget.palette()
        palette.setBrush(widget.backgroundRole(), QBrush(scaled))
        widget.setPalette(palette)
        widget.setAutoFillBackground(True)

    update_background()
    widget.resizeEvent = lambda event: update_background()

    print(f"[INFO] Background loaded and auto-scaled from: {abs_path}")
