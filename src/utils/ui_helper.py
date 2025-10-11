import os
from PyQt5.QtGui import QPixmap, QPalette, QBrush

def set_background(widget, image_name: str):
    abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", image_name))
    if not os.path.exists(abs_path):
        print(f"[ERROR] Background image not found: {abs_path}")
        return

    pixmap = QPixmap(abs_path)
    if pixmap.isNull():
        print(f"[ERROR] Cannot load pixmap: {abs_path}")
        return

    palette = widget.palette()
    palette.setBrush(widget.backgroundRole(), QBrush(pixmap))
    widget.setPalette(palette)
    widget.setAutoFillBackground(True)
    print(f"[INFO] Background loaded successfully from: {abs_path}")
