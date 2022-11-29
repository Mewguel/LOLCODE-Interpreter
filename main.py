"""
    Main Program that reads a lol file and runs the lexer[WIP], syntax analyzer[ON QUEUE]

    Functions:
        display_tok
"""

# Imports
import sys

# ui imports
from PyQt5 import QtWidgets

# from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QTableWidgetItem
from gui import Ui_MainWindow

# custom modules
# import scanner
from scanner import Scanner
from lparser import Parser
from evaluator import Evaluator


# Constants
TEST_PATH = "inputs/test2.lol"
TABLE_H = ["Lexeme", "Type", "Description", "Line"]

# Class for main window ui setup
class Window(QtWidgets.QMainWindow):
    """
    UI setup
    """

    def __init__(self, token_list: list, abs_t: dict, contents: str) -> None:
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.tokens = token_list
        self.ast = abs_t
        self.load_text_edit(contents)
        self.load_symbol_table()

        # self.update_symbol_table()

    def load_text_edit(self, contents: str):
        """
        Display the file contents in the text editor
        """
        self.ui.textEdit.setText(contents)

    def load_symbol_table(self):
        """
        Loads the tokens in the symbol table ui
        """
        tmp_node = self.ast
        self.ui.symbolTable.setRowCount(len(self.tokens))
        self.ui.symbolTable.setColumnCount(4)

        self.ui.symbolTable.setHorizontalHeaderLabels(TABLE_H)

        self.ui.symbolTable.setColumnWidth(3, 40)

        # setting contents in the table here use for loop
        for ind, obj in enumerate(self.tokens):
            self.ui.symbolTable.setItem(ind, 0, QTableWidgetItem(obj.value))
            self.ui.symbolTable.setItem(ind, 1, QTableWidgetItem(obj.type))
            if tmp_node is not None:
                self.ui.symbolTable.setItem(
                    ind, 2, QTableWidgetItem(str(tmp_node["description"]))
                )
                self.ui.symbolTable.setItem(
                    ind, 3, QTableWidgetItem(str(tmp_node["line"]))
                )
                tmp_node = tmp_node["children"][0]

        # def update_symbol_table(self):
        #     """
        #     update symbol table from ast
        #     """
        #     size = len(self.tokens)
        #     ind = 0

        #     tmp_node = self.ast

        #     # setting contents in the table here use for loop
        #     print(tmp_node["line"])
        #     for ind, obj in enumerate(self.tokens):
        #         self.ui.symbolTableWidget.setItem(ind, 0, QTableWidgetItem(obj.value))
        #         self.ui.symbolTableWidget.setItem(ind, 1, QTableWidgetItem(obj.type))

        # while tmp_node is not None:
        #     self.ui.symbolTableWidget.setItem(
        #         ind, 3, QTableWidgetItem(tmp_node["line"])
        #     )
        #     tmp_node = tmp_node["children"][0]
        #     ind += 1
        #     if ind > size:
        #         break

    #     QTimer.singleShot(2000, self.update_symbol_table)


# functions
def display_tok(tok_list: list):
    """
    Takes a list of Tokens
    Displays the symbol table with token type and the value of the lexeme
    """
    print("------- Symbol Table --------")
    for token in tok_list:
        print(f"{token.type}: {token.value}")


def create_app(token_list: list, abs_t: dict, contents: str):
    """
    UI initialization
    """
    app = QtWidgets.QApplication(sys.argv)
    win = Window(token_list, abs_t, contents)
    win.repaint()
    win.show()
    sys.exit(app.exec_())


def print_ast(abs_t: dict):
    """
    visualize ast
    """
    # root node
    tmp_node = abs_t

    # if node has no children then leaf node
    # children_count = len(tmp_node.children)
    print("-----------------------------------------------\n")
    print(f"ROOT: {tmp_node['type']} - {tmp_node['value']} \n")
    while tmp_node is not None:

        print(
            f"{tmp_node['value']} - line_no: {tmp_node['line']} - desc: {tmp_node['description']} - parent - {tmp_node['parent']}\n"
        )
        tmp_node = tmp_node["children"][0]


if __name__ == "__main__":
    # lol program source code will be stored here
    code_contents = ""

    with open(TEST_PATH, "r", encoding="utf-8") as lol_file:
        code_contents = lol_file.read()

    # Instantiate the Lexical Analyzer
    # lexi = scanner.Scanner(code_contents)
    lexi = Scanner(code_contents, [])

    # Store tokens obtained from scanner
    tok = lexi.tokenize()
    # display_tok(tok)
    # display_tok(lexi.tokens)

    # Parser: tokens, AST list
    parsy = Parser(lexi.tokens, [])
    ast = parsy.build_ast()

    # print(f"test: {test} \n")
    # print_ast(test)
    semantics = Evaluator(ast)

    semantics.evaluate()

    create_app(tok, ast, code_contents)
