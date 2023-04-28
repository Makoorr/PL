# import pyqt5 packages with designer tools
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.uic import loadUi
import sys
import os

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__()
         # Load the UI Page - added path too
        ui_path = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(ui_path, "ro.ui"), self)

app = QApplication(sys.argv)  # create application
main = Ui_MainWindow()  # create ui object
main.show()  # show ui object
sys.exit(app.exec_())  # execute application