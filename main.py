from mainwindow import MainWindow
from PyQt5 import QtWidgets

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setup_ui()
    window.set_logic()
    window.show()

    sys.exit(app.exec_())
