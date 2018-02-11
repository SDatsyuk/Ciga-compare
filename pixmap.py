

import sys
from PyQt5 import QtGui, QtWidgets


class Window(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.button = QtWidgets.QPushButton("Make child")
        self.button.clicked.connect(self.openChildWindow)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.button)

    def openChildWindow(self):
        self.childWindow = ChildWindow(self)
        self.childWindow.setGeometry(650, 350, 200, 300)
        self.childWindow.show()

    def printResult(self, value):  
        print(value)

class ChildWindow(Window):
    def __init__(self, parentWindow):
        super(ChildWindow, self).__init__()
        self.parentWindow = parentWindow
        self.parentWindow.printResult("I'm in child init")
        self.button.setDisabled(1)

    def closeEvent(self, event):
        self.parentWindow.printResult("Closing child, this text is returned to parent")

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(600, 300, 200, 300)
    window.show()
    sys.exit(app.exec_())