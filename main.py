# import pyqt5 packages with designer tools
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication
import sys
import os
import PLs

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__()
         # Load the UI Page - added path too
        ui_path = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(ui_path, "ro.ui"), self)
    
        # Connect the buttons
        self.pl1_pushButton.clicked.connect(self.on_pl1_pushButton_clicked)
    
    def on_pl1_pushButton_clicked(self):
        print("Button clicked")
        try:
            self.pl1_pushButton.clicked.disconnect()
        except:
            pass

if "__main__" == __name__:
    app = QApplication(sys.argv)  # create application
    main = Ui_MainWindow()  # create ui object
    main.show()  # show ui object
    sys.exit(app.exec_())  # execute application