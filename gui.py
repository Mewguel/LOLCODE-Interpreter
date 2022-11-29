"""
 -*- coding: utf-8 -*-
"""


from PyQt5 import QtCore, QtWidgets


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
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Clear Output"))
        self.pushButton_2.setText(_translate("MainWindow", "RUN"))
        # self.terminalOutput.setPlainText(_translate("MainWindow", "> Hello World!"))
