# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets


class Ui_Dialog_Text_Area(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1200, 600)
        self.semantic_text = QtWidgets.QTextEdit(Dialog)
        self.semantic_text.setGeometry(QtCore.QRect(3, 10, 1190, 590))
        self.semantic_text.setReadOnly(True)
        self.semantic_text.setObjectName("semantic_text")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Семантический анализ"))

    def fill(self, text: str):
        self.semantic_text.setText(text)
