# -*- coding: utf-8 -*-

import os
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
        self.ciga_config = self.data_from_json()
        self.fname = ''

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1050, 596)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.compareButton = QtWidgets.QPushButton("Compare",self.centralwidget)
        self.compareButton.setObjectName("compareButton")
        self.compareButton.clicked.connect(self.compare_placements)
        self.grid.addWidget(self.compareButton, 0, 0)

        self.saveButton = QtWidgets.QPushButton("Save",self.centralwidget)
        self.saveButton.setObjectName("saveButton")
        self.saveButton.clicked.connect(self.save_current_placement)
        self.grid.addWidget(self.saveButton, 0, 1)

        self.loadButton = QtWidgets.QPushButton("Load",self.centralwidget)
        self.loadButton.setObjectName("loadButton")
        self.loadButton.clicked.connect(self.load_placement)
        self.grid.addWidget(self.loadButton, 0, 2)

        self.filename_label = QtWidgets.QLabel("File: %s" % self.fname, self.centralwidget)
        self.filename_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.filename_label, 0, 3)

        # self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        # self.grid.addWidget(self.progressBar, 0, 2)
        # self.progressBar.setProperty("value", 24)
        # self.progressBar.setObjectName("progressBar")

        self.scroll_grid = QGridLayout(self)
        self.scroll_grid.setSpacing(1)
        
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        # self.scrollArea.setWidget(self.scrollAreaWidget)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0,0,950,586))
        self.scroll_grid.addWidget(self.scrollAreaWidgetContents, 0,0)    
        
        self.grid_2 = QGridLayout(self.scrollAreaWidgetContents)
        self.placement()

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.grid.addWidget(self.scrollArea, 1, 0, 1, 10)


        self.centralwidget.setLayout(self.grid)
        self.centralwidget.setGeometry(0, 0, 1050, 596)

        
    def placement(self):
    

        for count, i in enumerate(self.ciga_config.keys()):
            # print(count, i)
            self.groupBox = QtWidgets.QGroupBox(i, self.scrollAreaWidgetContents)
            # self.groupBox.setGeometry(QtCore.QRect(10, 40, 971, 161))
            self.groupBox.setObjectName(i)
            # count += 1
            # print('Object name:', self.groupBox.objectName())
            self.grid_2.addWidget(self.groupBox, count, 0, 1, 1)

            groupBox_grid = QGridLayout()
            groupBox_grid.setSpacing(10)

            for c, j in enumerate(self.ciga_config[i].keys()):
                # print(j, self.ciga_config[i][j])
                try:
                    name, image = select_item(DB_CONNECTION, self.ciga_config[i][j])
                except TypeError as e:
                    print("Can`t load data from db\n %s" % e)
                # print(name, image)
                self.graphicsView = QLabel_alterada(self.groupBox)
                self.graphicsView.setAlignment(QtCore.Qt.AlignCenter)
                self.graphicsView.setObjectName("%s:%s:%s" % (i, j, name))
                pixmap = self.pixmap_check(image)
                pixmap_scale = pixmap.scaledToWidth(50)
                self.graphicsView.setPixmap(pixmap_scale)
                self.graphicsView.filename = image
                self.graphicsView.clicked.connect(self.imageClicked)
                groupBox_grid.addWidget(self.graphicsView, 0,c)

                name_spl = '\n'.join(name.split('_'))
                self.label = QtWidgets.QLabel(name_spl, self.groupBox)
                self.label.setAlignment(QtCore.Qt.AlignCenter)
                self.label.setObjectName("%s:%s:%s_label" % (i, j, name))
                groupBox_grid.addWidget(self.label, 1,c)


            self.groupBox.setLayout(groupBox_grid)
        
        

        MainWindow.setCentralWidget(self.centralwidget)
        # self.menubar = QtWidgets.QMenuBar(MainWindow)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 983, 21))
        # self.menubar.setObjectName("menubar")

        # self.filemenu = self.menubar.addMenu('File')
        # self.loadAct = QtWidgets.QAction("Load", self)
        # self.saveAct = QtWidgets.QAction("Save", self)

        # self.filemenu.addAction(self.loadAct)
        # self.filemenu.addAction(self.saveAct)

        # self.menuExit = QtWidgets.QMenu(self.menubar)
        # self.menuExit.setObjectName("menuExit")

        # MainWindow.setMenuBar(self.menubar)

        self.exitAct = QtWidgets.QAction(QtGui.QIcon('/images/icons/exit.png'), 'Exit', MainWindow)
        self.exitAct.setShortcut('Ctrl+Q')
        self.exitAct.setStatusTip('Exit application')
        self.exitAct.triggered.connect(MainWindow.close)

        self.toolbar = MainWindow.addToolBar('Exit')
        self.toolbar.addAction(self.exitAct)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # self.menubar.addAction(self.menuExit.menuAction())

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

    def data_from_json(self, file='ciga_conf.json'):
        
        with open(file, 'r') as f:
            json_data = f.read()
        config = json.loads(json_data)
        return config

    def imageClicked(self):
        print("Click on label")
        sender = self.sender()
        self.dialog = SelectionWindow(self)
        self.updObjName = sender.objectName()

    def pixmap_check(self, image):
        if os.path.isfile(image):
            pixmap = QtGui.QPixmap(image)
        else:
            pixmap = QtGui.QPixmap('images/noimage.png')
        return pixmap

    def update_placement(self, name):
        shelf, id, bundle = self.updObjName.split(':')
        self.ciga_config[shelf][id] = name
        print(self.ciga_config[shelf][id])
        # self.scrollAreaWidgetContents.update()
        self.clearLayout(self.grid_2)
        self.placement()

    def save_current_placement(self):
        with open('new_config.json', 'w') as file:
            json.dump(self.ciga_config, file)

    def load_placement(self):
        self.fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '.')[0]
        self.ciga_config = self.data_from_json(self.fname)
        # print(self.ciga_config)
        self.filename_label.setText(self.fname)
        self.clearLayout(self.grid_2)
        self.placement()

    def compare_placements(self, placement):
        data = self.data_from_json('new_config.json')
        for i in data.keys():
            for j in data[i].keys():
                obj = self.centralwidget.findChild(QLabel, "%s:%s:%s_label" % (i, j, self.ciga_config[i][j]))
                if data[i][j] == self.ciga_config[i][j]:
                    obj.setStyleSheet('color: green')
                else:
                    obj.setStyleSheet('color: red')
                    obj.setToolTip(data[i][j])

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                clearLayout(child.layout())

    



