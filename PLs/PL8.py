import gurobipy as gp
import numpy as np

class PL8:
    def __init__(self,costs):
        self.costs = costs

    def run(self):
        # Création du modèle
        m = gp.Model("chemin_le_plus_court")

        # Variables de décision : binaire indiquant si un arc est utilisé ou non
        x = m.addVars(10, 10, vtype=gp.GRB.BINARY, name="x")

        # Fonction objectif : minimiser la somme des coûts des arcs utilisés
        m.setObjective(gp.quicksum(self.costs[i][j] * x[i,j] for i in range(10) for j in range(10) if not np.isnan(self.costs[i][j])), gp.GRB.MINIMIZE)

        # Contrainte : il ne peut y avoir de cycle dans le graphe
        for i in range(1, 10):
            for j in range(1, 10):
                if i != j:
                    m.addConstr(x[i,j] + x[j,i] <= 1)

        # Résolution du modèle
        m.optimize()

        # Affichage de la solution
        if m.status == gp.GRB.OPTIMAL:
            print(f"Coût minimal : {m.objVal}")
            chemin = [0]
            ville_act = 0
            while ville_act != 9:
                for j in range(10):
                    if x[ville_act, j].x > 0.9:
                        chemin.append(j)
                        ville_act = j
                        break
            print(f"Chemin le plus court : {' -> '.join(str(ville + 1) for ville in chemin)}")
        else:
            print("Pas de chemin optimal!")


if "__main__"== __name__:
    # Données d'entrée : matrice des coûts entre chaque ville
    costs = [
        [np.nan, 70, 63, 56, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
        [np.nan, np.nan, 25, 19, 73, 50, 79, np.nan, np.nan, np.nan],
        [np.nan, 25, np.nan, 29, 69, 61, np.nan, np.nan, np.nan, np.nan],
        [np.nan, 19, 29, np.nan, 67, 45, np.nan, np.nan, 85, np.nan],
        [np.nan, np.nan, np.nan, np.nan, np.nan, 18, 67, 69, 54, 87],
        [np.nan, np.nan, np.nan, np.nan, 18, np.nan, 72, 52, 51, 97],
        [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 17, 31, 72],
        [np.nan, np.nan, np.nan, np.nan, np.nan,np.nan, 17, np.nan, 15, np.nan],
        [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 31, 15, np.nan, 69],
        [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,np.nan, np.nan]
    ]

    pl8 = PL8(costs)
    pl8.run()