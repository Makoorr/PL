import gurobipy as gp

# Initialisation des paramètres
jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
demandes = [17, 13, 15, 19, 14, 16, 11]
nb_jours = range(len(jours))
nb_jours_travail = 5

# Initialisation du modèle
model = gp.Model("Poste")

# Définition des variables de décision
x = {jour: model.addVar(vtype=gp.GRB.CONTINUOUS, name=jour) for jour in jours} # x[i] = nombre d'employés travaillant le jour i

# Fonction objectif
model.setObjective(gp.quicksum(x[i] for i in nb_jours), gp.GRB.MINIMIZE)

# Contraintes
for i in nb_jours:
    model.addConstr(x[i] >= demandes[i]) # Minimum d'employe requis

