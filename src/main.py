import sys
from PyQt5.QtWidgets import QApplication
from ui.demo_view import DemoView

if __name__ == "__main__":
    app = QApplication(sys.argv)

    demo_view = DemoView()
    demo_view.show()

    sys.exit(app.exec_())