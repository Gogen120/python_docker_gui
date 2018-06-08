import sys
from PyQt5.QtWidgets import QApplication
from main import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mv = MainWindow()
    sys.exit(app.exec_())
