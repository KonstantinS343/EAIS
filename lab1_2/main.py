from PyQt5 import QtWidgets

import sys

from gui.gui import Ui_MainWindow


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Аргументы!!!')
        exit()
    mode = sys.argv[1]
    if sys.argv[1] not in ('1', '2', '3', '4'):
        exit()

    if sys.argv[1] in ('3', '4'):
        column = 1
    else:
        column = 3

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(mode=mode, column=column)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
