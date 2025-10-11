import sys
from PyQt5.QtWidgets import QApplication
from ui.main_view import MainView

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_view = MainView()
    main_view.show()

    sys.exit(app.exec_())