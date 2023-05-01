# import pyqt5 packages with designer tools
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMessageBox
import numpy as np
from PLs.PL1 import PL1
from PLs.PL2 import PL2
from PLs.PL3 import PL3
from PLs.PL7 import PL7
from PLs.PL9 import PL9
import sys
import os


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
         # Load the UI Page - added path too
        ui_path = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(ui_path, "ro.ui"), self)

        # Connection des buttons
        self.pl1PushButton.clicked.connect(self.onPl1ButtonClicked)
        self.pl2PushButton.clicked.connect(self.onPl2ButtonClicked)
        self.pl3PushButton.clicked.connect(self.onPl3ButtonClicked)
        self.pl7PushButton.clicked.connect(self.onPl7ButtonClicked)
        self.pl9PushButton.clicked.connect(self.onPl9ButtonClicked)

    def getTableValues(self, table):
        values = []
        for row in range(table.rowCount()):
            row_values = []
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item is not (None):
                    try:
                        row_values.append(int(item.text()))
                    except ValueError:
                        try:
                            row_values.append(float(item.text()))
                        except ValueError:
                            row_values.append(np.nan)
                else:
                    row_values.append(np.nan)
            values.append(row_values)
        return values
 
    def showOutput(self, output):
        # Create a message box and show the output
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Output")
        msg_box.setText("Résultat de l'éxecution:\n\n"+ output)
        msg_box.exec_()

    # PL1
    def onPl1ButtonClicked(self):
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

    # PL2
    def onPl2ButtonClicked(self):
        # Réception des parametres du Tableau de PL2
        parametres = self.getTableValues(self.pl2Parametres)
        niveau_qualite = parametres[0]
        nb_barils = parametres[1]
        prix_vente = parametres[2]
        frais_marketing = parametres[3]

        # Appel de la classe PL2
        self.pl2 = PL2(niveau_qualite=niveau_qualite,nb_barils=nb_barils,prix_vente=prix_vente,frais_marketing=frais_marketing)

        # Affichage des résultats
        self.showOutput(self.pl2.run())

    # PL3
    def onPl3ButtonClicked(self):
        # Réception des parametres du Tableau de PL3
        parametres3 = self.getTableValues(self.pl3Parametres)
        x1 = parametres3[0][0]
        x2 = parametres3[0][1]
        x3 = parametres3[0][2]
        x4 = parametres3[0][3]
        x5 = parametres3[0][4]
        x6 = parametres3[0][5]
        x7 = parametres3[0][6]

        # Appel de la classe PL3
        self.pl3 = PL3(x1=x1,x2=x2,x3=x3,x4=x4,x5=x5,x6=x6,x7=x7)

        # Affichage des résultats
        self.showOutput(self.pl3.run())

    # PL7
    def onPl7ButtonClicked(self):        
        # Réception des parametres du Tableau de PL7
        parametres = self.getTableValues(self.pl7Parametres)
        print(parametres)

        # Appel de la classe PL7
        self.pl7 = PL7(costs=parametres)

        # Affichage des résultats
        self.showOutput(self.pl7.run())

    # PL9
    def onPl9ButtonClicked(self):
        # Réception des parametres du Tableau de PL9
        capacite_prod = self.getTableValues(self.pl9Parametres1)[0]
        prix_usinedepot = self.getTableValues(self.pl9Parametres2)
        prix_depotclient = self.getTableValues(self.pl9Parametres3)
        demande = self.getTableValues(self.pl9Parametres4)[0]
        frais = self.getTableValues(self.pl9Parametres5)[0]

        # Appel de la classe PL9
        self.pl9 = PL9(capacite_prod=capacite_prod,prix_usinedepot=prix_usinedepot,prix_depotclient=prix_depotclient,
                    demande=demande,frais=frais)
        
        # Affichage des résultats
        self.showOutput(self.pl9.run())

if "__main__" == __name__:
    app = QApplication(sys.argv)  # Création d'application
    main = Ui_MainWindow()  # Création d'ui object
    main.show()  # affichage ui object
    sys.exit(app.exec_())  # execution d'application