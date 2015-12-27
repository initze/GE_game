# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\SettingsMenu.ui'
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

class Ui_SettingsMenu(object):
    def setupUi(self, SettingsMenu):
        SettingsMenu.setObjectName(_fromUtf8("SettingsMenu"))
        SettingsMenu.resize(264, 108)
        self.pushButton = QtGui.QPushButton(SettingsMenu)
        self.pushButton.setGeometry(QtCore.QRect(10, 70, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(SettingsMenu)
        self.pushButton_2.setGeometry(QtCore.QRect(110, 70, 81, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.lineEdit = QtGui.QLineEdit(SettingsMenu)
        self.lineEdit.setGeometry(QtCore.QRect(80, 30, 113, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label = QtGui.QLabel(SettingsMenu)
        self.label.setGeometry(QtCore.QRect(10, 30, 61, 16))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(SettingsMenu)
        QtCore.QMetaObject.connectSlotsByName(SettingsMenu)

    def retranslateUi(self, SettingsMenu):
        SettingsMenu.setWindowTitle(_translate("SettingsMenu", "Settings", None))
        self.pushButton.setText(_translate("SettingsMenu", "OK", None))
        self.pushButton_2.setText(_translate("SettingsMenu", "Main Menu", None))
        self.label.setText(_translate("SettingsMenu", "View height", None))

