# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\mainMenu.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(259, 215)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 231, 151))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.radioButton = QtGui.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(10, 20, 101, 17))
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.buttonGroup = QtGui.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.radioButton)
        self.radioButton_2 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 50, 151, 17))
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.buttonGroup.addButton(self.radioButton_2)
        self.toolButton = QtGui.QToolButton(self.groupBox)
        self.toolButton.setGeometry(QtCore.QRect(130, 50, 81, 19))
        self.toolButton.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.pushButton = QtGui.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(10, 110, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 110, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.spinBox = QtGui.QSpinBox(self.groupBox)
        self.spinBox.setGeometry(QtCore.QRect(130, 20, 42, 22))
        self.spinBox.setMaximum(500)
        self.spinBox.setProperty("value", 10)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.lineEdit_filePath = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_filePath.setEnabled(False)
        self.lineEdit_filePath.setGeometry(QtCore.QRect(10, 70, 201, 20))
        self.lineEdit_filePath.setText(_fromUtf8(""))
        self.lineEdit_filePath.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_filePath.setDragEnabled(False)
        self.lineEdit_filePath.setReadOnly(True)
        self.lineEdit_filePath.setObjectName(_fromUtf8("lineEdit_filePath"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 259, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuStart_Menu = QtGui.QMenu(self.menubar)
        self.menuStart_Menu.setObjectName(_fromUtf8("menuStart_Menu"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionSettings = QtGui.QAction(MainWindow)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
        self.menuStart_Menu.addSeparator()
        self.menuStart_Menu.addAction(self.actionSettings)
        self.menubar.addAction(self.menuStart_Menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.groupBox.setTitle(_translate("MainWindow", "Select Mode", None))
        self.radioButton.setText(_translate("MainWindow", "Random Point", None))
        self.radioButton_2.setText(_translate("MainWindow", "Points from File", None))
        self.toolButton.setText(_translate("MainWindow", "Select File", None))
        self.pushButton.setText(_translate("MainWindow", "Start Game", None))
        self.pushButton_2.setText(_translate("MainWindow", "Quit", None))
        self.menuStart_Menu.setTitle(_translate("MainWindow", "Start Menu", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.actionSettings.setText(_translate("MainWindow", "Settings", None))

