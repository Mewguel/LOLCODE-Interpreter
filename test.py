"""
Test GUI
"""

import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from gui import Ui_MainWindow

SYMBOL_TABLE_H = ["Lexeme", "Type", "Description", "Line"]


class Window(QtWidgets.QMainWindow):
    """
    UI setup
    """

    def __init__(self) -> None:
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.load_symbol_table()

    def load_symbol_table(self):
        self.ui.symbolTableWidget.setRowCount(2)
        self.ui.symbolTableWidget.setColumnCount(4)

        self.ui.symbolTableWidget.setHorizontalHeaderLabels(SYMBOL_TABLE_H)

        self.ui.symbolTableWidget.setColumnWidth(3, 40)

        # setting contents in the table here use for loop
        self.ui.symbolTableWidget.setItem(0, 0, QTableWidgetItem("HAI"))
        self.ui.symbolTableWidget.setItem(0, 1, QTableWidgetItem("HAI_keyword"))


def create_app():
    """
    UI initialization
    """
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())


create_app()
