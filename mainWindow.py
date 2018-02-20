# -*- coding: utf-8 -*-

import os
import sys
import json

from db import *
from placementconfig import placement
from childWindow import Ui_ConfigDialog

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTextEdit, QGridLayout, QLabel

from utils import sock_cl

DATABASE = "test.db"
DB_CONNECTION = create_connection(DATABASE)


class QLabel_alterada(QLabel):
  clicked=QtCore.pyqtSignal()
  def __init(self, parent):
    QLabel.__init__(self, QMouseEvent)

  def mousePressEvent(self, ev):
    self.clicked.emit()


class MessageBox(QtWidgets.QMessageBox):
    def __init__(self, parent):
        QtWidgets.QMessageBox.__init__(self, parent)
      

class Ui_MainWindow(QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ciga_config = {}#self.data_from_json()
        self.fname = ''
        self.shelf = placement['shelf']
        self.bundle = placement['bundle']
        self.temp_config = {}

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(85*int(self.bundle), 200*int(self.shelf))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # self.resized.connect(self.resizeEvent)

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

        self.loadButton = QtWidgets.QPushButton("Open",self.centralwidget)
        self.loadButton.setObjectName("loadButton")
        self.loadButton.clicked.connect(self.load_placement)
        self.grid.addWidget(self.loadButton, 0, 2)

        self.configButton = QtWidgets.QPushButton("Configure",self.centralwidget)
        self.configButton.setObjectName("configButton")
        self.configButton.clicked.connect(self.load_config_form)
        self.grid.addWidget(self.configButton, 0, 3)

        self.filename_label = QtWidgets.QLabel("File: %s" % self.fname, self.centralwidget)
        self.filename_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.filename_label, 0, 4)

        self.scroll_grid = QGridLayout(self)
        self.scroll_grid.setSpacing(1)
        
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        # self.scrollArea.setWidget(self.scrollAreaWidget)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0,0,950,586))
        self.scroll_grid.addWidget(self.scrollAreaWidgetContents, 0,0)    
        
        self.grid_2 = QGridLayout(self.scrollAreaWidgetContents)
        self.placement(self.shelf, self.bundle)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.grid.addWidget(self.scrollArea, 1, 0, 1, 10)


        self.centralwidget.setLayout(self.grid)
        # self.centralwidget.setGeometry(0, 0, 1050, 596)

    def placement(self, shelf=3, bundle=12):
        
        self.verify_shelf_placement()
        
        for count, i in enumerate(self.ciga_config.keys()):
            # print(count, i)
            self.groupBox = QtWidgets.QGroupBox(i, self.scrollAreaWidgetContents)
            self.groupBox.setObjectName(i)
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
       
        # QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

    def verify_shelf_placement(self):
        ciga_ln = len(self.ciga_config)
        if self.shelf > len(self.ciga_config):
            for i in range(self.shelf - len(self.ciga_config)):
                new_shelf = 'Shelf%s' % (ciga_ln+i+1)
                self.ciga_config[new_shelf] = {}
        elif self.shelf < len(self.ciga_config):
            nciga_config = {}
            for c, i in zip(range(self.shelf), self.ciga_config.keys()):
                nciga_config[i] = self.ciga_config[i]
            self.ciga_config = nciga_config
        for i in self.ciga_config.keys():
            self.verify_bundle_placement(i)
        
    def verify_bundle_placement(self, shelf):
        # print(self.ciga_config)
        shelf_ln = len(self.ciga_config[shelf])
        if shelf_ln < self.bundle:
            for j in range(self.bundle - len(self.ciga_config[shelf])):
                self.ciga_config[shelf][str(shelf_ln + j + 1)] = 'none' 
        elif shelf_ln > self.bundle:
            diff_len = shelf_ln - self.bundle
            for j in range(diff_len):
                # print(j)
                self.ciga_config[shelf].pop(str(j+self.bundle+1))

    def data_from_json(self, file='ciga_conf.json'):
        try:
            with open(file, 'r') as f:
                json_data = f.read()
            config = json.loads(json_data)
        except FileNotFoundError as e:
            print("Error!", e)
            config = {}
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

    def update_item(self, name):
        # print(self.ciga_config)
        shelf, id, bundle = self.updObjName.split(':')
        self.ciga_config[shelf][id] = name
        # print(self.ciga_config[shelf][id])
        # self.scrollAreaWidgetContents.update()
        self.update_placement()

    def update_placement(self):
        self.clearLayout(self.grid_2)
        # print(self.ciga_config)
        MainWindow.resize(85*int(self.bundle), 175*int(self.shelf))
        self.placement()

    def save_current_placement(self):
        self.save_fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', './placement', '*.json')[0]
        try:
            with open(self.save_fname, 'w') as file:
                json.dump(self.ciga_config, file)
        except FileNotFoundError as e:
            print(e)

    def load_placement(self):
        self.fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '.')[0]
        if self.fname:
            self.ciga_config = self.data_from_json(self.fname)
            self.shelf = len(self.ciga_config)
            self.bundle = len(self.ciga_config['Shelf1'])
            # print(self.ciga_config)
            self.filename_label.setText(self.fname)
            self.clearLayout(self.grid_2)
            self.placement()

    def compare_placements(self, placement):
        # fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open compare file', './placement')[0]
        # data = self.data_from_json(fname)
        placement = sock_cl.main()
        print(placement)
        print(self.ciga_config)
        check = self.check_placement_dimension(self.ciga_config, placement)
        print(check)
        if check:
            for i in placement.keys():
                # print(i)
                for j in placement[i].keys():
                    # print(j)
                    # print(self.ciga_config[i][str(j)])
                    obj = self.centralwidget.findChild(QLabel, "%s:%s:%s_label" % (i, str(j), self.ciga_config[i][str(j)]))
                    print(placement[i][j], ''.join(self.ciga_config[i][str(j)].split('_')))
                    if placement[i][j] == ''.join(self.ciga_config[i][str(j)].split('_')):
                        obj.setStyleSheet('color: green')
                    else:
                        obj.setStyleSheet('color: red')
                        obj.setToolTip(placement[i][j])
        # except KeyError as e:
        #     # print(e)
        #     self.showMessage(e)

                

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                clearLayout(child.layout())

    def load_config_form(self):
        dialog = Ui_ConfigDialog(self)
        # dialog.setupUi(dialog.Dialog)
        dialog.spinBox.setValue(self.shelf)
        dialog.spinBox_2.setValue(self.bundle)
        # dialog.Dialog.show()

        # self.update_placement()
        # print(self.bundle)

    def showMessage(self, error):
        msg = MessageBox(self.centralwidget)
        msg.setIcon(QtWidgets.QMessageBox.Information)

        msg.setText("{}".format(error))
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.show()

    def check_placement_dimension(self, curr, received):
        err = ''
        if len(curr) != len(received):
            err += "expected {} shelf but get {} shelf\n".format(len(curr), len(received))
        for curr_shelf, rec_shelf in zip(curr.keys(), received.keys()):
            if len(curr[curr_shelf]) != len(received[rec_shelf]):
                err += "{} expected {} bundles but get {} bundles\n".format(curr_shelf, len(curr[curr_shelf]), len(received[rec_shelf]))
        if err:
            self.showMessage("Wrong placement dimension:\n {}".format(err))
            return False
        else:
            return True




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
        
        self.all_items = select_all(DB_CONNECTION)

        self.resize(917,647)

        self.grid = QGridLayout(self)
        self.grid.setSpacing(10)

        self.searchLine = QtWidgets.QLineEdit(self)
        self.searchLine.textChanged.connect(self.searchByName)
        self.grid.addWidget(self.searchLine, 0, 0)
        
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        # self.scrollArea.setWidget(self.scrollAreaWidget)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0,0,897,586))
    
        self.grid_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)

        self.show_bundles()

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.grid.addWidget(self.scrollArea, 1, 0)

        # self.grid.addWidget(self.scrollArea)
    def show_bundles(self):
        row = 0
        col = 0
        for c, i in enumerate(self.all_items):
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



    def returnEvent(self):
        sender = self.sender()
        self.name = sender.name
        # self.image = sender.image
        self.close()

    def closeEvent(self, event):
        if self.name:# and self.image:
            self.parentWindow.update_item(self.name)

    def searchByName(self):
        text = self.searchLine.text()
        # print(text)        
        self.all_items = select_like_name(DB_CONNECTION, text)
        self.clearLayout(self.grid_2)
        self.show_bundles()


    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                clearLayout(child.layout())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    w = Ui_MainWindow()
    w.setupUi(MainWindow)
    MainWindow.show()
    
    sys.exit(app.exec_())

