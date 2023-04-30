import gurobipy as gp
from gurobipy import *

# Création du modèle
m = gp.Model("chemin_le_plus_court")

# Données d'entrée : matrice des coûts entre chaque ville
coûts = [
    [0, 70, 63, 56, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
    [float('inf'), 0, 25, 19, 73, 50, 79, float('inf'), float('inf'), float('inf')],
    [float('inf'), 25, 0, 29, 69, 61, float('inf'), float('inf'), float('inf'), float('inf')],
    [float('inf'), 19, 29, 0, 67, 45, float('inf'), float('inf'), 85, float('inf')],
    [float('inf'), float('inf'), float('inf'), float('inf'), 0, 18, 67, 69, 54, 87],
    [float('inf'), float('inf'), float('inf'), float('inf'), 18, 0, 72, 52, 51, 97],
    [float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 0, 17, 31, 72],
    [float('inf'), float('inf'), float('inf'), float('inf'), float('inf'),float('inf'), 17, 0, 15, float('inf')],
    [float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 31, 15, 0, 69],
    [float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'),float('inf'), 0]
]

# Variables de décision : binaire indiquant si un arc est utilisé ou non
x = m.addVars(10, 10, vtype=GRB.BINARY, name="x")

# Fonction objectif : minimiser la somme des coûts des arcs utilisés
m.setObjective(gp.quicksum(coûts[i][j] * x[i,j] for i in range(10) for j in range(10)), GRB.MINIMIZE)



# Contrainte : il ne peut y avoir de cycle dans le graphe
for i in range(1, 10):
    for j in range(1, 10):
        if i != j:
            m.addConstr(x[i,j] + x[j,i] <= 1, name=f"no_cycle_{i}_{j}")

# Résolution du modèle
m.optimize()

# Affichage de la solution
if m.status == GRB.OPTIMAL:
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
