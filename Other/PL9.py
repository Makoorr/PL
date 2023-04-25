import gurobipy as gp
from gurobipy import GRB

# Données du problème
capacites_production = [300, 200, 300, 200, 400]
couts_usine_depot = [
    [800, 1000, 1200],
    [700, 500, 700],
    [800, 600, 500],
    [500, 600, 700],
    [700, 600, 500]
]
couts_depot_client = [
    [40, 80, 90, 50],
    [70, 40, 60, 80],
    [80, 30, 50, 60]
]
demande_clients = [200, 300, 150, 250]
couts_fixes = [35000, 45000, 40000, 42000, 40000, 40000, 20000, 60000]

# Indices
usines = range(len(capacites_production))
depots = range(len(couts_depot_client))
clients = range(len(demande_clients))

# Création du modèle
m = gp.Model("localisation_usine_depot")

# Variables
x = m.addVars(usines, depots, name="x")
y_usines = m.addVars(usines, vtype=GRB.BINARY, name="y_usines")
y_depots = m.addVars(depots, vtype=GRB.BINARY, name="y_depots")

# Contraintes
# Contraintes de capacité des usines
for i in usines:
    m.addConstr(gp.quicksum(x[i, j] for j in depots) <= capacites_production[i] * y_usines[i], name=f"capacite_usine_{i}")

# Contraintes de demande des clients
for j in depots:
    for k in clients:
        m.addConstr(gp.quicksum(x[i, j] for i in usines) >= demande_clients[k], name=f"demande_client_{j}_{k}")

# Fonction objectif
m.setObjective(gp.quicksum(couts_usine_depot[i][j] * x[i, j] for i in usines for j in depots) + gp.quicksum(couts_depot_client[j][k] * x[i, j] for i in usines for j in depots for k in clients) + gp.quicksum(couts_fixes[i] * y_usines[i] for i in usines) + gp.quicksum(couts_fixes[len(usines) + j] * y_depots[j] for j in depots), GRB.MINIMIZE)

# Résoudre le modèle
m.optimize()

# Afficher les résultats
if m.status == GRB.Status.OPTIMAL:
    print("Coût total optimal :", m.objVal)
    print("Quantités produites et transportées (x) :")
    for i in usines:
        for j in depots:
            if x[i, j].x > 1e-6:
                print("Usine", i+1, "vers Dépôt", j+1, ":", x[i, j].x)
                print("    Coûts de transport du Dépôt", j+1, "vers les Clients :")
                for k in clients:
                    print("        Client", k+1, ":", couts_depot_client[j][k])

  
