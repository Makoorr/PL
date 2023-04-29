import gurobipy as gp

# Paramètres du problème
capacite_prod = [300, 200, 300, 200, 400] # Capacité de production
prix_usinedepot = [ # Prix de transport
    [800, 1000, 1200],
    [700, 500, 700],
    [800, 600, 500],
    [500, 600, 700],
    [700, 600, 500]
]
prix_depotclient = [ # Prix de transport
    [40, 80, 90, 50],
    [70, 40, 60, 80],
    [80, 30, 50, 60]
]
demande = [200, 300, 150, 250] # Demande Client
frais = [35000, 45000, 40000, 42000, 40000, 40000, 20000, 60000] # Prix Fixe

# model
model = gp.Model("PL9")

# Variables
x = model.addVars(range(5), range(3), name="x") # x[i, j] = quantité transportée de l'usine i au dépot j
usine = model.addVars(range(5), vtype=gp.GRB.BINARY, name="usine") # usine[i] = 1 si l'usine i est ouverte
depot = model.addVars(range(3), vtype=gp.GRB.BINARY, name="depot") # depot[j] = 1 si le dépot j est ouvert

# Fonction objectif
model.setObjective(
    gp.quicksum(prix_usinedepot[i][j] * x[i, j] for i in range(5) for j in range(3))
    + gp.quicksum(prix_depotclient[j][k] * x[i, j] for i in range(5) for j in range(3) for k in range(4))
    + gp.quicksum(frais[i] * usine[i] for i in range(5))
    + gp.quicksum(frais[len(range(5)) + j] * depot[j] for j in range(3)), gp.GRB.MINIMIZE)

# Contraintes
for i in range(5):
    model.addConstr(gp.quicksum(x[i, j] for j in range(3)) <= capacite_prod[i] * usine[i], name=f"capacite_usine_{i}")
for j in range(3):
    for k in range(4):
        model.addConstr(gp.quicksum(x[i, j] for i in range(5)) >= demande[k], name=f"demande_client_{j}_{k}")

# Résolution
model.optimize()

# Affichage des resultats
for i in range(5):
    for j in range(3):
        if x[i, j].x != 0:
            print("Usine", i+1, "--> Depot", j+1, ":", x[i, j].x)
            for k in range(4):
                print("Client", k+1, ":", prix_depotclient[j][k])
            print("-----------------------------------------------")