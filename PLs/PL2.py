import gurobipy as gp

# Initialisation des paramètres du problème
niveau_qualite = [10, 5]  # Niveau de qualité pour chaque type de pétrole brut
nb_barils = [5000, 10000]  # Nombre de barils pour chaque type de pétrole brut
prix_vente = [25, 20]  # Prix de vente pour chaque produit final (gazoline, pétrole de chauffage)
frais_marketing = [0.2, 0.1]  # Frais de marketing pour chaque produit final

# Initialisation du modèle
model = gp.Model("PL2")
model.params.NonConvex = 2

# Ajout des variables de décision
gazoline = model.addVar(lb=0, ub=1, name="gazoline")
chauffage = model.addVar(lb=0, ub=1, name="chauffage")

# Fonction objectif : maximiser le profit total
model.setObjective((prix_vente[0] - frais_marketing[0]) * gazoline + (prix_vente[1] - frais_marketing[1]) * chauffage, gp.GRB.MAXIMIZE)

# Contraintes
d1 = model.addVar(0, name="denominateur1")
d2 = model.addVar(0, name="denominateur2")
model.addConstr( d1 == 1 / nb_barils[0]*gazoline + nb_barils[1]*chauffage )
model.addConstr( d2 == 1 / nb_barils[0]*(1-gazoline) + nb_barils[1]*(1-chauffage) )

model.addConstr( ( (niveau_qualite[0]*nb_barils[0]*gazoline + niveau_qualite[1]*nb_barils[1]*chauffage) * d1 ) >= 8, name="c1")
model.addConstr( ( (niveau_qualite[0]*nb_barils[0]*(1-gazoline) + niveau_qualite[1]*nb_barils[1]*(1-chauffage)) * d2) >= 6, name="c2")

# Resolution
model.optimize()

# Affichage des résultats
print("Mixage optimal :")
print("Gazoline :", gazoline.x)
print("Pétrole de chauffage :", chauffage.x)
print("Profit total :", model.objVal, "DT")
