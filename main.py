# import pyqt5 packages with designer tools
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMessageBox
from PLs.PL1 import PL1
import sys
import os

from PLs.PL2 import PL2

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
         # Load the UI Page - added path too
        ui_path = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(ui_path, "ro.ui"), self)
    
     
        # Connection des buttons
        self.pl1PushButton.clicked.connect(self.onPl1ButtonClicked)
        self.pl3PushButton.clicked.connect(self.onPl3ButtonClicked)
        self.pl7PushButton.clicked.connect(self.onPl7ButtonClicked)

    def getTableValues(self, table):
        values = []
        for row in range(table.rowCount()):
            row_values = []
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item is not None:
                    row_values.append(int(item.text()))
                else:
                    row_values.append('')
            values.append(row_values)
        return values
 
    def showOutput(self, output):
        # Create a message box and show the output
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Output")
        msg_box.setText("Résultat de l'éxecution:\n\n"+ output)
        msg_box.exec_()


        

    def onPl1ButtonClicked(self):
        print("Button clicked")

        # Réception des parametres du Tableau de PL1
        parametres = self.getTableValues(self.pl1Parametres)
        rendement = parametres[0]
        prix_vente = parametres[1]
        main_doeuvre = parametres[2]
        temps_machine = parametres[3]
        eau = parametres[4]
        salaire_annuel = parametres[5]
        frais_gestion = parametres[6]
        
        # Réception des constantes du Tableau de PL1
        constantes = self.getTableValues(self.pl1Constantes)
        prix_main_doeuvre = constantes[0][0]
        eau_dirrigation = constantes[1][0]
        heure_machine = constantes[2][0]

        # Appel de la classe PL1
        self.pl1 = PL1(Rendement=rendement,Prix_vente=prix_vente,main_doeuvre=main_doeuvre,Temps_machine=temps_machine,
                 Eau=eau,Salaire_annuel=salaire_annuel,Frais_gestion=frais_gestion,prix_main_doeuvre=prix_main_doeuvre,
                 eau_dirrigation=eau_dirrigation,heure_machine=heure_machine)

        # Affichage des résultats
        self.showOutput(self.pl1.run())


#PL3    
    def onPl3ButtonClicked(self):
        print("Button clicked")

        # Réception des parametres du Tableau de PL3
        parametres3 = self.getTableValues(self.tableWidget)
        x1 = parametres3[0]
        x2 = parametres3[1]
        x3 = parametres3[2]
        x4 = parametres3[3]
        x5 = parametres3[4]
        x6 = parametres3[5]
        x7 = parametres3[6]

        # Appel de la classe PL3
        self.pl3 = PL1(x1=x1,x2=x2,x3=x3,x4=x4,x5=x5,x6=x6,x7=x7)

        # Affichage des résultats
        self.showOutput(self.pl3.run())

    #pl7
    def onPl7ButtonClicked(self):
        print("Button clicked")
        costs=[[]]
        # Réception des parametres du Tableau de PL2
        parametres7 = self.getTableValues(self.tableWidget_3)
        for i in range(6):
            for j in range(8):
                costs[i][j]=parametres7[i][j]
                
        # Appel de la classe PL7
        self.pl7 = PL1(costs)

        # Affichage des résultats
        self.showOutput(self.pl7.run())



if "__main__" == __name__:
    app = QApplication(sys.argv)  # Création d'application
    main = Ui_MainWindow()  # Création d'ui object
    main.show()  # affichage ui object
    sys.exit(app.exec_())  # execution d'application