"""
 -*- coding: utf-8 -*-
"""


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QFileDialog, QTableWidgetItem

# custom modules
# import scanner
from scanner import Scanner
from lparser import Parser

TABLE_H = ["Lexeme", "Type", "Description", "Line"]


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(25, 25, 1485, 819))

        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.terminalContainer = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)

        self.terminalContainer.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.terminalContainer.setContentsMargins(0, 0, 0, 0)
        self.terminalContainer.setObjectName("terminalContainer")

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.textEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.textEdit.setMinimumSize(QtCore.QSize(480, 0))
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit)

        self.symbolTable = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.symbolTable.setMinimumSize(QtCore.QSize(480, 0))
        self.symbolTable.setObjectName("symbolTable")
        self.symbolTable.setColumnCount(0)
        self.symbolTable.setRowCount(0)
        self.horizontalLayout.addWidget(self.symbolTable)

        self.varTable = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.varTable.setMinimumSize(QtCore.QSize(480, 0))
        self.varTable.setObjectName("varTable")
        self.varTable.setColumnCount(0)
        self.varTable.setRowCount(0)
        self.horizontalLayout.addWidget(self.varTable)

        self.terminalContainer.addLayout(self.horizontalLayout)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.terminalContainer.addWidget(self.pushButton)

        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.terminalContainer.addWidget(self.pushButton_2)

        self.terminalOutput = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget)
        self.terminalOutput.setObjectName("terminalOutput")
        self.terminalContainer.addWidget(self.terminalOutput)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuRun = QtWidgets.QMenu(self.menubar)
        self.menuRun.setObjectName("menuRun")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionRun = QtWidgets.QAction(MainWindow)
        self.actionRun.setObjectName("actionRun")
        self.menuFile.addAction(self.actionOpen)
        self.menuRun.addAction(self.actionRun)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuRun.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Adding pushbutton actions/event handlers
        self.pushButton.clicked.connect(self.clear_output)
        self.pushButton_2.clicked.connect(self.execute)

        # Adding Menu actions
        self.actionOpen.triggered.connect(lambda: self.open(MainWindow))
        self.actionRun.triggered.connect(lambda: self.execute())

    def retranslateUi(self, MainWindow):
        """
        For Updating the strings/labels of the MainWindow
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Clear Output"))
        self.pushButton_2.setText(_translate("MainWindow", "RUN"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuRun.setTitle(_translate("MainWindow", "Run"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionRun.setText(_translate("MainWindow", "Run"))
        self.terminalOutput.setPlainText(_translate("MainWindow", "> Hello World!"))

    def clear_output(self):
        """
        Clears the output terminal
        """
        self.terminalOutput.setPlainText("")

    def execute(self):
        """
        Runs the code on the text editor
        """
        print("I am running")

    def open(self, MainWindow):
        """
        Open the File Explorer
        """
        fname = QFileDialog.getOpenFileName(MainWindow, "Open LOL file", "/inputs")
        self.input_path = fname[0]
        self.terminalOutput.setPlainText(f"{self.input_path} has been loaded.")
        self.load_file_cont()

    def load_file_cont(self):
        """
        Read file contents to UI
        """
        code_contents = ""

        with open(self.input_path, "r", encoding="utf-8") as lol_file:
            code_contents = lol_file.read()

        self.textEdit.setText(code_contents)
        self.update_symbol_table(code_contents)

    def update_symbol_table(self, code_conts):
        """
        Update Symbol Table from the new file
        """
        lexi = Scanner(code_conts, [])
        tok = lexi.tokenize()
        parsy = Parser(lexi.tokens, [])
        ast = parsy.build_ast()

        self.tokens = tok
        self.ast = ast

        self.load_symbol_table()

        # semantics = Evaluator(ast)
        # semantics.evaluate()

    def load_symbol_table(self):
        """
        Loads the tokens in the symbol table ui
        """
        if self.tokens is None:
            return
        tmp_node = self.ast
        self.symbolTable.setRowCount(len(self.tokens))
        self.symbolTable.setColumnCount(4)

        # self.symbolTable.setHorizontalHeaderLabels(TABLE_H)

        self.symbolTable.setColumnWidth(3, 40)

        # setting contents in the table here use for loop
        for ind, obj in enumerate(self.tokens):
            self.symbolTable.setItem(ind, 0, QTableWidgetItem(obj.value))
            self.symbolTable.setItem(ind, 1, QTableWidgetItem(obj.type))
            if tmp_node is not None:
                self.symbolTable.setItem(
                    ind, 2, QTableWidgetItem(str(tmp_node["description"]))
                )
                self.symbolTable.setItem(
                    ind, 3, QTableWidgetItem(str(tmp_node["line"]))
                )
                tmp_node = tmp_node["children"][0]
