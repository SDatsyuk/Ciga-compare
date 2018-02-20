from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,\
                            QTextEdit, QGridLayout, QLabel, QDialog
import os
import sys
import json
from db import *

class Ui_ConfigDialog(QDialog):

    def __init__(self, parent=None):
        super(Ui_ConfigDialog, self).__init__(parent)

        self.parent = parent
        self.Dialog = QDialog()
        self.setupUi(self.Dialog)
        self.Dialog.show()


    def setupUi(self, Dialog):

        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(206, 147)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 100, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(self.Dialog)
        self.label.setGeometry(QtCore.QRect(40, 20, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 60, 51, 16))
        self.label_2.setObjectName("label_2")
        self.spinBox = QtWidgets.QSpinBox(self.Dialog)
        self.spinBox.setRange(1, 6)
        self.spinBox.setGeometry(QtCore.QRect(130, 20, 42, 22))
        self.spinBox.setObjectName("spinBox")
        self.spinBox_2 = QtWidgets.QSpinBox(self.Dialog)
        self.spinBox_2.setRange(1, 20)
        self.spinBox_2.setGeometry(QtCore.QRect(130, 60, 42, 22))
        self.spinBox_2.setObjectName("spinBox_2")

        self.retranslateUi(self.Dialog)
        # self.buttonBox.accepted.connect(self.Dialog.accept)
        self.buttonBox.accepted.connect(self.acceptConf)
        self.buttonBox.rejected.connect(self.rejectConf)
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Shelf"))
        self.label_2.setText(_translate("Dialog", "Bundle"))

    def acceptConf(self):
        print('accept')
        # self.parent.temp_config = {'shelf': self.spinBox.value(), 'bundle': self.spinBox_2.value()}
        self.parent.shelf = self.spinBox.value()
        self.parent.bundle = self.spinBox_2.value()
        self.parent.update_placement()
        self.Dialog.accept()
        # print(self.parent.temp_config)
        # self.close()

    def rejectConf(self):
        print('rejected')
        self.Dialog.reject()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Dialog = QDialog()
    w = Ui_Dialog()
    # w.setupUi(Dialog)
    # Dialog.show()
    
    sys.exit(app.exec_())