import gurobipy as gp

# Initialiser les paramètres du problème
jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
minimum_requis = [17, 13, 15, 19, 14, 16, 11]
nb_jours = len(jours)
nb_employes = 10
jours_semaine = range(nb_jours)
employes = range(nb_employes)

# Initialiser le modèle
model = gp.Model("Planification")

# Ajouter les variables
travail = model.addVars(employes, jours_semaine, vtype=gp.GRB.BINARY, name="travail")

# Définir la fonction objective
model.setObjective(gp.quicksum(travail[i, j] for i in employes for j in jours_semaine), gp.GRB.MINIMIZE)

# Ajouter les contraintes
# Chaque employé doit travailler pendant cinq jours consécutifs avant de prendre deux jours de congé
for i in employes:
    for j in range(nb_jours - 5):
        model.addConstr(gp.quicksum(travail[i, k] for k in range(j, j+5)) == 5)
        model.addConstr(gp.quicksum(travail[i, k] for k in range(j+5, j+7)) == 0)
    model.addConstr(gp.quicksum(travail[i, k] for k in range(nb_jours-5, nb_jours)) == 5)

# Les besoins en personnel doivent être satisfaits
for j in jours_semaine:
    model.addConstr(gp.quicksum(travail[i, j] for i in employes) >= minimum_requis[j])

# Résoudre le modèle
model.optimize()

# Afficher les résultats
if model.status == gp.GRB.OPTIMAL:
    print("Solution optimale trouvée")
    for i in employes:
        print("Employé %d : " % i, end="")
        for j in jours_semaine:
            if travail[i, j].x > 0:
                print("%s " % jours[j], end="")
        print("")
else:
    print("Pas de solution optimale trouvée")
