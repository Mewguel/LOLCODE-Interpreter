"""
    Main Program that reads a lol file and runs the lexer[WIP], syntax analyzer[ON QUEUE]

    Functions:
        display_tok
"""

# Imports
import sys

# ui imports
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from gui import Ui_MainWindow

# custom modules
import scanner


# Constants
TEST_PATH = "inputs/test.lol"
TABLE_H = ["Lexeme", "Type", "Description", "Line"]

# Class for main window ui setup
class Window(QtWidgets.QMainWindow):
    """
    UI setup
    """

    def __init__(self, token_list: list) -> None:
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.tokens = token_list

        self.load_symbol_table()

    def load_symbol_table(self):
        self.ui.symbolTableWidget.setRowCount(len(self.tokens))
        self.ui.symbolTableWidget.setColumnCount(4)

        self.ui.symbolTableWidget.setHorizontalHeaderLabels(TABLE_H)

        self.ui.symbolTableWidget.setColumnWidth(3, 40)

        # setting contents in the table here use for loop
        for ind, obj in enumerate(self.tokens):
            self.ui.symbolTableWidget.setItem(ind, 0, QTableWidgetItem(obj.value))
            self.ui.symbolTableWidget.setItem(ind, 1, QTableWidgetItem(obj.type))


# functions
def display_tok(tok_list: list):
    """
    Takes a list of Tokens
    Displays the symbol table with token type and the value of the lexeme
    """
    print("------- Symbol Table --------")
    for token in tok_list:
        print(f"{token.type}: {token.value}")


def create_app(token_list: list):
    """
    UI initialization
    """
    app = QtWidgets.QApplication(sys.argv)
    win = Window(token_list)
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # lol program source code will be stored here
    code_contents = ""

    with open(TEST_PATH, "r", encoding="utf-8") as lol_file:
        code_contents = lol_file.read()

    # Instantiate the Lexical Analyzer
    lexi = scanner.Scanner(code_contents)
    # Store tokens obtained from scanner
    tok = lexi.tokenize()
    display_tok(tok)

    create_app(tok)