class SelectionWindow(Ui_MainWindow):
    def __init__(self, parentWindow):
        super(SelectionWindow, self).__init__()
        self.parentWindow = parentWindow
        # self.parentWindow.printRes("child window")

        self.name = ''
        self.image = ''

        self.initUI()
        self.show()

    def initUI(self):
        
        items = select_all(DB_CONNECTION)

        self.resize(917,647)

        self.grid = QGridLayout(self)
        self.grid.setSpacing(10)
        
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        # self.scrollArea.setWidget(self.scrollAreaWidget)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0,0,897,586))
    
        self.grid_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)

        # self.grid.addWidget(self.scrollArea)

        row = 0
        col = 0
        for c, i in enumerate(items):
            # print(c, row)
            if c % 5 == 0:
                row +=2
                col = 0
            name, image = i
            # print(name, image)
            self.graphicsView = QLabel_alterada(self.scrollAreaWidgetContents)
            self.graphicsView.setObjectName(name)
            self.graphicsView.setAlignment(QtCore.Qt.AlignCenter)
            self.graphicsView.setMinimumSize(104, 172)
            pixmap = self.pixmap_check(image)
            # print(pixmap)
            pixmap_scale = pixmap.scaledToWidth(50)
            self.graphicsView.setPixmap(pixmap_scale)
            self.graphicsView.name = name
            self.graphicsView.image = image
            self.graphicsView.clicked.connect(self.returnEvent)
            self.grid_2.addWidget(self.graphicsView, row,col)

            self.label = QtWidgets.QLabel(name, self)
            self.label.setAlignment(QtCore.Qt.AlignCenter)
            self.label.setObjectName("%s_label" % name)
            self.grid_2.addWidget(self.label, row+1,col)

            col += 1

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.grid.addWidget(self.scrollArea, 1, 0, 1, 1)

    def returnEvent(self):
        sender = self.sender()
        self.name = sender.name
        # self.image = sender.image
        self.close()

    def closeEvent(self, event):
        if self.name:# and self.image:
            self.parentWindow.update_placement(self.name)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    w = Ui_MainWindow()
    w.setupUi(MainWindow)
    MainWindow.show()
    
    sys.exit(app.exec_())

