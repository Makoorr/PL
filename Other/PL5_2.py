import gurobipy as gp
from gurobipy import GRB

# Offres des centrales
offres = [50, 70, 80]

# Demandes des villes (augmentées de 5 millions de Kwh)
demandes = [35, 45, 25, 65]

# Coûts de transport de chaque centrale à chaque ville
couts = [
    [2, 4, 5, 3],
    [3, 1, 2, 4],
    [4, 3, 1, 2]
]

# Pénalités pour la demande non satisfaite
penalites = [7, 8, 9, 6]

# Création du modèle
model = gp.Model('Probleme de transport avec pénalités')

# Ajout des variables de décision
x = model.addVars(3, 4, vtype=GRB.INTEGER, name='x')
d = model.addVars(4, vtype=GRB.INTEGER, name='d')

# Ajout des contraintes
for i in range(3):
    for j in range(4):
        model.addConstr(x[i, j] >= 0)
        model.addConstr(x[i, j] <= offres[i])

for j in range(4):
    model.addConstr(gp.quicksum(x[i, j] for i in range(3)) + d[j] >= demandes[j])
    model.addConstr(d[j] >= 0)
    model.addConstr(d[j] <= demandes[j])

# Ajout de la fonction objectif
model.setObjective(gp.quicksum(x[i, j] * couts[i][j] for i in range(3) for j in range(4)) +
                   gp.quicksum(d[j] * penalites[j] for j in range(4)), GRB.MINIMIZE)

# Résolution du modèle
model.optimize()

# Affichage de la solution
if model.status == GRB.OPTIMAL:
    for i in range(3):
        for j in range(4):
            if x[i, j].x != 0:
                print(f'La centrale {i+1} fournit {x[i,j].x} Kwh à la ville {j+1}')
    for j in range(4):
        if d[j].x != 0:
            print(f'La ville {j+1} a une demande non satisfaite de {d[j].x} Kwh')
