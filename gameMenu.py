# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\gameMenu.ui'
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

class Ui_GameMenu(object):
    def setupUi(self, GameMenu):
        GameMenu.setObjectName(_fromUtf8("GameMenu"))
        GameMenu.resize(207, 110)
        self.pushButton_Next = QtGui.QPushButton(GameMenu)
        self.pushButton_Next.setGeometry(QtCore.QRect(20, 20, 75, 23))
        self.pushButton_Next.setObjectName(_fromUtf8("pushButton_Next"))
        self.pushButton_Quit = QtGui.QPushButton(GameMenu)
        self.pushButton_Quit.setGeometry(QtCore.QRect(110, 20, 75, 23))
        self.pushButton_Quit.setObjectName(_fromUtf8("pushButton_Quit"))
        self.pushButton_Reload = QtGui.QPushButton(GameMenu)
        self.pushButton_Reload.setGeometry(QtCore.QRect(110, 50, 75, 23))
        self.pushButton_Reload.setObjectName(_fromUtf8("pushButton_Reload"))
        self.pushButton_Settings = QtGui.QPushButton(GameMenu)
        self.pushButton_Settings.setGeometry(QtCore.QRect(20, 50, 75, 23))
        self.pushButton_Settings.setObjectName(_fromUtf8("pushButton_Settings"))
        self.label = QtGui.QLabel(GameMenu)
        self.label.setGeometry(QtCore.QRect(25, 80, 151, 20))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(GameMenu)
        QtCore.QMetaObject.connectSlotsByName(GameMenu)

    def retranslateUi(self, GameMenu):
        GameMenu.setWindowTitle(_translate("GameMenu", "Game", None))
        self.pushButton_Next.setText(_translate("GameMenu", "Next", None))
        self.pushButton_Quit.setText(_translate("GameMenu", "Quit", None))
        self.pushButton_Reload.setText(_translate("GameMenu", "Reload", None))
        self.pushButton_Settings.setText(_translate("GameMenu", "Settings", None))
        self.label.setText(_translate("GameMenu", "TextLabel", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    GameMenu = QtGui.QDialog()
    ui = Ui_GameMenu()
    ui.setupUi(GameMenu)
    GameMenu.show()
    sys.exit(app.exec_())

