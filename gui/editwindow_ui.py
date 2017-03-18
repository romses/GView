# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editwindow.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_EditWindow(object):
    def setupUi(self, EditWindow):
        EditWindow.setObjectName("EditWindow")
        EditWindow.resize(869, 538)
        self.centralwidget = QtWidgets.QWidget(EditWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.tableWidget = QtWidgets.QTableWidget(self.splitter)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.splitter)
        EditWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(EditWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 869, 31))
        self.menubar.setObjectName("menubar")
        EditWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(EditWindow)
        self.statusbar.setObjectName("statusbar")
        EditWindow.setStatusBar(self.statusbar)

        self.retranslateUi(EditWindow)
        QtCore.QMetaObject.connectSlotsByName(EditWindow)

    def retranslateUi(self, EditWindow):
        _translate = QtCore.QCoreApplication.translate
        EditWindow.setWindowTitle(_translate("EditWindow", "MainWindow"))

