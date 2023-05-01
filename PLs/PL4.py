import gurobipy as gp

# Initialisation des paramètres du problème
nb_mois = 4
nb_ouvriers_initiaux = 100
nb_heures_travail_par_ouvrier = 160
nb_heures_max_supplementaires = 20
cout_recrutement_ouvrier = 1600
cout_licenciement_ouvrier = 2000
cout_stockage_paire_chaussure = 3
cout_heure_supplementaire_ouvrier = 13
cout_mat_paire_chaussure = 15
heures_travail_paire_chaussure = 4
demande_par_mois = [3000, 5000, 2000, 1000]
stock_initial = 500

# Initialisation du modèle
model = gp.Model("ChausseTous")

# Déclaration des variables
x = {}
y = {}
for t in range(nb_mois):
    x[t] = model.addVar(vtype=gp.GRB.INTEGER, name="production_%s" % t)
    y[t] = model.addVar(vtype=gp.GRB.INTEGER, name="ouvriers_%s" % t)

# Fonction objectif
model.setObjective(
    gp.quicksum(y[t] * cout_recrutement_ouvrier for t in range(nb_mois) if y[t] > 0)
    + gp.quicksum(y[t] * cout_licenciement_ouvrier for t in range(nb_mois) if y[t] < 0)
    + gp.quicksum(
        x[t] * cout_mat_paire_chaussure + y[t] * nb_heures_travail_par_ouvrier * 1500
        + (x[t] * heures_travail_paire_chaussure - y[t] * nb_heures_travail_par_ouvrier, nb_heures_max_supplementaires) * cout_heure_supplementaire_ouvrier
        + (stock_initial * cout_stockage_paire_chaussure)
        for t in range(nb_mois)
    ),
    gp.GRB.MINIMIZE,
)

# Ajout des contraintes
model.addConstr(y[0] == nb_ouvriers_initiaux)
for t in range(1, nb_mois):
    model.addConstr(y[t] >= y[t-1] - gp.ceil((nb_ouvriers_initiaux - y[0])/5))
    model.addConstr(y[t] <= y[t-1] + gp.floor((y[0] - nb_ouvriers_initiaux)/5))
for t in range(nb_mois):
    model.addConstr(x[t] * heures_travail_paire_chaussure <= y[t] * nb_heures_travail_par_ouvrier + nb_heures_max_supplementaires)

# Résolution
model.optimize()

# Affichage des résultats
print("Plan de production optimal :")
for t in range(nb_mois):
    print("Mois %s : %s" % (t+1, int(x[t].x)))