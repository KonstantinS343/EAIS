from PyQt5 import QtWidgets

import sys

from gui.gui import Ui_MainWindow


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Аргументы!!!')
        exit()
    if sys.argv[1] == '1':
        mode = False
    elif sys.argv[1] == '2':
        mode = True
    else:
        exit()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(mode=mode)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
