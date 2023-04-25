import gurobipy as gp
from gurobipy import *
# Données du problème
projets = ["projet1", "projet2", "projet3", "projet4", "projet5", "projet6", "projet7", "projet8"]
entreprises = ["entreprise1", "entreprise2", "entreprise3", "entreprise4", "entreprise5", "entreprise6"]
offres = {
    ("entreprise1", "projet2"): 8200, ("entreprise1", "projet3"): 7800, ("entreprise1", "projet4"): 5400,
    ("entreprise1", "projet6"): 3900,
    ("entreprise2", "projet1"): 7800, ("entreprise2", "projet2"): 8200, ("entreprise2", "projet4"): 6300,
    ("entreprise2", "projet6"): 3300, ("entreprise2", "projet7"): 4900,
    ("entreprise3", "projet2"): 4800, ("entreprise3", "projet6"): 4400, ("entreprise3", "projet7"): 5600,
    ("entreprise3", "projet8"): 3600,
    ("entreprise4", "projet3"): 8000, ("entreprise4", "projet4"): 5000, ("entreprise4", "projet5"): 6800,
    ("entreprise4", "projet7"): 6700, ("entreprise4", "projet8"): 4200,
    ("entreprise5", "projet1"): 7200, ("entreprise5", "projet2"): 6400, ("entreprise5", "projet4"): 3900,
    ("entreprise5", "projet5"): 6400, ("entreprise5", "projet6"): 2800, ("entreprise5", "projet8"): 3000,
    ("entreprise6", "projet1"): 7000, ("entreprise6", "projet2"): 5800, ("entreprise6", "projet3"): 7500,
    ("entreprise6", "projet4"): 4500, ("entreprise6", "projet5"): 5600, ("entreprise6", "projet7"): 6000,
    ("entreprise6", "projet8"): 4200
}

model = gp.Model("Affectation_optimale")

x = model.addVars(offres.keys(), vtype=gp.GRB.BINARY, name="x")

model.addConstrs((gp.quicksum(x[e, p] for e in entreprises if (e, p) in offres) == 1 for p in projets), name="projet")

model.addConstrs((gp.quicksum(x[e, p] for p in projets if (e, p) in offres) <= 2 for e in entreprises), "entreprise")

model.addConstrs((x[e, p] <= offres.get((e, p), 0) for e, p in x.keys()), "offre")

model.setObjective(gp.quicksum(offres[e, p] * x[e, p] for e, p in x.keys()), gp.GRB.MINIMIZE)

model.optimize()

if model.status == gp.GRB.OPTIMAL:
    print("Solution optimal")
    for e in entreprises:
     for p in projets:
         if (e, p) in offres and x[e, p].x > 0:
            print(f"L'entreprise {e} a obtenu le projet {p} avec un bénéfice de {offres[e, p]}")

else:
    print("Pas de solution optimale ")
