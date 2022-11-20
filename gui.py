"""
 -*- coding: utf-8 -*-
"""


from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1097, 886)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(119, 489, 871, 331))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.terminalContainer = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.terminalContainer.setContentsMargins(0, 0, 0, 0)
        self.terminalContainer.setObjectName("terminalContainer")

        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")

        self.terminalContainer.addWidget(self.pushButton)

        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")

        self.terminalContainer.addWidget(self.pushButton_2)
        self.terminalOutput = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget)
        self.terminalOutput.setObjectName("terminalOutput")
        self.terminalContainer.addWidget(self.terminalOutput)

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(50, 20, 981, 421))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.textBrowser = QtWidgets.QTextBrowser(self.horizontalLayoutWidget)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout.addWidget(self.textBrowser)

        self.symbolTableWidget = QtWidgets.QTableWidget(self.horizontalLayoutWidget)
        self.symbolTableWidget.setObjectName("symbolTableWidget")
        self.symbolTableWidget.setColumnCount(0)
        self.symbolTableWidget.setRowCount(0)
        self.horizontalLayout.addWidget(self.symbolTableWidget)

        self.tableWidget_2 = QtWidgets.QTableWidget(self.horizontalLayoutWidget)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.horizontalLayout.addWidget(self.tableWidget_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1097, 26))
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
        self.terminalOutput.setPlainText(_translate("MainWindow", "> Hello World!"))
