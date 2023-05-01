import gurobipy as gp
from gurobipy import GRB

class PL5:
    def __init__(self,offres,demandes,couts,penalites):
        self.offres = offres
        self.demandes = demandes
        self.couts = couts
        self.penalites = penalites

    def run(self):
        # Création du modèle
        model = gp.Model('PL5')

        # Ajout des variables de décision
        x = model.addVars(3, 4, vtype=GRB.INTEGER, name='x')
        d = model.addVars(4, vtype=GRB.INTEGER, name='d')

        # Ajout des contraintes
        for i in range(3):
            for j in range(4):
                model.addConstr(x[i, j] >= 0)
                model.addConstr(x[i, j] <= self.offres[i])

        for j in range(4):
            model.addConstr(gp.quicksum(x[i, j] for i in range(3)) + d[j] >= self.demandes[j])
            model.addConstr(d[j] >= 0)
            model.addConstr(d[j] <= self.demandes[j])

        # Ajout de la fonction objectif
        model.setObjective(gp.quicksum(x[i, j] * self.couts[i][j] for i in range(3) for j in range(4)) +
                        gp.quicksum(d[j] * self.penalites[j] for j in range(4)), GRB.MINIMIZE)

        # Résolution du modèle
        model.optimize()

        if model.status == GRB.OPTIMAL:
            for i in range(3):
                for j in range(4):
                    if x[i, j].x != 0:
                        print(f'La centrale {i+1} fournit {x[i,j].x} Kwh à la ville {j+1}')
            for j in range(4):
                if d[j].x != 0:
                    print(f'La ville {j+1} a une demande non satisfaite de {d[j].x} Kwh')


if "__main__" == __name__:
    # Offres des centrales
    offres = [35, 50, 40]

    # Demandes des villes (augmentées de 5 millions de Kwh)
    demandes = [45, 20, 30, 30]

    # Coûts de transport de chaque centrale à chaque ville
    couts = [
        [8, 6, 10, 9],
        [9, 12, 13, 7],
        [14, 9, 16, 5]
    ]

    # Pénalités pour la demande non satisfaite
    penalites = [20, 25, 22, 35]

    pl5 = PL5(offres,demandes,couts,penalites)
    pl5.run()