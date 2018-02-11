# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ciga_main.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import sys
import json
from db import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTextEdit, QGridLayout, QLabel

DATABASE = "test.db"
DB_CONNECTION = create_connection(DATABASE)


class QLabel_alterada(QLabel):
  clicked=QtCore.pyqtSignal()
  def __init(self, parent):
    QLabel.__init__(self, QMouseEvent)

  def mousePressEvent(self, ev):
    self.clicked.emit()
      

class Ui_MainWindow(QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ciga_config = {}
        self.data_from_json()
        # self.MainWindow = QWidget
        # self.setupUi()
        # self.initUI()

    # def initUI(self):
    #     self.setGeometry(100, 100, 300, 300)
    #     self.setWindowTitle("Icon")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(983, 596)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.compareButton = QtWidgets.QPushButton("Compare",self.centralwidget)
        self.compareButton.setObjectName("compareButton")
        self.compareButton.clicked.connect(self.data_from_json)
        self.grid.addWidget(self.compareButton, 0, 0)

        self.saveButton = QtWidgets.QPushButton("Save",self.centralwidget)
        self.saveButton.setObjectName("saveButton")
        self.saveButton.clicked.connect(self.save_current_placement)
        self.grid.addWidget(self.saveButton, 0, 1)

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.grid.addWidget(self.progressBar, 0, 2)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")

        

        for count, i in enumerate(self.ciga_config.keys()):
            # print(count, i)
            self.groupBox = QtWidgets.QGroupBox(i, self.centralwidget)
            # self.groupBox.setGeometry(QtCore.QRect(10, 40, 971, 161))
            self.groupBox.setObjectName(i)
            count += 1
            # print('Object name:', self.groupBox.objectName())
            self.grid.addWidget(self.groupBox, count, 0, 1, 3)

            groupBox_grid = QGridLayout()
            groupBox_grid.setSpacing(10)

            for c, j in enumerate(self.ciga_config[i].keys()):
                # print(j, self.ciga_config[i][j])
                name, image = select_item(DB_CONNECTION, self.ciga_config[i][j])
                # print(name, image)
                self.graphicsView = QLabel_alterada(self.groupBox)
                self.graphicsView.setObjectName("%s_%s_%s" % (i, j, name))
                pixmap = QtGui.QPixmap(image)
                pixmap_scale = pixmap.scaledToWidth(50)
                self.graphicsView.setPixmap(pixmap_scale)
                self.graphicsView.filename = image
                self.graphicsView.clicked.connect(self.imageClicked)
                groupBox_grid.addWidget(self.graphicsView, 0,c)

                self.label = QtWidgets.QLabel(name, self.groupBox)
                self.label.setObjectName("%s_%s_%s_label" % (i, j, name))
                groupBox_grid.addWidget(self.label, 1,c)


            self.groupBox.setLayout(groupBox_grid)
        
        

        # MainWindow.setCentralWidget(self.centralwidget)
        # self.menubar = QtWidgets.QMenuBar(MainWindow)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 983, 21))
        # self.menubar.setObjectName("menubar")
        # self.menuExit = QtWidgets.QMenu(self.menubar)
        # self.menuExit.setObjectName("menuExit")
        # MainWindow.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)
        # self.menubar.addAction(self.menuExit.menuAction())

        # self.retranslateUi(MainWindow)
        # QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # # self.show()
        self.centralwidget.setLayout(self.grid)
        self.centralwidget.setGeometry(0, 0, 983, 596)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.compareButton.setText(_translate("MainWindow", "Compare"))
        self.groupBox.setTitle(_translate("MainWindow", "Shelf 1"))
        self.label.setText(_translate("MainWindow", "Label"))
        self.label_2.setText(_translate("MainWindow", "Status"))
        self.label_3.setText(_translate("MainWindow", "Label"))
        self.label_4.setText(_translate("MainWindow", "Status"))
        self.label_5.setText(_translate("MainWindow", "Label"))
        self.label_6.setText(_translate("MainWindow", "Status"))


    def data_from_json(self):
        file = 'ciga_conf.json'
        with open(file, 'r') as f:
            json_data = f.read()
        self.ciga_config = json.loads(json_data)

    def imageClicked(self):
        print("Click on label")
        # self.print_child()
        sender = self.sender()
        self.dialog = SelectionWindow(self)
        # self.dialog.initUI(self.centralwidget)
        # self.dialog.show()
        self.updObjName = sender.objectName()

    def printRes(self, value):
        print(value)

    def updateItem(self, name, image):
        obj = self.centralwidget.findChild(QLabel, self.updObjName)
        print(self.updObjName)
        # print(dir(obj))
        pixmap = QtGui.QPixmap(image)
        pixmap_scale = pixmap.scaledToWidth(50)
        obj.setPixmap(pixmap_scale)

        obj_label = self.centralwidget.findChild(QLabel, "%s_label" %self.updObjName)
        # print(dir(obj_label))
        obj_label.setText(name)

        self.updateConfig(name)

    def updateConfig(self, name):
        shelf, id, bundle = self.updObjName.split('_')
        self.ciga_config[shelf][id] = name

    def save_current_placement(self):
        with open('new_config.json', 'w') as file:
            json.dump(self.ciga_config, file)


class SelectionWindow(Ui_MainWindow):
    def __init__(self, parentWindow):
        super(SelectionWindow, self).__init__()
        self.parentWindow = parentWindow
        self.parentWindow.printRes("child window")

        self.name = ''
        self.image = ''

        self.initUI()
        self.show()

    def initUI(self):
        

        self.resize(300,300)

        items = select_all(DB_CONNECTION)
        print(items)

        changeItem_grid = QGridLayout()
        changeItem_grid.setSpacing(10)

        for c, i in enumerate(items):
            print(i)
            name, image = i
            # print(name, image)
            self.graphicsView = QLabel_alterada(self)
            self.graphicsView.setObjectName(name)
            pixmap = QtGui.QPixmap(image)
            pixmap_scale = pixmap.scaledToWidth(50)
            self.graphicsView.setPixmap(pixmap_scale)
            self.graphicsView.name = name
            self.graphicsView.image = image
            self.graphicsView.clicked.connect(self.returnEvent)
            changeItem_grid.addWidget(self.graphicsView, 0,c)

            self.label = QtWidgets.QLabel(name, self)
            self.label.setObjectName("%s_label" % name)
            changeItem_grid.addWidget(self.label, 1,c)

        self.setLayout(changeItem_grid)
    
    def returnEvent(self):
        sender = self.sender()
        self.name = sender.name
        self.image = sender.image
        self.close()

    def closeEvent(self, event):
        if self.name and self.image:
            self.parentWindow.updateItem(self.name, self.image)
        else:
            pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    w = Ui_MainWindow()
    w.setupUi(MainWindow)
    MainWindow.show()
    # w.show()
    
    sys.exit(app.exec_())

