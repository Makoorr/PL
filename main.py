# import pyqt5 packages with designer tools
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.uic import loadUi
import sys
import os


# from PySide2.QtUiTools import QUiLoader

# if __name__ == '__main__':
#     # Some code to obtain the form file name, ui_file_name
#     app = QApplication(sys.argv)
#     ui_file = QFile(ui_file_name)
#     if not ui_file.open(QIODevice.ReadOnly):
#         print("Cannot open {}: {}".format(ui_file_name, ui_file.errorString()))
#         sys.exit(-1)
#     loader = QUiLoader()
#     widget = loader.load(ui_file, None)
#     ui_file.close()
#     if not widget:
#         print(loader.errorString())
#         sys.exit(-1)
#     widget.show()
#     sys.exit(app.exec_())


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__()
         # Load the UI Page - added path too
        ui_path = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(ui_path, "ro.ui"), self)



    

app= QApplication(sys.argv)  # create application
main= Ui_MainWindow()  # create ui object
main.show()  # show ui object
sys.exit(app.exec_())  # execute application
