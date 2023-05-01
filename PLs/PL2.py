import gurobipy as gp

class PL2:
    def __init__(self,niveau_qualite=[10, 5],nb_barils=[5000, 10000],prix_vente=[25, 20],frais_marketing=[0.2, 0.1]):
        self.niveau_qualite = niveau_qualite
        self.nb_barils = nb_barils
        self.prix_vente = prix_vente
        self.frais_marketing = frais_marketing

    def run(self):
        # Initialisation du modèle
        model = gp.Model("PL2")
        model.params.NonConvex = 2

        # Ajout des variables de décision
        gazoline = model.addVar(lb=0, ub=1, name="gazoline")
        chauffage = model.addVar(lb=0, ub=1, name="chauffage")

        # Fonction objectif : maximiser le profit total
        model.setObjective((self.prix_vente[0] - self.frais_marketing[0]) * gazoline + (self.prix_vente[1] - self.frais_marketing[1]) * chauffage, gp.GRB.MAXIMIZE)

        # Contraintes
        d1 = model.addVar(0, name="denominateur1")
        d2 = model.addVar(0, name="denominateur2")
        model.addConstr( d1 == 1 / self.nb_barils[0]*gazoline + self.nb_barils[1]*chauffage )
        model.addConstr( d2 == 1 / self.nb_barils[0]*(1-gazoline) + self.nb_barils[1]*(1-chauffage) )

        model.addConstr( ( (self.niveau_qualite[0]*self.nb_barils[0]*gazoline + self.niveau_qualite[1]*self.nb_barils[1]*chauffage) * d1 ) >= 8, name="c1")
        model.addConstr( ( (self.niveau_qualite[0]*self.nb_barils[0]*(1-gazoline) + self.niveau_qualite[1]*self.nb_barils[1]*(1-chauffage)) * d2) >= 6, name="c2")

        # Resolution
        model.optimize()

        # Affichage des résultats
        resultat = "Mixage optimal :"
        resultat += "\nGazoline : "+ str(gazoline.x)
        resultat += "\nPétrole de chauffage : "+ str(chauffage.x)
        resultat += "\nProfit total : "+ str(model.objVal) + "DT"

        return resultat

if "__main__" == __name__:
    pl2 = PL2()
    print(pl2.run())